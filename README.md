# Transcription 

Easy-to-use transcription application via the [parakeet model](https://parakeettdt.com/).

Features: 
1.  Easy to use.
1.  Offline inference.
1.  Low compute requirements.

## Usage

Run `python main.py <audio_file>` to transcribe the audio into text.
The text is stored in a markdown file called `transcribed_audio.md`.

Audio files must be in `.wav` format. 
You can use FFmpeg to convert between audio files.

```bash
ffmpeg -i audio.mp4 audio.wav
```

## Installation

Install python 3.13, then run 
```bash 
pip install -r requirements.txt
```
