import math
import random
from typing import List
from models import DriftResult
from config import settings

def _fake_embed(text: str) -> List[float]:
    """Deterministic pseudo-embedding based on text hash."""
    random.seed(hash(text) % (2**32))
    vec = [random.gauss(0, 1) for _ in range(64)]
    norm = math.sqrt(sum(v**2 for v in vec))
    return [v / norm for v in vec]

def _cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    return max(-1.0, min(1.0, dot))

# Baseline corpus embeddings (simulated)
BASELINE_QUERIES = [
    "What is machine learning?",
    "Explain neural networks",
    "How does retrieval augmented generation work?",
    "What are transformers in NLP?",
    "Describe attention mechanisms",
    "How do embeddings represent text?",
    "What is fine-tuning in AI?",
    "Explain RLHF",
]

class CosineDriftMonitor:
    def __init__(self):
        self.baseline_embeddings = [_fake_embed(q) for q in BASELINE_QUERIES]
        self.drift_events: List[float] = []
        self.threshold = settings.DRIFT_THRESHOLD
        print("[CosineDriftMonitor] Initialized with baseline corpus")

    def analyze(self, query: str) -> DriftResult:
        query_embedding = _fake_embed(query)

        # Compute similarity against all baseline queries
        similarities = [
            _cosine_similarity(query_embedding, base)
            for base in self.baseline_embeddings
        ]
        max_sim = max(similarities)
        baseline_sim = sum(similarities) / len(similarities)

        # Drift = how far from the average baseline
        drift_score = round(1.0 - max_sim, 4)
        drift_detected = drift_score > self.threshold

        if drift_detected:
            self.drift_events.append(drift_score)

        return DriftResult(
            drift_detected=drift_detected,
            drift_score=drift_score,
            baseline_similarity=round(baseline_sim, 4),
            threshold=self.threshold,
        )

    @property
    def total_drift_events(self) -> int:
        return len(self.drift_events)
