from typing import Protocol

import pyttsx3


class SpeechEngine(Protocol):
    def say(self, text: str) -> None:
        ...

    def runAndWait(self) -> None:
        ...

    def stop(self) -> None:
        ...


class Narrator:
    """Speaks supplied text without deciding what should be read next."""

    def __init__(self, engine: SpeechEngine) -> None:
        self._engine = engine

    @classmethod
    def system_default(cls) -> "Narrator":
        return cls(pyttsx3.init())

    def speak(self, text: str) -> None:
        if not text.strip():
            return
        self._engine.say(text)
        self._engine.runAndWait()

    def stop(self) -> None:
        self._engine.stop()
