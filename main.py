import nemo.collections.asr as nemo_asr
import torch

# Load Parakeet TDT model from Hugging Face or local checkpoint
model = nemo_asr.models.ASRModel.from_pretrained("nvidia/parakeet-tdt-0.6b-v3")

# Ensure inference on CPU
device = torch.device("cpu")
model.to(device)

# Audio file path (.wav or .flac recommended)
audio_path = "longform.wav"

# Long form audio only, limit context
model.change_attention_model(
    self_attention_model="rel_pos_local_attn", att_context_size=[256, 256]
)
from pydub import AudioSegment


def split_audio(input_path, chunk_ms=100000):
    audio = AudioSegment.from_file(input_path)
    chunks = [audio[i : i + chunk_ms] for i in range(0, len(audio), chunk_ms)]
    for idx, chunk in enumerate(chunks):
        chunk.export(f"chunk_{idx}.wav", format="wav")
    return [f"chunk_{idx}.wav" for idx in range(len(chunks))]


# Then transcribe each chunk in a loop using Parakeet
# Transcribe - offline, no GPU required
audios = split_audio("longform.wav")
results = model.transcribe(audios[:2])

for result in results:
    print(25 * "=")
    print(result.text)
    print(25 * "=")
