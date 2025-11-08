import sys
from transcription.transcribe_audio import AudioTranscriber
from transcription.format_markdown import MarkdownFormatter


def main() -> None:
    """Transcribes audio files using Parakeet ASR model, then formats the text.

    Usage: python main.py <audio_file>
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py <audio_file>", file=sys.stderr)
        sys.exit(1)

    audio_path = sys.argv[1]

    transcriber = AudioTranscriber()
    transcribed_text = transcriber.transcribe(audio_path)

    formatter = MarkdownFormatter()
    formatted_text = formatter.process_content(transcribed_text)

    print(formatted_text)


if __name__ == "__main__":
    main()
