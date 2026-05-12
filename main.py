from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from routers import health, query, attacks, metrics
from ml.bert_classifier import BERTClassifier
from ml.cosine_drift_monitor import CosineDriftMonitor
from ml.retrieval_engine import RetrievalEngine
from ml.integrity_scorer import IntegrityScorer
from ml.pipeline import RAGPipeline

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize ML components
    classifier = BERTClassifier()
    drift_monitor = CosineDriftMonitor()
    retrieval_engine = RetrievalEngine()
    integrity_scorer = IntegrityScorer()
    pipeline = RAGPipeline(classifier, drift_monitor, retrieval_engine, integrity_scorer)

    app.state.classifier = classifier
    app.state.drift_monitor = drift_monitor
    app.state.retrieval_engine = retrieval_engine
    app.state.integrity_scorer = integrity_scorer
    app.state.pipeline = pipeline

    print("✅ Adversarial AI backend started")
    yield
    print("🛑 Shutting down")

app = FastAPI(
    title="Adversarial AI RAG Security API",
    description="Detects prompt injection, adversarial attacks, and monitors RAG pipeline integrity",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(query.router, prefix="/api", tags=["Query"])
app.include_router(attacks.router, prefix="/api", tags=["Attacks"])
app.include_router(metrics.router, prefix="/api", tags=["Metrics"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
