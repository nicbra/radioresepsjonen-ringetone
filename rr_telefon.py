import numpy as np
import wave

filename= "rr_telefon.wav"
sample_rate = 44100

freqs = [804, 1075, 1343]
volumes = [0.55, 0.55, 0.55]
tone_ms = 50
repeats = 7
silence_seconds = 2

samples_per_tone = int(sample_rate * tone_ms / 1000)


def create_tone(frequency, volume):
    if not hasattr(create_tone, "phase"):
        create_tone.phase = 0.0
    t = np.arange(samples_per_tone) / sample_rate
    tone = np.empty(samples_per_tone)

    phase_increment = 2 * np.pi * frequency / sample_rate

    for i in range(samples_per_tone):
            tone[i] = np.sin(create_tone.phase)
            create_tone.phase += phase_increment

    # keep phase bounded
    create_tone.phase %= 2 * np.pi

    return tone

def main():

    audio = []

    for _ in range(repeats):
        for i, freq in enumerate(freqs):
            tone = create_tone(freq, volumes[i])
            audio.append(tone * volumes[i])

    # end with a low tone:
    tone =  create_tone(freqs[0], volumes[0])
    audio.append(tone * volumes[0])


    audio = np.concatenate(audio)

    silence_samples = int(sample_rate * silence_seconds)
    audio = np.concatenate([
        audio,
        np.zeros(silence_samples)
    ])

    audio_int16 = np.int16(audio * 32767)

    with wave.open(filename, "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(audio_int16.tobytes())

    print("Wrote %s" % filename)

if __name__ == "__main__":
    main()