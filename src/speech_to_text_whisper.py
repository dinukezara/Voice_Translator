from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np
import tempfile
import wave

class WhisperSTT:
    def __init__(self):
        self.model = WhisperModel("base", compute_type="int8")

    def record_audio(self, duration=5, sample_rate=16000):
        print("Recording...")
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
        sd.wait()
        return audio, sample_rate

    def save_wav(self, audio, sample_rate):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        with wave.open(temp_file.name, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes((audio * 32767).astype(np.int16))
        return temp_file.name

    def transcribe(self):
        audio, sr = self.record_audio()
        file_path = self.save_wav(audio, sr)

        segments, info = self.model.transcribe(file_path)

        text = ""
        for segment in segments:
            text += segment.text

        return {
            "success": True,
            "text": text.strip(),
            "language": info.language
        }