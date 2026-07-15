# aksharam

aksharam is a Python library for transliterating Malayalam text into English-style Manglish with a small set of compatibility fixes built on top of ml2en.

It provides a simple API for converting Malayalam words and phrases into Romanized Manglish output while preserving common transliteration nuances such as anusvaram handling, retroflex voicing, and compound-letter fixes.

## Installation

```bash
pip install aksharam
```

## Usage

```python
from aksharam import transliterate

print(transliterate("കൈ"))
# Kai
```

You can also transliterate multiple items at once:

```python
from aksharam import transliterate_text

print(transliterate_text(["കൈ", "ജ്ഞാനം", "ഓടുക"]))
```

## CLI

```bash
aksharam "കൈ"
```

## License and dependency notice

This package is distributed under the MIT License for the original work in this repository.
However, it depends on ml2en, which is licensed under GPLv2. If you redistribute or bundle this package in a way that includes or adapts ml2en code, the GPLv2 terms of that dependency should be considered.

## Author

Ajish K B

