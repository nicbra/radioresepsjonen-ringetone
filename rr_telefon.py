import numpy as np
import wave

sample_rate = 44100

freqs = [804, 1075, 1343]
volumes = [0.25, 0.25, 0.55]
tone_ms = 50
repeats = 7
silence_seconds = 2

samples_per_tone = int(sample_rate * tone_ms / 1000)

audio = []

for _ in range(repeats):
    for i, freq in enumerate(freqs):
        t = np.arange(samples_per_tone) / sample_rate
        tone = np.sin(2 * np.pi * freq * t)

        # tiny fade
        fade_ms = 10
        fade_len = int(sample_rate * fade_ms / 1000)
        fade = np.ones_like(tone)
        fade[-fade_len:] = np.linspace(1, 0, fade_len)

        audio.append(tone * fade*  volumes[i])


audio = np.concatenate(audio)

silence_samples = int(sample_rate * silence_seconds)
audio = np.concatenate([
    audio,
    np.zeros(silence_samples)
])

audio_int16 = np.int16(audio * 32767)

with wave.open("rr_telefon.wav", "w") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(sample_rate)
    wav.writeframes(audio_int16.tobytes())

print("Wrote rr_telefon.wav")