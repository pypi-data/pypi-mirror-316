from . import adjanimal, adjectives, display, utils


def cmd_wordnet(limit: int) -> None:
    animals = utils.get_animal_synsets()
    adjectives = utils.get_physical_adjectives_direct()
    display.print_results(animals, adjectives, limit)


def cmd_wordnet_deep(limit: int) -> None:
    animals = utils.get_all_animal_synsets()
    adjectives = utils.get_all_physical_adjectives()
    display.print_results(animals, adjectives, limit)


def cmd_adjectives(limit: int) -> None:
    all_adjectives = adjectives.get_all_adjectives()
    adjectives.display_adjectives(all_adjectives, limit)


def cmd_adjanimal(limit: int) -> None:
    combinations, total_count = adjanimal.get_random_combinations(limit)
    adjanimal.display_combinations(combinations, total_count)
