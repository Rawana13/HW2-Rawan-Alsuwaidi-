# Meeting Summarizer

A Python application that records audio from your microphone, transcribes it locally using Whisper, and generates a structured meeting summary using Google Gemini.

## Workflow

**Who is the user:** Team leads, project managers, or any professional who runs or attends meetings and needs a quick written record.

**Input:** Live audio recorded from your microphone during or immediately after a meeting.

**Output:** A structured document saved to `output.txt` containing:
- A concise meeting summary (2–3 sentences)
- Key highlights and decisions made
- A checklist of action items with owners and deadlines (when mentioned)
- Notes flagging anything unclear or requiring human review

**Why automate this:** Writing up meeting notes is time-consuming and often delayed or skipped entirely. This tool records, transcribes, and summarizes in one step — saving 15–20 minutes per meeting while keeping a human reviewer in the loop before distribution.

## Setup

```bash
pip install sounddevice soundfile openai-whisper google-generativeai numpy
```

Set your Gemini API key directly in `app.py`:

```python
GEMINI_API_KEY = "your_key_here"
```

Get a free key at: https://aistudio.google.com

## Usage

```bash
python app.py
```

1. The microphone starts immediately — begin speaking.
2. Press **Enter** when the meeting (or recording) is done.
3. Whisper transcribes the audio locally (first run downloads the model, ~140MB).
4. The summary is printed to the terminal and saved to `output.txt`.

## Files

| File | Purpose |
|---|---|
| `app.py` | Main application — records, transcribes, and summarizes |
| `prompts.md` | Prompt versions and iteration notes |
| `eval_set.md` | Evaluation test cases (read aloud to test) |
| `report.md` | Analysis and findings |
| `meeting_audio.wav` | Last recorded audio (created at runtime) |
| `output.txt` | Last summary output (created at runtime) |
