"""Dashboard rendering helpers for the political party kit."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


@dataclass(slots=True)
class ModuleEntry:
    """Beschreibung eines Moduls für die Dashboard-Seite."""

    name: str
    description: str
    command: str
    documentation: str | None = None


def default_modules() -> list[ModuleEntry]:
    """Return the built-in modules that can be launched from the dashboard."""

    return [
        ModuleEntry(
            name="Sitzungsprotokolle",
            description=(
                "Erstellt aus Audioaufnahmen automatisch strukturierte Sitzungsprotokolle "
                "mithilfe von Whisper und GPT."
            ),
            command="python -m political_party_kit.meeting_minutes",
            documentation="README.md#meeting-minutes-module",
        ),
    ]


def render_dashboard(modules: Sequence[ModuleEntry] | None = None) -> str:
    """Render the dashboard HTML for the given modules."""

    modules = list(modules or default_modules())
    module_cards = "\n".join(
        _render_card(
            title=module.name,
            description=module.description,
            command=module.command,
            documentation=module.documentation,
        )
        for module in modules
    )
    return f"""
<!DOCTYPE html>
<html lang=\"de\">
  <head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <title>Political Party Kit – Dashboard</title>
    <style>
      :root {{
        color-scheme: light dark;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif;
        background: #f6f7fb;
        color: #1c1c1c;
      }}
      body {{
        margin: 0;
        padding: 2rem 1.5rem 4rem;
        background: linear-gradient(135deg, #f6f7fb 0%, #e5e9ff 100%);
      }}
      h1 {{
        text-align: center;
        margin-bottom: 0.5rem;
      }}
      p.lead {{
        text-align: center;
        margin-top: 0;
        margin-bottom: 2rem;
        color: #444;
        max-width: 48rem;
        margin-left: auto;
        margin-right: auto;
      }}
      main {{
        display: grid;
        gap: 1.5rem;
        max-width: 72rem;
        margin: 0 auto;
        grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr));
      }}
      article {{
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 20px 45px rgba(41, 51, 76, 0.15);
        display: flex;
        flex-direction: column;
        gap: 1rem;
      }}
      article h2 {{
        margin: 0;
        font-size: 1.4rem;
      }}
      article p {{
        margin: 0;
        flex-grow: 1;
        line-height: 1.5;
      }}
      .actions {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
      }}
      .actions a, .actions code {{
        font-size: 0.95rem;
      }}
      a.button {{
        background: #1c4ed8;
        color: white;
        text-decoration: none;
        padding: 0.6rem 1rem;
        border-radius: 999px;
        font-weight: 600;
        transition: background 0.15s ease-in-out, transform 0.15s ease-in-out;
      }}
      a.button:hover {{
        background: #173da8;
        transform: translateY(-1px);
      }}
      code {{
        background: rgba(28, 78, 216, 0.08);
        color: #0f1f4b;
        padding: 0.4rem 0.6rem;
        border-radius: 0.5rem;
        display: inline-flex;
        align-items: center;
      }}
      footer {{
        text-align: center;
        margin-top: 3rem;
        color: #555;
        font-size: 0.9rem;
      }}
      @media (prefers-color-scheme: dark) {{
        :root {{
          background: #111827;
          color: #f9fafb;
        }}
        body {{
          background: radial-gradient(circle at top, #1f2937 0%, #0f172a 70%);
        }}
        article {{
          background: rgba(17, 24, 39, 0.95);
          box-shadow: 0 20px 45px rgba(7, 11, 19, 0.35);
        }}
        article p {{
          color: #e5e7eb;
        }}
        a.button {{
          background: #2563eb;
        }}
        a.button:hover {{
          background: #1d4ed8;
        }}
        code {{
          background: rgba(37, 99, 235, 0.25);
          color: #bfdbfe;
        }}
        footer {{
          color: #9ca3af;
        }}
      }}
    </style>
  </head>
  <body>
    <h1>Political Party Kit</h1>
    <p class=\"lead\">
      Zentrale Anlaufstelle für alle Module des Toolkits. Wähle ein Modul aus, um direkt
      in den jeweiligen Workflow zu starten.
    </p>
    <main>
      {module_cards}
    </main>
    <footer>
      Weitere Module lassen sich problemlos ergänzen, indem sie in der Konfiguration des Dashboards registriert werden.
    </footer>
  </body>
</html>
"""


def _render_card(*, title: str, description: str, command: str, documentation: str | None) -> str:
    doc_link = (
        f'<a class="button" href="{documentation}">Dokumentation</a>' if documentation else ""
    )
    command_html = f"<code>{command}</code>"
    actions = " ".join(filter(None, [doc_link, command_html]))
    return f"""
      <article>
        <h2>{title}</h2>
        <p>{description}</p>
        <div class=\"actions\">{actions}</div>
      </article>
    """


def write_dashboard(output: str | Path, modules: Iterable[ModuleEntry] | None = None) -> Path:
    """Write the dashboard HTML file and return the resulting path."""

    target = Path(output).expanduser().resolve()
    target.write_text(render_dashboard(list(modules) if modules else None), encoding="utf-8")
    return target
