import random
import typing

from .data import wordnet


def get_all_adjectives() -> typing.List[wordnet.synset]:
    adjectives = wordnet.all_synsets(pos=wordnet.ADJ)
    return list(adjectives)


def display_adjectives(adjectives: typing.List, limit: int) -> None:
    print(f"Found {len(adjectives)} total adjective synsets")

    if adjectives:
        print("\nExample adjectives:")
        sample_size = len(adjectives) if limit <= 0 else min(limit, len(adjectives))
        for adj in random.sample(adjectives, sample_size):
            name = adj.name().split(".")[0]
            print(f"- {name.replace('_', ' ')}: {adj.definition()}")
