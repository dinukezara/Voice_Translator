from config import LANGUAGE_MAP, LANGUAGE_CODE_MAP, DEFAULT_TARGET, get_logger
from database import Database
from speech_to_text_whisper import WhisperSTT
from text_to_speech import TextToSpeech
from translator import TranslatorService

logger = get_logger(__name__)


def run_pipeline(target_lang: str = DEFAULT_TARGET) -> None:
    logger.info("Initializing Whisper Translation Pipeline...")

    stt = WhisperSTT()
    translator = TranslatorService()
    tts = TextToSpeech()
    db = Database()

    try:
        target_translate = LANGUAGE_MAP[target_lang]["translate"]
        target_tts = LANGUAGE_MAP[target_lang]["tts"]
    except KeyError as e:
        logger.error(f"Invalid target language provided: {e}")
        return

    logger.info("Starting Whisper STT Phase...")
    result_stt = stt.transcribe()

    if not result_stt.get("success"):
        logger.error(f"STT Error: {result_stt.get('error')}")
        return

    original_text = result_stt.get("text", "").strip()
    detected_language_code = result_stt.get("language", "").strip().lower()
    source_lang = LANGUAGE_CODE_MAP.get(detected_language_code, "Unknown")

    print(f"Detected Source Language: {source_lang} ({detected_language_code})")
    print(f"Original Text: {original_text}")

    logger.info("Starting Translation Phase...")
    result_translate = translator.translate(
        text=original_text,
        source="auto",
        target=target_translate,
    )

    if not result_translate.get("success"):
        logger.error(f"Translation Error: {result_translate.get('error')}")
        return

    translated_text = result_translate.get("text", "").strip()
    print(f"Translated ({target_lang}): {translated_text}")

    db.insert(source_lang, target_lang, original_text, translated_text)

    logger.info("Starting TTS Phase...")
    result_tts = tts.speak(translated_text, lang=target_tts)

    if not result_tts.get("success"):
        logger.error(f"TTS Error: {result_tts.get('error')}")
        return

    logger.info("Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline(DEFAULT_TARGET)