# aksharam

aksharam is a Python library for transliterating Malayalam text into English-style commonly known as Manglish.

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

## License

This package is distributed under the MIT License for the original work in this repository.

## Author

Ajish K B

