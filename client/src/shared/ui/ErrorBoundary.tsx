import { Component, type ReactNode } from "react";
export class ErrorBoundary extends Component<
  { children: ReactNode },
  { failed: boolean }
> {
  state = { failed: false };
  static getDerivedStateFromError() {
    return { failed: true };
  }
  componentDidCatch(error: Error) {
    console.error("Map screen failed", error);
  }
  render() {
    if (this.state.failed)
      return (
        <main className="fatal-error">
          <h1>Не удалось открыть карту</h1>
          <p>Попробуйте перезагрузить страницу.</p>
          <button onClick={() => window.location.reload()}>
            Перезагрузить
          </button>
        </main>
      );
    return this.props.children;
  }
}
