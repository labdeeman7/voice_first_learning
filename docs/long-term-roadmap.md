# Long-Term Roadmap

## Stage 1 — Stabilize the validated loop

Only proceed if the weekend interaction feels valuable.

- Formalize the Conductor’s explicit state machine.
- Enforce exclusive ownership of audio input and output.
- Separate durable reading progress from temporary playback progress.
- Make interruption, cancellation, retry, and recovery predictable.
- Preserve an immutable return point for the duration of each tangent.
- Record which sentences were completed, interrupted, and replayed.
- Recover safely from application termination in every interaction state.
- Introduce replaceable boundaries around TTS, transcription, and Tutor providers without building a plugin framework.
- Add focused tests for state transitions and persistence.
- Keep one process and simple local storage until actual scale requires otherwise.

Deterministic code remains responsible for playback, position, commands, persistence, and recovery. The LLM supplies explanations, not control authority.

## Stage 2 — Improve the laptop listening experience

- Add reliable media-key control.
- Improve cancellation latency and prevent audio overlap.
- Add repeat sentence, previous paragraph, next paragraph, and speed controls.
- Add spoken status and recovery prompts where useful.
- Support multiple EPUBs and separate progress for each.
- Improve chapter selection and navigation.
- Develop better heuristics for selecting “what I actually heard” as Tutor context.
- Add lightweight conversation compaction so longer tangents remain coherent.
- Measure real interaction latency across interruption, transcription, Tutor response, and speech.

This stage establishes behavioral expectations before moving to mobile.

## Stage 3 — Android Listen Mode

- Build a native Android playback shell around the proven Conductor behavior.
- Support background playback through the appropriate Android media service.
- Operate with the screen locked.
- Expose pause, interrupt, resume, and navigation through lock-screen and notification controls.
- Support wired and Bluetooth earbud/media buttons.
- Handle audio focus correctly when calls, alarms, navigation, or other media intervene.
- Manage microphone permissions and temporary audio routing safely.
- Resume sessions after process eviction or device restart.
- Make downloaded books and essential session state available offline.
- Ensure phone-in-another-room use works before adding visual polish.

Only after reliable media controls exist should wake-word detection be considered. A wake word introduces battery, privacy, false-trigger, echo-cancellation, and background-execution problems. It should activate the Conductor, not talk directly to the Tutor.

## Stage 4 — Mature conversational Tutor

- Preserve coherent multi-turn conversation over long tangents.
- Distinguish source-grounded explanation from broader speculation.
- Let the Tutor refer explicitly to the current passage and nearby context.
- Compact older turns without losing decisions, questions, or the learner’s mental model.
- Maintain the narration return point independently from conversation length.
- Support provider swapping based on quality, latency, privacy, or cost.
- Add model evaluation using representative technical passages and real learner questions.
- Stream text to reduce perceived latency.
- Add realtime transcription and incremental turn detection.
- Add Tutor barge-in so the learner can interrupt a long answer.
- Eventually evaluate native speech-to-speech models while keeping Conductor authority over mode and playback.
- Provide a clean spoken transition back to the source: brief recap if requested, then resume.

Realtime models may combine transcription, reasoning, and Tutor speech internally, but they still occupy the Tutor role. They do not inherit reading-position control.

## Stage 5 — Better narration

- Replace basic TTS when its limitations become the dominant usability problem.
- Add pronunciation dictionaries for technical abbreviations, symbols, names, and domain terms.
- Normalize prose selectively for speech.
- Add appropriate pauses around definitions, examples, headings, lists, and contrasts.
- Improve cadence and emphasis without changing the author’s meaning.
- Expand abbreviations according to context.
- Detect prose that is unintelligible when spoken literally.
- Handle inline mathematics with consistent spoken forms.
- Offer a literal mode and a speech-adapted mode.
- Preserve links between adapted narration and original source positions.
- Evaluate richer neural TTS or controllable voices after correctness and interruption remain reliable.

Speech adaptation should be inspectable and reversible. It must not silently turn narration into LLM-authored summarization.

## Stage 6 — Document model expansion

- Support a library of EPUBs with stable identities and per-book progress.
- Preserve chapters, sections, paragraphs, sentences, footnotes, and source anchors.
- Improve handling of tables, code, references, sidebars, and citations.
- Add PDF only after defining what makes a PDF suitable for Listen Mode.
- Extract native PDF text before considering OCR.
- Add layout-aware reconstruction for multi-column pages and broken reading order.
- Remove repeated headers, footers, and page numbers.
- Use OCR only for scanned or image-based regions that require it.
- Represent equations, citations, and footnotes explicitly rather than flattening everything into prose.
- Preserve mappings from normalized spoken text back to pages and source fragments.
- Allow the Tutor to receive a small relevant window rather than the whole document.

This becomes a structured document pipeline only when multiple real documents demonstrate the need. It should not become a general-purpose ingestion platform by default.

## Stage 7 — Multimodal and figure-aware listening

- Detect explicit references such as “as shown in Figure 6.”
- Associate captions and nearby explanatory text with the referenced figure.
- Estimate whether comprehension depends materially on seeing the figure.
- Introduce a short Conductor-owned choice:
  - describe it;
  - show or save it for later;
  - skip it;
  - continue.
- Generate spoken descriptions that distinguish visible facts from interpretation.
- Save a figure bookmark with source location.
- When a screen is available, open the correct page or image.
- When hands-free, postpone the figure without disrupting reading progress.
- Let the Tutor discuss the figure only when the relevant visual and text context are available.

Figure importance should begin with transparent heuristics and user choice. An LLM can help interpret a figure, but should not unilaterally derail narration.

## Stage 8 — Selective notes and session memory

- Add “remember that” as a Conductor command.
- Capture the immediately relevant passage, conversation turn, and source position.
- Allow “save my explanation” and “save the Tutor’s explanation.”
- Let the learner dictate a note without advancing the book.
- Support brief end-of-session summaries.
- Preserve explicit provenance:
  - **Source claim:** what the document states.
  - **Learner idea:** the learner’s own interpretation or hypothesis.
  - **Tutor explanation:** an AI-generated explanation.
  - **Conclusion:** a synthesis reached during discussion.
  - **Open question:** something unresolved.
- Store only deliberately selected or clearly summarized material.
- Keep raw session history available temporarily without treating every utterance as durable knowledge.
- Allow correction, deletion, and review before permanent export.

The first memory system can remain structured local data. No vector database is required for capture or provenance.

## Stage 9 — Knowledge-base integration

- Export selected notes and summaries as readable Markdown.
- Place them in an Obsidian inbox rather than automatically reorganizing the vault.
- Preserve source identifiers, locations, timestamps, and provenance labels.
- Add a review workflow before notes become permanent.
- Introduce linking suggestions after a useful body of notes exists.
- Add retrieval over approved durable notes.
- Let the Tutor recall prior learning when it is genuinely relevant.
- Clearly distinguish retrieved personal knowledge from the current source and the Tutor’s own reasoning.
- Add controls for forgetting, correcting, and superseding knowledge.

Only later introduce an ingestion or librarian agent to:

- process reviewed inbox notes;
- propose links;
- identify duplicates or contradictions;
- enrich citations;
- maintain topic indexes;
- connect related reading sessions;
- surface unresolved questions.

The agent should propose knowledge-base changes for review rather than silently rewriting the learner’s record.

## Stage 10 — Study Mode integration

Treat visual study as a sibling mode, not an extension of audio narration.

```text
                    SHARED FOUNDATION
             Tutor, identity, notes, memory
                    /               \
             Listen Mode         Study Mode
          continuous audio      visible document
```

- Continue using Gemini Live or another screen-aware assistant while it already solves the immediate visual interaction.
- Avoid rebuilding screen sharing, diagram discussion, and visual navigation without a demonstrated product gap.
- First connect Study Mode through lightweight exports or shared notes.
- Later add shared Tutor preferences, provenance, session summaries, and prior-learning retrieval.
- Build a native Study Mode only if tighter source navigation, figure capture, annotation, or knowledge-base integration creates enough value.
- Keep its Conductor distinct: visual pointing, page position, and screen context require different interaction states from continuous narration.

## Stage 11 — Selective agent architecture

Keep these responsibilities deterministic:

- narration progression;
- reading position;
- audio focus and ownership;
- interruption;
- “continue” and navigation commands;
- persistence;
- permissions;
- cancellation;
- error recovery;
- provenance storage;
- user-approved deletion or export.

Use ordinary LLM calls for:

- passage explanation;
- Socratic questioning;
- conversational tutoring;
- speech adaptation;
- figure description;
- session summarization.

Agents become justified only for open-ended, multi-step background work such as:

- ingesting a reviewed knowledge inbox;
- proposing note links across many sources;
- reconciling duplicate or conflicting notes;
- enriching literature metadata and citations;
- synthesizing multiple sessions;
- maintaining long-term memory indexes;
- finding connections between prior learning and new material.

Even then, agent actions should be bounded, observable, reversible, and separated from the realtime listening loop.
