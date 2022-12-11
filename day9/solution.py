"""
Advent of Code 2022: day 9
"""
import os

input_file = os.path.join(os.path.dirname(__file__), 'input.txt')
split_input = open(input_file).read().splitlines()
commands = [command.split(' ') for command in split_input]
commands = [(x, int(y)) for x, y in commands]


def run_command(command: tuple[str, int], rope: list[tuple[int, int]],
                visited_positions: set[tuple[int, int]]) -> None:
    """
    Runs a single directional command on a rope.
    It moves the rope in the direction and adds the positions of the tail to the visited positions.
    :param command: The command to run.
    :param rope: The rope to move.
    :param visited_positions: The locations the tail has visited.
    """
    direction, distance = command

    for _ in range(distance):
        for i in range(len(rope)):
            # Move head in direction requested
            if i == 0:
                if direction == 'R':
                    rope[i] = (rope[i][0] + 1, rope[i][1])
                elif direction == 'L':
                    rope[i] = (rope[i][0] - 1, rope[i][1])
                elif direction == 'U':
                    rope[i] = (rope[i][0], rope[i][1] + 1)
                elif direction == 'D':
                    rope[i] = (rope[i][0], rope[i][1] - 1)
                continue

            # Compute difference between knot and previous knot
            diff_x = rope[i-1][0] - rope[i][0]
            diff_y = rope[i-1][1] - rope[i][1]

            # Move the knot in the direction of the previous knot
            if rope[i-1][0] == rope[i][0] or rope[i-1][1] == rope[i][1]:
                rope[i] = (rope[i][0] + int(diff_x/2),
                           rope[i][1] + int(diff_y/2))
            elif max(abs(diff_x), abs(diff_y)) > 1:
                rope[i] = (rope[i][0] + 1 if diff_x > 0 else rope[i][0] - 1,
                           rope[i][1] + 1 if diff_y > 0 else rope[i][1] - 1)

        # Record tail position
        visited_positions.add(rope[-1])


def run_commands(_commands: list[tuple[str, int]], rope_length: int = 2) -> set[tuple[int, int]]:
    """
    Runs a list of directional move commands on a rope.
    :param _commands: The commands to run.
    :param rope_length: The length of the rope.
    :return: The visited locations of the tail of the rope.
    """
    # Create rope and initialize visited positions
    rope = [(0, 0)] * rope_length
    visited_positions = {rope[-1]}

    # Run commands
    for command in _commands:
        run_command(command, rope, visited_positions)

    # Return the visited positions of the tail
    return visited_positions


print(f'part1: {len(run_commands(commands))}')
print(f'part2: {len(run_commands(commands, 10))}')
