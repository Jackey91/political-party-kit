"""CLI to generate the HTML dashboard page."""

from __future__ import annotations

import argparse
import webbrowser
from pathlib import Path

from . import ModuleEntry, default_modules, render_dashboard, write_dashboard


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Erstellt die Dashboard-Übersicht als HTML-Datei")
    parser.add_argument(
        "--output",
        "-o",
        default="dashboard.html",
        help="Zieldatei für das Dashboard (Standard: dashboard.html im aktuellen Ordner)",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Nach dem Erstellen automatisch im Standardbrowser öffnen",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    target = write_dashboard(args.output, default_modules())
    print(f"Dashboard gespeichert unter: {target}")

    if args.open:
        webbrowser.open(target.as_uri())

    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
