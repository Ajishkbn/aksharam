from aksharam import transliterate


def test_ai_modifier_fix():
    assert transliterate("കൈ") == "Kai"


def test_visarga_fix():
    assert transliterate("ദുഃഖം") == "Dukham"


def test_jnya_compound_fix():
    assert transliterate("ജ്ഞാനം") == "Jnaanam"


def test_chchha_compound_fix():
    assert transliterate("അച്ഛൻ") == "Achhan"


def test_anusvaram_assimilation():
    assert transliterate("ഗംഗ") == "Ganga"


def test_retroflex_voicing():
    assert transliterate("ഓടുക") == "Oduka"
