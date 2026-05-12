import time
import uuid
from typing import List

from models import QueryRequest, QueryResponse, RetrievedDocument
from ml.bert_classifier import BERTClassifier
from ml.cosine_drift_monitor import CosineDriftMonitor
from ml.retrieval_engine import RetrievalEngine
from ml.integrity_scorer import IntegrityScorer

# Simple in-memory metrics store
_metrics = {
    "total_queries": 0,
    "attacks_detected": 0,
    "attack_breakdown": {},
    "integrity_scores": [],
}


def _generate_response(
    query: str, documents: List[RetrievedDocument], is_attack: bool
) -> str:
    if is_attack:
        return (
            "⚠️ This query was flagged as potentially adversarial. "
            "For security reasons, the full RAG pipeline has been paused. "
            "Please rephrase your query using safe, legitimate language."
        )

    if not documents:
        return "No relevant documents were found in the knowledge base for your query."

    top_doc = documents[0]
    return (
        f"Based on retrieved knowledge: {top_doc.content} "
        f"(Source: {top_doc.source})"
    )


class RAGPipeline:
    def __init__(
        self,
        classifier: BERTClassifier,
        drift_monitor: CosineDriftMonitor,
        retrieval_engine: RetrievalEngine,
        integrity_scorer: IntegrityScorer,
    ):
        self.classifier = classifier
        self.drift_monitor = drift_monitor
        self.retrieval_engine = retrieval_engine
        self.integrity_scorer = integrity_scorer
        print("[RAGPipeline] All components wired")

    def process(self, request: QueryRequest) -> QueryResponse:
        start = time.time()
        query_id = str(uuid.uuid4())[:8]

        # 1. Attack classification
        attack_result = self.classifier.classify(request.query)

        # 2. Drift analysis
        drift_result = self.drift_monitor.analyze(request.query)

        # 3. Retrieval (still retrieve for display, but flag if attack)
        documents = self.retrieval_engine.retrieve(request.query)

        # 4. Integrity scoring
        integrity_score = self.integrity_scorer.score(request.query, documents)

        # 5. Generate response
        response_text = _generate_response(
            request.query, documents, attack_result.is_attack
        )

        # Update metrics
        _metrics["total_queries"] += 1
        _metrics["integrity_scores"].append(integrity_score)
        if attack_result.is_attack:
            _metrics["attacks_detected"] += 1
            atype = attack_result.attack_type.value
            _metrics["attack_breakdown"][atype] = (
                _metrics["attack_breakdown"].get(atype, 0) + 1
            )

        elapsed_ms = round((time.time() - start) * 1000, 2)

        return QueryResponse(
            query_id=query_id,
            original_query=request.query,
            attack_detection=attack_result,
            drift_analysis=drift_result,
            retrieved_documents=documents,
            response=response_text,
            overall_integrity_score=integrity_score,
            processing_time_ms=elapsed_ms,
        )

    def get_metrics(self):
        total = _metrics["total_queries"]
        attacks = _metrics["attacks_detected"]
        scores = _metrics["integrity_scores"]
        return {
            "total_queries": total,
            "attacks_detected": attacks,
            "attack_rate": round(attacks / total, 4) if total else 0.0,
            "avg_integrity_score": round(sum(scores) / len(scores), 4) if scores else 0.0,
            "drift_events": self.drift_monitor.total_drift_events,
            "attack_breakdown": _metrics["attack_breakdown"],
        }
