"""Shared RAG pipeline: embed docs -> FAISS search -> vLLM (via llm-d router) generates the answer."""
import numpy as np
import faiss
import requests
from sentence_transformers import SentenceTransformer

from docs import DOCUMENTS

LLM_ENDPOINT = "http://localhost:8080/v1/completions"
MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

print("Loading embedding model (all-MiniLM-L6-v2)...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

print(f"Embedding {len(DOCUMENTS)} incident reports...")
_texts = [d["text"] for d in DOCUMENTS]
_embeddings = embedder.encode(_texts, normalize_embeddings=True)

index = faiss.IndexFlatIP(_embeddings.shape[1])
index.add(np.array(_embeddings, dtype="float32"))
print(f"FAISS index built: {index.ntotal} vectors, dim={_embeddings.shape[1]}\n")


def retrieve(question: str, k: int = 2):
    q_vec = embedder.encode([question], normalize_embeddings=True)
    scores, idxs = index.search(np.array(q_vec, dtype="float32"), k)
    return [(DOCUMENTS[i], float(scores[0][rank])) for rank, i in enumerate(idxs[0])]


def generate(question: str, retrieved):
    context = "\n\n".join(f"[{doc['id']}] {doc['text']}" for doc, _ in retrieved)
    prompt = (
        "You are a security analyst assistant. Answer the question using ONLY the "
        "incident reports below. Cite the incident ID(s) you used.\n\n"
        f"{context}\n\n"
        f"Question: {question}\n"
        "Answer:"
    )
    resp = requests.post(
        LLM_ENDPOINT,
        json={"model": MODEL_NAME, "prompt": prompt, "max_tokens": 80, "temperature": 0.2},
        timeout=180,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["text"].strip()


def ask(question: str):
    retrieved = retrieve(question)
    answer = generate(question, retrieved)
    return {
        "question": question,
        "retrieved": [
            {"id": doc["id"], "text": doc["text"], "score": score}
            for doc, score in retrieved
        ],
        "answer": answer,
    }
