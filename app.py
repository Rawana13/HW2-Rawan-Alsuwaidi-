"""
Meeting Summarizer
------------------
Records audio from your microphone, transcribes it with Whisper,
and summarizes it using Google Gemini.

How to run:
    python app.py

Press Enter to stop the recording.
The summary is printed to the screen and saved to output.txt.
"""

import sounddevice as sd        # records audio from your microphone
import soundfile as sf          # saves audio to a .wav file
import whisper                  # converts speech to text (runs locally)
import google.generativeai as genai  # sends text to Google Gemini
import numpy as np              # handles the raw audio data
import threading                # lets us record while waiting for user input

# ----------------------------------------------------------------
# CONFIGURATION — put your Gemini API key here
# ----------------------------------------------------------------
GEMINI_API_KEY = "AIzaSyC4cUJEz5oR0ZTCv_Aac8aZbqngSq791bI"

# Whisper model size: "tiny", "base", "small", "medium", "large"
# "base" is a good balance of speed and accuracy for most computers
WHISPER_MODEL = "base"

# Audio settings
SAMPLE_RATE = 44100   # standard audio quality (44,100 samples per second)
CHANNELS = 1          # mono audio (one microphone channel)
AUDIO_FILE = "meeting_audio.wav"
OUTPUT_FILE = "output.txt"

# ----------------------------------------------------------------
# THE PROMPT — this is what we send to Gemini along with the transcript
# This is Revision 2 of the prompt (see prompts.md for full history)
# ----------------------------------------------------------------
SYSTEM_PROMPT = """You are a professional meeting assistant. Your job is to analyze meeting transcripts and produce clear, structured summaries for busy professionals.

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
Flag anything that was unclear in the transcript, any names that seemed uncertain, or any action items that lacked enough detail to be actionable.

Be concise and professional. Do not add information that was not in the transcript."""


# ----------------------------------------------------------------
# STEP 1: RECORD AUDIO
# ----------------------------------------------------------------
def record_audio():
    """
    Records audio from the microphone until the user presses Enter.
    Returns the recorded audio as a numpy array.
    """
    print("\n" + "="*50)
    print("  MEETING SUMMARIZER")
    print("="*50)
    print("\nMicrophone is ON. Start speaking...")
    print("Press ENTER when you are done.\n")

    # This list will collect chunks of audio as they come in
    audio_chunks = []
    recording = True

    def audio_callback(indata, frames, time, status):
        # This function is called automatically every time new audio arrives
        # indata is a small chunk of audio — we just append it to our list
        if recording:
            audio_chunks.append(indata.copy())

    # Start recording in the background
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=audio_callback):
        input()  # wait here until user presses Enter

    recording = False
    print("Recording stopped.")

    # Combine all the small chunks into one long audio array
    audio_data = np.concatenate(audio_chunks, axis=0)
    return audio_data


# ----------------------------------------------------------------
# STEP 2: SAVE AUDIO TO FILE
# ----------------------------------------------------------------
def save_audio(audio_data):
    """Saves the recorded audio to a .wav file so Whisper can read it."""
    sf.write(AUDIO_FILE, audio_data, SAMPLE_RATE)
    print(f"Audio saved to: {AUDIO_FILE}")


# ----------------------------------------------------------------
# STEP 3: TRANSCRIBE WITH WHISPER
# ----------------------------------------------------------------
def transcribe_audio():
    """
    Loads the Whisper model and converts the audio file to text.
    The first time this runs it downloads the model (~140MB).
    """
    print(f"\nLoading Whisper model ({WHISPER_MODEL})...")
    print("(First run will download the model — this is a one-time step)\n")

    model = whisper.load_model(WHISPER_MODEL)

    print("Transcribing audio... (this may take 30-60 seconds)")
    result = model.transcribe(AUDIO_FILE)
    transcript = result["text"].strip()

    print("\nTranscript complete.")
    print("-" * 40)
    print(transcript)
    print("-" * 40)

    return transcript


# ----------------------------------------------------------------
# STEP 4: SUMMARIZE WITH GOOGLE GEMINI
# ----------------------------------------------------------------
def summarize_transcript(transcript):
    """
    Sends the transcript to Google Gemini and returns the structured summary.
    """
    print("\nSending transcript to Google Gemini...")

    # Set up the Gemini API with your key
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Build the full message: system prompt + the actual transcript
    full_prompt = SYSTEM_PROMPT + "\n\n---\n\nMEETING TRANSCRIPT:\n" + transcript

    response = model.generate_content(full_prompt)
    summary = response.text

    return summary


# ----------------------------------------------------------------
# STEP 5: SAVE AND DISPLAY OUTPUT
# ----------------------------------------------------------------
def save_output(transcript, summary):
    """Prints the summary to the screen and saves everything to output.txt."""

    output = f"""MEETING SUMMARIZER — OUTPUT
{'='*50}

{summary}

{'='*50}
RAW TRANSCRIPT
{'='*50}
{transcript}
"""

    # Print to screen
    print("\n" + "="*50)
    print("  SUMMARY")
    print("="*50)
    print(summary)

    # Save to file
    with open(OUTPUT_FILE, "w") as f:
        f.write(output)

    print(f"\nFull output saved to: {OUTPUT_FILE}")


# ----------------------------------------------------------------
# MAIN — runs all the steps in order
# ----------------------------------------------------------------
def main():
    if GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        print("ERROR: Please open app.py and replace YOUR_API_KEY_HERE with your actual Gemini API key.")
        print("Get a free key at: https://aistudio.google.com")
        return

    # Run the pipeline
    audio_data = record_audio()
    save_audio(audio_data)
    transcript = transcribe_audio()
    summary = summarize_transcript(transcript)
    save_output(transcript, summary)


if __name__ == "__main__":
    main()
