from fastapi import APIRouter, Request, HTTPException
from models import QueryRequest, QueryResponse

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def process_query(body: QueryRequest, request: Request):
    try:
        pipeline = request.app.state.pipeline
        result = pipeline.process(body)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
