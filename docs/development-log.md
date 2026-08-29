# Development Log

This log preserves important architectural and product questions, decisions, trade-offs, and lessons discovered while building. It does not duplicate Git history or record every discussion.

Resolved entries will be added only after the user is satisfied with the decision. Unresolved matters will be marked clearly as open questions rather than given invented conclusions.

## Open questions

None recorded yet.

## Decisions and lessons

### Replaceable speech engine and test double

**Question:** How can the Narrator use the real Windows speech engine in the application but a fake engine in tests without requiring inheritance from a shared base class?

**Why it mattered:** Narration should remain replaceable, and automated tests should verify behaviour without producing sound or depending on a particular audio device.

**Decision:** Describe the small required speech interface with a Python `Protocol` and inject an engine into `Narrator`. Normal application startup uses a named factory class method to construct a Narrator backed by `pyttsx3`; tests inject a `FakeSpeechEngine` that records calls instead.

**Reasoning:** A protocol supports structural typing: compatible objects satisfy it by providing the required methods, without inheriting from an abstract base class. Dependency injection means the Narrator receives its collaborator from outside; this is broader and more precise than merely wrapping a tool. The fake records requested speech but never synthesizes audio. The voice heard during the manual check came from the real path: `main.py` created a `pyttsx3` engine, which delegated to Windows SAPI.

`runAndWait()` is a synchronous, blocking call that runs the TTS engine loop until queued speech finishes. It is not itself evidence that the application is multithreaded. Concurrency becomes necessary when keyboard input must remain responsive while speech is running.

**Future:** Test real cancellation separately before relying on `pyttsx3.stop()`. Keep the Narrator dependent on a small speech capability rather than on provider-specific behaviour.

### Pre-commit learning checkpoint

**Question:** When should milestone implementation be explained and committed?

**Decision:** Before each meaningful milestone commit, summarize what works, show a small amount of important code or engineering context, explain limitations, and pause for questions. Commit after the user is satisfied.

**Reasoning:** The project is intended both to produce a useful system and to develop the user’s understanding without requiring a line-by-line code review.

**Future:** Keep explanations selective and deepen them when the user asks, especially around audio, concurrency, state, persistence, speech recognition, and LLM context.
