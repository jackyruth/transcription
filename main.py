import sys
from transcription.transcribe_audio import AudioTranscriber
from transcription.format_markdown import MarkdownFormatter


def main() -> None:
    """
    Main function to transcribe audio files using Parakeet ASR model.

    Processes an audio file by:
    1. Splitting into manageable chunks
    2. Transcribing each chunk using the Parakeet model
    3. Combining results into a markdown file
    4. Formatting the markdown output

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
