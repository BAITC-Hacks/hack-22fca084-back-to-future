import { useState } from "react";
import type { useSimulator } from "./useSimulator";
import { ResultsPanel, delta, number } from "./ResultsPanel";
import styles from "./Simulator.module.css";
const directions: Record<string, string> = {
  transport: "Транспорт",
  ecology: "Экология",
  social: "Соцсфера",
  safety: "Безопасность",
  services: "Сервисы",
};
type Props = { sim: ReturnType<typeof useSimulator> };
export function ScenarioPanel({ sim }: Props) {
  const [tab, setTab] = useState<"decisions" | "results" | "saved">(
    "decisions",
  );
  const [filter, setFilter] = useState("all");
  const [name, setName] = useState("");
  const busy = sim.phase !== "idle";
  if (!sim.data)
    return (
      <div className={styles.loading}>
        <h2>Готовим кабинет акима</h2>
        <p>{sim.error || "Загружаем районы и городские инициативы…"}</p>
        {sim.error && <button onClick={sim.retry}>Повторить</button>}
      </div>
    );
  const { catalog } = sim.data;
  return (
    <section className={styles.panel} aria-label="Симулятор городских решений">
      <div className={styles.heading}>
        <span className={styles.eyebrow}>АКИМ НА 5 ЧАСОВ</span>
        <h1>
          Город начинается
          <br />
          <em>с ваших решений.</em>
        </h1>
        <p>Пять инициатив. Один бюджет. Будущее Астаны.</p>
      </div>
      <div className={styles.budget}>
        <div>
          <span>Бюджет развития</span>
          <strong>
            {sim.spent}
            <small> / {catalog.budget}</small>
          </strong>
        </div>
        <span className={styles.remaining}>
          Осталось {catalog.budget - sim.spent}
        </span>
        <progress max={catalog.budget} value={sim.spent} />
      </div>
      <nav className={styles.tabs} aria-label="Разделы симулятора">
        {(
          [
            ["decisions", "Решения"],
            ["results", "Результат"],
            ["saved", `Сценарии · ${sim.saved.length}`],
          ] as const
        ).map(([id, label]) => (
          <button
            key={id}
            className={tab === id ? styles.activeTab : ""}
            onClick={() => setTab(id)}
          >
            {label}
          </button>
        ))}
      </nav>
      <div className={styles.content}>
        {sim.error && (
          <p className={styles.error} role="alert">
            {sim.error}
          </p>
        )}
        {sim.notice && (
          <p className={styles.notice} role="status">
            {sim.notice}
          </p>
        )}
        {tab === "decisions" && (
          <>
            <div className={styles.quick}>
              <span>
                Выбрано{" "}
                <b>
                  {sim.selections.length} из {catalog.required_selections}
                </b>
              </span>
              <button disabled={busy} onClick={sim.example}>
                Пример из кейса ↗
              </button>
              <button
                disabled={busy || !sim.selections.length}
                onClick={sim.clear}
              >
                Сбросить
              </button>
            </div>
            <div className={styles.filters}>
              <button
                className={filter === "all" ? styles.selectedFilter : ""}
                onClick={() => setFilter("all")}
              >
                Все 14
              </button>
              {Object.entries(directions).map(([id, label]) => (
                <button
                  key={id}
                  className={filter === id ? styles.selectedFilter : ""}
                  onClick={() => setFilter(id)}
                >
                  {label}
                </button>
              ))}
            </div>
            <div className={styles.measures}>
              {catalog.measures
                .filter((m) => filter === "all" || m.direction === filter)
                .map((measure) => {
                  const selected = sim.selections.find(
                    (item) => item.measure_id === measure.id,
                  );
                  const blocked =
                    !selected &&
                    (sim.selections.length >= catalog.required_selections ||
                      sim.spent + measure.cost > catalog.budget);
                  return (
                    <article
                      key={measure.id}
                      className={`${styles.measure} ${selected ? styles.chosen : ""}`}
                    >
                      <button
                        className={styles.measureToggle}
                        disabled={busy || blocked}
                        onClick={() => sim.toggle(measure.id)}
                        aria-pressed={!!selected}
                        aria-label={`${selected ? "Убрать" : "Добавить"} ${measure.name}`}
                      >
                        <span className={styles.check}>
                          {selected ? "✓" : "+"}
                        </span>
                        <span>
                          <small>
                            {directions[measure.direction]} ·{" "}
                            {measure.scope === "city"
                              ? "Весь город"
                              : "Один район"}
                          </small>
                          <strong>{measure.name}</strong>
                        </span>
                        <b>
                          {measure.cost}
                          <small>ед.</small>
                        </b>
                      </button>
                      <div className={styles.effectLine}>
                        <span>
                          {measure.effects
                            .map(
                              (e) =>
                                `${e.indicator_id} ${Number(e.value) > 0 ? "+" : ""}${e.value}`,
                            )
                            .join(" · ")}
                        </span>
                        <span>Лаг {measure.lag} кв.</span>
                      </div>
                      {selected && measure.scope === "district" && (
                        <label className={styles.districtSelect}>
                          Район
                          <select
                            disabled={busy}
                            value={selected.district_id ?? ""}
                            onChange={(event) =>
                              sim.district(measure.id, event.target.value)
                            }
                          >
                            {catalog.districts.map((d) => (
                              <option key={d.id} value={d.id}>
                                {d.name}
                              </option>
                            ))}
                          </select>
                        </label>
                      )}
                    </article>
                  );
                })}
            </div>
            <p className={styles.footnote}>
              Не более двух мер одного направления. Эффекты показаны до учёта
              лага; синергии и ограничения проверяются сервером.
            </p>
          </>
        )}
        {tab === "results" &&
          (sim.result ? (
            <>
              <ResultsPanel
                result={sim.result}
                catalog={catalog}
                ai={sim.ai}
                busy={busy}
                onAnalyze={() => {
                  void sim.explain();
                }}
              />
              <form
                className={styles.save}
                onSubmit={(event) => {
                  event.preventDefault();
                  sim.save(name);
                }}
              >
                <label>
                  Название сценария
                  <input
                    maxLength={80}
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Например, Нура — приоритет"
                  />
                </label>
                <button type="submit">Сохранить сценарий</button>
              </form>
            </>
          ) : (
            <div className={styles.empty}>
              <span>↗</span>
              <h3>Каким станет ваш город?</h3>
              <p>
                Выберите пять инициатив и запустите расчёт. Здесь появятся Score
                и изменения районов.
              </p>
              <button onClick={() => setTab("decisions")}>К решениям</button>
            </div>
          ))}
        {tab === "saved" && (
          <>
            <h3>Ваши стратегии</h3>
            <p className={styles.footnote}>
              Сохраняются только в этом браузере. До 20 сценариев.
            </p>
            {sim.saved.length ? (
              sim.saved.map((item) => (
                <article className={styles.saved} key={item.id}>
                  <div>
                    <h3>{item.name}</h3>
                    <strong>
                      {number(item.score)} <small>{delta(item.delta)}</small>
                    </strong>
                  </div>
                  <button
                    disabled={busy}
                    onClick={() => {
                      sim.load(item);
                      setTab("decisions");
                    }}
                  >
                    Открыть
                  </button>
                  <button
                    onClick={() => sim.remove(item.id)}
                    aria-label={`Удалить ${item.name}`}
                  >
                    ×
                  </button>
                </article>
              ))
            ) : (
              <div className={styles.empty}>
                <p>
                  Рассчитайте и сохраните первый сценарий, чтобы сравнить
                  варианты.
                </p>
              </div>
            )}
          </>
        )}
      </div>
      <footer className={styles.actions}>
        {sim.issues.length > 0 && (
          <ul className={styles.errors} role="alert">
            {sim.issues.map((issue, i) => (
              <li key={i}>
                {issue.message} {issue.measure_ids?.join(", ")}
              </li>
            ))}
          </ul>
        )}
        <button
          className={styles.primary}
          disabled={busy}
          onClick={() => {
            void sim.calculate().then((ok) => {
              if (ok) setTab("results");
              else setTab("decisions");
            });
          }}
        >
          {sim.phase === "calculating"
            ? "Считаем влияние…"
            : "Рассчитать будущее города"}{" "}
          <span>→</span>
        </button>
      </footer>
    </section>
  );
}
