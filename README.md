# 🚀 KittenTTS on Raspberry Pi 5: A Step-by-Step Guide with Troubleshooting

Welcome to this comprehensive guide for setting up and running the **KittenTTS** model (`KittenML/kitten-tts-nano-0.1`) on a **Raspberry Pi 5** from scratch using **Raspberry Pi OS (Bookworm, 64-bit)**. KittenTTS is an ultra-lightweight text-to-speech (TTS) model (~25 MB) designed for CPU-only devices, making it ideal for the Pi 5. This guide covers the full setup process, including all troubleshooting steps for issues encountered, such as DNS errors, incomplete Git LFS cloning, and API mismatches. By the end, you’ll have a working TTS system generating audio at ~10-15 words/second.

---

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Step 1: Install Raspberry Pi OS](#step-1-install-raspberry-pi-os)
- [Step 2: Set Up Python Environment](#step-2-set-up-python-environment)
- [Step 3: Install KittenTTS](#step-3-install-kittentts)
- [Step 4: Clone Model Files](#step-4-clone-model-files)
- [Step 5: Run KittenTTS](#step-5-run-kittentts)
- [Troubleshooting](#troubleshooting)
  - [DNS Resolution Error](#issue-1-dns-resolution-error)
  - [Incomplete Git Clone (~2 MB)](#issue-2-incomplete-git-clone-2-mb)
  - [`KittenTTS` API Mismatch (`local_path` Error)](#issue-3-kittentts-api-mismatch-local_path-error)
- [Step 6: Test with Sample Texts and Voices](#step-6-test-with-sample-texts-and-voices)
- [Tips and Tricks](#tips-and-tricks)
- [Conclusion](#conclusion)

---

## 📦 Prerequisites

Before starting, ensure you have the following:

| **Category** | **Details** |
|--------------|-------------|
| **Hardware** | - Raspberry Pi 5 (4GB or 8GB RAM)<br>- MicroSD card (32GB+ Class 10, e.g., SanDisk Extreme)<br>- MicroSD card reader<br>- USB-C power supply (5V/5A official)<br>- HDMI cable, monitor, keyboard/mouse (optional for headless)<br>- Ethernet or Wi-Fi |
| **Software** | - Raspberry Pi OS (64-bit, Bookworm)<br>- Internet connection for setup<br>- Terminal access (SSH or local) |

---

## 🖥️ Step 1: Install Raspberry Pi OS

1. **Download Raspberry Pi Imager**:
   - Get it from [raspberrypi.com/software](https://www.raspberrypi.com/software/) on a computer.
   - Install and launch the Imager.

2. **Flash the OS**:
   - Insert the microSD card.
   - In Imager:
     - Select **Raspberry Pi 5**.
     - Choose **Raspberry Pi OS (64-bit)** (full for desktop, lite for headless).
     - Click the gear icon to configure:
       - Enable SSH.
       - Set hostname (e.g., `bcpscRobot`), username (`bcpsc`), password.
       - Configure Wi-Fi (if needed).
     - Write to the microSD card (~5-10 minutes).

3. **Boot the Pi**:
   - Insert the microSD card into the Pi 5, connect power, and boot.
   - Complete the setup wizard if using the desktop (locale, updates).
   - Update the system:
     ```bash
     sudo apt update && sudo apt upgrade -y
     sudo reboot
     ```

---

## 🐍 Step 2: Set Up Python Environment

1. **Install essential packages**:
   ```bash
   sudo apt install python3-pip python3-venv python3-dev git git-lfs -y
   ```

2. **Create a project directory and virtual environment**:
   ```bash
   mkdir ~/Codes/TTS
   cd ~/Codes/TTS
   python3 -m venv kitten-env
   source kitten-env/bin/activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install soundfile torch onnxruntime huggingface_hub espeakng_loader misaki num2words numpy spacy --index-url https://download.pytorch.org/whl/cpu
   ```

---

## 🔧 Step 3: Install KittenTTS

1. **Install the `kittentts` package** (version 0.1.0):
   ```bash
   pip install https://github.com/KittenML/KittenTTS/releases/download/0.1/kittentts-0.1.0-py3-none-any.whl
   ```

2. **Verify installation**:
   ```bash
   python -c "from kittentts import KittenTTS; print('Installed successfully!')"
   ```
   - If no errors, the package is ready.

---

## 📥 Step 4: Clone Model Files

1. **Clone the model repository**:
   ```bash
   cd ~/Codes/TTS
   git clone https://huggingface.co/KittenML/kitten-tts-nano-0.1
   cd kitten-tts-nano-0.1
   git lfs pull
   ```
   - Downloads: `config.json` (~177 B), `kitten_tts_nano_v0_1.onnx` (~23.8 MB), `voices.npz` (~11 KB), `README.md` (~1.2 KB).

2. **Verify file sizes**:
   ```bash
   ls -lh
   ```
   - Expected output:
     ```
     total 23M
     -rw-r--r-- 1 bcpsc bcpsc  177 Sep 17 21:37 config.json
     -rw-r--r-- 1 bcpsc bcpsc  23M Sep 17 21:37 kitten_tts_nano_v0_1.onnx
     -rw-r--r-- 1 bcpsc bcpsc 1.2K Sep 17 21:37 README.md
     -rw-r--r-- 1 bcpsc bcpsc  11K Sep 17 21:37 voices.npz
     ```

---

## 🎙️ Step 5: Run KittenTTS

1. **Create the script**:
   ```bash
   nano ~/Codes/TTS/run_tts.py
   ```
   Add:
   ```python
   from kittentts import KittenTTS
   import soundfile as sf

   # Use repo_id to load from cache
   m = KittenTTS("KittenML/kitten-tts-nano-0.1")

   # Generate audio
   audio = m.generate("This high quality TTS model works without a GPU", voice='expr-voice-2-f')

   # Save the audio
   sf.write('output.wav', audio, 24000)
   print("Audio saved as output.wav")
   ```

2. **Move model files to Hugging Face cache**:
   To avoid downloading, place files in the cache:
   ```bash
   mkdir -p ~/.cache/huggingface/hub/models--KittenML--kitten-tts-nano-0.1/snapshots/main
   cp ~/Codes/TTS/kitten-tts-nano-0.1/* ~/.cache/huggingface/hub/models--KittenML--kitten-tts-nano-0.1/snapshots/main/
   ```

3. **Run the script**:
   ```bash
   source ~/Codes/TTS/kitten-env/bin/activate
   python ~/Codes/TTS/run_tts.py
   ```

4. **Play the output**:
   ```bash
   aplay output.wav
   ```
   - Install ALSA if needed:
     ```bash
     sudo apt install alsa-utils -y
     ```

---

## 🛠️ Troubleshooting

### Issue 1: DNS Resolution Error
- **Problem**:
  Running `run_tts.py` with `m = KittenTTS("KittenML/kitten-tts-nano-0.2")` failed due to a DNS error:
  ```plaintext
  socket.gaierror: [Errno -3] Temporary failure in name resolution
  ...
  huggingface_hub.errors.LocalEntryNotFoundError: An error happened while trying to locate the file on the Hub...
  ```
  The Pi couldn’t resolve `huggingface.co` due to network/DNS issues.

- **Solution**:
  1. Tested connectivity:
     ```bash
     ping 8.8.8.8
     nslookup huggingface.co
     ```
  2. Set public DNS servers:
     ```bash
     sudo nano /etc/resolv.conf
     ```
     Added:
     ```
     nameserver 8.8.8.8
     nameserver 8.8.4.4
     ```
  3. Restarted networking:
     ```bash
     sudo systemctl restart systemd-resolved
     ```
  4. Used local model files to bypass network dependency (see Step 4).

### Issue 2: Incomplete Git Clone (~2 MB)
- **Problem**:
  Cloning `https://huggingface.co/KittenML/kitten-tts-nano-0.1` downloaded only ~2 MB, with `kitten_tts_nano_v0_1.onnx` and `voices.npz` as LFS pointer files (~128 bytes) instead of full sizes (~23.8 MB and ~11 KB).

- **Cause**:
  Git LFS was not properly set up, fetching only pointers.

- **Solution**:
  1. Installed Git LFS:
     ```bash
     sudo apt install git-lfs -y
     git lfs install
     ```
  2. Fetched LFS files:
     ```bash
     cd ~/Codes/TTS/kitten-tts-nano-0.1
     git lfs pull
     ```
  3. Verified file sizes:
     ```bash
     ls -lh
     ```
  4. If `git lfs pull` failed, set Hugging Face token:
     ```bash
     export HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
     git lfs pull
     ```
  5. Re-cloned if needed:
     ```bash
     cd ~/Codes/TTS
     rm -rf kitten-tts-nano-0.1
     git clone https://huggingface.co/KittenML/kitten-tts-nano-0.1
     cd kitten-tts-nano-0.1
     git lfs pull
     ```

### Issue 3: `KittenTTS` API Mismatch (`local_path` Error)
- **Problem**:
  Running `run_tts.py` with `m = KittenTTS(local_path="/home/bcpsc/Codes/TTS/kitten-tts-nano-0.1")` failed:
  ```plaintext
  TypeError: KittenTTS.__init__() got an unexpected keyword argument 'local_path'
  ```
  The `kittentts` package (version 0.1.0) does not support `local_path`.

- **Cause**:
  The package expects `repo_id` (e.g., `"KittenML/kitten-tts-nano-0.1"`) and downloads from Hugging Face.

- **Solution**:
  1. Moved model files to the Hugging Face cache:
     ```bash
     mkdir -p ~/.cache/huggingface/hub/models--KittenML--kitten-tts-nano-0.1/snapshots/main
     cp ~/Codes/TTS/kitten-tts-nano-0.1/* ~/.cache/huggingface/hub/models--KittenML--kitten-tts-nano-0.1/snapshots/main/
     ```
  2. Updated `run_tts.py`:
     ```python
     m = KittenTTS("KittenML/kitten-tts-nano-0.1")
     ```
  3. Checked for package updates:
     ```bash
     pip show kittentts
     ```
     - Version `0.1.0` confirmed; no newer releases found at [github.com/KittenML/KittenTTS/releases](https://github.com/KittenML/KittenTTS/releases).
  4. Ensured dependencies:
     ```bash
     pip install torch soundfile onnxruntime huggingface_hub espeakng_loader misaki num2words numpy spacy --index-url https://download.pytorch.org/whl/cpu
     ```

---

## 🎵 Step 6: Test with Sample Texts and Voices

1. **Create a test script**:
   ```bash
   nano ~/Codes/TTS/run_tts.py
   ```
   Add:
   ```python
   from kittentts import KittenTTS
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

   # Generate audio
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
   ```

2. **Run and play**:
   ```bash
   python ~/Codes/TTS/run_tts.py
   aplay output_text1_voice_expr-voice-2-f.wav
   ```

3. **Check voices**:
   If voices fail, inspect `voices.npz`:
   ```bash
   python -c "import numpy as np; print(np.load('/home/bcpsc/Codes/TTS/kitten-tts-nano-0.1/voices.npz').files)"
   ```

---

## 💡 Tips and Tricks

- **Performance**: Generation takes ~1-2 seconds per short sentence. Use a fan/heatsink for extended runs.
- **Memory**: If memory is low, add swap:
  ```bash
  sudo fallocate -l 1G /swapfile
  sudo chmod 600 /swapfile
  sudo mkswap /swapfile
  sudo swapon /swapfile
  ```
- **Audio issues**: Test with:
  ```bash
  speaker-test -t wav
  ```
- **Upgrading to 0.2**: Clone and set up `kitten-tts-nano-0.2`:
  ```bash
  cd ~/Codes/TTS
  git clone https://huggingface.co/KittenML/kitten-tts-nano-0.2
  cd kitten-tts-nano-0.2
  git lfs pull
  ```

---

## 🎉 Conclusion

This guide provides a complete setup for running KittenTTS on a Raspberry Pi 5, overcoming DNS issues, Git LFS cloning problems, and API mismatches. The model now runs offline, producing high-quality audio suitable for low-resource devices. For further assistance, check [github.com/KittenML/KittenTTS](https://github.com/KittenML/KittenTTS) or share error logs.

Happy TTS-ing! 🎤
