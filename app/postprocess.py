from __future__ import annotations
import re
import unicodedata

US_STATE_WORDS = {
    "ALABAMA","ALASKA","ARIZONA","ARKANSAS","CALIFORNIA","COLORADO","CONNECTICUT",
    "DELAWARE","FLORIDA","GEORGIA","HAWAII","IDAHO","ILLINOIS","INDIANA","IOWA",
    "KANSAS","KENTUCKY","LOUISIANA","MAINE","MARYLAND","MASSACHUSETTS","MICHIGAN",
    "MINNESOTA","MISSISSIPPI","MISSOURI","MONTANA","NEBRASKA","NEVADA",
    "NEWHAMPSHIRE","NEWJERSEY","NEWMEXICO","NEWYORK","NORTHCAROLINA","NORTHDAKOTA",
    "OHIO","OKLAHOMA","OREGON","PENNSYLVANIA","RHODEISLAND","SOUTHCAROLINA",
    "SOUTHDAKOTA","TENNESSEE","TEXAS","UTAH","VERMONT","VIRGINIA","WASHINGTON",
    "WESTVIRGINIA","WISCONSIN","WYOMING"
}
SLOGAN_WORDS = {
    "DMV","EXPLORE","DISCOVER","AMERICA","GARDENSTATE","SUNSHINESTATE",
    "LIVFREEORDIE","THELONESTARSTATE","CONSTITUTIONSTATE","LANDOFLINCOLN"
}

def _clean_unicode(text: str) -> str:
    return unicodedata.normalize("NFKC", text or "").strip()

def normalize_plate(text: str) -> str:
    text = _clean_unicode(text).upper()
    chunks = re.findall(r"[\u3400-\u9fff]|[A-Z0-9]+", text)
    kept = []
    for chunk in chunks:
        flat = chunk.replace(" ", "")
        if flat in US_STATE_WORDS or flat in SLOGAN_WORDS:
            continue
        kept.append(flat)
    return "".join(kept)

def normalize_sign(text: str) -> str:
    text = _clean_unicode(text).upper().replace("\r", "\n")
    lines = [re.sub(r"\s+", " ", line).strip(" .,:;") for line in text.split("\n")]
    lines = [x for x in lines if x]
    joined = " ".join(lines)
    m = re.fullmatch(r"(?:MPH\s*)?(\d{1,3})(?:\s*(?:MPH|KM/?H))?", joined)
    return m.group(1) if m else joined

def normalize_output(text: str, task: str) -> str:
    if (task or "").lower() == "plate":
        return normalize_plate(text)
    if (task or "").lower() == "sign":
        return normalize_sign(text)
    return re.sub(r"\s+", " ", _clean_unicode(text)).strip()
