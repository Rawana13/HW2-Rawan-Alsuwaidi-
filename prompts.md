# Prompt Versions — Meeting Transcript Summarizer

---

## Version 1 — Initial Prompt

**System prompt:**
```
You are a helpful assistant that summarizes meeting transcripts.
Extract the key points, decisions, and action items.
```

**User prompt:**
```
Please summarize the following meeting transcript:

{transcript}
```

**What changed:** Nothing — this is the baseline first draft.

**What happened:** The model produced a reasonable summary but the output format varied widely between runs. Sometimes it used bullet points, sometimes paragraphs. Action items were buried in the summary text rather than listed clearly. The model also occasionally skipped the "decisions made" category entirely.

---

## Version 2 — Revision 1: Added Role and a Factuality Constraint

**System prompt:**
```
You are an expert meeting facilitator. Given a raw meeting transcript,
produce a clean, professional summary. Be concise and factual.
Do not add information that was not discussed in the transcript.
```

**User prompt:**
```
Please summarize the following meeting transcript:

{transcript}
```

**What changed:** Added a specific role ("expert meeting facilitator"), the word "concise," and an explicit instruction not to hallucinate ("Do not add information that was not discussed").

**What improved:** The factuality constraint helped on Case 4 (vague transcript) — the model stopped inventing owners and deadlines. Summaries became more professional in tone. However, the output structure was still inconsistent: some runs included action items as a numbered list, others as prose.

**What stayed the same / got worse:** The format was still unpredictable. On Case 5 (complex planning meeting), the model sometimes missed action items because it was summarizing in paragraph form and didn't have an explicit instruction to list every task.

---

## Version 3 — Revision 2: Enforced Structure with Explicit Sections

**System prompt:**
```
You are an expert meeting facilitator and note-taker.
Given a raw meeting transcript, produce a structured summary using
exactly the sections below. Be concise and factual.
If a section has no content, write 'None identified.'
Do not invent owners, deadlines, or details not stated in the transcript.

Sections to include:
1. SUMMARY (2-4 sentences)
2. DECISIONS MADE
3. ACTION ITEMS (format: [Owner] - [Task] - [Deadline if stated])
4. OPEN QUESTIONS / FOLLOW-UPS
```

**User prompt:**
```
Please summarize the following meeting transcript:

{transcript}
```

**What changed:** Added explicit section headings, a required format for action items (`[Owner] - [Task] - [Deadline]`), and the instruction to write "None identified." when a section is empty.

**What improved:** Output is now consistent across all 5 eval cases. Action items are always separated from the summary. The structured format makes it easy to scan the output quickly. On Case 2 (short meeting), the model correctly wrote "None identified." for action items and decisions rather than inventing them. On Case 5, it captured all 5+ action items with correct owners and deadlines.

**What stayed the same / got worse:** The model still struggles slightly with Case 3 (conflicting deadline). It tends to pick one date rather than flagging the conflict explicitly. A future revision could add: "If participants disagree on a fact, note the disagreement rather than resolving it."
