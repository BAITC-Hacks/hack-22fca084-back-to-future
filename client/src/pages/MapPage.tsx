import { useState } from "react";
import { LANDMARKS } from "../features/map/mapConfig";
import { useCityMap } from "../features/map/useCityMap";
import { Icon } from "../shared/ui/Icon";
import styles from "./MapPage.module.css";

export default function MapPage() {
  const map = useCityMap();
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
            <small>ГОРОД С ВЫСОТЫ</small>
          </span>
        </a>
        <div className={styles.breadcrumb}>
          Казахстан <span>/</span> Астана <span>/</span>{" "}
          <strong>Обзор города</strong>
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
        <aside className={styles.sidebar} aria-label="Обзор Астаны">
          <div className={styles.intro}>
            <span className={styles.eyebrow}>
              <span /> ИССЛЕДУЙТЕ ГОРОД
            </span>
            <h1>
              Астана.
              <br />
              <span>Новый ракурс.</span>
            </h1>
            <p>
              Знакомые места, настоящие улицы
              <br />и город в трёх измерениях.
            </p>
          </div>
          <div className={styles.sectionTitle}>
            <h2>Городские ориентиры</h2>
            <span>04</span>
          </div>
          <nav className={styles.landmarks} aria-label="Городские ориентиры">
            {LANDMARKS.map((landmark, index) => (
              <button
                key={landmark.id}
                disabled={!ready}
                onClick={() => map.flyTo(landmark)}
                aria-pressed={map.selected?.id === landmark.id}
                className={`${styles.landmark} ${map.selected?.id === landmark.id ? styles.selected : ""}`}
              >
                <span className={styles.landmarkIcon}>
                  <Icon name={landmark.icon} size={26} />
                </span>
                <span className={styles.landmarkText}>
                  <small>
                    0{index + 1} / {landmark.category}
                  </small>
                  <strong>{landmark.name}</strong>
                </span>
                <Icon name="chevron" size={16} />
              </button>
            ))}
          </nav>
          <section className={styles.settings} aria-label="Отображение карты">
            <div className={styles.sectionTitle}>
              <h2>Отображение</h2>
              <Icon name="layers" size={17} />
            </div>
            <button
              className={styles.setting}
              disabled={!ready}
              onClick={map.toggleDimension}
              role="switch"
              aria-checked={map.is3d}
            >
              <span>
                Объёмные здания <small>Вид с высоты</small>
              </span>
              <span
                className={`${styles.switch} ${map.is3d ? styles.on : ""}`}
              />
            </button>
            <button
              className={styles.setting}
              disabled={!ready}
              onClick={map.toggleLabels}
              role="switch"
              aria-checked={map.labelsVisible}
            >
              <span>
                Подписи на карте <small>Улицы и места</small>
              </span>
              <span
                className={`${styles.switch} ${map.labelsVisible ? styles.on : ""}`}
              />
            </button>
          </section>
          <div className={styles.sourceNote}>
            <span className={styles.sourceIcon}>
              <Icon name="map" size={18} />
            </span>
            <div>
              <strong>Реальная география</strong>
              <p>
                OpenStreetMap · OpenFreeMap
                <br />
                Детализация зависит от данных карты.
              </p>
            </div>
          </div>
          <div className={styles.sidebarFooter}>
            <span>ASTANA CITY EXPLORER</span>
            <span>01 — КАРТА</span>
          </div>
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
            <div className={styles.mapTag}>51°07′ N &nbsp; 71°26′ E</div>
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
          {map.selected && ready && (
            <article className={styles.placeCard}>
              <div className={styles.placeSymbol}>
                <Icon name={map.selected.icon} size={32} />
              </div>
              <div>
                <span className={styles.eyebrow}>В ФОКУСЕ</span>
                <h2>{map.selected.name}</h2>
                <p>{map.selected.description}</p>
              </div>
              <span className={styles.placeIndex}>
                {String(
                  LANDMARKS.findIndex(
                    (place) => place.id === map.selected?.id,
                  ) + 1,
                ).padStart(2, "0")}
              </span>
            </article>
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
