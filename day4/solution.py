"""
Advent of Code 2022: day 4
"""
split_input = open("input.txt").read().split("\n")


def get_min_max_ranges(line: str) -> tuple[int, int, int, int]:
    """
    Get the min and max of the pairs ranges.
    :param line: The line containing both ranges.
    :return: The minimum and maximum of the first and second range.
    """
    # Split the line into the two ranges.
    r1, r2 = line.split(',')

    # Split the ranges into the min and max.
    r1_min, r1_max = r1.split('-')
    r2_min, r2_max = r2.split('-')

    # Return the min and max of the ranges.
    return int(r1_min), int(r1_max), int(r2_min), int(r2_max)


def is_fully_contained(r1_min: int, r1_max: int, r2_min: int, r2_max: int) -> bool:
    """
    Check if the second range is fully contained within the first.
    :param r1_min: The minimum of the first range.
    :param r1_max: The maximum of the first range.
    :param r2_min: The minimum of the second range.
    :param r2_max: The maximum of the second range.
    :return: True if the second range is fully contained within the first.
    """
    # Check if one range is fully contained within the other.
    return (r1_min <= r2_min and r2_max <= r1_max) or (r2_min <= r1_min and r1_max <= r2_max)


def overlaps(r1_min: int, r1_max: int, r2_min: int, r2_max: int) -> bool:
    """
    Check if the two ranges overlap.
    :param r1_min: The minimum of the first range.
    :param r1_max: The maximum of the first range.
    :param r2_min: The minimum of the second range.
    :param r2_max: The maximum of the second range.
    :return: True if the two ranges overlap.
    """
    # Check if the two ranges overlap.
    return (r1_min <= r2_min <= r1_max) or (r2_min <= r1_min <= r2_max)


solution = sum([int(is_fully_contained(*get_min_max_ranges(line))) for line in split_input])
print(f'part1: {solution}')


solution = sum([int(overlaps(*get_min_max_ranges(line))) for line in split_input])
print(f'part2: {solution}')
