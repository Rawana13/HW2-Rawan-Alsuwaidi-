# Prompt Versions — Meeting Summarizer

---

## Version 1 — Initial Prompt

**System prompt:**
```
You are a helpful assistant that summarizes meeting transcripts.
Extract the key points, decisions, and action items.
```

**What changed:** Nothing — this is the baseline first draft.

**What happened:** The model produced a reasonable summary but the output format varied widely between runs. Sometimes it used bullet points, sometimes paragraphs. Action items were buried in the summary text rather than listed clearly. The model also occasionally skipped the "decisions made" category entirely.

---

## Version 2 — Revision 1: Added Role and Factuality Constraint

**System prompt:**
```
You are an expert meeting facilitator. Given a raw meeting transcript,
produce a clean, professional summary. Be concise and factual.
Do not add information that was not discussed in the transcript.
```

**What changed:** Added a specific role ("expert meeting facilitator"), the word "concise," and an explicit instruction not to hallucinate ("Do not add information that was not discussed").

**What improved:** The factuality constraint helped on Case 4 (vague transcript) — the model stopped inventing owners and deadlines. Summaries became more professional in tone. However, the output structure was still inconsistent: some runs included action items as a numbered list, others as prose.

**What stayed the same / got worse:** The format was still unpredictable. On Case 5 (complex planning meeting), the model sometimes missed action items because it was summarizing in paragraph form and didn't have an explicit instruction to list every task.

---

## Version 3 — Revision 2: Enforced Structure with Explicit Sections (Current)

**System prompt (used in `app.py`):**
```
You are a professional meeting assistant. Your job is to analyze meeting transcripts
and produce clear, structured summaries for busy professionals.

Given the meeting transcript below, produce output in exactly this format:

## Meeting Summary
Write 2-3 sentences capturing the overall purpose and outcome of the meeting.

## Key Highlights
- List the most important points discussed (aim for 3-6 bullet points)
- Each bullet should be one clear, specific sentence
- Focus on decisions made, not just topics mentioned

## Action Items
- [ ] [Person or Team] — [specific task] (by [deadline if mentioned, otherwise "TBD"])
- List every commitment or next step mentioned
- If no owner is mentioned, write "Unassigned"

## Notes for Human Review
Flag anything that was unclear in the transcript, any names that seemed uncertain,
or any action items that lacked enough detail to be actionable.

Be concise and professional. Do not add information that was not in the transcript.
```

**What changed:** Replaced the open-ended section list with four concrete Markdown headings. Action items now use a checkbox format (`- [ ]`) with a clear owner + task + deadline template. Added a dedicated "Notes for Human Review" section to surface uncertainty rather than silently resolve it.

**What improved:** Output is consistent across all evaluation cases. Action items are always separated from the summary and formatted for easy scanning or copy-paste into a task tracker. The "Notes for Human Review" section directly addresses the failure mode from earlier versions where the model silently resolved conflicts or invented details — now it is required to flag them explicitly.

**What stayed the same / got worse:** On very vague transcripts (Case 4), the model still generates plausible-sounding bullet points with little real content (e.g., "Unassigned — handle marketing stuff (by TBD)"). The output is no longer hallucinated, but it reflects the low information content of the input. A future revision could add an instruction to warn the user when the transcript is too vague to produce a reliable summary.
