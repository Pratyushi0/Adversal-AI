from fastapi import APIRouter, Request
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check(request: Request):
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "bert_classifier": "operational",
            "drift_monitor": "operational",
            "retrieval_engine": "operational",
            "integrity_scorer": "operational",
        },
        "model": request.app.state.classifier.model_name,
    }
