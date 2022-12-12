"""
Advent of Code 2022: day 12
"""
import os

from collections import deque


# Read input for problem
input_file = os.path.join(os.path.dirname(__file__), 'input.txt')
split_input = open(input_file).read().splitlines()

# Constants used in solution
MARKER_START: str = 'S'
MARKER_GOAL: str = 'E'
MARKER_H: dict[str, int] = {
    MARKER_START: ord('a'),
    MARKER_GOAL: ord('z'),
}


def find_start_coord(height_map: list[str], marker: str) -> tuple[int, int]:
    """
    Find the starting coordinate of the height map, defined by a marker.
    :param height_map: The height map of the environment.
    :param marker: The start location marker to look for.
    :return: The found starting coordinate.
    """
    for r, row in enumerate(height_map):
        for c, h in enumerate(row):
            if h == marker:
                return r, c

    raise Exception('No starting coordinate found.')


def least_steps_to_goal(height_map: list[str], reverse: bool = False) -> int:
    """
    Find the least amount of steps to reach a goal from a starting position.
    :param height_map: The height map of the environment.
    :param reverse: Whether to reverse the path finding.
    :return: The least amount of steps needed to reach the goal.
    """
    # Find the starting coordinate and target for the path finding (start at goal for reversed)
    target: str = MARKER_START if reverse else MARKER_GOAL
    start_r, start_c = find_start_coord(height_map, MARKER_GOAL if reverse else MARKER_START)

    # Queue with each entry: (row, column, steps taken)
    queue: deque[tuple[int, int, int]] = deque([(start_r, start_c, 0)])
    visited: set[tuple[int, int]] = {(start_r, start_c)}

    # Perform breadth-first search
    while len(queue) > 0:
        r, c, steps = queue.popleft()

        # Reached goal destination
        if height_map[r][c] == target:
            return steps

        # Check all 4 directions
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            new_r, new_c = r + dr, c + dc

            # Out of bounds row
            if new_r < 0 or new_r > len(height_map) - 1:
                continue

            # Out of bounds column
            if new_c < 0 or new_c > len(height_map[0]) - 1:
                continue

            # Already visited
            if (new_r, new_c) in visited:
                continue

            cur_h = MARKER_H.get(height_map[r][c], ord(height_map[r][c]))
            adj_h = MARKER_H.get(height_map[new_r][new_c], ord(height_map[new_r][new_c]))

            # Reverse height comparison
            adj_h, cur_h = (cur_h, adj_h) if reverse else (adj_h, cur_h)

            # Height difference too large
            if adj_h > cur_h + 1:
                continue

            # Go to adjacent cell
            visited.add((new_r, new_c))
            queue.append((new_r, new_c, steps + 1))

    raise Exception('No path to goal found, BFS queue is empty.')


print(f'part1: {least_steps_to_goal(split_input)}')
split_input = [line.replace('a', 'S') for line in split_input]
print(f'part2: {least_steps_to_goal(split_input, reverse=True)}')
