from kittentts import KittenTTS
import soundfile as sf

# Use repo_id to load from cache
m = KittenTTS("KittenML/kitten-tts-nano-0.1")

# Generate audio
audio = m.generate("Oh no, did I forget to save the output? Let’s try again!", voice='expr-voice-4-m')

# Save the audio
sf.write('output.wav', audio, 24000)
print("Audio saved as output.wav")