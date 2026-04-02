# Report — Meeting Transcript Summarizer

## Business Use Case

Professionals spend significant time in meetings but often lack a reliable system for capturing and distributing notes afterward. This prototype automates the first-pass summarization of raw meeting transcripts, producing a structured output with a summary, decisions, action items, and open questions. The intended user is a team lead or project manager who wants to distribute meeting notes quickly without spending 15–20 minutes writing them up manually.

## Model Choice

I used **Claude Opus 4.6** (`claude-opus-4-6`) via the Anthropic API. I chose this model because it follows complex, multi-part instructions reliably and produces coherent output even when transcripts are messy or contain conflicting information. Its strong instruction-following made it well-suited for the structured output format required in prompt version 3.

I did not test other models for this assignment, but based on the task characteristics (structured extraction, factuality over creativity, moderate output length), a smaller model like Claude Haiku 4.5 would likely work well for straightforward transcripts at lower cost. Opus 4.6 is appropriate for cases with ambiguity or complex multi-stakeholder meetings.

## Baseline vs. Final Design

**Baseline (Prompt v1):** A minimal system prompt asking the model to "extract key points, decisions, and action items." The output was unpredictable in structure — sometimes bullet points, sometimes prose — and action items were buried in summary text. On the vague transcript (Case 4), the model invented owners and deadlines that were not in the transcript.

**Final (Prompt v3):** Added an explicit role, a factuality constraint ("do not invent details not stated in the transcript"), and required section headings with a specific action item format. The output became consistent across all five evaluation cases. The factuality instruction meaningfully reduced hallucination on Case 4 — the model correctly declined to invent owners. The forced structure made action items immediately scannable.

The most important single improvement was adding the section format with a required action item template (`[Owner] - [Task] - [Deadline if stated]`). This prevented the model from merging action items into prose and made downstream use (e.g., pasting into a task tracker) much easier.

## Where the Prototype Still Fails

The system handles the five evaluation cases acceptably, but two failure modes remain. First, on transcripts with conflicting information (Case 3), the model tends to silently resolve the conflict by picking one value rather than flagging the disagreement. A reviewer who does not read the original transcript may not notice this. Second, on very vague transcripts (Case 4), while the model no longer invents owners, it sometimes generates plausible-sounding but technically empty bullet points like "discuss budget — owner TBD" when the transcript provides no real basis for even that framing. Both failures could mislead someone who trusts the output without reading the source.

## Deployment Recommendation

I would recommend deploying this workflow **only with a mandatory human review step before distribution**. The output is a useful first draft that saves time, but it should not be sent to stakeholders automatically. The main risks are: (1) hallucinated deadlines or owners on messy transcripts, (2) silent conflict resolution that loses important information, and (3) model confidence in structuring even low-quality input, which may give reviewers false confidence in the output.

A reasonable deployment path: generate the summary automatically after a meeting ends, route it to the meeting organizer for a 2–3 minute review and approval, then distribute. This preserves the time savings while keeping a human accountable for accuracy.
