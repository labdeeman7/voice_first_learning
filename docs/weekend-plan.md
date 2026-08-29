# Saturday–Sunday Weekend Plan

## Guiding scope

The weekend still has one purpose:

> Prove that the learner can listen to one known EPUB, interrupt it, have a contextual multi-turn voice discussion, say “continue,” and resume from a trustworthy position that survives application restarts.

Build one understandable Python process around the established conceptual boundaries:

- **DocumentReader:** extracts stable narration units from one known EPUB.
- **Narrator:** speaks supplied units and stops when directed.
- **SpeechInput:** records and transcribes one utterance at a time.
- **Tutor:** conducts contextual, multi-turn discussion through a replaceable provider.
- **SessionState / SessionStore:** preserves reading progress, the interruption return point, heard context, and recent discussion.
- **Conductor:** exclusively owns interaction state and audio handoff.

Use sentence-level playback and restart the interrupted sentence when narration resumes. Use a keyboard to enter Tutor mode. Use voice for questions and “continue,” with typed input retained as a diagnostic fallback.

```text
NARRATING
→ INTERRUPTING
→ LISTENING
→ TUTOR_THINKING
→ TUTOR_SPEAKING
→ LISTENING
→ RESUMING
→ NARRATING
```

No PDF, OCR, figures, Obsidian, RAG, agents, custom TTS, wake word, Android, polished UI, microservices, or generalized ingestion.

## Saturday

### 1. Primary objective

Finish with a dependable, resumable narration prototype:

> One known EPUB is read continuously, can be interrupted, and retains a trustworthy sentence-level position across restarts.

### 2. Milestones in order

#### Milestone A — Environment and first speech

- Establish the minimal Python environment and project structure.
- Confirm that a simple local or system TTS engine speaks: “Hello, this is the study companion.”
- Confirm that the selected TTS approach has a plausible cancellation path before building around it.

**Checkpoint:** fixed text is spoken reliably from the command line.

#### Milestone B — One EPUB to structured text

- Open one known, mostly prose-based EPUB.
- Follow its reading order and extract useful chapter text.
- Remove only obviously unusable markup and empty content.
- Divide text into paragraphs and sentences with stable positions.
- Print several extracted units and their positions for inspection.
- Select one known technical passage for Sunday’s demo.

**Checkpoint:** several paragraphs from the chosen book appear in the correct order with stable chapter, paragraph, and sentence positions.

#### Milestone C — Continuous narration

- Have the Conductor request narration one sentence at a time.
- Make the Conductor the only component that decides which unit comes next.
- Display minimal terminal diagnostics showing the current position.
- Continue automatically across several paragraphs.

**Checkpoint:** the chosen EPUB can be listened to continuously without manual advancement.

#### Milestone D — Interrupt, resume, and persist

- Add keyboard interruption, preferably Space.
- Stop the current sentence if the TTS engine permits reliable cancellation.
- Otherwise stop at the nearest sentence boundary and expose that limitation clearly.
- Freeze the return point at the beginning of the interrupted sentence.
- Resume by replaying that sentence.
- Persist the next safe narration position in human-readable local state.
- Restore it after closing and reopening the application.
- Keep current/started, completed, and next-safe positions conceptually distinct.
- Retain a small heard-context window for Sunday’s Tutor work.

**Checkpoint:** interruption and restart tests do not lose or incorrectly advance the reading position.

### 3. Saturday acceptance test

1. Start the application with the chosen EPUB.
2. Listen through several paragraphs.
3. Interrupt during a known sentence.
4. Resume and hear that sentence replayed.
5. Close the application.
6. Reopen it and resume from the saved sentence or next correctly recorded sentence.
7. Repeat interruption and restart at three different positions.

Saturday succeeds without any AI if this test passes.

### 4. Biggest technical risks

- Laptop audio or Python setup consumes too much time.
- EPUB reading order is poor or includes navigation and publishing material.
- TTS blocks keyboard handling or cannot be cancelled promptly.
- Reading position advances before speech actually completes.
- Sentence segmentation is poor around technical abbreviations or notation.
- State writes are ambiguous or damaged by shutdown.

### 5. What to cut if behind schedule

Cut in this order:

1. Automatic title and chapter-title detection.
2. General EPUB cleanup; use book-specific rules.
3. Sophisticated sentence segmentation.
4. Navigation commands and speed control.
5. Immediate mid-sentence cancellation; stop at the boundary and replay the sentence.
6. General EPUB support; manually pre-extract the chosen demonstration chapter if necessary.

Do not cut continuous narration, a trustworthy return point, or persistent sentence-level progress.

### 6. Saturday stop rule

Once the acceptance test passes, stop improving narration. Do not add Tutor work late at night unless the narration path is stable and the remaining setup is trivial.

## Sunday

### 1. Primary objective

Complete and repeatedly exercise the core experience:

> Interrupt narration, conduct a contextual multi-turn voice discussion, say “continue,” and resume reliably.

### 2. Milestones in order

#### Milestone E — Capture one spoken question

- Record one finite microphone utterance only after narration has stopped.
- Transcribe it through the simplest reliable speech-to-text path.
- Show the transcript for debugging.
- Preserve typed input as a recovery path, not as the target interaction.

**Checkpoint:** a spoken technical question becomes usable text without Narrator audio leaking into the recording.

#### Milestone F — Contextual Tutor response

- Send the Tutor only the relevant context:
  - book and chapter identity;
  - preceding heard passage;
  - current paragraph;
  - interrupted sentence;
  - recent Tutor turns;
  - the learner’s latest question.
- Clearly distinguish completed text from the interrupted sentence.
- Speak the Tutor response using the existing TTS path.
- Recover sensibly from network, rate-limit, empty-response, and TTS failures.

**Checkpoint:** the Tutor answers a spoken question using the correct passage rather than generic book-level context.

#### Milestone G — Multi-turn Tutor mode

- Remain in Tutor mode after an answer.
- Accept at least one spoken follow-up.
- Preserve recent discussion across turns.
- Keep the original narration return point frozen throughout the tangent.
- Do not allow Tutor calls to change document position.

**Checkpoint:** a follow-up can challenge or refine the learner’s mental model without losing the source location.

#### Milestone H — Conductor-owned continue and full loop

- Recognize a narrow set of explicit continuation phrases deterministically before calling the Tutor.
- At minimum support “continue” and “okay, continue.”
- End Tutor mode and release its audio activity.
- Resume narration by replaying the interrupted sentence.
- Repeat the complete loop several times and test restart persistence.

**Checkpoint:** “continue” is a reliable state transition, not another Tutor prompt.

### 3. Sunday acceptance test

Complete three full cycles:

```text
narrate
→ interrupt
→ spoken contextual question
→ useful spoken answer
→ spoken follow-up
→ useful spoken answer
→ say “continue”
→ resume the interrupted sentence
```

At least one cycle should contain a tangent not directly answered by the passage. Then close and reopen the application and confirm that durable reading progress is retained.

### 4. Biggest technical risks

- Recording captures residual Narrator or Tutor audio.
- Speech recognition damages important technical terminology.
- End-to-end latency makes conversation feel laborious.
- Tutor context describes text that was not actually heard.
- “Continue” reaches the LLM instead of the Conductor.
- Narrator and Tutor audio overlap.
- Long tangents corrupt or advance the return point.
- Provider setup, credentials, or rate limits consume the available time.

### 5. What to cut if behind schedule

Cut in this order:

1. Varied resume phrases; support only exact “continue.”
2. Response streaming.
3. Spoken error messages.
4. Automatic microphone reactivation; require a key before each follow-up.
5. Separate Tutor TTS; reuse the Narrator’s basic voice.
6. Voice for every follow-up; require at least the first question and “continue” by voice, with typed follow-ups as fallback.

Do not cut contextual passage delivery, persistent multi-turn Tutor mode, Conductor-owned continuation, the frozen return point, or restart persistence.

### 6. Sunday stop rule

Once the exact demo works reliably, stop. Run it repeatedly, record the result if useful, inspect the repository, and commit the working milestone. Do not add wake words, notes, better voices, mobile work, or document features.

## Exact Sunday demo

1. Start the application with the known EPUB; it restores saved progress.
2. Let the Narrator read into the selected technical passage.
3. Press Space during a meaningful sentence.
4. Narration stops and the Conductor enters listening mode.
5. Ask: “I don’t understand why this follows from the previous point. Can you explain it?”
6. The Tutor answers using the interrupted passage.
7. Ask: “So does that mean that …?” and state a plausible mental model.
8. The Tutor confirms or corrects that model.
9. Say: “Okay, continue.”
10. The Conductor exits Tutor mode without treating the phrase as a substantive Tutor question.
11. The Narrator replays the interrupted sentence and continues.
12. Close and reopen the application and confirm that the latest durable reading position is restored.

The demo succeeds even with keyboard interruption, finite push-to-talk recordings, one basic TTS voice, sentence replay, and typed recovery controls.
