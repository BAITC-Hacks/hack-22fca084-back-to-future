import { StrictMode, Suspense, lazy } from "react";
import { createRoot } from "react-dom/client";
import { ErrorBoundary } from "./shared/ui/ErrorBoundary";
import "maplibre-gl/dist/maplibre-gl.css";
import "./styles/global.css";
const MapPage = lazy(() => import("./pages/MapPage"));
const root = document.getElementById("root");
if (!root) throw new Error("Root element missing");
createRoot(root).render(
  <StrictMode>
    <ErrorBoundary>
      <Suspense
        fallback={<main className="boot-loading">Открываем Астану…</main>}
      >
        <MapPage />
      </Suspense>
    </ErrorBoundary>
  </StrictMode>,
);
