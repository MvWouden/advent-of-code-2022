"""
Advent of Code 2022: day 14
"""
import os

from functools import reduce
from itertools import count
from operator import ior


# Read input for problem
input_file: str = os.path.join(os.path.dirname(__file__), 'input.txt')
lines: list[str] = open(input_file).read().splitlines()

# Add easier type support for points and paths
Point = tuple[int, int]
Path = set[Point]


def parse_path(line: str) -> Path:
    """
    Parse a line of input into a set of points, also called a path.
    :param line: The line of input.
    :return: The parsed path.
    """
    path: Path = set()
    prev_x, prev_y = None, None
    points = line.split(' -> ')

    # Iterate over each point in the path
    for point in points:
        # Extract the x and y coordinate of the path
        x, y = tuple(map(int, point.split(',')))

        # First point in path, add point to set
        if not prev_x or not prev_y:
            prev_x, prev_y = x, y
            path.add((x, y))
            continue

        # Point 1 should be left or atop of point 2
        p1, p2 = (x, y), (prev_x, prev_y)
        if x + prev_y > prev_x + y:
            p1, p2 = p2, p1

        if p1[0] == p2[0]:
            # Y coordinate is increasing while X coordinate is constant, interpolate and add all points
            y_interpolated = range(p2[1], p1[1] + 1)
            path.update([(p2[0], y) for y in y_interpolated])
            prev_x, prev_y = x, y
            continue

        # X coordinate is increasing while Y coordinate is constant, interpolate and add all points
        x_interpolated = range(p1[0], p2[0] + 1)
        path.update([(x, p2[1]) for x in x_interpolated])
        prev_x, prev_y = x, y

    return path


def units_before_end(solid_points: Path, part: int = 1) -> int:
    """
    Calculate the number of units before the end of the simulation is reached.
    The simulation ends when:
      - sand will start to only flow into the abyss (part 1).
      - sand has filled the maximum amount of space possible and the start point is blocked (part 2).
    :param solid_points: The points that are solid (i.e. all the paths).
    :param part: Whether to solve part 1 or part 2.
    :return: The number of sand units spawned before the end of the simulation is reached.
    """
    # Determine boundary Y coordinate
    x_coords, y_coords = zip(*solid_points)
    _, max_y = min(y_coords), max(y_coords)

    # Spawn sand units infinitely (until the simulation ends)
    for sand_units in count(start=0):
        # Spawn sand unit at the start point
        sand_unit: Point = (500, 0)

        # Maximum space filled possible is reached when the start point is blocked
        if sand_unit in solid_points:
            return sand_units

        # Flow sand unit along path
        while True:
            # Sand unit has reached the abyss
            if part == 1 and sand_unit[1] > max_y + 1:
                return sand_units

            coord_down: Point = (sand_unit[0], sand_unit[1] + 1)

            # Sand unit has reached the floor
            if part == 2 and coord_down[1] == max_y + 2:
                solid_points.add(sand_unit)
                break

            # Sand unit can flow down
            if coord_down not in solid_points:
                sand_unit = coord_down
                continue

            # Sand unit can flow diagonally left and down
            coord_left_down: Point = (sand_unit[0] - 1, sand_unit[1] + 1)
            if coord_left_down not in solid_points:
                sand_unit = coord_left_down
                continue

            # Sand unit can flow diagonally right and down
            coord_right_down: Point = (sand_unit[0] + 1, sand_unit[1] + 1)
            if coord_right_down not in solid_points:
                sand_unit = coord_right_down
                continue

            # Sand unit flow cannot continue, sand settles
            solid_points.add(sand_unit)
            break


paths: Path = reduce(ior, [parse_path(line) for line in lines])
print(f'part1: {units_before_end(paths)}')

paths: Path = reduce(ior, [parse_path(line) for line in lines])
print(f'part2: {units_before_end(paths, part=2)}')
