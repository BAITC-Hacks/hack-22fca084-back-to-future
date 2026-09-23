export type IconName =
  | "map"
  | "arrow"
  | "layers"
  | "plus"
  | "minus"
  | "compass"
  | "home"
  | "info"
  | "close"
  | "tower"
  | "tent"
  | "sphere"
  | "palace"
  | "chevron";
const paths: Record<IconName, string> = {
  map: "m3 6 6-3 6 3 6-3v15l-6 3-6-3-6 3V6Zm6-3v15m6-12v15",
  arrow: "M5 12h14m-6-6 6 6-6 6",
  layers: "m3 8 9-5 9 5-9 5-9-5Zm0 5 9 5 9-5M3 18l9 5 9-5",
  plus: "M12 5v14M5 12h14",
  minus: "M5 12h14",
  compass: "m16 8-3 5-5 3 3-5 5-3ZM12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20",
  home: "m3 10 9-7 9 7v11H3V10Zm6 11v-8h6v8",
  info: "M12 11v6m0-10v.1M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20",
  close: "m6 6 12 12M6 18 18 6",
  tower: "M8 21h8M10 21l1-10m2 0 1 10M12 3a4 4 0 1 0 0 8 4 4 0 0 0 0-8",
  tent: "M3 20 13 3l8 17H3Zm10-17-3 17m3-17 3 17",
  sphere:
    "M3 21h18M12 3a8 8 0 1 0 0 16 8 8 0 0 0 0-16Zm0 0c-5 5-5 11 0 16 5-5 5-11 0-16ZM4 10h16",
  palace: "M3 21h18M4 21V11h16v10M8 11V8h8v3M12 3v5m0-5h4M8 15v3m4-3v3m4-3v3",
  chevron: "m9 5 7 7-7 7",
};
export function Icon({ name, size = 20 }: { name: IconName; size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d={paths[name]} />
    </svg>
  );
}
