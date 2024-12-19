import argparse
import random
import importlib.resources

def load_words(filename):
    """Loads words from a file, splitting by spaces."""
    with importlib.resources.open_text("etiopique_lorem_texts.text", filename) as f:
        return f.read().split()


def generate_lorem_ipsum(words, num_words):
    """Generates a lorem ipsum string using the given words."""
    if not words:
        return ""
    return " ".join(random.choice(words) for _ in range(num_words))

def main():
    parser = argparse.ArgumentParser(description="Generates Amharic or English Lorem Ipsum text.")
    parser.add_argument("-l", "--language", choices=['amharic', 'english'], default='english',
                        help="Language of Lorem Ipsum to generate.")
    parser.add_argument("-w", "--words", type=int, default=100,
                         help="Number of words to generate.")
    args = parser.parse_args()

    if args.language == "amharic":
        words = load_words("amharic.txt")
    elif args.language == "english":
        words = load_words("english.txt")

    text = generate_lorem_ipsum(words, args.words)
    print(text)

if __name__ == "__main__":
    main()