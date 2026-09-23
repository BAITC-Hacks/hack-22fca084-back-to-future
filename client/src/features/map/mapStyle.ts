import type { Map } from "maplibre-gl";
import { BUILDING_LAYER } from "./mapConfig";

export function applyCityStyle(map: Map) {
  map.setPaintProperty("background", "background-color", "#edf0eb");
  map.setPaintProperty("water", "fill-color", "#a5d6e1");
  map.setPaintProperty("waterway", "line-color", "#a5d6e1");
  map.setPaintProperty("park", "fill-color", "#ccddc3");
  map.setPaintProperty("landcover_wood", "fill-color", "#bdd3b3");
  map.setPaintProperty("building", "fill-color", "#d6dcd6");
  map.setLight({
    anchor: "viewport",
    color: "#fff8e9",
    intensity: 0.45,
    position: [1.5, 210, 45],
  });

  const layers = map.getStyle().layers;
  for (const layer of layers) {
    if (layer.type === "symbol" && layer.layout?.["text-field"]) {
      map.setLayoutProperty(layer.id, "text-field", [
        "coalesce",
        ["get", "name:ru"],
        ["get", "name"],
      ]);
    }
  }
  const firstLabel = layers.find((layer) => layer.type === "symbol")?.id;
  // GOTCHA: render_height/render_min_height — поля OpenFreeMap, проверены по TileJSON 2026-09-23.
  map.addLayer(
    {
      id: BUILDING_LAYER,
      source: "openmaptiles",
      "source-layer": "building",
      type: "fill-extrusion",
      minzoom: 13,
      filter: ["!=", ["get", "hide_3d"], true],
      paint: {
        "fill-extrusion-color": [
          "interpolate",
          ["linear"],
          ["coalesce", ["get", "render_height"], 0],
          0,
          "#f5f3e9",
          40,
          "#e5e9e3",
          120,
          "#b9cdcc",
        ],
        "fill-extrusion-height": ["coalesce", ["get", "render_height"], 0],
        "fill-extrusion-base": ["coalesce", ["get", "render_min_height"], 0],
        "fill-extrusion-opacity": 1,
        "fill-extrusion-vertical-gradient": true,
      },
    },
    firstLabel,
  );
}
