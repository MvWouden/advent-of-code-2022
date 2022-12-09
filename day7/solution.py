"""
Advent of Code 2022: day 7
"""
import re
import sys
from collections import deque


class File:
    """File class, represents a file on the system."""
    def __init__(self, name: str, size: int) -> None:
        """
        Initialize a file object.
        :param name: The name of the file.
        :param size: The file size.
        """
        self._name: str = name
        self._size: int = size

    @property
    def name(self) -> str:
        """Get the name of the file."""
        return self._name

    @property
    def size(self) -> int:
        """Get the size of the file."""
        return self._size


class Directory:
    """Directory class, represents a directory on the system."""
    def __init__(self, _name: str, _parent: 'Directory' = None) -> None:
        """
        Initialize a directory object.
        :param _name: The directory name.
        :param _parent: The parent directory, if any.
        """
        self._name: str = _name
        self._parent: Directory | None = _parent
        self._directories: dict[str, Directory] = {}
        self._files: dict[str, File] = {}
        self._size: int = 0

    def __str__(self) -> str:
        """Get the string representation of the directory."""
        return f'dir {self.name} ({self.size})'

    @property
    def name(self) -> str:
        """Get the name of the directory."""
        return self._name

    @property
    def size(self) -> int:
        """Get the size of the directory."""
        return self._size

    @property
    def directories(self) -> dict[str, 'Directory']:
        """Get the subdirectories in the directory."""
        return self._directories

    @property
    def parent(self) -> 'Directory':
        """Get the parent directory."""
        return self._parent

    def get_directory(self, _name: str) -> 'Directory':
        """
        Get a subdirectory by name.
        :param _name: The directory name.
        :return: The retrieved directory or None if it doesn't exist.
        """
        return self._directories.get(_name, None)

    def add_object(self, _object: 'File | Directory') -> None:
        """
        Add a file or subdirectory to the current directory.
        Also updates the (parent(s)) directory sizes.
        :param _object: The file or directory to add.
        """
        target_dict = self._files if isinstance(_object, File) else self._directories

        # Add the object to the current directory
        target_dict[_object.name] = _object
        self._size += _object.size

        # Update the parent directory sizes
        current_dir = self
        while current_dir.parent:
            current_dir = current_dir.parent
            current_dir._size += _object.size


def parse_commands(_commands: deque[str]) -> Directory:
    """
    Parse the commands and return the root directory.
    :param _commands: The commands to parse.
    :return: The root directory.
    """
    # Initialize the root directory
    root_dir = Directory('/')
    current_dir = root_dir

    while len(_commands) > 0:
        command = _commands.popleft()

        # Change directory to root directory
        if re.match(r'^\$ cd /$', command):
            current_dir = root_dir
            continue

        # Change directory to parent directory
        if re.match(r'^\$ cd \.\.$', command):
            current_dir = current_dir.parent
            continue

        # Change directory to a subdirectory
        if re.match(r'^\$ cd \S+$', command):
            dir_name = command.split(' ')[-1]

            # Add directory if not known yet
            if not current_dir.get_directory(dir_name):
                current_dir.add_object(Directory(dir_name, current_dir))

            # Change directory
            current_dir = current_dir.get_directory(dir_name)
            continue

        # List files in current directory
        if re.match(r'^\$ ls$', command):
            while len(_commands) > 0 and _commands[0][0] != '$':
                listing = _commands.popleft()

                # File listing
                if re.match(r'^\d+ \S+$', listing):
                    file_size, file_name = listing.split(' ')

                    # File already known
                    if current_dir.get_directory(file_name):
                        continue

                    # Add file
                    current_dir.add_object(File(file_name, int(file_size)))
                    continue

                # Directory listing
                if re.match(r'dir \S+$', listing):
                    dir_name = listing.split(' ')[-1]

                    # Directory already known
                    if current_dir.get_directory(dir_name):
                        continue

                    # Add directory
                    current_dir.add_object(Directory(dir_name, current_dir))
                    continue
            continue
    return root_dir


# Read in the system commands and parse to a directory structure
commands: deque[str] = deque(open('input.txt').read().splitlines())
start_dir: Directory = parse_commands(commands)

# Setup queue and other variables
queue: deque[Directory] = deque([start_dir])
solution1 = 0
solution2 = sys.maxsize
min_dir_size = 30_000_000 - (70_000_000 - start_dir.size)

# Traverse folders and sum directory sizes under a certain size
while len(queue) > 0:
    curr_dir = queue.popleft()

    # Meets target size for part 1
    if curr_dir.size <= 100_000:
        solution1 += curr_dir.size

    # Meets target size for part 2
    if curr_dir.size >= min_dir_size:
        solution2 = min(curr_dir.size, solution2)

    # Add subdirectories to queue
    for directory in curr_dir.directories.values():
        queue.append(directory)

print(f'part1: {solution1}')
print(f'part2: {solution2}')
