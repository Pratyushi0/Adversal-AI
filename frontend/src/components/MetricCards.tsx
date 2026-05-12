"use client";
import { Shield, AlertTriangle, Activity, Database } from "lucide-react";
import type { MetricsSummary } from "../lib/api";

interface Props {
  metrics: MetricsSummary | null;
}

const cards = (m: MetricsSummary | null) => [
  {
    label: "Total Queries",
    value: m?.total_queries ?? 0,
    icon: Database,
    color: "text-accent-glow",
    bg: "bg-indigo-500/10",
  },
  {
    label: "Attacks Detected",
    value: m?.attacks_detected ?? 0,
    icon: AlertTriangle,
    color: "text-danger",
    bg: "bg-red-500/10",
  },
  {
    label: "Attack Rate",
    value: m ? `${(m.attack_rate * 100).toFixed(1)}%` : "0%",
    icon: Shield,
    color: "text-warning",
    bg: "bg-yellow-500/10",
  },
  {
    label: "Avg Integrity",
    value: m ? `${(m.avg_integrity_score * 100).toFixed(1)}%` : "—",
    icon: Activity,
    color: "text-success",
    bg: "bg-green-500/10",
  },
];

export default function MetricCards({ metrics }: Props) {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {cards(metrics).map((c) => {
        const Icon = c.icon;
        return (
          <div
            key={c.label}
            className="bg-surface border border-border rounded-xl p-4 flex items-center gap-4"
          >
            <div className={`${c.bg} p-3 rounded-lg`}>
              <Icon className={`w-5 h-5 ${c.color}`} />
            </div>
            <div>
              <p className="text-xs text-gray-400">{c.label}</p>
              <p className={`text-2xl font-bold ${c.color}`}>{c.value}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
