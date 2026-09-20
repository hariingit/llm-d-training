"""Minimal RAG demo: embed docs -> FAISS search -> vLLM (via llm-d router) generates the answer."""
import sys
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
texts = [d["text"] for d in DOCUMENTS]
embeddings = embedder.encode(texts, normalize_embeddings=True)

index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(np.array(embeddings, dtype="float32"))
print(f"FAISS index built: {index.ntotal} vectors, dim={embeddings.shape[1]}\n")


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
    print(f"Q: {question}\n")
    retrieved = retrieve(question)
    print("Retrieved (semantic search, not keyword match):")
    for doc, score in retrieved:
        preview = doc["text"][:90].replace("\n", " ")
        print(f"  [{doc['id']}] score={score:.3f}  {preview}...")
    print("\nAsking the LLM to answer using only the retrieved context...")
    answer = generate(question, retrieved)
    print(f"\nA: {answer}\n")
    print("-" * 70)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ask(" ".join(sys.argv[1:]))
    else:
        for q in [
            "Was there any ransomware activity recently?",
            "Did any incident involve customer data being exposed?",
            "Summarize any incidents involving phishing or fake login pages.",
        ]:
            ask(q)
