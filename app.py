"""
Meeting Transcript Summarizer
Usage: python app.py <transcript_file> [--prompt-version 1|2|3] [--output <file>]

Requires: pip install google-generativeai
API key:  export GOOGLE_API_KEY=your_key_from_aistudio.google.com
"""

import argparse
import os
import sys
from datetime import datetime

import google.generativeai as genai

# ---------------------------------------------------------------------------
# Prompt versions (configurable via --prompt-version flag)
# ---------------------------------------------------------------------------

SYSTEM_PROMPTS = {
    1: (
        "You are a helpful assistant that summarizes meeting transcripts. "
        "Extract the key points, decisions, and action items."
    ),
    2: (
        "You are an expert meeting facilitator. Given a raw meeting transcript, "
        "produce a clean, professional summary. Be concise and factual. "
        "Do not add information that was not discussed in the transcript."
    ),
    3: (
        "You are an expert meeting facilitator and note-taker. "
        "Given a raw meeting transcript, produce a structured summary using "
        "exactly the sections below. Be concise and factual. "
        "If a section has no content, write 'None identified.' "
        "Do not invent owners, deadlines, or details not stated in the transcript.\n\n"
        "Sections to include:\n"
        "1. SUMMARY (2-4 sentences)\n"
        "2. DECISIONS MADE\n"
        "3. ACTION ITEMS (format: [Owner] - [Task] - [Deadline if stated])\n"
        "4. OPEN QUESTIONS / FOLLOW-UPS"
    ),
}

USER_PROMPT_TEMPLATE = "Please summarize the following meeting transcript:\n\n{transcript}"

# ---------------------------------------------------------------------------
# Core function
# ---------------------------------------------------------------------------

def summarize_transcript(transcript: str, prompt_version: int = 3) -> str:
    """Call the Gemini API and return the structured meeting summary."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable is not set.", file=sys.stderr)
        print("Get a free key at https://aistudio.google.com and run:", file=sys.stderr)
        print("  export GOOGLE_API_KEY=your_key_here", file=sys.stderr)
        sys.exit(1)

    genai.configure(api_key=api_key)

    system = SYSTEM_PROMPTS[prompt_version]
    user_message = USER_PROMPT_TEMPLATE.format(transcript=transcript)

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=system,
    )

    print(f"[Using prompt version {prompt_version}]")
    print("[Calling Gemini API — streaming response...]\n")

    result_parts = []

    response = model.generate_content(user_message, stream=True)
    for chunk in response:
        text = chunk.text
        print(text, end="", flush=True)
        result_parts.append(text)

    print("\n")
    return "".join(result_parts)


# ---------------------------------------------------------------------------
# Save output
# ---------------------------------------------------------------------------

def save_output(summary: str, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"[Saved to {output_path}]")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Summarize a meeting transcript using Gemini.")
    parser.add_argument("transcript_file", help="Path to the plain-text transcript file")
    parser.add_argument(
        "--prompt-version",
        type=int,
        choices=[1, 2, 3],
        default=3,
        help="Prompt version to use (1=basic, 2=improved, 3=structured). Default: 3",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path. Default: output/summary_<timestamp>.txt",
    )
    args = parser.parse_args()

    # Read transcript
    if not os.path.isfile(args.transcript_file):
        print(f"Error: File not found: {args.transcript_file}", file=sys.stderr)
        sys.exit(1)

    with open(args.transcript_file, "r", encoding="utf-8") as f:
        transcript = f.read().strip()

    if not transcript:
        print("Error: Transcript file is empty.", file=sys.stderr)
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join("output", f"summary_{timestamp}.txt")

    # Run
    summary = summarize_transcript(transcript, prompt_version=args.prompt_version)
    save_output(summary, output_path)


if __name__ == "__main__":
    main()
