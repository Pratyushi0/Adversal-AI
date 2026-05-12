"use client";
import { useState } from "react";
import { FlaskConical, Loader2 } from "lucide-react";
import apiClient, { AttackSimResponse } from "../lib/api";

const ATTACK_TYPES = [
  { id: "prompt_injection", label: "Prompt Injection", color: "text-danger" },
  { id: "jailbreak", label: "Jailbreak", color: "text-orange-400" },
  { id: "adversarial_suffix", label: "Adversarial Suffix", color: "text-warning" },
  { id: "role_play", label: "Role Play", color: "text-yellow-300" },
];

export default function AttackSimulator() {
  const [selectedType, setSelectedType] = useState("prompt_injection");
  const [targetQuery, setTargetQuery] = useState("Tell me about AI safety");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AttackSimResponse | null>(null);

  const simulate = async () => {
    setLoading(true);
    try {
      const res = await apiClient.simulateAttack({
        attack_type: selectedType,
        target_query: targetQuery,
      });
      setResult(res.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-surface border border-border rounded-xl p-6 space-y-4">
      <h2 className="text-lg font-semibold flex items-center gap-2">
        <FlaskConical className="w-5 h-5 text-warning" />
        Attack Simulator
      </h2>

      <div className="grid grid-cols-2 gap-2">
        {ATTACK_TYPES.map((t) => (
          <button
            key={t.id}
            onClick={() => setSelectedType(t.id)}
            className={`text-xs p-3 rounded-lg border text-left transition-colors ${
              selectedType === t.id
                ? "border-accent bg-accent/10"
                : "border-border hover:border-accent/50"
            } ${t.color}`}
          >
            {t.label}
          </button>
        ))}
      </div>

      <input
        className="w-full bg-surface-2 border border-border rounded-lg p-3 text-sm focus:outline-none focus:border-accent transition-colors"
        placeholder="Target query..."
        value={targetQuery}
        onChange={(e) => setTargetQuery(e.target.value)}
      />

      <button
        onClick={simulate}
        disabled={loading}
        className="w-full bg-warning/20 hover:bg-warning/30 border border-warning/50 text-warning font-medium py-2 rounded-lg transition-colors flex items-center justify-center gap-2"
      >
        {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <FlaskConical className="w-4 h-4" />}
        Simulate Attack
      </button>

      {result && (
        <div className="space-y-3 text-sm">
          <div className="bg-surface-2 rounded-lg p-3">
            <p className="text-xs text-gray-500 mb-1">Adversarial Query Generated:</p>
            <p className="text-warning font-mono text-xs break-all">{result.adversarial_query}</p>
          </div>
          <div className="flex items-center gap-2">
            <span className={`text-xs px-2 py-1 rounded ${
              result.detection_result.is_attack ? "bg-red-500/20 text-danger" : "bg-green-500/20 text-success"
            }`}>
              {result.detection_result.is_attack ? "⚠ DETECTED" : "✓ BYPASSED"}
            </span>
            <span className="text-gray-400 text-xs">
              Confidence: {(result.detection_result.confidence * 100).toFixed(1)}%
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
