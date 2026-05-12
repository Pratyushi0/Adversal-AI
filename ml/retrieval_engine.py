import math
import random
from typing import List
from models import RetrievedDocument
from config import settings

KNOWLEDGE_BASE = [
    {
        "id": "doc_001",
        "content": "Prompt injection attacks attempt to override AI system instructions by embedding malicious directives within user input. These attacks exploit the model's tendency to follow instructions without verifying their source.",
        "source": "AI Security Handbook, Chapter 4",
    },
    {
        "id": "doc_002",
        "content": "Retrieval Augmented Generation (RAG) combines a retrieval system with a language model. The retrieval component fetches relevant documents from a knowledge base, which the LLM uses to generate grounded responses.",
        "source": "RAG Architecture Overview",
    },
    {
        "id": "doc_003",
        "content": "Adversarial suffixes are specially crafted token sequences appended to benign queries to manipulate model outputs. Research shows these can reliably bypass safety filters when optimized via gradient-based methods.",
        "source": "Zou et al., Universal Adversarial Attacks, 2023",
    },
    {
        "id": "doc_004",
        "content": "Cosine similarity measures the angle between two embedding vectors in high-dimensional space. Values close to 1 indicate high semantic similarity; values near 0 indicate orthogonality; negative values indicate opposition.",
        "source": "Information Retrieval Fundamentals",
    },
    {
        "id": "doc_005",
        "content": "Jailbreaking refers to techniques that attempt to make an AI model produce content that violates its safety guidelines, often through roleplay framing, hypothetical scenarios, or persona injection.",
        "source": "Red-Teaming AI Systems, NIST Report",
    },
    {
        "id": "doc_006",
        "content": "Data poisoning in RAG systems occurs when malicious documents are introduced into the knowledge base. These documents can steer model outputs toward attacker-controlled responses.",
        "source": "RAG Security Threat Model",
    },
    {
        "id": "doc_007",
        "content": "BERT (Bidirectional Encoder Representations from Transformers) pre-trains deep bidirectional representations by jointly conditioning on both left and right context. It achieves state-of-the-art results on classification and NER tasks.",
        "source": "Devlin et al., BERT Paper, 2019",
    },
    {
        "id": "doc_008",
        "content": "Semantic drift in AI deployments refers to gradual divergence of input distributions from training-time distributions. Monitoring embedding distances over time can detect when model assumptions no longer hold.",
        "source": "MLOps Best Practices Guide",
    },
    {
        "id": "doc_009",
        "content": "Defense in depth for LLM systems includes input sanitization, output filtering, intent classification, retrieval integrity checks, and human-in-the-loop review for high-risk decisions.",
        "source": "LLM Security Framework v2",
    },
    {
        "id": "doc_010",
        "content": "Integrity scoring evaluates the trustworthiness of retrieved documents by checking source provenance, content consistency, embedding coherence, and cross-reference validation with known-good sources.",
        "source": "Document Integrity Assessment Methods",
    },
]


def _fake_embed(text: str, dim: int = 64) -> List[float]:
    random.seed(hash(text) % (2**32))
    vec = [random.gauss(0, 1) for _ in range(dim)]
    norm = math.sqrt(sum(v**2 for v in vec))
    return [v / norm for v in vec]


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    return max(0.0, min(1.0, dot))


class RetrievalEngine:
    def __init__(self):
        self._embeddings = {
            doc["id"]: _fake_embed(doc["content"]) for doc in KNOWLEDGE_BASE
        }
        print(f"[RetrievalEngine] Indexed {len(KNOWLEDGE_BASE)} documents")

    def retrieve(self, query: str, top_k: int = None) -> List[RetrievedDocument]:
        if top_k is None:
            top_k = settings.TOP_K_RETRIEVAL

        query_emb = _fake_embed(query)
        scored = []
        for doc in KNOWLEDGE_BASE:
            sim = _cosine_similarity(query_emb, self._embeddings[doc["id"]])
            # Slight noise for realism
            sim = min(1.0, sim + random.uniform(-0.05, 0.05))
            scored.append((doc, sim))

        scored.sort(key=lambda x: x[1], reverse=True)

        results = []
        for doc, sim in scored[:top_k]:
            integrity = round(random.uniform(0.70, 0.99), 4)
            results.append(
                RetrievedDocument(
                    id=doc["id"],
                    content=doc["content"],
                    source=doc["source"],
                    similarity_score=round(sim, 4),
                    integrity_score=integrity,
                )
            )
        return results
