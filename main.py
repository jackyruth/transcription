import nemo.collections.asr as nemo_asr
from pydub import AudioSegment
from format_markdown import process_markdown_file
import torch
import sys


def split_audio(input_path: str, chunk_ms: int = 100000) -> list[str]:
    """
    Split an audio file into smaller chunks for processing.

    Args:
        input_path: Path to the input audio file
        chunk_ms: Length of each chunk in milliseconds

    Returns:
        List of paths to the generated audio chunks
    """
    import os

    chunk_dir = ".chunks"
    os.makedirs(chunk_dir, exist_ok=True)

    audio = AudioSegment.from_file(input_path)
    chunks = [audio[i : i + chunk_ms] for i in range(0, len(audio), chunk_ms)]
    chunk_paths = []
    for idx, chunk in enumerate(chunks):
        chunk_path = os.path.join(chunk_dir, f"chunk_{idx}.wav")
        chunk.export(chunk_path, format="wav")
        chunk_paths.append(chunk_path)
    return chunk_paths


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
    MODEL = r"nvidia/parakeet-tdt-0.6b-v3"
    PROCESSOR = r"cpu"
    OUTPUT_FILE = r"transcribed_audio.md"

    model = nemo_asr.models.ASRModel.from_pretrained(MODEL)
    device = torch.device(PROCESSOR)
    model.to(device)

    if len(sys.argv) < 2:
        print("Usage: python main.py <audio_file>")
        sys.exit(1)

    audio_path = sys.argv[1]

    # Limit context to save ram. Untested.
    model.change_attention_model(
        self_attention_model="rel_pos_local_attn", att_context_size=[256, 256]
    )

    # Transcribe - offline, no GPU required
    audios = split_audio(audio_path)
    results = model.transcribe(audios)

    # Combine results and save to markdown file
    combined_text = "".join([result.text for result in results])
    with open(OUTPUT_FILE, "w") as f:
        f.write(combined_text)

    process_markdown_file(OUTPUT_FILE, OUTPUT_FILE)
    print("Finished transcription")


if __name__ == "__main__":
    main()
