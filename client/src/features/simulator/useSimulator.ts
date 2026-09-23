import { useEffect, useState } from "react";
import { analyze, evaluate, getCatalog } from "../../shared/api/client";
import type {
  AiResponse,
  CatalogResponse,
  Evaluation,
  Issue,
  Selection,
} from "../../shared/api/types";
import { readSaved, writeSaved, type SavedScenario } from "./storage";

export function useSimulator() {
  const [data, setData] = useState<CatalogResponse | null>(null);
  const [selections, setSelections] = useState<Selection[]>([]);
  const [result, setResult] = useState<Evaluation | null>(null);
  const [issues, setIssues] = useState<Issue[]>([]);
  const [ai, setAi] = useState<AiResponse | null>(null);
  const [phase, setPhase] = useState<"idle" | "calculating" | "analyzing">(
    "idle",
  );
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [saved, setSaved] = useState<SavedScenario[]>([]);
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    const controller = new AbortController();
    void getCatalog(controller.signal)
      .then((value) => {
        setData(value);
        setError("");
        try {
          setSaved(readSaved());
        } catch {
          setNotice("Сохранённые сценарии недоступны в этом браузере.");
        }
      })
      .catch((cause: unknown) => {
        if (!controller.signal.aborted)
          setError(
            cause instanceof Error
              ? cause.message
              : "Не удалось загрузить каталог.",
          );
      });
    return () => controller.abort();
  }, [attempt]);
  const spent = selections.reduce(
    (sum, item) =>
      sum +
      (data?.catalog.measures.find((m) => m.id === item.measure_id)?.cost ?? 0),
    0,
  );
  function change(next: Selection[]) {
    setSelections(next);
    setResult(null);
    setAi(null);
    setIssues([]);
    setError("");
    setNotice("");
  }
  function toggle(id: string) {
    if (selections.some((item) => item.measure_id === id)) {
      change(selections.filter((item) => item.measure_id !== id));
      return;
    }
    const measure = data?.catalog.measures.find((item) => item.id === id);
    if (
      !measure ||
      !data ||
      selections.length >= data.catalog.required_selections ||
      spent + measure.cost > data.catalog.budget
    )
      return;
    change([
      ...selections,
      measure.scope === "city"
        ? { measure_id: id }
        : { measure_id: id, district_id: "nura" },
    ]);
  }
  function district(id: string, district_id: string) {
    change(
      selections.map((item) =>
        item.measure_id === id ? { ...item, district_id } : item,
      ),
    );
  }
  function example() {
    change([
      { measure_id: "M7", district_id: "nura" },
      { measure_id: "M8", district_id: "nura" },
      { measure_id: "M10", district_id: "nura" },
      { measure_id: "M12" },
      { measure_id: "M5", district_id: "saryarka" },
    ]);
  }
  async function calculate(): Promise<boolean> {
    setPhase("calculating");
    setError("");
    setAi(null);
    try {
      const outcome = await evaluate(selections);
      setIssues(outcome.issues);
      setResult(outcome.result);
      return outcome.result !== null;
    } catch {
      setError(
        "Не удалось выполнить расчёт. Проверьте соединение и повторите.",
      );
      return false;
    } finally {
      setPhase("idle");
    }
  }
  async function explain() {
    setPhase("analyzing");
    try {
      setAi(await analyze(selections));
    } catch {
      setError("Не удалось получить AI-анализ. Численный результат сохранён.");
    } finally {
      setPhase("idle");
    }
  }
  function save(name: string) {
    if (!result) return;
    const next = [
      {
        id: crypto.randomUUID(),
        name: name.trim() || `Сценарий ${saved.length + 1}`,
        selections,
        score: result.after.score,
        delta: result.score_delta,
      },
      ...saved,
    ].slice(0, 20);
    try {
      writeSaved(next);
      setSaved(next);
      setNotice("Сценарий сохранён в этом браузере.");
    } catch {
      setNotice("Не удалось сохранить: хранилище браузера недоступно.");
    }
  }
  function remove(id: string) {
    const next = saved.filter((item) => item.id !== id);
    try {
      writeSaved(next);
      setSaved(next);
    } catch {
      setNotice("Не удалось удалить сохранение.");
    }
  }
  return {
    data,
    selections,
    result,
    issues,
    ai,
    phase,
    error,
    notice,
    saved,
    spent,
    toggle,
    district,
    example,
    calculate,
    explain,
    save,
    remove,
    clear: () => change([]),
    load: (item: SavedScenario) => change(item.selections),
    retry: () => setAttempt((value) => value + 1),
  };
}
