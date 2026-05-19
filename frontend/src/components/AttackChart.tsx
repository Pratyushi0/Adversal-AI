"use client";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import type { MetricsSummary } from "../lib/api";
import { BarChart2 } from "lucide-react";

const COLORS = ["#ef4444", "#f97316", "#f59e0b", "#84cc16"];

interface Props {
  metrics: MetricsSummary | null;
}

export default function AttackChart({ metrics }: Props) {
  const data = metrics
    ? Object.entries(metrics.attack_breakdown).map(([k, v]) => ({
        name: k.replace(/_/g, " "),
        count: v,
      }))
    : [];

  return (
    <div className="bg-surface border border-border rounded-xl p-6">
      <h2 className="text-lg font-semibold flex items-center gap-2 mb-4">
        <BarChart2 className="w-5 h-5 text-accent" />
        Attack Breakdown
      </h2>
      {data.length === 0 ? (
        <p className="text-gray-500 text-sm text-center py-8">
          No attacks recorded yet. Submit some queries to see data.
        </p>
      ) : (
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={data}>
            <XAxis dataKey="name" tick={{ fill: "#9ca3af", fontSize: 11 }} />
            <YAxis tick={{ fill: "#9ca3af", fontSize: 11 }} />
            <Tooltip
              contentStyle={{
                background: "#111827",
                border: "1px solid #374151",
                borderRadius: "8px",
                fontSize: "12px",
              }}
            />
            <Bar dataKey="count" radius={[4, 4, 0, 0]}>
              {data.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}
