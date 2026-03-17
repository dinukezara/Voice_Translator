from translator import TranslatorService


def test_translation():
    service = TranslatorService()
    result = service.translate("Hello", source="en", target="fr")
    assert result["success"] is True
    assert isinstance(result["text"], str)
