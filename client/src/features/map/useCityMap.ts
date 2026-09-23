import { useEffect, useRef, useState } from "react";
import {
  Map,
  Marker,
  ScaleControl,
  setWorkerUrl,
  type MapOptions,
} from "maplibre-gl";
import workerUrl from "maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url";
import { applyCityStyle } from "./mapStyle";
import {
  BUILDING_LAYER,
  CITY_BOUNDS,
  INITIAL_CAMERA,
  LANDMARKS,
  MAP_STYLE_URL,
  type Landmark,
} from "./mapConfig";

// GOTCHA: Vite должен собрать worker вместе с зависимостями; ?url оставляет внешние импорты.
// Проверено по руководству MapLibre 6 и production-сборке 2026-09-23.
setWorkerUrl(workerUrl);

export function useCityMap() {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<Map | null>(null);
  const [attempt, setAttempt] = useState(0);
  const [status, setStatus] = useState<"loading" | "ready" | "error">(
    "loading",
  );
  const [error, setError] = useState("");
  const [is3d, setIs3d] = useState(true);
  const [labelsVisible, setLabelsVisible] = useState(true);
  const [selected, setSelected] = useState<Landmark | null>(
    LANDMARKS[0] ?? null,
  );
  const [camera, setCamera] = useState({ zoom: 15.6, pitch: 58, bearing: -28 });

  useEffect(() => {
    if (!containerRef.current) return;
    let disposed = false;
    let resourceFailed = false;
    let map: Map;
    const reducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;
    const goTo = (landmark: Landmark) => {
      setSelected(landmark);
      map.flyTo({
        center: landmark.coordinates,
        zoom: landmark.zoom,
        bearing: landmark.bearing,
        duration: reducedMotion ? 0 : 1800,
      });
    };
    const options: MapOptions = {
      container: containerRef.current,
      style: MAP_STYLE_URL,
      ...INITIAL_CAMERA,
      minZoom: 11,
      maxZoom: 19,
      maxPitch: 70,
      maxBounds: CITY_BOUNDS,
      canvasContextAttributes: { antialias: true },
      attributionControl: { compact: true },
    };
    try {
      map = new Map(options);
    } catch (cause) {
      console.error("Map initialization failed", cause);
      setStatus("error");
      setError(
        "Не удалось включить 3D-карту. Проверьте поддержку WebGL и аппаратное ускорение браузера.",
      );
      return;
    }
    mapRef.current = map;
    const timeout = window.setTimeout(() => {
      if (disposed) return;
      setStatus("error");
      setError(
        "Карта загружается дольше обычного. Проверьте интернет и повторите загрузку.",
      );
    }, 25000);
    map.addControl(new ScaleControl({ unit: "metric" }), "bottom-left");
    const markers: Marker[] = [];
    map.on("load", () => {
      if (disposed) return;
      applyCityStyle(map);
      for (const landmark of LANDMARKS) {
        const button = document.createElement("button");
        button.className = "city-marker";
        button.type = "button";
        button.textContent = landmark.name;
        button.setAttribute(
          "aria-label",
          `Перейти к ориентиру ${landmark.name}`,
        );
        button.addEventListener("click", () => goTo(landmark));
        markers.push(
          new Marker({ element: button, anchor: "bottom" })
            .setLngLat(landmark.coordinates)
            .addTo(map),
        );
      }
    });
    map.on("idle", () => {
      if (disposed || resourceFailed || !map.getLayer(BUILDING_LAYER)) return;
      window.clearTimeout(timeout);
      setStatus("ready");
      setError("");
    });
    map.on("error", (event) => {
      if (disposed) return;
      resourceFailed = true;
      console.error("Map resource failed", event.error);
      window.clearTimeout(timeout);
      setStatus("error");
      setError(
        "Не удалось загрузить часть карты. Проверьте подключение к интернету и попробуйте снова.",
      );
    });
    map.on("moveend", () => {
      if (!disposed)
        setCamera({
          zoom: map.getZoom(),
          pitch: map.getPitch(),
          bearing: map.getBearing(),
        });
    });
    map.on("dragstart", () => setSelected(null));
    const resize = new ResizeObserver(() => map.resize());
    resize.observe(containerRef.current);
    return () => {
      disposed = true;
      window.clearTimeout(timeout);
      resize.disconnect();
      for (const marker of markers) marker.remove();
      map.remove();
      mapRef.current = null;
    };
  }, [attempt]);

  function flyTo(landmark: Landmark) {
    setSelected(landmark);
    mapRef.current?.flyTo({
      center: landmark.coordinates,
      zoom: landmark.zoom,
      bearing: landmark.bearing,
      pitch: is3d ? 58 : 0,
      duration: 1800,
    });
  }
  function toggleDimension() {
    const next = !is3d;
    setIs3d(next);
    mapRef.current?.setLayoutProperty(
      BUILDING_LAYER,
      "visibility",
      next ? "visible" : "none",
    );
    mapRef.current?.easeTo({ pitch: next ? 58 : 0, duration: 700 });
  }
  function toggleLabels() {
    const next = !labelsVisible;
    setLabelsVisible(next);
    const map = mapRef.current;
    for (const layer of map?.getStyle().layers ?? []) {
      if (layer.type === "symbol")
        map?.setLayoutProperty(
          layer.id,
          "visibility",
          next ? "visible" : "none",
        );
    }
  }
  function resetCamera() {
    setSelected(LANDMARKS[0] ?? null);
    mapRef.current?.flyTo({
      ...INITIAL_CAMERA,
      pitch: is3d ? 58 : 0,
      duration: 1600,
    });
  }
  function retry() {
    setStatus("loading");
    setError("");
    setIs3d(true);
    setLabelsVisible(true);
    setSelected(LANDMARKS[0] ?? null);
    setAttempt((value) => value + 1);
  }
  return {
    containerRef,
    status,
    error,
    is3d,
    labelsVisible,
    selected,
    camera,
    flyTo,
    toggleDimension,
    toggleLabels,
    resetCamera,
    retry,
    zoomIn: () => mapRef.current?.zoomIn(),
    zoomOut: () => mapRef.current?.zoomOut(),
    north: () => mapRef.current?.easeTo({ bearing: 0, duration: 700 }),
  };
}
