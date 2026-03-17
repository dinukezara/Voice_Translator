from deep_translator import GoogleTranslator
from config import get_logger

logger = get_logger(__name__)

class TranslatorService:
    def translate(self, text: str, source: str = "auto", target: str = "es") -> dict[str, str | bool]:
        """
        Translates text from a source language to a target language.

        Args:
            text (str): The text to translate.
            source (str): Source language code or "auto" for detection.
            target (str): Target language code.

        Returns:
            dict: Contains 'success' (bool) and either 'text' (str) or 'error' (str).
        """
        try:
            logger.debug(f"Attempting to translate text ({len(text)} chars) from '{source}' to '{target}'...")
            translated = GoogleTranslator(source=source, target=target).translate(text)
            logger.info(f"Translation completed successfully ({target}).")
            return {"success": True, "text": translated}
        except Exception as e:
            logger.exception(f"Translation failed: {e}")
            return {"success": False, "error": f"Translation failed: {e}"}
