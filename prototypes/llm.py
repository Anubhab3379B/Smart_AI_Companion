# File: llm.py
"""
Enhanced LLaMA3 / Mixtral + RAG brain with:
- Integrated conversational loop using voice (voice.py)
- Self-healing: verifies integrity of model files, auto-repairs if corrupted.
- Cleanly documented.
"""

from transformers import AutoTokenizer, AutoModelForCausalLM # type: ignore
import faiss # type: ignore
import numpy as np
import hashlib
import os
import subprocess
from voice import speak, record_audio, transcribe_audio # type: ignore

# Load tokenizer + local LLaMA3 or Mixtral model
tokenizer = AutoTokenizer.from_pretrained("TheBloke/LLaMA-3-8B-GGUF")
model = AutoModelForCausalLM.from_pretrained("TheBloke/LLaMA-3-8B-GGUF")

# Example personal knowledge base
personal_docs = [
    "Quantum entanglement means particles can be correlated beyond classical limits.",
    "CRISPR allows precise gene editing by targeting specific DNA sequences.",
    "In Indian law, Article 21 guarantees the right to life and personal liberty."
]

# Embeddings (mocked by slicing tokens)
def embed(text):
    tokens = tokenizer(text, return_tensors="pt")
    return tokens.input_ids[0][:384].detach().numpy()

# Build FAISS index
index = faiss.IndexFlatL2(384)
vectors = np.array([embed(doc) for doc in personal_docs]).astype('float32')
index.add(vectors)

# Retrieve related context
def retrieve_context(query):
    qvec = embed(query).astype('float32').reshape(1, -1)
    D, I = index.search(qvec, k=2)
    return [personal_docs[i] for i in I[0]]

# Generate answer from local model
def ask_brain(query):
    context = "\n".join(retrieve_context(query))
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=100)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Self-healing: verify model integrity
def checksum_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def self_heal():
    expected = "abc123..."  # your real expected checksum
    current = checksum_file("model.safetensors")
    if current != expected:
        print("[ALERT] Model corrupted. Auto-repairing...")
        subprocess.run(["wget", "https://huggingface.co/.../model.safetensors", "-O", "model.safetensors"])
    else:
        print("[OK] Model integrity verified.")

# Main conversational loop with voice
if __name__ == "__main__":
    self_heal()
    while True:
        speak("Hi, ask me anything or say exit.")
        audio_file = record_audio()
        question = transcribe_audio(audio_file)
        if "exit" in question.lower():
            speak("Goodbye, dear friend.")
            break
        answer = ask_brain(question)
        speak(answer)
        print(f"Q: {question}\nA: {answer}")