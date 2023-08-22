from math import ceil

import librosa as la

from speech2text.config import get_config
from speech2text.model import SpeechToText


def audio_transcript(audio_file_path: str, frames_batch_size: int = 10):
    asr_model = SpeechToText(get_config().whisper_path)
    sr_resampled = 16000
    audio, sr = la.load(audio_file_path)
    audio_resampled = la.resample(audio, orig_sr=sr, target_sr=sr_resampled)

    # Calculate the frame size and frame overlap
    frame_size = int(sr_resampled * 30)  # 5 second frames
    hop_length = int(frame_size / 2)  # 50% overlap

    # Break the audio into frames
    audio_frames = la.util.frame(
        audio_resampled, frame_length=frame_size, hop_length=hop_length
    ).transpose()

    for i in range(ceil(len(audio_frames) / frames_batch_size)):
        batch = audio_frames[
            i * frames_batch_size : i * frames_batch_size + frames_batch_size
        ]
        transcripts = asr_model.generate_transcript(
            asr_model.featurize_audio_batch(batch, sr_resampled)
        )

        for j, _ in enumerate(transcripts):
            frame_start = (i * (j + 1) + j) * frame_size / 2 / sr_resampled
            frame_end = frame_start + frame_size / sr_resampled
            print(f">> {frame_start}s - {frame_end}s:")
            print("\n" + transcripts[j].strip())
            print("\n------------------------------------\n")


if __name__ == "__main__":
    audio_file_path = (
        "audio_sample/AI_Images_Last_Week_Tonight_with_John_Oliver_(HBO).mp3"
    )
    audio_transcript(audio_file_path)
