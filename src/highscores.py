"""Highscore persistence: JSON list of {name, score}."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ScoreEntry = dict[str, Any]


class Highscores:
    def __init__(self, filepath: Path):
        self.filepath: Path = filepath
        self.entries: list[ScoreEntry] = []
        self.error: bool = False
        self.reload()

    def reload(self) -> None:
        self.error = False
        if not self.filepath.is_file():
            self.entries = []
            return
        try:
            raw: Any = json.loads(self.filepath.read_text(encoding="utf-8"))
            if not isinstance(raw, list):
                self.entries = []
                self.error = True
                return
            cleaned: list[ScoreEntry] = []
            for item in raw:
                if not isinstance(item, dict):
                    continue
                name = item.get("name")
                score = item.get("score")
                if not isinstance(name, str) or not isinstance(score, int):
                    continue
                if score < 0:
                    continue
                cleaned.append({"name": name[:10], "score": score})
            cleaned.sort(key=lambda e: e["score"], reverse=True)
            self.entries = cleaned
        except (OSError, json.JSONDecodeError, TypeError):
            self.entries = []
            self.error = True

    def save(self) -> None:
        try:
            _ = self.filepath.write_text(
                json.dumps(self.entries, indent=2) + "\n",
                encoding="utf-8",
            )
            self.error = False
        except OSError:
            self.error = True

    def add(self, name: str, score: int) -> None:
        self.entries.append({"name": name[:10], "score": max(0, int(score))})
        self.entries.sort(key=lambda e: e["score"], reverse=True)
        self.save()

    @property
    def empty(self) -> bool:
        return self.error or len(self.entries) == 0
