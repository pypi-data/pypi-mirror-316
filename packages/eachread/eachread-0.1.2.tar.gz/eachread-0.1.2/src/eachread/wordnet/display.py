import random
import typing


def print_results(animals: typing.List, adjectives: typing.List, limit: int) -> None:
    if animals:
        print(f"Found {len(animals)} total animal synsets")
        print("\nExample animals:")
        sample_size = len(animals) if limit <= 0 else min(limit, len(animals))

        print("\nWords with underscores:")
        underscored = [a for a in animals if "_" in a.name()]
        if len(underscored) > 0:
            print(
                f"Found {len(underscored)} compound words ({len(underscored)/len(animals)*100:.1f}%)"
            )
            for animal in random.sample(underscored, min(5, len(underscored))):
                name = animal.name().split(".")[0]
                print(f"- {name} ({name.replace('_', ' ')}): {animal.definition()}")

        print("\nSingle word animals:")
        single_words = [a for a in animals if "_" not in a.name()]
        if len(single_words) > 0:
            print(
                f"Found {len(single_words)} single words ({len(single_words)/len(animals)*100:.1f}%)"
            )
            for animal in random.sample(single_words, min(5, len(single_words))):
                print(f"- {animal.name().split('.')[0]}: {animal.definition()}")

    if adjectives:
        print(f"\nFound {len(adjectives)} total physical adjective synsets")
        print("\nExample physical adjectives:")
        sample_size = len(adjectives) if limit <= 0 else min(limit, len(adjectives))
        for adj in random.sample(adjectives, sample_size):
            print(f"- {adj.name().split('.')[0]}: {adj.definition()}")
