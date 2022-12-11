"""
Advent of Code 2022: day 10
"""
import os

from collections import deque


def determine_signal(_instructions: deque[str]) -> list[int]:
    """
    Computes the signal per cycle based on the given instructions.
    :param _instructions: The signal instructions given.
    :return: The resulting signal.
    """
    # Initialize the signal with X=1
    _signal: list[int] = [1]

    # Process all instructions
    while len(_instructions) > 0:
        instruction = _instructions.popleft()

        # Wait one cycle
        if instruction == 'noop':
            _signal.append(_signal[-1])
            continue

        # Wait two cycles and increment signal with X
        x_to_add = int(instruction.split(' ')[1])
        _signal.extend([_signal[-1], _signal[-1] + x_to_add])

    return _signal


def get_signal_strength(_signal: list[int], cycle: int) -> int:
    """
    Computes the signal strength at the given cycle.
    :param _signal: The signal in question.
    :param cycle: The cycle to compute the signal strength for.
    :return: The signal strength at the given cycle.
    """
    return _signal[cycle-1] * cycle


def render_CRT(_signal: list[int]) -> None:
    """
    Renders the signal on the CRT.
    :param _signal: The signal to render.
    """
    # 40x6 CRT display
    for cycle in range(240):
        curr_X = _signal[cycle]

        if (cycle + 1) % 40 == 1:
            print('\n', end='')

        # Render 3 pixel wide sprite if intersection is found
        if curr_X - 1 <= cycle % 40 <= curr_X + 1:
            print('█', end='')  # instead of '#' for better readability
            continue

        # Render background
        print(' ', end='')  # instead of '.' for better readability


# Common
input_file = os.path.join(os.path.dirname(__file__), 'input.txt')
instructions: deque[str] = deque(open(input_file).read().splitlines())
signal = determine_signal(instructions)

# Part 1
signal_strengths = [get_signal_strength(signal, c) for c in range(20, 221, 40)]
print(f'Part 1: {sum(signal_strengths)}')

# Part 2
print(f'Part 2:')
render_CRT(signal)
