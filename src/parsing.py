from commentjson import loads
from pathlib import Path
from pydantic import BaseModel, PositiveInt, Field, ValidationError
from typing import Any


class Config(BaseModel):
    highscore_filename: str = Field(
        pattern=r"\.json$", default="highscore.json"
    )
    lives: PositiveInt = Field(default=3)
    width: PositiveInt = Field(default=10)
    height: PositiveInt = Field(default=20)
    pacgum: PositiveInt = Field(default=42)
    points_per_pacgum: PositiveInt = Field(default=10)
    points_per_super_pacgum: PositiveInt = Field(default=50)
    points_per_ghost: PositiveInt = Field(default=200)
    seed: Any = Field(default=None)
    level_max_time: PositiveInt = Field(default=90)


def format_config_error(e: ValidationError) -> str:
    lines: list[str] = []
    for err in e.errors():
        key = ".".join(str(part) for part in err["loc"])
        lines.append(f"Invalid config key '{key}', using default")
    return "\n".join(lines)


class Parsing:
    def __init__(self, filepath: Path):
        self.filepath: Path = filepath

    def load_data(self) -> dict[str, Any]:
        try:
            text = self.filepath.read_text(encoding="utf-8")
            data: dict[str, Any] = loads(text)
        except FileNotFoundError:
            raise
        except Exception as e:
            print(f"config: invalid file ({e}), using defaults")
            return {}

        return data

    def build_config(self, data: dict[str, Any]) -> Config:
        try:
            config = Config(**data)
        except ValidationError as e:
            print(format_config_error(e))
            for err in e.errors():
                data.pop(str(err["loc"][0]), None)
            config = Config(**data)

        for name, field in Config.model_fields.items():
            if name not in data:
                print(
                    f"config: missing '{name}', using default: {field.default}"
                )

        return config

    def parse(self) -> Config:
        data = self.load_data()
        return self.build_config(data)
