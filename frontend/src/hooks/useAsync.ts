import { useCallback, useEffect, useState, type DependencyList } from "react";

export function useAsync<T>(loader: () => Promise<T>, deps: DependencyList) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      setData(await loader());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Não foi possível carregar.");
    } finally {
      setLoading(false);
    }
  // The caller provides the same dependency list that controls the loader.
  // eslint-disable-next-line react-hooks/exhaustive-deps, react-hooks/use-memo
  }, deps);

  useEffect(() => {
    void load();
  }, [load]);

  return { data, loading, error, reload: load };
}
