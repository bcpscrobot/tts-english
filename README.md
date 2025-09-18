Setting Up KittenTTS on Raspberry Pi 5: A Complete Guide with Troubleshooting
This guide outlines the process of installing and running the KittenTTS model (KittenML/kitten-tts-nano-0.1) on a Raspberry Pi 5 from scratch, using Raspberry Pi OS (Bookworm, 64-bit). It includes all troubleshooting steps for issues encountered, such as DNS resolution errors, incomplete Git LFS cloning, and KittenTTS API mismatches. The setup was tested on a Raspberry Pi 5 with 4GB/8GB RAM, and the model generates audio at ~10-15 words/second.
Prerequisites

Hardware:
Raspberry Pi 5 (4GB or 8GB RAM).
MicroSD card (32GB+ Class 10, e.g., SanDisk Extreme).
MicroSD card reader.
USB-C power supply (5V/5A official recommended).
HDMI cable, monitor, keyboard/mouse (optional for headless setup).
Ethernet cable or Wi-Fi for internet access.


Software:
Raspberry Pi OS (64-bit, Bookworm).
Internet connection for initial setup.
Terminal access (via SSH or local).



Step 1: Install Raspberry Pi OS

Download Raspberry Pi Imager from raspberrypi.com/software on a computer.
Flash the OS:
Insert the microSD card.
In Imager, select Raspberry Pi 5, choose Raspberry Pi OS (64-bit) (full or lite).
Configure advanced settings (optional):
Enable SSH.
Set hostname (e.g., bcpscRobot), username (bcpsc), password.
Configure Wi-Fi.


Write to the microSD card (takes ~5-10 minutes).


Boot the Pi:
Insert the microSD card into the Pi 5, connect power, and boot.
If using the desktop, complete the setup wizard (locale, updates).
Update the system:sudo apt update && sudo apt upgrade -y
sudo reboot





Step 2: Set Up Python Environment

Install dependencies:sudo apt install python3-pip python3-venv python3-dev git git-lfs -y


Create a project directory and virtual environment:mkdir ~/Codes/TTS
cd ~/Codes/TTS
python3 -m venv kitten-env
source kitten-env/bin/activate


Install required Python packages:pip install soundfile torch onnxruntime huggingface_hub espeakng_loader misaki num2words numpy spacy --index-url https://download.pytorch.org/whl/cpu



Step 3: Install KittenTTS

Install the kittentts package:pip install https://github.com/KittenML/KittenTTS/releases/download/0.1/kittentts-0.1.0-py3-none-any.whl


This installs version 0.1.0, which uses ~25 MB for the model and dependencies.


Verify installation:python -c "from kittentts import KittenTTS; print('Installed successfully!')"



Step 4: Clone the Model Files

Clone the model repository:cd ~/Codes/TTS
git clone https://huggingface.co/KittenML/kitten-tts-nano-0.1
cd kitten-tts-nano-0.1
git lfs pull


This downloads config.json (177 B), kitten_tts_nano_v0_1.onnx (23.8 MB), voices.npz (11 KB), and README.md (1.2 KB).


Verify file sizes:ls -lh


Expected output:total 23M
-rw-r--r-- 1 bcpsc bcpsc  177 Sep 17 21:37 config.json
-rw-r--r-- 1 bcpsc bcpsc  23M Sep 17 21:37 kitten_tts_nano_v0_1.onnx
-rw-r--r-- 1 bcpsc bcpsc 1.2K Sep 17 21:37 README.md
-rw-r--r-- 1 bcpsc bcpsc  11K Sep 17 21:37 voices.npz





Step 5: Run the KittenTTS Model

Create and run the script:Create run_tts.py:nano ~/Codes/TTS/run_tts.py

Add:from kittentts import KittenTTS
import soundfile as sf

# Use repo_id to load from cache
m = KittenTTS("KittenML/kitten-tts-nano-0.1")

# Generate audio
audio = m.generate("This high quality TTS model works without a GPU", voice='expr-voice-2-f')

# Save the audio
sf.write('output.wav', audio, 24000)
print("Audio saved as output.wav")


Move model files to Hugging Face cache (to avoid downloading):mkdir -p ~/.cache/huggingface/hub/models--KittenML--kitten-tts-nano-0.1/snapshots/main
cp ~/Codes/TTS/kitten-tts-nano-0.1/* ~/.cache/huggingface/hub/models--KittenML--kitten-tts-nano-0.1/snapshots/main/


Run the script:source ~/Codes/TTS/kitten-env/bin/activate
python ~/Codes/TTS/run_tts.py


Play the output:aplay output.wav


Install ALSA if needed:sudo apt install alsa-utils -y





Troubleshooting Issues Encountered
Issue 1: DNS Resolution Error

Error:When running run_tts.py with m = KittenTTS("KittenML/kitten-tts-nano-0.2"), a DNS error occurred:socket.gaierror: [Errno -3] Temporary failure in name resolution
...
huggingface_hub.errors.LocalEntryNotFoundError: An error happened while trying to locate the file on the Hub...

This was caused by the Pi failing to resolve huggingface.co due to network/DNS issues.
Resolution:
Tested connectivity:ping 8.8.8.8
nslookup huggingface.co


Set public DNS servers:sudo nano /etc/resolv.conf

Added:nameserver 8.8.8.8
nameserver 8.8.4.4


Restarted networking:sudo systemctl restart systemd-resolved


Used local model files to avoid network dependency (see Step 4).



Issue 2: Incomplete Git Clone (~2 MB Instead of Full Files)

Error:Cloning https://huggingface.co/KittenML/kitten-tts-nano-0.1 downloaded only 2 MB, with kitten_tts_nano_v0_1.onnx and voices.npz as small LFS pointer files (128 bytes) instead of their full sizes (~23.8 MB and ~11 KB).
Cause:Git LFS was not properly set up, so only pointer files were fetched.
Resolution:
Installed Git LFS:sudo apt install git-lfs -y
git lfs install


Fetched LFS files:cd ~/Codes/TTS/kitten-tts-nano-0.1
git lfs pull


Verified file sizes:ls -lh


If git lfs pull failed silently, ensured authentication:export HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
git lfs pull


Re-cloned if necessary:cd ~/Codes/TTS
rm -rf kitten-tts-nano-0.1
git clone https://huggingface.co/KittenML/kitten-tts-nano-0.1
cd kitten-tts-nano-0.1
git lfs pull





Issue 3: KittenTTS API Mismatch (local_path Error)

Error:Running run_tts.py with m = KittenTTS(local_path="/home/bcpsc/Codes/TTS/kitten-tts-nano-0.1") failed:TypeError: KittenTTS.__init__() got an unexpected keyword argument 'local_path'

The kittentts package (version 0.1.0) does not support local_path.
Cause:The package expects a repo_id (e.g., "KittenML/kitten-tts-nano-0.1") and downloads from Hugging Face, not local files.
Resolution:
Moved model files to the Hugging Face cache:mkdir -p ~/.cache/huggingface/hub/models--KittenML--kitten-tts-nano-0.1/snapshots/main
cp ~/Codes/TTS/kitten-tts-nano-0.1/* ~/.cache/huggingface/hub/models--KittenML--kitten-tts-nano-0.1/snapshots/main/


Updated run_tts.py to use repo_id:m = KittenTTS("KittenML/kitten-tts-nano-0.1")


Checked for package updates:pip show kittentts


Confirmed version 0.1.0. No newer releases found at github.com/KittenML/KittenTTS/releases.


Ensured dependencies:pip install torch soundfile onnxruntime huggingface_hub espeakng_loader misaki num2words numpy spacy --index-url https://download.pytorch.org/whl/cpu





Step 6: Test with Different Texts and Voices

Create a test script:Edit run_tts.py:from kittentts import KittenTTS
import soundfile as sf

# Initialize model
m = KittenTTS("KittenML/kitten-tts-nano-0.1")

# Test texts and voices
test_texts = [
    "Hello, welcome to KittenTTS on Raspberry Pi!",
    "Hey there! How’s it going? I’m just testing this awesome TTS model.",
    "The Raspberry Pi 5 processes this TTS model with a 2.4 GHz quad-core CPU.",
    "Wow, this is so exciting! I love how clear my voice sounds!"
]
test_voices = ["expr-voice-2-f", "expr-voice-2-m", "default"]

# Generate audio for each combination
for i, text in enumerate(test_texts):
    for voice in test_voices:
        try:
            print(f"Generating audio for text {i+1} with voice: {voice}")
            audio = m.generate(text, voice=voice)
            output_file = f"output_text{i+1}_voice_{voice}.wav"
            sf.write(output_file, audio, 24000)
            print(f"Saved as {output_file}")
        except Exception as e:
            print(f"Error with voice {voice} for text {i+1}: {e}")


Run and play:python ~/Codes/TTS/run_tts.py
aplay output_text1_voice_expr-voice-2-f.wav



Additional Tips

Performance: Generation takes ~1-2 seconds per short sentence. Use a fan/heatsink for long runs.
Memory: If memory issues occur, add swap:sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile


Audio issues: Test with:speaker-test -t wav


Upgrading to 0.2: If needed, clone kitten-tts-nano-0.2 and repeat the cache setup:cd ~/Codes/TTS
git clone https://huggingface.co/KittenML/kitten-tts-nano-0.2
cd kitten-tts-nano-0.2
git lfs pull



Conclusion
This guide provides a complete setup for KittenTTS on Raspberry Pi 5, addressing DNS issues, Git LFS cloning problems, and API mismatches. The model runs offline using local files, producing high-quality audio suitable for low-resource devices.
For further help, check github.com/KittenML/KittenTTS or share error logs.
