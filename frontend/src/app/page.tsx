"use client";
import { useEffect } from "react";
import { useAppStore } from "../store";
import { useQuery } from "../hooks/useQuery";
import Header from "../components/Header";
import MetricCards from "../components/MetricCards";
import QueryPanel from "../components/QueryPanel";
import ResultCard from "../components/ResultCard";
import AttackSimulator from "../components/AttackSimulator";
import AttackChart from "../components/AttackChart";

export default function Home() {
  const { metrics, queryHistory } = useAppStore();
  const { loadMetrics } = useQuery();

  useEffect(() => {
    loadMetrics();
  }, []);

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main className="max-w-7xl mx-auto px-6 py-8 space-y-8">
        {/* Metrics */}
        <MetricCards metrics={metrics} />

        {/* Main grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left: Query + Results */}
          <div className="lg:col-span-2 space-y-4">
            <QueryPanel />

            {queryHistory.length > 0 && (
              <div className="space-y-3">
                <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">
                  Query History ({queryHistory.length})
                </h2>
                {queryHistory.map((r) => (
                  <ResultCard key={r.query_id} result={r} />
                ))}
              </div>
            )}

            {queryHistory.length === 0 && (
              <div className="border border-border rounded-xl p-12 text-center">
                <p className="text-gray-500 text-sm">
                  Submit a query above to analyze it for adversarial attacks, drift, and integrity.
                </p>
              </div>
            )}
          </div>

          {/* Right: Simulator + Chart */}
          <div className="space-y-6">
            <AttackSimulator />
            <AttackChart metrics={metrics} />

            {/* Drift info */}
            <div className="bg-surface border border-border rounded-xl p-4">
              <h3 className="text-sm font-semibold mb-3">Drift Monitor</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-400">Drift Events</span>
                  <span className="text-warning font-mono">{metrics?.drift_events ?? 0}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Threshold</span>
                  <span className="text-gray-300 font-mono">0.15</span>
                </div>
                <div className="w-full bg-surface-2 rounded-full h-1.5 mt-2">
                  <div
                    className="bg-accent rounded-full h-1.5 transition-all"
                    style={{
                      width: `${Math.min(100, (metrics?.drift_events ?? 0) * 10)}%`,
                    }}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
