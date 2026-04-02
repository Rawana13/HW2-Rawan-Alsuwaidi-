# Meeting Transcript Summarizer

A Python prototype that converts raw meeting transcripts into structured summaries and action items using the Claude API.

## Workflow

**Who is the user:** Team leads, project managers, or any professional who runs or attends meetings and needs a quick written record.

**Input:** A plain-text meeting transcript (typed or auto-generated from a recording tool).

**Output:** A structured document containing:
- A concise meeting summary (2–4 sentences)
- Key decisions made during the meeting
- A numbered list of action items with owners and deadlines (when mentioned)
- Any open questions or follow-up items

**Why automate this:** Writing up meeting notes is time-consuming and often delayed or skipped entirely. An automated first-pass summary saves 10–20 minutes per meeting and ensures nothing important is lost. A human reviewer still checks the output before distribution.

## Setup

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your_key_here
```

## Usage

```bash
# Summarize a transcript file
python app.py transcript.txt

# Use a specific prompt version (1, 2, or 3)
python app.py transcript.txt --prompt-version 2

# Save output to a custom file
python app.py transcript.txt --output my_summary.txt
```

Output is saved to `output/summary_<timestamp>.txt` by default and also printed to the terminal.

## Files

| File | Purpose |
|---|---|
| `app.py` | Main Python application |
| `prompts.md` | Prompt versions and iteration notes |
| `eval_set.md` | Evaluation test cases |
| `report.md` | Analysis and findings |
