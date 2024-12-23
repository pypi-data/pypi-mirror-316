import random
import signal
import sys
import typing

from . import utils
from .data import wordnet


def signal_handler(sig, frame):
    print("\nStopped by user")
    sys.exit(0)


def get_random_combinations(limit: int) -> typing.List[typing.Tuple[str, str]]:
    adjectives = list(wordnet.all_synsets(pos=wordnet.ADJ))
    animals = utils.get_all_animal_synsets()

    if limit <= 0:
        total_possible = len(adjectives) * len(animals)
        return (adjectives, animals), total_possible

    combinations = []
    seen = set()
    while len(combinations) < limit:
        adj = random.choice(adjectives)
        animal = random.choice(animals)
        adj_name = adj.name().split(".")[0].replace("_", " ")
        animal_name = animal.name().split(".")[0].replace("_", " ")

        combo = f"{adj_name} {animal_name}"
        if combo not in seen:
            seen.add(combo)
            combinations.append((adj_name, animal_name))
    return combinations, len(combinations)


def display_combinations(
    combinations: typing.Union[typing.List[typing.Tuple[str, str]], typing.Tuple],
    total_count: int,
) -> None:
    signal.signal(signal.SIGINT, signal_handler)

    print(f"\nGenerating {total_count} adjective-animal combinations:")

    if isinstance(combinations, list):
        for adj, animal in combinations:
            print(f"- {adj} {animal}")
        return

    adjectives, animals = combinations
    batch_size = 100
    seen = set()

    try:
        while True:
            for _ in range(batch_size):
                adj = random.choice(adjectives)
                animal = random.choice(animals)
                adj_name = adj.name().split(".")[0].replace("_", " ")
                animal_name = animal.name().split(".")[0].replace("_", " ")

                combo = f"{adj_name} {animal_name}"
                if combo not in seen:
                    seen.add(combo)
                    print(f"- {combo}")

    except KeyboardInterrupt:
        print("\nStopped by user")
        sys.exit(0)
