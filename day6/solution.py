"""
Advent of Code 2022: day 6
"""
from collections import deque


signal = open('input.txt').read()


def get_start_marker_index(signal: str, marker_len: int = 4) -> int:
    # Set up a history with max length
    history = deque(maxlen=marker_len-1)
    [history.append(None) for _ in range(marker_len-1)]

    # Go over signal to detect start marker
    for i, char in enumerate(signal):
        # Enough distinct characters, marker encountered
        if all(history) and len({char, *history}) == marker_len:
            return i + 1

        # Oldest are automatically popped due to max deque length
        history.append(char)


solution = get_start_marker_index(signal)
print(f'part1: {solution}')


solution = get_start_marker_index(signal, 14)
print(f'part2: {solution}')
