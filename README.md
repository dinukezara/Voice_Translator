# 🎙️ Voice-Based Multilingual Speech-to-Speech Translation System

## 📌 Overview

This project is a **voice-driven multilingual translation system** that captures spoken input from a user, converts it into text, translates it into a selected target language, and generates spoken output in that language.

The system integrates **Speech Recognition, Natural Language Processing (NLP), and Text-to-Speech (TTS)** technologies to provide a seamless speech-to-speech translation experience.

---

## 🚀 Features

### Core Features

* 🎤 Speech-to-Text using **Whisper (faster-whisper)**
* 🌐 Automatic language detection
* 🔄 Text translation between multiple languages
* 🔊 Text-to-Speech output using **gTTS**
* 🖥️ User-friendly GUI built with **Tkinter**

### Advanced Features

* ⚡ Multithreading (prevents GUI freezing)
* 💾 Translation history stored in **SQLite database**
* 📤 Export translation history to CSV
* 🔁 Replay translated audio
* 📊 Real-time status updates with progress bar
* 🌙 Dark mode / Light mode toggle
* 📜 Built-in history viewer (table format)

---

## 🏗️ System Architecture

```
User Speech
     ↓
Microphone Input
     ↓
Whisper Speech Recognition
     ↓
Language Detection
     ↓
Translation Engine
     ↓
Translated Text
     ↓
Text-to-Speech (gTTS)
     ↓
Speaker Output
     ↓
SQLite Database Storage
```

---

## 🧰 Technology Stack

### Programming Language

* Python 3.10+

### Libraries & Frameworks

* faster-whisper (Speech Recognition)
* deep-translator (Translation)
* gTTS (Text-to-Speech)
* Tkinter (GUI)
* SQLite3 (Database)
* sounddevice (Audio capture)
* numpy (Audio processing)
* playsound (Audio playback)

---

## 💻 Hardware Requirements

* Laptop or Desktop Computer
* Microphone (built-in or external)
* Speakers or Headphones
* Internet connection (for translation & TTS)

---

## ⚙️ Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/voice-translator.git
cd voice-translator
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/macOS
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install faster-whisper sounddevice numpy gTTS playsound==1.2.2 deep-translator
```

---

## ▶️ How to Run

### Run GUI Version

```bash
python src/gui.py
```

### Run CLI Version

```bash
python src/main.py
```

---

## 📂 Project Structure

```
voice_translator/
│
├── src/
│   ├── main.py
│   ├── gui.py
│   ├── config.py
│   ├── speech_to_text_whisper.py
│   ├── translator.py
│   ├── text_to_speech.py
│   ├── database.py
│
├── data/
│   └── translations.db
│
├── requirements.txt
├── README.md
```

---

## 🧪 Testing

Test the system using:

* Quiet vs noisy environments
* Different languages (English, Tamil, Hindi, etc.)
* Short and long sentences

Example test inputs:

* "Hello, how are you?"
* "Where is the nearest hospital?"
* "Thank you very much"

---

## ⚠️ Limitations

* Requires internet connection for translation and TTS
* Accuracy may reduce in noisy environments
* Accent variations may affect recognition
* Limited offline capability

---

## 🔮 Future Enhancements

* Real-time streaming translation
* Offline translation support
* Mobile application (Android/iOS)
* Raspberry Pi portable device version
* Voice customization (male/female voices)
* Domain-specific translation modes (medical, travel)

---

## 📊 Evaluation Metrics

* Speech recognition accuracy
* Translation accuracy
* Response time
* User experience

---

## 📜 License

This project is for academic and educational purposes.

---

## 🙌 Acknowledgements

* OpenAI Whisper (Speech Recognition)
* Google Text-to-Speech (gTTS)
* deep-translator library
* Python community

---

## 👨‍💻 Author

Developed as part of a university-level project.

---

## ⭐ Final Note

This project demonstrates the integration of **AI-based speech recognition, machine translation, and speech synthesis** into a unified system. It serves as a scalable foundation for real-world multilingual communication applications.
