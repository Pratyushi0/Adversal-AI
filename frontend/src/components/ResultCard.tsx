"use client";
import { ChevronDown, ChevronUp, ShieldCheck, ShieldAlert } from "lucide-react";
import { useState } from "react";
import type { QueryResponse } from "../lib/api";

const THREAT_COLORS: Record<string, string> = {
  safe: "text-success bg-green-500/10 border-green-500/30",
  low: "text-lime-400 bg-lime-500/10 border-lime-500/30",
  medium: "text-warning bg-yellow-500/10 border-yellow-500/30",
  high: "text-orange-400 bg-orange-500/10 border-orange-500/30",
  critical: "text-danger bg-red-500/10 border-red-500/30",
};

function ThreatBadge({ level }: { level: string }) {
  const cls = THREAT_COLORS[level] ?? "text-gray-400 bg-gray-500/10";
  return (
    <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${cls} uppercase`}>
      {level}
    </span>
  );
}

interface Props {
  result: QueryResponse;
}

export default function ResultCard({ result }: Props) {
  const [open, setOpen] = useState(false);
  const isAttack = result.attack_detection.is_attack;

  return (
    <div
      className={`border rounded-xl overflow-hidden transition-all ${
        isAttack ? "border-red-500/50 bg-red-950/20" : "border-border bg-surface"
      }`}
    >
      {/* Header */}
      <div
        className="flex items-center justify-between p-4 cursor-pointer"
        onClick={() => setOpen(!open)}
      >
        <div className="flex items-center gap-3 min-w-0">
          {isAttack ? (
            <ShieldAlert className="w-5 h-5 text-danger shrink-0" />
          ) : (
            <ShieldCheck className="w-5 h-5 text-success shrink-0" />
          )}
          <div className="min-w-0">
            <p className="text-sm font-medium truncate">{result.original_query}</p>
            <p className="text-xs text-gray-500">
              ID: {result.query_id} · {result.processing_time_ms}ms
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3 shrink-0">
          <ThreatBadge level={result.attack_detection.threat_level} />
          {open ? <ChevronUp className="w-4 h-4 text-gray-400" /> : <ChevronDown className="w-4 h-4 text-gray-400" />}
        </div>
      </div>

      {/* Expanded */}
      {open && (
        <div className="border-t border-border p-4 space-y-4">
          {/* Attack detection */}
          <Section title="Attack Detection">
            <Row label="Type" value={result.attack_detection.attack_type.replace(/_/g, " ")} />
            <Row label="Confidence" value={`${(result.attack_detection.confidence * 100).toFixed(1)}%`} />
            <Row label="Explanation" value={result.attack_detection.explanation} />
          </Section>

          {/* Drift */}
          <Section title="Drift Analysis">
            <Row label="Drift Detected" value={result.drift_analysis.drift_detected ? "Yes" : "No"} />
            <Row label="Drift Score" value={result.drift_analysis.drift_score.toFixed(4)} />
            <Row label="Baseline Similarity" value={result.drift_analysis.baseline_similarity.toFixed(4)} />
          </Section>

          {/* Integrity */}
          <Section title="Pipeline Integrity">
            <Row
              label="Overall Score"
              value={`${(result.overall_integrity_score * 100).toFixed(1)}%`}
            />
          </Section>

          {/* Retrieved docs */}
          <Section title={`Retrieved Documents (${result.retrieved_documents.length})`}>
            <div className="space-y-2">
              {result.retrieved_documents.map((doc) => (
                <div key={doc.id} className="bg-surface-2 rounded-lg p-3 text-xs space-y-1">
                  <p className="text-gray-400">{doc.source}</p>
                  <p className="text-gray-300 line-clamp-2">{doc.content}</p>
                  <div className="flex gap-4 text-gray-500">
                    <span>Similarity: {(doc.similarity_score * 100).toFixed(1)}%</span>
                    <span>Integrity: {(doc.integrity_score * 100).toFixed(1)}%</span>
                  </div>
                </div>
              ))}
            </div>
          </Section>

          {/* Response */}
          <Section title="System Response">
            <p className="text-sm text-gray-300 leading-relaxed">{result.response}</p>
          </Section>
        </div>
      )}
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div>
      <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">{title}</h4>
      <div className="space-y-1">{children}</div>
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex gap-2 text-sm">
      <span className="text-gray-500 shrink-0 w-36">{label}:</span>
      <span className="text-gray-200">{value}</span>
    </div>
  );
}
