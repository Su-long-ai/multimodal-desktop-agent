from __future__ import annotations

from typing import Protocol


class AvatarAdapter(Protocol):
    def set_expression(self, expression: str) -> None: ...
    def speak_started(self) -> None: ...
    def speak_finished(self) -> None: ...


class NullAvatar:
    def set_expression(self, expression: str) -> None:
        pass

    def speak_started(self) -> None:
        pass

    def speak_finished(self) -> None:
        pass
