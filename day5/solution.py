"""
Advent of Code 2022: day 5
"""
import re
from collections import deque


# Read in input
starting_stacks, procedure = open('input.txt').read().split('\n\n')
steps = procedure.split('\n')


def parse_starting_stacks(starting_stacks: str) -> list[deque]:
    """
    Parse the starting stack states.
    :param starting_stacks: The starting representation.
    :return: A list of stacks.
    """
    lines = starting_stacks.split('\n')
    n_stacks = int(starting_stacks[-1].split(' ')[-1])
    stacks = [deque() for _ in range(n_stacks)]

    # Parse lines possibly containing stacks
    for line in lines[::-1][1:]:
        # Parse individual stacks in line
        for i in range(n_stacks):
            # Index where crate character would be present
            char_idx = 1 + i*4

            # Out of bounds
            if char_idx > len(line) - 1:
                continue

            stack_char = line[char_idx]

            # Crate present
            if stack_char != ' ':
                stacks[i].append(stack_char)

    return stacks


def parse_step(step: str) -> tuple[int, int, int]:
    """
    Parse a single step of the procedure.
    :param step: The representation of a step.
    :return: The number of moves, and the from- and to-stack.
    """
    result = re.search(r'move (\d+) from (\d+) to (\d+)', step)

    # Validate step format
    if not result or len(result.groups()) != 3:
        raise ValueError(f'Invalid step format: {step}')

    # Convert instructions to int
    x, y, z = result.groups()
    return int(x), int(y), int(z)


def perform_steps_one_by_one(stacks: list[deque], n: int, from_stack: int, to_stack: int) -> None:
    """
    Perform a single step of the procedure, while moving crates one by one.
    :param stacks: The current stack states.
    :param n: The number of crates to move.
    :param from_stack: The stack to move crates from.
    :param to_stack: The stack to move crates to.
    :return: The new stack states.
    """
    for i in range(n):
        stacks[to_stack-1].append(stacks[from_stack-1].pop())


def perform_steps(stacks: list[deque], n: int, from_stack: int, to_stack: int) -> None:
    """
    Perform a single step of the procedure, while moving multiple crates at once.
    :param stacks: The current stack states.
    :param n: The number of crates to move.
    :param from_stack: The stack to move crates from.
    :param to_stack: The stack to move crates to.
    :return: The new stack states.
    """
    crates_to_move = [stacks[from_stack-1].pop() for _ in range(n)]
    stacks[to_stack-1].extend(crates_to_move[::-1])


stacks = parse_starting_stacks(starting_stacks)
[perform_steps_one_by_one(stacks, *parse_step(step)) for step in steps]
solution = ''.join([stack[-1] for stack in stacks])
print(f'part1: {solution}')


stacks = parse_starting_stacks(starting_stacks)
[perform_steps(stacks, *parse_step(step)) for step in steps]
solution = ''.join([stack[-1] for stack in stacks])
print(f'part2: {solution}')