import assert from "node:assert/strict";
import { URL } from "node:url";
import { readdir, readFile } from "node:fs/promises";
import { test } from "node:test";

// GOTCHA: без worker&url Vite собирает интерфейс, но MapLibre 6 не загружает здания.
// Регрессия воспроизведена в production-контейнере 2026-09-23.
test("production contains a bundled MapLibre worker", async () => {
  const files = await readdir(new URL("../dist/assets/", import.meta.url));
  const worker = files.find((name) => /^maplibre-gl-worker-.*\.js$/.test(name));
  assert.ok(worker, "MapLibre worker asset is missing from production build");
  const source = await readFile(
    new URL(`../dist/assets/${worker}`, import.meta.url),
    "utf8",
  );
  assert.ok(source.length > 10000, "Worker bundle is unexpectedly empty");
  assert.equal(
    source.includes('from"./maplibre-gl-shared.mjs"'),
    false,
    "Worker references an unbundled sibling",
  );
});
