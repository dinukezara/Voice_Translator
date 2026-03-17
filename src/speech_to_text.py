import speech_recognition as sr
from config import get_logger

logger = get_logger(__name__)

class SpeechToText:
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()

    def listen(self, language_code: str = "en-US", timeout: int = 10, phrase_time_limit: int = 10) -> dict[str, str | bool]:
        """
        Listens to microphone input and converts it to text using Google Speech Recognition.

        Args:
            language_code (str): The language code to recognize.
            timeout (int): Maximum seconds to wait for speech before giving up.
            phrase_time_limit (int): Maximum seconds a phrase can last before it's cut off.

        Returns:
            dict: Contains 'success' (bool) and either 'text' (str) or 'error' (str).
        """
        try:
            with sr.Microphone() as source:
                logger.debug("Adjusting for background noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info(f"Listening for speech (Language: {language_code})...")
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_time_limit
                )

            logger.debug("Audio captured, sending to Google Speech Recognition...")
            text = self.recognizer.recognize_google(audio, language=language_code)
            logger.info(f"Successfully recognized text: '{text}'")
            return {"success": True, "text": text}

        except sr.WaitTimeoutError:
            logger.warning("Listening timed out. No speech detected.")
            return {
                "success": False,
                "error": "Listening timed out. No speech detected.",
            }
        except sr.UnknownValueError:
            logger.warning("Speech could not be understood.")
            return {"success": False, "error": "Speech could not be understood."}
        except sr.RequestError as e:
            logger.error(f"Speech service error: {e}")
            return {"success": False, "error": f"Speech service error: {e}"}
        except Exception as e:
            logger.exception(f"Unexpected error during speech-to-text: {e}")
            return {"success": False, "error": f"Unexpected error: {e}"}
