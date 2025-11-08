# Transcription 

Easy-to-use transcription application via the [parakeet model](https://parakeettdt.com/).

Features: 
1.  Easy to use.
1.  Offline inference.
1.  Low compute requirements.

## Usage

Run `python main.py <audio_file>` to transcribe the audio into text streamed to
stdout.

The text is formatted so that each sentence is on its own line, with line breaks
if the line goes over a certain column number (set to 80).

Try it out with the supplied audio clip `sample.wav`.

```bash
python main.py sample.wav | tee output.md
```

## Installation

Install dependencies with `poetry install`.
