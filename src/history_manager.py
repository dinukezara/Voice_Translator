import os
from datetime import datetime
from config import get_logger, HISTORY_FILE_PATH

logger = get_logger(__name__)

class HistoryManager:
    def __init__(self, file_path: str = HISTORY_FILE_PATH) -> None:
        self.file_path = file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        logger.debug(f"History initialized at '{self.file_path}'")

    def save(self, source_lang: str, target_lang: str, original_text: str, translated_text: str) -> None:
        """
        Saves translation details safely into the history log.

        Args:
            source_lang (str): Name of the source language.
            target_lang (str): Name of the target language.
            original_text (str): The recognized original text.
            translated_text (str): The translated text.
        """
        try:
            with open(self.file_path, "a", encoding="utf-8") as file:
                file.write(f"Timestamp: {datetime.now()}\n")
                file.write(f"Source Language: {source_lang}\n")
                file.write(f"Target Language: {target_lang}\n")
                file.write(f"Original Text: {original_text}\n")
                file.write(f"Translated Text: {translated_text}\n")
                file.write("-" * 60 + "\n")
            logger.info("Successfully appended transaction to history log.")
        except IOError as e:
            logger.error(f"Failed to write to history file ({self.file_path}): {e}")
