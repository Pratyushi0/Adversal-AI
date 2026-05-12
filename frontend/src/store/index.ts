import { create } from "zustand";
import type { QueryResponse, MetricsSummary } from "../lib/api";

interface AppState {
  queryHistory: QueryResponse[];
  metrics: MetricsSummary | null;
  isLoading: boolean;
  error: string | null;
  addQueryResult: (result: QueryResponse) => void;
  setMetrics: (m: MetricsSummary) => void;
  setLoading: (v: boolean) => void;
  setError: (e: string | null) => void;
  clearHistory: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  queryHistory: [],
  metrics: null,
  isLoading: false,
  error: null,

  addQueryResult: (result) =>
    set((s) => ({ queryHistory: [result, ...s.queryHistory].slice(0, 50) })),

  setMetrics: (metrics) => set({ metrics }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
  clearHistory: () => set({ queryHistory: [] }),
}));
