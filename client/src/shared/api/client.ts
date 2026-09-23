import type { AiResponse, CatalogResponse, Outcome, Selection } from "./types";

async function request<T>(
  path: string,
  selections?: Selection[],
  signal?: AbortSignal,
): Promise<T> {
  const response = await fetch(`/api${path}`, {
    method: selections ? "POST" : "GET",
    headers: { "Content-Type": "application/json" },
    ...(selections ? { body: JSON.stringify({ selections }) } : {}),
    ...(signal ? { signal } : { signal: AbortSignal.timeout(200000) }),
  });
  if (!response.ok && response.status !== 422)
    throw new Error("Сервер недоступен. Попробуйте ещё раз.");
  return (await response.json()) as T;
}
export const getCatalog = (signal: AbortSignal) =>
  request<CatalogResponse>("/catalog", undefined, signal);
export const evaluate = (selections: Selection[]) =>
  request<Outcome>("/scenarios/evaluate", selections);
export const analyze = (selections: Selection[]) =>
  request<AiResponse>("/scenarios/analyze", selections);
