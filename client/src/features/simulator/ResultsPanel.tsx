import type { AiResponse, Catalog, Evaluation } from "../../shared/api/types";
import styles from "./Simulator.module.css";
export const number = (value: string | number) =>
  Number(value).toLocaleString("ru-RU", {
    maximumFractionDigits: 2,
    minimumFractionDigits: 2,
  });
export const delta = (value: string) =>
  `${Number(value) > 0 ? "+" : ""}${number(value)}`;
interface Props {
  result: Evaluation;
  catalog: Catalog;
  ai: AiResponse | null;
  busy: boolean;
  onAnalyze: () => void;
}
export function ResultsPanel({ result, catalog, ai, busy, onAnalyze }: Props) {
  return (
    <div className={styles.results}>
      <div className={styles.resultHero}>
        <span>ASTANA QUALITY OF LIFE</span>
        <div>
          {number(result.after.score)}
          <small>{delta(result.score_delta)}</small>
        </div>
        <p>Было {number(result.before.score)} · горизонт 2 года</p>
      </div>
      <div className={styles.metrics}>
        <div>
          <strong>
            {result.spent}
            <small> / 100</small>
          </strong>
          <span>Инвестировано</span>
        </div>
        <div>
          <strong>
            {result.after.critical_count}
            <small> / {result.before.critical_count}</small>
          </strong>
          <span>Критических: стало / было</span>
        </div>
      </div>
      <h3>Как изменились районы</h3>
      {result.district_changes.map((item) => (
        <div key={item.district_id} className={styles.districtRow}>
          <div>
            <strong>
              {catalog.districts.find((d) => d.id === item.district_id)?.name}
            </strong>
            <span>
              {number(item.before)} → {number(item.after)}
            </span>
          </div>
          <b>{delta(item.delta)}</b>
          <progress max={100} value={Number(item.after)} />
        </div>
      ))}
      <details className={styles.details}>
        <summary>Показатели и вклад решений</summary>
        {result.changes
          .filter((c) => Number(c.delta) !== 0)
          .map((c) => (
            <p key={`${c.district_id}${c.indicator_id}`}>
              <strong>
                {catalog.districts.find((d) => d.id === c.district_id)?.name}
              </strong>{" "}
              · {catalog.indicators.find((i) => i.id === c.indicator_id)?.name}
              <br />
              {number(c.before)} → {number(c.after)} <b>{delta(c.delta)}</b>
            </p>
          ))}
        <h4>Сработавшие синергии</h4>
        {result.contributions.filter((c) => c.kind === "synergy").length ? (
          result.contributions
            .filter((c) => c.kind === "synergy")
            .map((c) => (
              <p key={c.measure_ids.join("-")}>
                {c.measure_ids.join(" + ")} ·{" "}
                {catalog.districts.find((d) => d.id === c.district_id)?.name}:{" "}
                {c.indicator_id} +{number(c.raw_delta)}
              </p>
            ))
        ) : (
          <p>В этом наборе нет синергий.</p>
        )}
      </details>
      <section className={styles.ai}>
        <div className={styles.aiTitle}>
          <span>✦</span>
          <h3>Советник акима</h3>
          <small>OPENAI</small>
        </div>
        <p>Сильные стороны, риски и последствия ваших решений.</p>
        <button disabled={busy} onClick={onAnalyze}>
          {busy
            ? "Готовим анализ…"
            : ai?.analysis
              ? "Обновить AI-анализ"
              : "Проанализировать с ИИ"}{" "}
          →
        </button>
        {ai && (
          <div aria-live="polite">
            {ai.analysis ? (
              <>
                <p>{ai.analysis.summary}</p>
                {(
                  [
                    ["Сильные стороны", ai.analysis.strengths],
                    ["Риски", ai.analysis.risks],
                    ["Последствия", ai.analysis.consequences],
                    ["Рекомендации", ai.analysis.recommendations],
                  ] as const
                ).map(([label, items]) => (
                  <div key={label}>
                    <h4>{label}</h4>
                    <ul>
                      {items.map((text, i) => (
                        <li key={i}>{text}</li>
                      ))}
                    </ul>
                  </div>
                ))}
              </>
            ) : (
              <p className={styles.aiNotice}>{ai.message}</p>
            )}
          </div>
        )}
      </section>
      <p className={styles.footnote}>
        Показатели синтетические. Результат описывает учебную модель, а не
        прогноз реальной жизни города.
      </p>
    </div>
  );
}
