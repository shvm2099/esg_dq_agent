from transformers import AutoTokenizer, TFAutoModel
import tensorflow as tf
import numpy as np
import json
import os

MODEL_NAME = "bert-base-uncased"
CHUNK_SIZE = 240  # 200-300

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = TFAutoModel.from_pretrained(MODEL_NAME)

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output.last_hidden_state
    input_mask_expanded = tf.cast(tf.expand_dims(attention_mask, -1), tf.float32)
    return tf.reduce_sum(token_embeddings * input_mask_expanded, 1) / tf.reduce_sum(input_mask_expanded, 1)

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="tf", truncation=True, padding=True)
    outputs = model(**inputs)
    return mean_pooling(outputs, inputs['attention_mask'])[0].numpy()

def cosine_similarity(a, b):
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)
    return float(np.dot(a, b))

def chunk_text(text, max_words=CHUNK_SIZE):
    words = text.split()
    return [' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

def load_chunks_from_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["chunks"]

def compute_similarity(source_chunks, ref_embeddings):
    similarities = []
    for chunk in source_chunks:
        emb = get_embedding(chunk)
        sims = [cosine_similarity(emb, ref_emb) for ref_emb in ref_embeddings]
        sims.sort(reverse=True)
        top_avg = np.mean(sims[:3])  # avg of top-3
        similarities.append(top_avg)
    return np.mean(similarities)

def benchmark_against_reference(input_text, final_text, ref_path):
    reference_chunks = load_chunks_from_json(ref_path)
    ref_embeddings = [get_embedding(chunk) for chunk in reference_chunks if chunk.strip()]

    input_chunks = chunk_text(input_text)
    final_chunks = chunk_text(final_text)

    input_score = compute_similarity(input_chunks, ref_embeddings)
    final_score = compute_similarity(final_chunks, ref_embeddings)

    improvement = round((final_score - input_score) * 100, 2)

    return {
        "input_similarity_score": round(input_score * 100, 2),
        "final_similarity_score": round(final_score * 100, 2),
        "improvement_score": improvement,
        "comment": f"Report similarity improved by {improvement} points after tone/structure correction."
    }

