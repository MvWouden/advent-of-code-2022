"""
Advent of Code 2022: day 3
"""
from more_itertools import chunked


split_input = open('input.txt', 'r').read().splitlines()


def type_to_priority(_type: str) -> int:
    """
    Determines the priority of a type (single character)
    :param _type: Single uppercase or lowercase character.
    :return: The priority of the type.
    """
    # Lowercase type
    if _type.islower():
        return ord(_type) - ord('a') + 1

    # Uppercase type
    return ord(_type) - ord('A') + 27


def split_rucksack(rucksack: str) -> tuple[str, str]:
    """
    Splits a rucksack down the middle into two parts.
    :param rucksack: The rucksack string representation.
    :return: The two compartments of the rucksack.
    """
    # Determine boundary of compartments
    splitter = len(rucksack) // 2

    # Return the two individual compartments
    return rucksack[:splitter], rucksack[splitter:]


def get_duplicate_type(rucksack: str) -> str:
    """
    Gets the type that is present in both rucksack compartments.
    :param rucksack: The rucksack.
    :return: The type present in both compartments.
    """
    # Split the rucksack into two compartments
    x, y = split_rucksack(rucksack)

    # Determine the common type
    return list(set(x) & set(y))[0]


def get_common_type(rucksacks: list[str]) -> str:
    """
    Gets the type that is present in all rucksacks.
    :param rucksacks: The rucksacks of a group.
    :return: The type present in all rucksacks.
    """
    # Extract each rucksack individually
    x, y, z = [set(rucksack) for rucksack in rucksacks]

    # Determine the common type
    return list(set(x) & set(y) & set(z))[0]


solution = sum([
    type_to_priority(get_duplicate_type(rucksack))
    for rucksack in split_input
])
print(f'part1: {solution}')


solution = sum([
    type_to_priority(get_common_type(rucksacks))
    for rucksacks in chunked(split_input, 3)
])
print(f'part2: {solution}')
