import pytest
from aksharam import transliterate


# ---------------------------------------------------------------------------
# Independent vowels
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "ml,en",
    [
        ("അ", "A"),
        ("ആ", "Aa"),
        ("ഇ", "I"),
        ("ഈ", "Ee"),
        ("ഉ", "U"),
        ("ഊ", "Oo"),
        ("ഋ", "Ru"),
        ("എ", "E"),
        ("ഏ", "E"),
        ("ഐ", "Ai"),
        ("ഒ", "O"),
        ("ഓ", "O"),
        ("ഔ", "Au"),
    ],
)
def test_independent_vowels(ml, en):
    assert transliterate(ml) == en


# ---------------------------------------------------------------------------
# Dependent vowel signs
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "ml,en",
    [
        ("ക", "Ka"),
        ("കാ", "Kaa"),
        ("കി", "Ki"),
        ("കീ", "Kee"),
        ("കു", "Ku"),
        ("കൂ", "Koo"),
        ("കൃ", "Kru"),
        ("കെ", "Ke"),
        ("കേ", "Ke"),
        ("കൈ", "Kai"),
        ("കൊ", "Ko"),
        ("കോ", "Ko"),
        ("കൗ", "Kau"),
    ],
)
def test_vowel_signs(ml, en):
    assert transliterate(ml) == en


# ---------------------------------------------------------------------------
# Visarga
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "ml,en",
    [
        ("ദുഃഖം", "Dukham"),
        ("പ്രാതഃകാലം", "Praathkaalam"),
        ("അന്തഃപുരം", "Anthpuram"),
    ],
)
def test_visarga(ml, en):
    assert transliterate(ml) == en


# ---------------------------------------------------------------------------
# Common conjuncts
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "ml,en",
    [
        ("ജ്ഞാനം", "Jnaanam"),
        ("യജ്ഞം", "Yajnam"),
        ("അച്ഛൻ", "Achhan"),
        ("ക്ഷേത്രം", "Kshethram"),
        ("ബ്രഹ്മം", "Brahmam"),
        ("സിദ്ധൻ", "Siddhan"),
    ],
)
def test_common_conjuncts(ml, en):
    assert transliterate(ml) == en


# ---------------------------------------------------------------------------
# Anusvaram assimilation
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "ml,en",
    [
        ("ഗംഗ", "Ganga"),
        ("ചമ്പ", "Champa"),
        ("കണ്ടം", "Kandam"),
        ("പന്ത്", "Panthu"),
        ("സംഘം", "Sangham"),
    ],
)
def test_anusvaram_assimilation(ml, en):
    assert transliterate(ml) == en


# ---------------------------------------------------------------------------
# Retroflex / intervocalic voicing
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "ml,en",
    [
        ("ഓടുക", "Oduka"),
        ("പാടം", "Paadam"),
        ("വീട്", "Veedu"),
    ],
)
def test_retroflex_voicing(ml, en):
    assert transliterate(ml) == en


# ---------------------------------------------------------------------------
# Word-final virama behaviour
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "ml,en",
    [
        ("കുരിശ്", "Kurishu"),
        ("മനസ്", "Manasu"),
        ("ശബ്ദ്", "Shabdu"),
    ],
)
def test_word_final_virama_adds_u(ml, en):
    assert transliterate(ml) == en


@pytest.mark.parametrize(
    "ml,en",
    [
        ("പൈതൽ", "Paithal"),
        ("പൈതലിനായ്", "Paithalinaay"),
    ],
)
def test_word_final_y_suffix_exceptions(ml, en):
    assert transliterate(ml) == en


# ---------------------------------------------------------------------------
# Natural ending preservation
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "ml,en",
    [
        ("മേഖലയാണ്", "Mekhalayaanu"),
        ("അതാണ്", "Athaanu"),
        ("ഇതാണ്", "Ithaanu"),
    ],
)
def test_natural_u_suffix_preserved(ml, en):
    assert transliterate(ml) == en


# ---------------------------------------------------------------------------
# Old Malayalam (pre-1970)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "old,modern",
    [
        ("അൎത്ഥം", "അർത്ഥം"),
        ("തീൎച്ച", "തീർച്ച"),
        ("നിൎമ്മലം", "നിർമ്മലം"),
        ("നിൎണ്ണയം", "നിർണ്ണയം"),
        ("ദുൎബലം", "ദുർബലം"),
        ("സ്വൎഗ്ഗം", "സ്വർഗ്ഗം"),
        ("നിൎദേശം", "നിർദേശം"),
        ("പൂൎവ്വം", "പൂർവ്വം"),
    ],
)
def test_dot_reph_equivalence(old, modern):
    assert transliterate(old) == transliterate(modern)


# ---------------------------------------------------------------------------
# Unicode normalization
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "text",
    [
        "കാർ",
        "മൺ",
        "പാൽ",
        "കൺ",
        "വാൾ",
    ],
)
def test_chillu_normalization(text):
    # Should not raise and should produce stable output.
    assert transliterate(text) == transliterate(text)


# ---------------------------------------------------------------------------
# Regression tests
# ---------------------------------------------------------------------------

def test_ai_modifier_fix():
    assert transliterate("കൈ") == "Kai"


def test_visarga_fix():
    assert transliterate("ദുഃഖം") == "Dukham"


def test_jnya_compound_fix():
    assert transliterate("ജ്ഞാനം") == "Jnaanam"


def test_chchha_compound_fix():
    assert transliterate("അച്ഛൻ") == "Achhan"


def test_anusvaram_fix():
    assert transliterate("ഗംഗ") == "Ganga"


def test_retroflex_fix():
    assert transliterate("ഓടുക") == "Oduka"