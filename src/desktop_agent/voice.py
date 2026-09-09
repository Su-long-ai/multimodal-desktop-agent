from __future__ import annotations

from typing import Protocol


class SpeechToText(Protocol):
    def transcribe(self, pcm: bytes, sample_rate: int) -> str: ...


class TextToSpeech(Protocol):
    def synthesize(self, text: str) -> bytes: ...


class NullSpeechToText:
    def transcribe(self, pcm: bytes, sample_rate: int) -> str:
        return ""


class NullTextToSpeech:
    def synthesize(self, text: str) -> bytes:
        return b""
