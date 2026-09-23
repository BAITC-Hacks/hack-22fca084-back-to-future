import { useState } from "react";
import { useSimulator } from "../features/simulator/useSimulator";
import { ScenarioPanel } from "../features/simulator/ScenarioPanel";
import { number, delta } from "../features/simulator/ResultsPanel";
import { LANDMARKS } from "../features/map/mapConfig";
import { useCityMap } from "../features/map/useCityMap";
import { Icon } from "../shared/ui/Icon";
import styles from "./MapPage.module.css";

export default function MapPage() {
  const map = useCityMap();
  const sim = useSimulator();
  const [showHelp, setShowHelp] = useState(false);
  const ready = map.status === "ready";
  return (
    <div className={styles.app}>
      <header className={styles.header}>
        <a className={styles.brand} href="/" aria-label="Астана — на главную">
          <span className={styles.brandIcon}>
            <Icon name="map" size={23} />
          </span>
          <span>
            astana<span className={styles.brandDot}>.</span>
            <small>CITY DECISION LAB</small>
          </span>
        </a>
        <div className={styles.breadcrumb}>
          Казахстан <span>/</span> Астана <span>/</span>{" "}
          <strong>Симулятор развития</strong>
        </div>
        <button
          className={styles.helpButton}
          aria-label="Как управлять"
          onClick={() => setShowHelp(!showHelp)}
          aria-expanded={showHelp}
        >
          <Icon name="info" />
          <span>Как управлять</span>
        </button>
      </header>
      <main className={styles.workspace}>
        <aside className={styles.simulatorSidebar}>
          <ScenarioPanel sim={sim} />
        </aside>
        <section
          className={styles.mapRegion}
          aria-label="Интерактивная карта Астаны"
        >
          <div ref={map.containerRef} className={styles.mapCanvas} />
          <div className={styles.mapTop}>
            <div className={styles.locationPill}>
              <span className={styles.liveDot} />
              <strong>Астана, Казахстан</strong>
              <span className={styles.divider} />
              <span>{map.is3d ? "3D" : "2D"}</span>
            </div>
            <select
              className={styles.landmarkSelect}
              aria-label="Городские ориентиры"
              value={map.selected?.id ?? ""}
              onChange={(event) => {
                const landmark = LANDMARKS.find(
                  (item) => item.id === event.target.value,
                );
                if (landmark) map.flyTo(landmark);
              }}
            >
              <option value="" disabled>
                Городские ориентиры
              </option>
              {LANDMARKS.map((item) => (
                <option key={item.id} value={item.id}>
                  {item.name}
                </option>
              ))}
            </select>
          </div>
          <div className={styles.tools} aria-label="Управление камерой">
            <button
              disabled={!ready}
              onClick={map.north}
              aria-label="Повернуть карту на север"
              title="На север"
            >
              <span style={{ transform: `rotate(${-map.camera.bearing}deg)` }}>
                <Icon name="compass" size={24} />
              </span>
              <small>N</small>
            </button>
            <div className={styles.toolGroup}>
              <button
                disabled={!ready}
                onClick={map.zoomIn}
                aria-label="Приблизить"
              >
                <Icon name="plus" />
              </button>
              <button
                disabled={!ready}
                onClick={map.zoomOut}
                aria-label="Отдалить"
              >
                <Icon name="minus" />
              </button>
            </div>
            <button
              disabled={!ready}
              onClick={map.toggleDimension}
              aria-label={map.is3d ? "Включить вид 2D" : "Включить вид 3D"}
              className={styles.dimension}
            >
              {map.is3d ? "2D" : "3D"}
            </button>
            <button
              disabled={!ready}
              onClick={map.resetCamera}
              aria-label="Вернуться к начальному виду"
              title="Начальный вид"
            >
              <Icon name="home" />
            </button>
          </div>
          {map.status !== "ready" && (
            <div
              className={styles.statusCard}
              role={map.status === "error" ? "alert" : "status"}
            >
              {map.status === "loading" ? (
                <>
                  <span className={styles.spinner} />
                  <strong>Открываем Астану</strong>
                  <p>Загружаем улицы и объёмные здания…</p>
                </>
              ) : (
                <>
                  <Icon name="info" size={28} />
                  <strong>Карта пока недоступна</strong>
                  <p>{map.error}</p>
                  <button onClick={map.retry}>
                    Повторить загрузку <Icon name="arrow" size={16} />
                  </button>
                </>
              )}
            </div>
          )}
          {sim.data && (
            <>
              <div className={styles.cityScore}>
                <span>
                  {sim.result
                    ? "РЕЗУЛЬТАТ ВАШЕЙ СТРАТЕГИИ"
                    : "ИСХОДНОЕ СОСТОЯНИЕ ГОРОДА"}
                </span>
                <strong>
                  {number(sim.result?.after.score ?? sim.data.baseline.score)}
                  <small> / 100</small>
                </strong>
                <p>
                  {sim.result
                    ? `${delta(sim.result.score_delta)} к качеству жизни`
                    : "Astana Quality of Life Score"}
                </p>
              </div>
              <div className={styles.districtDock}>
                {sim.data.catalog.districts.map((district) => {
                  const after = (
                    sim.result?.after ?? sim.data?.baseline
                  )?.districts.find((item) => item.district_id === district.id);
                  const change = sim.result?.district_changes.find(
                    (item) => item.district_id === district.id,
                  );
                  return (
                    <article key={district.id}>
                      <span>{district.name}</span>
                      <strong>{number(after?.score ?? "0")}</strong>
                      <small>
                        {change ? delta(change.delta) : "Исходный балл"}
                      </small>
                      <progress max={100} value={Number(after?.score ?? 0)} />
                    </article>
                  );
                })}
                <div className={styles.syntheticNote}>
                  УСЛОВНЫЕ РАЙОНЫ · ДАННЫЕ КЕЙСА
                </div>
              </div>
            </>
          )}
          <div className={styles.cameraInfo}>
            <span className={styles.liveDot} />
            <span>{map.is3d ? "ОБЪЁМНЫЙ ВИД" : "ПЛАН ГОРОДА"}</span>
            <span className={styles.cameraDetails}>
              Наклон {Math.round(map.camera.pitch)}° <i /> Масштаб{" "}
              {map.camera.zoom.toFixed(1)}
            </span>
          </div>
          {showHelp && (
            <section
              className={styles.helpPanel}
              aria-label="Как управлять картой"
            >
              <button
                className={styles.closeHelp}
                onClick={() => setShowHelp(false)}
                aria-label="Закрыть подсказки"
              >
                <Icon name="close" />
              </button>
              <h2>Город в ваших руках</h2>
              <p>
                <strong>Перемещение</strong> — перетащите карту.
              </p>
              <p>
                <strong>Масштаб</strong> — колесо мыши или кнопки + / −.
              </p>
              <p>
                <strong>Поворот и наклон</strong> — перетащите с правой кнопкой
                мыши. На сенсорном экране используйте два пальца.
              </p>
              <p>
                <strong>Клавиатура</strong> — сфокусируйте карту, используйте
                стрелки; Shift + стрелки меняют ракурс.
              </p>
              <small>
                Объём построен по данным зданий. Фасады и высоты могут
                отличаться от реальных.
              </small>
            </section>
          )}
        </section>
      </main>
    </div>
  );
}
