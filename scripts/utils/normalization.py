import unicodedata
import re

# kullanıcılar gogus, chest, CHEST, göğüs vs yazabilir. bu gibi durumların tamamını normalize edecek olan script

def normalize_text(text: str) -> str:
    if not text:
        return ""

    # Unicode normalizasyonu
    text = unicodedata.normalize("NFKD", text)

    # Türkçe karakterleri ascii'ye çevir
    replace_map = {
        "ı": "i", "İ": "i",
        "ğ": "g", "Ğ": "g",
        "ş": "s", "Ş": "s",
        "ö": "o", "Ö": "o",
        "ü": "u", "Ü": "u",
        "ç": "c", "Ç": "c"
    }
    for src, tgt in replace_map.items():
        text = text.replace(src, tgt)

    # Harf dışındaki şeyleri kaldır
    text = re.sub(r"[^a-zA-Z0-9 ]+", " ", text)

    # Küçük harf
    text = text.lower()

    # Tek boşluğa indir, baş/son boşlukları sil
    text = re.sub(r"\s+", " ", text).strip()

    return text
