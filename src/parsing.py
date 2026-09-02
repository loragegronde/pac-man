from commentjson import loads
from pathlib import Path
from pydantic import BaseModel, PositiveInt, Field
from typing import Any

class Config(BaseModel):
    highscore_filename: str = Field(pattern=r"\.json$")
    levels: list[str]
    lives: PositiveInt
    width: PositiveInt
    height: PositiveInt
    pacgum: PositiveInt
    points_per_pacgum: PositiveInt
    points_per_super_pacgum: PositiveInt
    points_per_ghost: PositiveInt
    seed: Any
    level_max_time: PositiveInt

class Parsing:
    def __init__(self, filepath: Path):
        self.filepath: Path = filepath

    def parse(self) -> Config:
        text = self.filepath.read_text()
        data = loads(text)
        return Config(**data)
