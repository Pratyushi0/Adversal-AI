import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  headers: { "Content-Type": "application/json" },
});

export interface QueryRequest {
  query: string;
  context?: string;
}

export interface AttackDetectionResult {
  is_attack: boolean;
  attack_type: string;
  confidence: number;
  threat_level: string;
  explanation: string;
}

export interface DriftResult {
  drift_detected: boolean;
  drift_score: number;
  baseline_similarity: number;
  threshold: number;
}

export interface RetrievedDocument {
  id: string;
  content: string;
  source: string;
  similarity_score: number;
  integrity_score: number;
}

export interface QueryResponse {
  query_id: string;
  original_query: string;
  attack_detection: AttackDetectionResult;
  drift_analysis: DriftResult;
  retrieved_documents: RetrievedDocument[];
  response: string;
  overall_integrity_score: number;
  processing_time_ms: number;
}

export interface MetricsSummary {
  total_queries: number;
  attacks_detected: number;
  attack_rate: number;
  avg_integrity_score: number;
  drift_events: number;
  attack_breakdown: Record<string, number>;
}

export interface AttackSimRequest {
  attack_type: string;
  target_query?: string;
}

export interface AttackSimResponse {
  original_query: string;
  adversarial_query: string;
  attack_type: string;
  detection_result: AttackDetectionResult;
}

export const apiClient = {
  health: () => api.get("/health"),
  query: (body: QueryRequest) => api.post<QueryResponse>("/query", body),
  metrics: () => api.get<MetricsSummary>("/metrics"),
  resetMetrics: () => api.delete("/metrics/reset"),
  attackTypes: () => api.get("/attacks/types"),
  simulateAttack: (body: AttackSimRequest) =>
    api.post<AttackSimResponse>("/attacks/simulate", body),
};

export default apiClient;
