from voice_first_learning.narrator import Narrator


class FakeSpeechEngine:
    def __init__(self) -> None:
        self.spoken: list[str] = []
        self.run_count = 0
        self.stop_count = 0

    def say(self, text: str) -> None:
        self.spoken.append(text)

    def runAndWait(self) -> None:
        self.run_count += 1

    def stop(self) -> None:
        self.stop_count += 1


def test_speak_queues_text_and_runs_engine() -> None:
    engine = FakeSpeechEngine()
    narrator = Narrator(engine)

    narrator.speak("Hello, this is the study companion.")

    assert engine.spoken == ["Hello, this is the study companion."]
    assert engine.run_count == 1


def test_speak_ignores_blank_text() -> None:
    engine = FakeSpeechEngine()
    narrator = Narrator(engine)

    narrator.speak("   ")

    assert engine.spoken == []
    assert engine.run_count == 0


def test_stop_delegates_to_engine() -> None:
    engine = FakeSpeechEngine()
    narrator = Narrator(engine)

    narrator.stop()

    assert engine.stop_count == 1
