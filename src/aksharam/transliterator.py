from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable


_ZWNJ = "\u200C"
_ZWJ = "\u200D"
_ANUSVARAM = "\u0D02"
_CHILLU_N = "\u0D7B"
_VIRAMA = "\u0D4D"
_VOICED_RETROFLEX = "\u0D21"
_VOICELESS_RETROFLEX = frozenset({"\u0D1F", "\u0D20"})
_NON_LABIAL_CONSONANTS = set("കഖഗഘചഛജഝടഠഡഢതഥദധയരലവ")
_WORD_BOUNDARIES = frozenset(" \t\n.,;:!?()[]{}\"'/\\")
_ALL_MALAYALAM_CONSONANTS = frozenset(
    "\u0D15\u0D16\u0D17\u0D18\u0D19"
    "\u0D1A\u0D1B\u0D1C\u0D1D\u0D1E"
    "\u0D1F\u0D20\u0D21\u0D22\u0D23"
    "\u0D24\u0D25\u0D26\u0D27\u0D28"
    "\u0D2A\u0D2B\u0D2C\u0D2D\u0D2E"
    "\u0D2F\u0D30\u0D32\u0D35"
    "\u0D36\u0D37\u0D38\u0D39"
    "\u0D33\u0D34\u0D31"
)
_TABLE_PATH = Path(__file__).resolve().parent / "data" / "malayalam_transliteration.json"


def _load_tables() -> dict[str, dict[str, str]]:
    with _TABLE_PATH.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    return {
        "vowels": dict(payload.get("vowels", {})),
        "compounds": dict(payload.get("compounds", {})),
        "consonants": dict(payload.get("consonants", {})),
        "chil": dict(payload.get("chil", {})),
        "modifiers": dict(payload.get("modifiers", {})),
    }


class _BundledTransliterator:
    """A small local transliterator backed by bundled JSON tables."""

    def __init__(self) -> None:
        self._tables = _load_tables()
        self._patch_tables()
        self._vowels = self._tables["vowels"]
        self._compounds = self._tables["compounds"]
        self._consonants = self._tables["consonants"]
        self._chil = self._tables["chil"]
        self._modifiers = self._tables["modifiers"]

    def _patch_tables(self) -> None:
        self._tables["modifiers"]["\u0D48"] = "ai"
        self._tables["modifiers"]["\u0D03"] = ""
        self._tables["compounds"]["\u0D1C\u0D4D\u0D1E"] = "jn"
        self._tables["compounds"]["\u0D1A\u0D4D\u0D1B"] = "chh"
        self._tables["compounds"] = dict(
            sorted(self._tables["compounds"].items(), key=lambda kv: -len(kv[0]))
        )

    def transliterate(self, text: str) -> str:
        input_text = re.sub(r"\xE2\x80\x8C", "", text)
        input_text = self._replace_modified_glyphs(self._compounds, input_text)
        input_text = self._replace_modified_glyphs(self._vowels, input_text)
        input_text = self._replace_modified_glyphs(self._consonants, input_text)

        for glyph, value in self._compounds.items():
            input_text = re.sub(glyph + "്([\\w])", value + r"\1", input_text)
            input_text = input_text.replace(glyph + "്", value + "u")
            input_text = input_text.replace(glyph, value + "a")

        for glyph, value in self._consonants.items():
            input_text = re.sub(glyph + r"(?!്)", value + "a", input_text)

        for glyph, value in self._consonants.items():
            input_text = re.sub(glyph + r"്(?![\s\)\.;,\"'\/\\\%\!])", value, input_text)

        for glyph, value in self._consonants.items():
            input_text = input_text.replace(glyph + "്", value + "u")

        for glyph, value in self._consonants.items():
            input_text = input_text.replace(glyph, value)

        for glyph, value in self._vowels.items():
            input_text = input_text.replace(glyph, value)

        for glyph, value in self._chil.items():
            input_text = input_text.replace(glyph, value)

        input_text = input_text.replace("ം", "m")

        for glyph, value in self._modifiers.items():
            input_text = input_text.replace(glyph, value)

        chunks = re.split(r"([.!?] *)", input_text)
        return "".join([chunk.capitalize() for chunk in chunks])

    def _replace_modified_glyphs(self, glyphs: dict[str, str], input_text: str) -> str:
        exp = re.compile("((" + "|".join(glyphs.keys()) + ")(" + "|".join(self._modifiers.keys()) + "))")
        matches = exp.findall(input_text)
        if matches is not None:
            for match in matches:
                input_text = input_text.replace(match[0], glyphs[match[1]] + self._modifiers[match[2]])
        return input_text


_LOCAL_TRANSLITERATOR = _BundledTransliterator()


def _preprocess_malayalam(text: str) -> str:
    """Fix anusvaram assimilation, retroflex voicing, and strip invisible joiners before transliteration."""
    result = []
    chars = list(text)
    n = len(chars)
    at_word_start = True

    for i, ch in enumerate(chars):
        if ch in (_ZWNJ, _ZWJ):
            continue

        if ch in _WORD_BOUNDARIES:
            at_word_start = True
            result.append(ch)
            continue

        if ch == _ANUSVARAM:
            next_ch = next(
                (chars[j] for j in range(i + 1, n) if chars[j] not in (_ZWNJ, _ZWJ)),
                "",
            )
            if next_ch in _NON_LABIAL_CONSONANTS:
                result.append(_CHILLU_N)
                at_word_start = False
                continue

        if ch in _VOICELESS_RETROFLEX and not at_word_start:
            prev_ch = result[-1] if result else ""
            next_ch = chars[i + 1] if i + 1 < n else ""
            if prev_ch != _VIRAMA:
                if next_ch != _VIRAMA:
                    result.append(_VOICED_RETROFLEX)
                    at_word_start = False
                    continue
                else:
                    char_after_virama = next(
                        (chars[j] for j in range(i + 2, n) if chars[j] not in (_ZWNJ, _ZWJ)),
                        "",
                    )
                    if char_after_virama not in _ALL_MALAYALAM_CONSONANTS:
                        result.append(_VOICED_RETROFLEX)
                        at_word_start = False
                        continue

        at_word_start = False
        result.append(ch)

    return "".join(result)


def _postprocess_manglish(original: str, manglish: str) -> str:
    """Remove artifacts from transliteration output and make word-final virama endings more colloquial."""
    result = manglish
    result = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", result)
    result = result.replace(_ZWNJ, "").replace(_ZWJ, "")
    result = re.sub(r"([aeiou])\1{2,}", r"\1\1", result)
    orig_clean = str(original).replace(_ZWNJ, "").replace(_ZWJ, "").rstrip()
    if orig_clean.endswith(_VIRAMA):
        if not result.rstrip().endswith(("y", "Y")):
            result = re.sub(r"([^aeiou\s])$", r"\1u", result)
    return result


def transliterate(text: str) -> str:
    """Transliterate Malayalam text to Manglish."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not text:
        return ""
    try:
        original = text
        cleaned = _preprocess_malayalam(original)
        raw = _LOCAL_TRANSLITERATOR.transliterate(cleaned)
        return _postprocess_manglish(original, raw)
    except Exception:
        return str(text)


def transliterate_text(text: Iterable[str]) -> list[str]:
    """Transliterate an iterable of Malayalam strings."""
    return [transliterate(item) for item in text]
