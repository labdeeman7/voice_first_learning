# Weekend Plan

## Guiding scope

Build one understandable Python process with four conceptual components:

- **Narrator:** extracts and speaks one known EPUB sentence by sentence.
- **Tutor:** handles contextual, multi-turn text conversations through one replaceable API provider.
- **Conductor:** exclusively controls narration, recording, Tutor speech, and transitions.
- **Session State:** stores the durable reading position, interruption return point, and current discussion.

Use sentence-level playback as the practical unit of narration. If interrupted, resume from the beginning of that sentence. This is precise, reliable, and sufficient to validate the experience.

Use keyboard activation for interruption. Use voice for questions and “continue.” Keep a typed-question fallback so microphone or transcription trouble cannot invalidate the wider interaction experiment.

The Conductor should use a small explicit state model:

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

No agent framework, database, GUI, asynchronous event infrastructure, or generalized document platform.

## Friday evening

### 1. Primary objective

Prove the basic audio and document path:

> One known EPUB can be opened, divided into stable reading units, and spoken aloud.

### 2. Concrete implementation milestones

- Establish the minimal Python project and dependency environment.
- Confirm that the laptop can speak a fixed test sentence through a simple TTS engine.
- Open one known, mostly prose-based EPUB.
- Extract its reading order and basic chapter text.
- Remove only obviously unusable empty content and markup.
- Divide the selected content into paragraphs and sentences.
- Assign stable chapter, paragraph, and sentence positions.
- Speak several consecutive sentences.
- Print the current position and sentence in the terminal for debugging.
- Decide on one fixed EPUB and one known passage for Sunday’s demonstration.

Do not attempt comprehensive EPUB cleaning. Hard-code exclusions for this particular book if necessary.

### 3. Acceptance test

Starting from the terminal, the prototype opens the chosen EPUB and speaks at least several consecutive paragraphs in the correct order without manual intervention.

### 4. Biggest technical risks

- EPUB reading order differs from the visible table of contents.
- Navigation, copyright material, or broken markup gets narrated.
- Sentence splitting behaves badly around abbreviations or technical notation.
- The selected TTS mechanism blocks the program in a way that makes interruption difficult.
- Laptop audio dependencies consume the whole evening.

### 5. What to cut if behind schedule

Cut, in this order:

1. Automatic book-title and chapter-title detection.
2. General EPUB cleanup.
3. Sophisticated sentence segmentation.
4. Multiple voices or speech settings.
5. Support for any EPUB other than the chosen test book.

If EPUB extraction remains troublesome, pre-extract the chosen chapter to plain text manually. The experiment is testing the interaction, not EPUB engineering.

## Saturday

### 1. Primary objective

Prove dependable continuous narration, interruption mechanics, and persistent position:

> The prototype behaves like a basic resumable audiobook reader.

### 2. Concrete implementation milestones

- Narrate the chosen book continuously, one sentence at a time.
- Make the Conductor the only component allowed to initiate or stop audio.
- Add keyboard interruption, preferably Space.
- Stop current speech if the selected TTS engine permits it.
- If true mid-utterance cancellation is unreliable, stop at the nearest sentence boundary and make this limitation visible.
- Preserve a return point at the beginning of the interrupted sentence.
- Resume from that return point.
- Save reading state after every completed sentence and during interruption.
- Restore the saved position when the application is reopened.
- Keep two distinct notions of position:
  - the sentence currently being spoken or interrupted;
  - the next sentence confirmed as safe to begin.
- Track a short “heard context” consisting of the current sentence, current paragraph, and a modest amount of preceding text.
- Add minimal terminal diagnostics showing state transitions and saved position.
- Test pause, resume, exit, and restart repeatedly.

Optional only after the acceptance test passes:

- Repeat current sentence.
- Previous or next paragraph.
- Basic speech-rate adjustment.

### 3. Acceptance test

Run the application, listen through several paragraphs, interrupt during a known sentence, resume that sentence, close the application, and reopen it. It returns to the saved sentence or the next correctly recorded sentence without losing the book location.

Repeat this at least three times at different positions.

### 4. Biggest technical risks

- TTS playback cannot be cancelled promptly.
- Position is advanced before speech has actually completed.
- A crash leaves partially written or ambiguous session state.
- Keyboard events are unavailable while playback blocks.
- Sentence boundaries do not correspond well to what was audibly heard.
- The system resumes one sentence too early or too late.

### 5. What to cut if behind schedule

Cut, in this order:

1. Navigation commands.
2. Speed control.
3. Mid-sentence resumption.
4. Immediate mid-sentence cancellation.
5. Chapter-level metadata polish.

Retain sentence-level position, persistent restart, and a trustworthy return point. If necessary, narration may stop after completing the current sentence and later replay it.

## Sunday

### 1. Primary objective

Prove the complete learning interaction:

> Interrupt narration, conduct a contextual multi-turn voice discussion, say “continue,” and resume reliably.

### 2. Concrete implementation milestones

- Record one microphone utterance after narration has stopped.
- Transcribe it through the simplest reliable speech-to-text path.
- Preserve a typed-input fallback for debugging and demo recovery.
- Have the Conductor distinguish “continue” from an ordinary Tutor question.
- Initially use a conservative deterministic check for clear continuation phrases such as:
  - “continue”;
  - “okay, continue”;
  - “resume the book”;
  - “carry on reading.”
- For other utterances, give the Tutor:
  - book and chapter identity;
  - preceding passage;
  - current paragraph;
  - interrupted sentence;
  - recent turns from this Tutor conversation;
  - the learner’s latest question.
- Explicitly describe which text was actually heard versus text not yet narrated.
- Maintain Tutor mode after every answer instead of automatically resuming.
- Speak each Tutor answer using TTS.
- Return to microphone listening for follow-up questions.
- Preserve the original narration return point throughout a long tangent.
- On “continue,” end Tutor mode, clear or archive the temporary discussion, and resume from the interrupted sentence.
- Handle recoverable failures simply:
  - failed transcription: ask to repeat;
  - failed Tutor call: retry or permit typed input;
  - failed Tutor TTS: print the answer and remain in Tutor mode;
  - accidental interruption: allow immediate resume.
- Run several complete loops before polishing anything.
- Stop development once the success criterion passes reliably.

### 3. Acceptance test

Complete three full cycles:

```text
narrate
→ interrupt
→ voice question
→ contextual answer
→ voice follow-up
→ useful answer
→ say “continue”
→ resume correct sentence
```

At least one cycle should include a tangent not answered directly by the passage. The Tutor must retain both the discussion context and the original return point.

Then close and reopen the application and confirm that narration resumes from the saved reading position.

### 4. Biggest technical risks

- Recording captures residual narrator audio.
- Transcription fails on technical vocabulary.
- “Continue” is passed to the Tutor instead of changing Conductor state.
- Tutor conversation history becomes confused with book context.
- Tutor speech and Narrator speech overlap.
- Latency makes the interaction feel cumbersome.
- A long tangent destroys or advances the narration return point.
- The Tutor confidently answers from general knowledge without relating its answer to the supplied passage.

### 5. What to cut if behind schedule

Cut, in this order:

1. Automatic detection of varied resume phrases; support only “continue.”
2. Tutor-response streaming.
3. Spoken error messages.
4. Automatic microphone reactivation; use a key before each follow-up.
5. Cloud TTS for Tutor responses; use the same basic TTS as Narrator.
6. Voice input as the sole path; preserve one voice question but allow typed follow-ups.

Do not cut:

- contextual passage delivery;
- at least one voice question;
- multi-turn Tutor mode;
- Conductor-owned “continue” transition;
- reliable narration return point;
- persistent reading state.

## Exact Sunday demo

1. Start the application with the known EPUB.
2. It restores the saved position and begins narrating.
3. Let it read into a preselected technical passage.
4. Press Space while a meaningful sentence is being spoken.
5. Narration stops, and the terminal indicates that the Tutor is listening.
6. Ask: “I don’t understand why this follows from the previous point. Can you explain it?”
7. The Tutor answers using the interrupted passage.
8. Ask a follow-up that tests reasoning: “So does that mean that …?”
9. The Tutor confirms or corrects the mental model.
10. Say: “Okay, continue.”
11. The Conductor exits Tutor mode without sending that phrase as a substantive question.
12. The Narrator restarts the interrupted sentence and continues.
13. Close the application.
14. Reopen it and confirm that it restores the latest durable reading position.

The demo succeeds even if interruption uses a key, questions are recorded one utterance at a time, and resumption replays the full interrupted sentence.
