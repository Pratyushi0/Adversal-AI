import { useCallback } from "react";
import apiClient from "../lib/api";
import { useAppStore } from "../store";

export function useQuery() {
  const { setLoading, setError, addQueryResult, setMetrics } = useAppStore();

  const submitQuery = useCallback(
    async (query: string, context?: string) => {
      setLoading(true);
      setError(null);
      try {
        const res = await apiClient.query({ query, context });
        addQueryResult(res.data);

        // Refresh metrics after query
        const mRes = await apiClient.metrics();
        setMetrics(mRes.data);

        return res.data;
      } catch (e: any) {
        const msg = e?.response?.data?.detail || e.message || "Unknown error";
        setError(msg);
        return null;
      } finally {
        setLoading(false);
      }
    },
    [setLoading, setError, addQueryResult, setMetrics]
  );

  const loadMetrics = useCallback(async () => {
    try {
      const res = await apiClient.metrics();
      setMetrics(res.data);
    } catch {}
  }, [setMetrics]);

  return { submitQuery, loadMetrics };
}
