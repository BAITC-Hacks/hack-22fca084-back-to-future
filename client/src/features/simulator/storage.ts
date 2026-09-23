import type { Selection } from "../../shared/api/types";

export interface SavedScenario {
  id: string;
  name: string;
  selections: Selection[];
  score: string;
  delta: string;
}
const KEY = "astana.scenarios.v1";
function validSelection(value: unknown): value is Selection {
  if (
    !value ||
    typeof value !== "object" ||
    !("measure_id" in value) ||
    typeof value.measure_id !== "string"
  )
    return false;
  return (
    !("district_id" in value) ||
    value.district_id === null ||
    typeof value.district_id === "string"
  );
}
export function readSaved(): SavedScenario[] {
  const raw: unknown = JSON.parse(localStorage.getItem(KEY) ?? "[]");
  if (!Array.isArray(raw)) return [];
  return raw
    .filter((item: unknown): item is SavedScenario => {
      if (!item || typeof item !== "object") return false;
      return (
        "id" in item &&
        typeof item.id === "string" &&
        "name" in item &&
        typeof item.name === "string" &&
        "score" in item &&
        typeof item.score === "string" &&
        Number.isFinite(Number(item.score)) &&
        "delta" in item &&
        typeof item.delta === "string" &&
        Number.isFinite(Number(item.delta)) &&
        "selections" in item &&
        Array.isArray(item.selections) &&
        item.selections.length === 5 &&
        item.selections.every(validSelection)
      );
    })
    .slice(0, 20);
}
export function writeSaved(items: SavedScenario[]) {
  localStorage.setItem(KEY, JSON.stringify(items));
}
