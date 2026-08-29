# Working Agreements

These agreements describe practical boundaries and collaboration habits for the weekend prototype. They are guidance, not formal software contracts. The priority is to preserve the product’s conceptual separation while choosing the simplest understandable implementation that proves:

```text
READ → INTERRUPT → DISCUSS → CONTINUE → RESUME
```

New components may be suggested when a concrete need appears, but they should not be introduced merely to make the architecture look more complete.

## DocumentReader

- **Responsible for:** opening the chosen EPUB, following its reading order, extracting useful text, dividing it into stable chapters, paragraphs, and sentences, and exposing source positions.
- **Not responsible for:** speech, playback, Tutor prompts, session transitions, persistence, or deciding what the learner should hear next.
- **Weekend implementation:** one established Python EPUB parser plus simple HTML/text cleanup and sentence splitting for one known book.
- **Acceptable weekend assumptions:** the EPUB is readable, mostly linear prose, and may receive small book-specific cleanup rules. Comprehensive EPUB compatibility is unnecessary.
- **Replaceable later:** EPUB parser, cleanup rules, segmentation, document representation, and eventually the entire ingestion pipeline.
- **Graceful failures:** missing or unreadable files, invalid EPUBs, empty chapters, extraction failures, and positions that no longer exist. Fail with a useful message rather than silently reading nonsense or corrupting progress.
- **May decide without asking:** filenames, internal data shapes, helper functions, parsing-library usage within the agreed design, and small cleanup heuristics for the test book.
- **Check first:** adding PDF/OCR/general ingestion, introducing heavy NLP infrastructure, changing source-position semantics materially, or adopting a dependency that constrains future mobile migration.

## Narrator

- **Responsible for:** speaking narration units supplied by the Conductor, reporting completion or failure, and stopping as reliably as the selected TTS mechanism permits.
- **Not responsible for:** parsing documents, choosing the next sentence, advancing reading position, handling Tutor conversation, or interpreting commands.
- **Weekend implementation:** one simple local or system TTS engine, probably speaking sentence-sized units.
- **Acceptable weekend assumptions:** one installed voice, modest voice quality, sentence-level playback, and restarting the interrupted sentence rather than resuming at an exact word.
- **Replaceable later:** TTS engine, voice, audio backend, speech settings, preprocessing, and cancellation mechanism.
- **Graceful failures:** unavailable TTS, failed playback, cancellation that times out, missing audio device, and unexpected termination. It must not claim completion when speech did not complete.
- **May decide without asking:** minor TTS configuration, temporary files if safely managed and ignored by Git, and implementation details that preserve behaviour.
- **Check first:** if reliable interruption is impossible with the selected approach; before accepting long interruption delay; before changing sentence-level resume behaviour; or before adding paid/custom/cloud TTS with meaningful cost or architectural impact.

## SpeechInput

- **Responsible for:** recording a learner utterance when asked, stopping the recording, transcribing it, and returning either a transcript or an explicit failure.
- **Not responsible for:** deciding whether an utterance means “continue,” prompting the Tutor, controlling narration, or changing session state.
- **Weekend implementation:** finite, push-to-talk recording with a simple transcription service or local recognizer, plus a typed-input fallback for debugging and recovery.
- **Acceptable weekend assumptions:** one microphone, one language, no wake word, no continuous listening, and manual activation before an utterance if necessary.
- **Replaceable later:** recorder, speech-to-text provider, turn detection, streaming transcription, microphone backend, and eventual wake-word activation.
- **Graceful failures:** missing microphone, denied permission, silence, unintelligible audio, timeouts, API/network errors, and poor technical-term transcription. It should offer retry or fallback rather than ending the session.
- **May decide without asking:** audio file format, safe temporary-file handling, recording limits, and minor noise/timeout settings.
- **Check first:** abandoning voice for the demonstration, adding always-on listening or wake-word dependencies, sending sensitive recordings to a new service, or adding non-negligible transcription cost.

## Tutor

- **Responsible for:** contextual explanation, reasoning with the learner, following multi-turn tangents, correcting mental models, and maintaining the recent discussion supplied to it.
- **Not responsible for:** narration, audio ownership, document progression, persistence semantics, or deciding when playback resumes.
- **Weekend implementation:** a cheap or free hosted text model receiving a small passage, a clear description of what was heard, recent conversation, and the current question.
- **Acceptable weekend assumptions:** one configured provider, bounded recent history, no whole-book context, no tools, no retrieval, and no agent framework.
- **Replaceable later:** model provider, model, prompt strategy, streaming, context compaction, and eventually realtime speech.
- **Graceful failures:** unavailable credentials, timeouts, rate limits, empty or malformed responses, overly long context, and weak answers. The learner should be able to retry or remain in Tutor mode.
- **May decide without asking:** prompt wording, conservative context-window sizing, retry details, and SDK usage that does not alter product behaviour.
- **Check first:** changing provider in a way that adds meaningful cost or data implications; adding tools, retrieval, or agents; allowing the Tutor to control playback; or changing persistent multi-turn Tutor mode into automatic resume.

## SessionState / SessionStore

- **Responsible for:** representing current book position, durable progress, active narration position, interruption return point, recent Tutor conversation, and enough heard context for recovery and tutoring; saving and restoring that state safely.
- **Not responsible for:** parsing the EPUB, speaking, recording, asking the LLM questions, or deciding state transitions.
- **Weekend implementation:** a small explicit in-memory session object persisted to a human-readable local JSON file.
- **Acceptable weekend assumptions:** one user, one active local session, one known EPUB, no synchronization, no database, and sentence-level positions.
- **Replaceable later:** storage format, migration/versioning strategy, multi-book storage, synchronization, encryption, and platform-specific persistence.
- **Graceful failures:** missing state, first run, malformed or partially written state, incompatible positions, interrupted writes, and moved or changed books. Prefer safe recovery and an explanation over silent progress loss.
- **May decide without asking:** JSON layout details, filenames, validation helpers, and atomic-write mechanics that preserve agreed semantics.
- **Check first:** changing when progress is considered complete, changing resume semantics, discarding conversation unexpectedly, introducing a database, or making persistence choices that materially constrain Android migration.

## Conductor

- **Responsible for:** explicit interaction states; exclusive coordination of narration, microphone capture, Tutor requests, and Tutor speech; interpreting control commands such as “continue”; preserving the return point; preventing overlapping audio; and directing recovery.
- **Not responsible for:** EPUB parsing, generating explanations itself, implementing TTS/STT internals, or hiding important control decisions inside an LLM.
- **Weekend implementation:** a small, explicit state-driven coordinator in one Python process, with keyboard interruption and deterministic recognition of a narrow set of control phrases.
- **Acceptable weekend assumptions:** a terminal interface, one active operation at a time, limited commands, sentence-level resumption, and straightforward sequential coordination with only the minimum concurrency required for interruption.
- **Replaceable later:** terminal input, media controls, platform audio-focus integration, command recognition, concurrency mechanism, and mobile host.
- **Graceful failures:** invalid transitions, repeated interrupts, cancellation failures, transcription/Tutor/TTS errors, accidental interruption, shutdown in any state, and attempted overlapping audio. It should preserve the return point and offer a safe route to resume or exit.
- **May decide without asking:** internal state names, small helper components, logging details, ordinary refactoring, and deterministic handling of equivalent “continue” phrases.
- **Check first:** changing the fundamental interaction; adding hidden LLM control; changing audio ownership; adding an architectural framework/layer; altering multi-turn behaviour or narration resume semantics; or making a difficult-to-reverse mobile trade-off.

## How we work together

### Work in small milestones

We will follow the approved weekend plan incrementally rather than implementing large sections of the roadmap at once.

For each meaningful milestone, the assistant will:

1. Briefly explain what is about to be implemented.
2. Implement only that milestone.
3. Run appropriate tests and checks.
4. Report what changed.
5. Explain what works.
6. State what does not yet work or was deliberately left out.
7. Explain important design decisions without reviewing every line.
8. Give the user a simple way to try or verify the behaviour.
9. Before committing, highlight a few interesting concepts or small code excerpts that help the user understand the milestone.
10. Pause for questions and corrections; commit after the user is satisfied with the explanation.
11. Stop before the next major milestone so the user can review and ask questions.

Questions about why something was implemented a particular way are part of the project. Explanations should support understanding without turning routine work into a tutorial.

### Git discipline

Use Git throughout the project. After a meaningful working milestone or substantial architectural change:

- run relevant tests and checks;
- inspect the diff;
- check for credentials, secrets, generated junk, large books, temporary audio, and other accidental files;
- make a focused commit with a descriptive message;
- ensure the milestone is runnable or otherwise in a sensible state.

Do not commit every tiny edit. Do not describe an experimental or broken change as a completed milestone merely to create a commit. Never commit API keys, credentials, copyrighted test books, generated audio, transient session state, or local environment files.

### Explain completed work

After a major milestone, report concisely:

- what was built;
- how it works conceptually;
- which files or components matter;
- important decisions;
- remaining limitations;
- how the user can test it;
- the logical next milestone.

## Questions, decisions, and lessons

Use `docs/development-log.md` for important resolved discussions and clearly marked open questions, not as a duplicate of Git history.

Record an entry only when a discussion:

- affects architecture;
- captures an important trade-off or lesson;
- changes the roadmap;
- establishes behaviour likely to be forgotten.

Before marking a decision resolved, ensure the user is satisfied. Otherwise record it as an open question. Entries should contain the question or problem, why it mattered, the decision, brief reasoning, and future consequences.

## When to check with the user

Stop and ask before:

- expanding weekend scope;
- adding a major dependency;
- changing the interaction model;
- introducing an unplanned framework or architectural layer;
- replacing deterministic behaviour with LLM or agent logic;
- making a choice that materially affects Android/mobile migration;
- adding non-negligible cost;
- changing persistence semantics;
- abandoning voice interaction because it is difficult;
- removing multi-turn conversation;
- changing narration resume behaviour;
- changing a main component’s responsibility;
- making a significant, difficult-to-reverse trade-off.

No permission is needed for filenames, small helper functions, ordinary refactoring, agreed library usage, ordinary bug fixes, test organization, formatting, linting, or minor details that do not change behaviour.

## Weekend engineering rule

Prefer the simplest implementation that proves the interaction. When two approaches are reasonable, prefer the one that:

1. is easiest to understand;
2. is easiest to debug;
3. keeps important components replaceable;
4. reaches the Sunday demo sooner.

Clean architecture means preserving the important conceptual boundaries, not maximizing abstraction.

## Learning rule

When audio playback, interruption, cancellation, concurrency, state machines, persistence, speech recognition, LLM context management, or future mobile implications become relevant, explain the important concept at the point where it helps the user understand a decision or observed behaviour. Do not turn every implementation step into a tutorial.
