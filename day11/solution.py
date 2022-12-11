"""
Advent of Code 2022: day 11
"""
import operator
from collections import deque
from functools import reduce


class Monkey:
    """Monkey class, represents a monkey in this problem."""
    def __init__(self, op: operator, constant: int | str,
                 divider: int, modulo: int, items: list[int] = None) -> None:
        """
        Initialize a monkey object.,
        :param op: The operator used to modify the worry level.
        :param constant: The constant used in the worry level modification (or 'old' to use the old worry level).
        :param divider: The constant used to divide the worry level.
        :param modulo: The modulo test condition.
        :param items: The starting items of the monkey.
        """
        self._operator: operator = op
        self._constant: int | str = constant
        self._divider: int = divider
        self._modulo: int = modulo
        self._monkey_if_true: Monkey | None = None
        self._monkey_if_false: Monkey | None = None
        self._items: deque[int] = deque(items if items else [])
        self._inspect_count: int = 0
        self._modulo_optimizer: int | None = None

    @property
    def inspect_count(self) -> int:
        """Get the number of items inspected by this monkey.
        :return: The number of items inspected by this monkey.
        """
        return self._inspect_count

    @property
    def modulo(self) -> int:
        """
        Get the modulo test condition.
        :return: The modulo test condition.
        """
        return self._modulo

    @property
    def modulo_optimizer(self) -> int | None:
        """
        Get the modulo optimizer.
        :return: The modulo optimizer.
        """
        return self._modulo_optimizer

    @modulo_optimizer.setter
    def modulo_optimizer(self, optimizer: int) -> None:
        """
        Set the modulo optimizer.
        :param optimizer: The modulo optimizer.
        """
        self._modulo_optimizer = optimizer

    @property
    def monkey_if_true(self) -> 'Monkey | None':
        """
        Get the monkey to use if the worry level is a multiple of the modulo.
        :return: The monkey, or None if not set.
        """
        return self._monkey_if_true

    @monkey_if_true.setter
    def monkey_if_true(self, monkey: 'Monkey') -> None:
        """
        Set the monkey to use if the worry level is a multiple of the modulo.
        :param monkey: The monkey to use.
        """
        self._monkey_if_true = monkey

    @property
    def monkey_if_false(self) -> 'Monkey | None':
        """
        Get the monkey to use if the worry level is not a multiple of the modulo.
        :return: The monkey, or None if not set.
        """
        return self._monkey_if_false

    @monkey_if_false.setter
    def monkey_if_false(self, monkey: 'Monkey') -> None:
        """
        Set the monkey to use if the worry level is not a multiple of the modulo.
        :param monkey: The monkey to use.
        """
        self._monkey_if_false = monkey

    def add_item(self, item: int) -> None:
        """
        Add an item to the monkey.
        :param item: The item to add.
        """
        self._items.append(item)

    def has_items(self) -> bool:
        """
        Check if the monkey has items to inspect.
        :return: True if the monkey has items to inspect, False otherwise.
        """
        return len(self._items) > 0

    def inspect_item(self) -> None:
        """Inspect the first item the monkey holds."""
        self._inspect_count += 1

        # Modify the worry level
        worry_level = self._items.popleft()
        worry_level = self._operator(worry_level, self._constant if isinstance(self._constant, int) else worry_level)
        worry_level //= self._divider

        # Optimize the worry level
        if self._modulo_optimizer:
            worry_level %= self._modulo_optimizer

        # Worry level meets test condition
        if worry_level % self._modulo == 0:
            self._monkey_if_true.add_item(worry_level)
            return

        # Worry level does not meet test condition
        self._monkey_if_false.add_item(worry_level)


def parse_monkey(monkey: str, divider: int = 1) -> tuple[Monkey, int, int]:
    """
    Parse a monkey from a string.
    :param monkey: The string representing the monkey.
    :param divider: The divider to use for the worry level.
    :return: A tuple containing the monkey, and the indices of monkeys for the test condition.
    """
    lines: list[str] = monkey.splitlines()
    ops = {'+': operator.add, '*': operator.mul}

    # Parse the monkey parameters
    starting_items = [int(item) for item in lines[1].split(': ')[-1].split(', ')]

    # Parse the operator and constant (number or 'old')
    op, constant = lines[2].split('= old ')[-1].split(' ')
    op = ops[op]
    constant = int(constant) if all(c.isdigit() for c in constant) else constant

    # Parse the remaining parameters
    modulo = int(lines[3].split(' ')[-1])
    if_true = int(lines[4].split(' ')[-1])
    if_false = int(lines[5].split(' ')[-1])

    # Create the monkey and return
    return Monkey(op, constant, divider, modulo, items=starting_items), if_true, if_false


def assign_monkey_relationships(_monkeys: list[tuple[Monkey, int, int]]) -> list[Monkey]:
    """
    Assigns the monkey relationships presented in the input.
    :param _monkeys: The monkeys to assign relationships to, and their defined relationships.
    :return: The list of monkeys.
    """
    monkey_list: list[Monkey] = []

    # Assign the related monkeys to each monkey
    for monkey, if_true_idx, if_false_idx in _monkeys:
        monkey.monkey_if_true = _monkeys[if_true_idx][0]
        monkey.monkey_if_false = _monkeys[if_false_idx][0]
        monkey_list.append(monkey)

    return monkey_list


def setup_game(part: int) -> list[Monkey]:
    """
    Set up the game for part 1 or part 2.
    :param part: The part number of the game.
    :return: The list of monkeys in the game.
    """
    divider: int = 3 if part == 1 else 1

    # Parse the monkeys and assign their relationships
    _monkeys: list[str] = open('input.txt').read().split('\n\n')
    _monkeys: list[tuple[Monkey, int, int]] = [parse_monkey(monkey, divider) for monkey in _monkeys]
    _monkeys: list[Monkey] = assign_monkey_relationships(_monkeys)

    # Set the modulo optimizer for the monkeys
    modulo_optimizer: int = reduce(operator.mul, [monkey.modulo for monkey in _monkeys])
    for monkey in _monkeys:
        monkey.modulo_optimizer = modulo_optimizer

    return _monkeys


def perform_rounds(_monkeys: list[Monkey], rounds: int) -> None:
    """
    Perform the rounds of the game.
    :param _monkeys: The monkeys to play with.
    :param rounds: The number of rounds to play.
    """
    # Perform the rounds
    for r in range(rounds):
        # Each monkey inspects all its items
        for monkey in _monkeys:
            while monkey.has_items():
                monkey.inspect_item()


monkeys: list[Monkey] = setup_game(1)
perform_rounds(monkeys, 20)
top1_monkey, top2_monkey = sorted([monkey.inspect_count for monkey in monkeys])[::-1][:2]
print(f'part1: {top1_monkey * top2_monkey}')


monkeys: list[Monkey] = setup_game(2)
perform_rounds(monkeys, 10000)
top1_monkey, top2_monkey = sorted([monkey.inspect_count for monkey in monkeys])[::-1][:2]
print(f'part2: {top1_monkey * top2_monkey}')
