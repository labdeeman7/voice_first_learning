from voice_first_learning.narrator import Narrator


def main() -> None:
    narrator = Narrator.system_default()
    narrator.speak("Hello, this is the study companion.")


if __name__ == "__main__":
    main()
