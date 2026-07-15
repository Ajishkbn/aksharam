import argparse

from .transliterator import transliterate


def main() -> None:
    parser = argparse.ArgumentParser(description="Transliterate Malayalam text to Manglish")
    parser.add_argument("text", help="Malayalam text to transliterate")
    args = parser.parse_args()
    print(transliterate(args.text))
