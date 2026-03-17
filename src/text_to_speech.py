import os
import uuid
from gtts import gTTS
from playsound import playsound

from config import get_logger

logger = get_logger(__name__)


class TextToSpeech:
    """
    Converts text to speech, plays it, and keeps the last generated audio for replay.
    """

    def __init__(self):
        self.last_file = None

    def speak(self, text: str, lang: str = "en") -> dict:
        try:
            if not text.strip():
                return {"success": False, "error": "Empty text cannot be spoken."}

            filename = f"tts_{uuid.uuid4().hex}.mp3"

            logger.info("Generating speech audio...")
            tts = gTTS(text=text, lang=lang)
            tts.save(filename)

            self.last_file = filename

            logger.info("Playing generated speech...")
            playsound(filename)

            return {"success": True}

        except Exception as e:
            logger.exception("TTS generation/playback failed.")
            return {"success": False, "error": f"TTS failed: {e}"}

    def replay(self) -> dict:
        try:
            if not self.last_file or not os.path.exists(self.last_file):
                return {"success": False, "error": "No previous audio available to replay."}

            logger.info("Replaying last generated audio...")
            playsound(self.last_file)
            return {"success": True}

        except Exception as e:
            logger.exception("Replay failed.")
            return {"success": False, "error": f"Replay failed: {e}"}

    def cleanup(self) -> None:
        """
        Optional cleanup for the last saved audio file.
        """
        try:
            if self.last_file and os.path.exists(self.last_file):
                os.remove(self.last_file)
                logger.info("Temporary TTS audio removed.")
                self.last_file = None
        except Exception as e:
            logger.warning(f"Failed to clean up audio file: {e}")