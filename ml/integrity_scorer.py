import random
from typing import List
from models import RetrievedDocument

class IntegrityScorer:
    """
    Scores the overall integrity of a RAG pipeline response based on:
    - Average document integrity scores
    - Retrieval consistency (score spread)
    - Query-document coherence (simulated)
    """

    def __init__(self):
        print("[IntegrityScorer] Ready")

    def score(self, query: str, documents: List[RetrievedDocument]) -> float:
        if not documents:
            return 0.0

        avg_integrity = sum(d.integrity_score for d in documents) / len(documents)
        avg_similarity = sum(d.similarity_score for d in documents) / len(documents)

        # Score spread penalty: high variance = less trustworthy
        scores = [d.integrity_score for d in documents]
        variance = sum((s - avg_integrity) ** 2 for s in scores) / len(scores)
        consistency_bonus = max(0, 1.0 - variance * 10)

        # Combine
        raw = (avg_integrity * 0.5) + (avg_similarity * 0.3) + (consistency_bonus * 0.2)

        # Small noise for realism
        raw += random.uniform(-0.02, 0.02)
        return round(max(0.0, min(1.0, raw)), 4)
