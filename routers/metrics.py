from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/metrics")
async def get_metrics(request: Request):
    pipeline = request.app.state.pipeline
    return pipeline.get_metrics()

@router.delete("/metrics/reset")
async def reset_metrics(request: Request):
    # Reset in-memory metrics via pipeline
    from ml.pipeline import _metrics
    _metrics["total_queries"] = 0
    _metrics["attacks_detected"] = 0
    _metrics["attack_breakdown"] = {}
    _metrics["integrity_scores"] = []
    return {"message": "Metrics reset successfully"}
