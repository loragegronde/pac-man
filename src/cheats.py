from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Cheats:
    invincibility: bool = False
    one_pacgum: bool = False
    always_chase: bool = False
    ghost_freeze: bool = False
    speed_mult: float = 1.0

    CONFLICTS: ClassVar[dict[str, tuple[str, ...]]] = {
        "always_chase": ("ghost_freeze",),
        "ghost_freeze": ("always_chase",),
    }

    def is_blocked(self, field: str) -> bool:
        for other, blocked in self.CONFLICTS.items():
            if field in blocked and bool(getattr(self, other)):
                return True
        return False

    def reset(self) -> None:
        self.invincibility = False
        self.one_pacgum = False
        self.always_chase = False
        self.ghost_freeze = False
        self.speed_mult = 1.0
