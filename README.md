# political-party-kit

Political Party Kit is a modular toolkit for political organizations. It supports internal organization, member management, campaigns, events, communication, and data analysis. Neutral, reusable, and extensible – currently a work in progress.

## Dashboard

Erstelle eine übersichtliche HTML-Dashboard-Seite, über die einzelne Module des Toolkits gestartet
oder dokumentiert werden können:

```bash
python -m political_party_kit.dashboard --open
```

Der Befehl erzeugt eine Datei `dashboard.html` (standardmäßig im aktuellen Ordner) und öffnet sie
bei Bedarf direkt im Browser. Die Seite listet alle verfügbaren Module auf und zeigt jeweils den
zugehörigen Startbefehl sowie einen Link zur Dokumentation an.

## Meeting minutes module

The `political_party_kit.meeting_minutes` package bundles a Whisper + GPT powered workflow for producing structured meeting minutes from audio recordings.  It offers a Python API as well as a CLI entry point.

### Installation

Install the dependencies into your virtual environment:

```bash
pip install openai python-docx python-dotenv tiktoken
```

Make sure that your `OPENAI_API_KEY` is available via environment variable or a local `.env` file.

### Command line usage

Run the generator directly via the module:

```bash
python -m political_party_kit.meeting_minutes --audio sitzung.mp3 --titel "Fraktionssitzung" --datum 2025-09-23 --teilnehmer "Müller;Yılmaz;Schneider" --agenda "TOP 1: Haushaltsplanung;TOP 2: Bürgeranfragen" --out Protokoll.docx
```

You can omit `--no_prompt` to receive an interactive wizard that allows you to adjust the meeting metadata before the document is created.

### Python usage

```python
from political_party_kit.meeting_minutes import MeetingMetadata, MeetingMinutesGenerator

metadata = MeetingMetadata(
    titel="Fraktionssitzung 23-09-2025",
    datum="2025-09-23",
    teilnehmer=["Müller", "Yılmaz", "Schneider"],
    agenda=["TOP 1: Haushaltsplanung", "TOP 2: Bürgeranfragen"],
)

generator = MeetingMinutesGenerator()
generator.generate(
    audio_path="sitzung.mp3",
    output_path="Protokoll_2025-09-23.docx",
    metadata=metadata,
    prompt_for_metadata=True,  # optional interactive refinement
)
```
