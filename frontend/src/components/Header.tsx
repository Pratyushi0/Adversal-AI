"use client";
import { Shield, RefreshCw } from "lucide-react";
import { useQuery } from "../hooks/useQuery";
import apiClient from "../lib/api";
import { useAppStore } from "../store";

export default function Header() {
  const { loadMetrics } = useQuery();
  const { clearHistory } = useAppStore();

  const handleReset = async () => {
    await apiClient.resetMetrics();
    clearHistory();
    await loadMetrics();
  };

  return (
    <header className="border-b border-border bg-surface/80 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-accent/20 p-2 rounded-lg">
            <Shield className="w-6 h-6 text-accent" />
          </div>
          <div>
            <h1 className="font-bold text-lg tracking-tight">Adversarial AI</h1>
            <p className="text-xs text-gray-400">RAG Security Monitor</p>
          </div>
        </div>
        <button
          onClick={handleReset}
          className="flex items-center gap-2 text-sm text-gray-400 hover:text-white border border-border hover:border-accent/50 px-3 py-2 rounded-lg transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
          Reset
        </button>
      </div>
    </header>
  );
}
