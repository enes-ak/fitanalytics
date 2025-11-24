# app/utils/normalization.py
import unicodedata
import re

def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = unicodedata.normalize("NFKD", text)

    # Türkçe karakter dönüşümü
    table = str.maketrans({
        "ı": "i", "İ": "i",
        "ğ": "g", "Ğ": "g",
        "ş": "s", "Ş": "s",
        "ö": "o", "Ö": "o",
        "ü": "u", "Ü": "u",
        "ç": "c", "Ç": "c"
    })
    text = text.translate(table)

    # harf & sayı dışı karakterleri temizle
    text = re.sub(r"[^a-zA-Z0-9 ]+", " ", text)

    # lowercase + trim
    text = re.sub(r"\s+", " ", text).strip().lower()

    return text
