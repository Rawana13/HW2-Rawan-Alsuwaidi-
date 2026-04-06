# Report — Meeting Summarizer

## Business Use Case

Professionals spend significant time in meetings but often lack a reliable system for capturing and distributing notes afterward. This prototype automates the full pipeline: it records audio from the microphone, transcribes it locally using Whisper, and passes the transcript to Google Gemini to produce a structured summary with action items. The intended user is a team lead or project manager who wants to walk away from a meeting with notes ready — without spending 15–20 minutes writing them up manually.

## Technology Stack

| Component | Tool | Reason |
|---|---|---|
| Audio recording | `sounddevice` | Simple cross-platform microphone access |
| Audio file I/O | `soundfile` | Saves raw audio to WAV for Whisper |
| Transcription | OpenAI Whisper (`base` model) | Runs fully locally, no API cost, good accuracy for clear speech |
| Summarization | Google Gemini 1.5 Flash | Fast, low-cost, follows structured output instructions reliably |

Whisper runs on-device, so no audio is sent to an external service. Only the transcript text is sent to the Gemini API.

## Model Choice

I used **Gemini 1.5 Flash** (`gemini-1.5-flash`) via the Google Generative AI API. This model is well-suited for structured text extraction tasks: it follows multi-part formatting instructions reliably, handles messy or conversational input gracefully, and is fast enough for interactive use after a meeting ends.

I did not test other models for this assignment, but Gemini 1.5 Flash is a strong default for this type of task. A smaller/faster model could work for simple transcripts; a larger model (e.g., Gemini 1.5 Pro) might be worth testing on long or complex multi-stakeholder meetings.

## Baseline vs. Final Design

**Baseline (Prompt v1):** A minimal system prompt asking the model to "extract key points, decisions, and action items." The output was unpredictable in structure — sometimes bullet points, sometimes prose — and action items were buried in summary text. On the vague transcript (Case 4), the model invented owners and deadlines not present in the transcript.

**Final (Prompt v3):** Added an explicit role, a factuality constraint ("do not add information that was not in the transcript"), and four required Markdown sections with a checkbox-style action item format. Added a "Notes for Human Review" section that requires the model to surface uncertainty rather than silently resolve it. The output is now consistent across all five evaluation cases.

The most impactful single change was the structured section format with an explicit action item template (`- [ ] [Person] — [task] (by [deadline])`). This prevented action items from being buried in prose and made the output immediately usable for follow-up.

## Where the Prototype Still Fails

Two failure modes remain. First, on transcripts with conflicting information (Case 3), the model sometimes picks one value rather than flagging the disagreement — though the "Notes for Human Review" section now catches most of these. Second, on very vague transcripts (Case 4), the model produces technically accurate but near-empty bullet points that look structured but contain little useful information. Both failures underscore that the quality of the output is bounded by the quality of the transcript, which is in turn bounded by audio clarity and speaker behavior.

A third limitation is microphone-only input. The current pipeline cannot process an existing audio file or a pre-written transcript without modifying the code.

## Deployment Recommendation

Deploy **only with a mandatory human review step before distribution**. The output is a useful first draft that saves time, but should not be sent to stakeholders automatically. Main risks: (1) hallucinated or misattributed details on messy transcripts, (2) silent conflict resolution, and (3) low-quality audio producing an inaccurate Whisper transcript that Gemini then summarizes confidently.

Recommended workflow: record and summarize immediately after the meeting → route to the meeting organizer for a 2–3 minute review → distribute. This preserves the time savings while keeping a human accountable for accuracy.
