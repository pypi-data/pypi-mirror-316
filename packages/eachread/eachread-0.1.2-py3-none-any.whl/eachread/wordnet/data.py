def ensure_nltk_data() -> None:
    try:
        import nltk.data

        nltk.data.find("corpora/wordnet")
    except LookupError:
        nltk.download("wordnet", quiet=True)


def get_wordnet():
    from nltk.corpus import wordnet

    return wordnet


# Download immediately when this module is imported
ensure_nltk_data()
wordnet = get_wordnet()

__all__ = ["wordnet"]
