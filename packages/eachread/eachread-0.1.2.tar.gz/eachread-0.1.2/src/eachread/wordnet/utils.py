import typing

from .data import wordnet


def get_all_hyponyms(synset) -> set:
    result = set()

    def recurse(current_synset):
        for hyponym in current_synset.hyponyms():
            result.add(hyponym)
            recurse(hyponym)

    recurse(synset)
    return result


def get_all_animal_synsets() -> typing.List[wordnet.synset]:
    animals = wordnet.synsets("animal", pos=wordnet.NOUN)
    all_animals = set()

    for synset in animals:
        all_animals.update(get_all_hyponyms(synset))

    return list(all_animals)


def get_all_physical_adjectives() -> typing.List[wordnet.synset]:
    physical_adj = wordnet.synsets("physical", pos=wordnet.ADJ)
    all_adj = set()

    for synset in physical_adj:
        all_adj.update(get_all_hyponyms(synset))

    return list(all_adj)


def get_animal_synsets() -> typing.List[wordnet.synset]:
    animals = wordnet.synsets("animal", pos=wordnet.NOUN)
    animal_hyponyms = []

    for synset in animals:
        animal_hyponyms.extend(synset.hyponyms())

    return animal_hyponyms


def get_physical_adjectives_direct() -> typing.List[wordnet.synset]:
    physical_adj = wordnet.synsets("physical", pos=wordnet.ADJ)
    adj_hyponyms = []

    for synset in physical_adj:
        adj_hyponyms.extend(synset.hyponyms())

    return adj_hyponyms
