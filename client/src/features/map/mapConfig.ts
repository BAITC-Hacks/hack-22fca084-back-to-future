import type { FlyToOptions } from "maplibre-gl";

export interface Landmark {
  id: string;
  name: string;
  category: string;
  description: string;
  coordinates: [number, number];
  bearing: number;
  zoom: number;
  icon: "tower" | "tent" | "sphere" | "palace";
}

export const LANDMARKS: Landmark[] = [
  {
    id: "bayterek",
    name: "Байтерек",
    category: "Символ столицы",
    description:
      "Начните с бульвара Нуржол. Поверните камеру, чтобы рассмотреть архитектуру левого берега.",
    coordinates: [71.4305, 51.1282],
    bearing: -28,
    zoom: 15.8,
    icon: "tower",
  },
  {
    id: "khan-shatyr",
    name: "Хан Шатыр",
    category: "Архитектура",
    description:
      "Западная часть бульвара Нуржол: Хан Шатыр, площадь и окружающие кварталы.",
    coordinates: [71.4036, 51.1325],
    bearing: 32,
    zoom: 15.7,
    icon: "tent",
  },
  {
    id: "expo",
    name: "EXPO",
    category: "Новый город",
    description:
      "Территория выставки EXPO и музей Нур Алем. Исследуйте застройку южной части города.",
    coordinates: [71.4153, 51.0892],
    bearing: -20,
    zoom: 15.6,
    icon: "sphere",
  },
  {
    id: "akorda",
    name: "Ак Орда",
    category: "У реки",
    description:
      "Резиденция на берегу Ишима. Отсюда открывается вид на реку, мосты и правый берег.",
    coordinates: [71.446, 51.1257],
    bearing: -42,
    zoom: 15.6,
    icon: "palace",
  },
];

export const MAP_STYLE_URL = "https://tiles.openfreemap.org/styles/positron";
export const INITIAL_CAMERA: FlyToOptions = {
  center: [71.4305, 51.1282],
  zoom: 15.6,
  pitch: 58,
  bearing: -28,
};
export const CITY_BOUNDS: [[number, number], [number, number]] = [
  [71.15, 50.94],
  [71.7, 51.32],
];
export const BUILDING_LAYER = "astana-buildings-3d";
