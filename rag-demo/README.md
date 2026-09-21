# RAG demo

Minimal Retrieval-Augmented Generation example: embed a set of documents, search
them with FAISS, then have an LLM served behind the llm-d router generate an
answer grounded in the retrieved context. See [`rag.py`](rag.py) for the
walkthrough (embed docs → semantic search → prompt the LLM with retrieved
context → answer).

## LLM concepts

- **LLM (Large Language Model)** — a machine learning model trained on a vast
  amount of text data that can comprehend and generate human-like language.

- **Context window** — the amount of text (tokens) a model can "see" at once
  when generating a response. Each prompt is evaluated independently within
  its own window: unless earlier turns are explicitly re-sent as part of the
  prompt, there's no memory carried over from one request to the next.

- **Inference** — using an already-trained model to produce output for new
  input (as opposed to training, where the model's weights are updated).
  The model itself doesn't change or "learn" during inference; it just
  applies what it already learned.

- **Accelerators** — purpose-built hardware for the parallel math LLMs need,
  e.g. GPUs and TPUs. (This demo intentionally runs on CPU instead, per the
  parent [`llm-d-training` README](../README.md).)

- **Weights** — the numerical parameters learned during training that define
  the strength of connections between neurons. This is what actually gets
  loaded onto the accelerator/CPU when a model is served.

- **Multimodal** — a model that can take in and/or generate more than one
  data type: text, images, audio, video.

- **Quantization** — reducing a model's numerical precision (e.g.
  FP16 → INT8/INT4) to shrink its memory footprint and speed up inference,
  at some cost to accuracy.

- **Serving engine** — software that standardizes serving an LLM and exposes
  it behind an API, like a web app for a model (e.g. vLLM, which this demo
  runs behind llm-d's router).
