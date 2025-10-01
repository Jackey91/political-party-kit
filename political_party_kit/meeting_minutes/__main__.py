"""Command line interface for the meeting minutes module."""

from __future__ import annotations

import argparse
from .whisper_minutes import (
    MeetingMetadata,
    MeetingMinutesGenerator,
    parse_semicolon_list,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audio → Whisper → Protokoll (GPT) → DOCX",
    )
    parser.add_argument("--audio", required=True, help="Pfad zur Audiodatei (mp3, m4a, wav, mp4, webm)")
    parser.add_argument("--titel", default="Sitzungsprotokoll", help="Titel des Protokolls")
    parser.add_argument("--datum", default="", help="Datum der Sitzung (z. B. 2025-10-01)")
    parser.add_argument(
        "--teilnehmer",
        default="",
        help="Teilnehmerliste, durch Semikolon getrennt (z. B. 'Müller;Yılmaz;Schneider')",
    )
    parser.add_argument("--gaeste", default="", help="Gästeliste, durch Semikolon getrennt")
    parser.add_argument("--agenda", default="", help="Tagesordnungspunkte, durch Semikolon getrennt")
    parser.add_argument("--ziele", default="", help="Sitzungsziele, durch Semikolon getrennt")
    parser.add_argument("--hinweise", default="", help="Besondere Hinweise, durch Semikolon getrennt")
    parser.add_argument("--ort", default="", help="Ort der Sitzung")
    parser.add_argument("--moderation", default="", help="Leitung/Moderation der Sitzung")
    parser.add_argument("--protokoll", default="", help="Protokollführende Person")
    parser.add_argument("--startzeit", default="", help="Geplanter Beginn der Sitzung (z. B. 09:00)")
    parser.add_argument("--endzeit", default="", help="Geplantes Ende der Sitzung (z. B. 11:30)")
    parser.add_argument("--language", default="de", help="Sprachhinweis an Whisper (z. B. 'de')")
    parser.add_argument("--out", default="Protokoll.docx", help="Ausgabedatei (.docx)")
    parser.add_argument("--save_transcript", default="", help="Optional: Pfad zum Speichern des Roh-Transkripts (.txt)")
    parser.add_argument("--save_partials", default="", help="Optional: Ordner zum Speichern der Chunk-Zusammenfassungen")
    parser.add_argument(
        "--no_prompt",
        action="store_true",
        help="Eingabemaske überspringen und nur Argumente verwenden",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    metadata = MeetingMetadata(
        titel=args.titel.strip(),
        datum=args.datum.strip() or None,
        ort=args.ort.strip() or None,
        teilnehmer=parse_semicolon_list(args.teilnehmer),
        gaeste=parse_semicolon_list(args.gaeste),
        agenda=parse_semicolon_list(args.agenda),
        ziele=parse_semicolon_list(args.ziele),
        hinweise=parse_semicolon_list(args.hinweise),
        moderation=args.moderation.strip() or None,
        protokoll=args.protokoll.strip() or None,
        startzeit=args.startzeit.strip() or None,
        endzeit=args.endzeit.strip() or None,
    )

    generator = MeetingMinutesGenerator()
    generator.generate(
        audio_path=args.audio,
        output_path=args.out,
        metadata=metadata,
        language_hint=args.language,
        save_transcript=args.save_transcript or None,
        save_partials=args.save_partials or None,
        prompt_for_metadata=not args.no_prompt,
    )

    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
