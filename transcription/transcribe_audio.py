import logging

logging.disable(
    logging.CRITICAL
)  # Disables all logging to prevent logs being sent to stdout
import nemo.collections.asr as nemo_asr
from pydub import AudioSegment
import torch
import os


class AudioTranscriber:
    """
    Transcribes audio files using the Parakeet ASR model.

    Processes an audio file by:
    1. Preprocessing the audio to adhere to model input requirements
    2. Splitting the audio into chunks to save on context
    3. Transcribing each chunk using the Parakeet model
    """

    def __init__(
        self, model_name: str = "nvidia/parakeet-tdt-0.6b-v3", processor: str = "cpu"
    ) -> None:
        """
        Initialize the AudioTranscriber with model configuration.

        Args:
            model_name: Name of the ASR model to use
            processor: Device to run the model on ("cpu" or "cuda")
        """
        self.model_name = model_name
        self.processor = processor
        self.model = None
        self.device = None

    def _initialize_model(self) -> None:
        """Initialize the ASR model and move it to the specified device."""
        if self.model is None:
            self.model = nemo_asr.models.ASRModel.from_pretrained(self.model_name)
            self.device = torch.device(self.processor)
            self.model.to(self.device)

            # Limit context to save RAM
            self.model.change_attention_model(
                self_attention_model="rel_pos_local_attn", att_context_size=[256, 256]
            )

    def _process_audio(self, input_path: str) -> AudioSegment:
        """
        Prepare audio for input into the ASR model.

        The expected input format is 16kHz monochannel audio in `.wav` format.

        Args:
            input_path: Path to the input audio file

        Returns:
            Processed AudioSegment object
        """
        audio = AudioSegment.from_file(input_path)

        # Pre-process audio to match model requirements
        if audio.channels > 1:
            audio = audio.set_channels(1)  # Convert to mono
        if audio.frame_rate != 16000:
            audio = audio.set_frame_rate(16000)  # Resample to 16kHz

        return audio

    def _split_audio(self, input_path: str, chunk_ms: int = 100000) -> list[str]:
        """
        Split an audio file into smaller chunks for processing.
        Pre-processes audio to match model requirements: 16kHz mono.

        Args:
            input_path: Path to the input audio file
            chunk_ms: Length of each chunk in milliseconds

        Returns:
            List of paths to the generated audio chunks
        """
        chunk_dir = ".chunks"
        os.makedirs(chunk_dir, exist_ok=True)

        audio = self._process_audio(input_path)
        chunks = [audio[i : i + chunk_ms] for i in range(0, len(audio), chunk_ms)]
        chunk_paths = []
        for idx, chunk in enumerate(chunks):
            chunk_path = os.path.join(chunk_dir, f"chunk_{idx}.wav")
            chunk.export(chunk_path, format="wav")
            chunk_paths.append(chunk_path)
        return chunk_paths

    def transcribe(self, audio_path: str) -> None:
        """Transcribes an audio file.

        Args:
            audio_path: Path to the input audio file
        """
        self._initialize_model()

        # Split audio into chunks and transcribe
        audios = self._split_audio(audio_path)
        results = self.model.transcribe(audios)

        # Combine results
        combined_text = "".join([result.text for result in results])
        return combined_text
