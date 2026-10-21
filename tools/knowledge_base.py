"""Search the existing HEC knowledge base; load RAG libraries only when called."""

import json
import logging
from pathlib import Path


def search_in_knowledge_base(query: str) -> str:
    """Search Pakistan university course outlines and return the five closest passages."""
    import numpy as np
    import ollama

    logging.info("TOOL | search_in_knowledge_base | %s", query)
    path = Path(__file__).resolve().parents[1] / "multi-tool agent" / "hec_outline_embeddings.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    response = ollama.embeddings(model=data.get("model_name", "mxbai-embed-large"), prompt=query)
    query_vector = np.array(response["embedding"])
    vectors = np.array(data["embeddings"])

    # Cosine similarity: compare the query with each saved passage embedding.
    lengths = np.linalg.norm(vectors, axis=1) * np.linalg.norm(query_vector)
    scores = np.divide(vectors @ query_vector, lengths,
                       out=np.zeros(len(vectors)), where=lengths != 0)
    best = np.argsort(scores)[::-1][:5]
    results = [{"text": data["texts"][index], "similarity": float(scores[index]),
                "index": int(index)} for index in best]
    return json.dumps(results)
