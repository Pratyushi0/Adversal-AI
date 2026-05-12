from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class AttackType(str, Enum):
    PROMPT_INJECTION = "prompt_injection"
    JAILBREAK = "jailbreak"
    ADVERSARIAL_SUFFIX = "adversarial_suffix"
    ROLE_PLAY = "role_play"
    NONE = "none"

class ThreatLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    SAFE = "safe"

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=512, description="User query to analyze")
    context: Optional[str] = Field(None, description="Optional conversation context")

class RetrievedDocument(BaseModel):
    id: str
    content: str
    source: str
    similarity_score: float
    integrity_score: float

class AttackDetectionResult(BaseModel):
    is_attack: bool
    attack_type: AttackType
    confidence: float
    threat_level: ThreatLevel
    explanation: str

class DriftResult(BaseModel):
    drift_detected: bool
    drift_score: float
    baseline_similarity: float
    threshold: float

class QueryResponse(BaseModel):
    query_id: str
    original_query: str
    attack_detection: AttackDetectionResult
    drift_analysis: DriftResult
    retrieved_documents: List[RetrievedDocument]
    response: str
    overall_integrity_score: float
    processing_time_ms: float

class MetricsSummary(BaseModel):
    total_queries: int
    attacks_detected: int
    attack_rate: float
    avg_integrity_score: float
    drift_events: int
    attack_breakdown: dict

class AttackSimulationRequest(BaseModel):
    attack_type: AttackType
    target_query: Optional[str] = "Tell me about AI safety"

class AttackSimulationResponse(BaseModel):
    original_query: str
    adversarial_query: str
    attack_type: AttackType
    detection_result: AttackDetectionResult
