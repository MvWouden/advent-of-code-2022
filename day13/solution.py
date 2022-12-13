"""
Advent of Code 2022: day 13
"""
import os
import json

from itertools import chain


# Add easier type support for packets and packet pairs
PacketInner = int | type([]) | list['PacketInner']
Packet = list[PacketInner]
PacketPair = tuple[Packet, Packet]


def quick_sort(container: list[Packet]) -> list[Packet]:
    """
    Sorts a list of packets using the quick sort algorithm.
    :param container: The list of packets.
    :return: The sorted list of packets.
    """
    # Base case
    if not container:
        return []

    # Get the first packet
    pivot = container[0]

    # Get both the left and right sides of the pivot
    left = [x for x in container[1:] if are_ordered_correctly((x, pivot))]
    right = [x for x in container[1:] if not are_ordered_correctly((x, pivot))]

    # Recursively sort the left and right sides
    return quick_sort(left) + [pivot] + quick_sort(right)


def parse_packet(packet: str) -> Packet:
    """
    Parses the string representation into a packet.
    Uses 'json.loads' instead of eval for safety.
    :param packet: The string representation of the packet.
    :return: The parsed packet.
    """
    return json.loads(packet)


def parse_packet_pair(packet_pair: list[str]) -> PacketPair:
    """
    Parses two string representations of packets into a packet pair.
    :param packet_pair: The two string representations of the packets.
    :return: The packet pair.
    """
    return parse_packet(packet_pair[0]), parse_packet(packet_pair[1])


def are_ordered_correctly(packet_pair: PacketPair, idx: int = 0) -> bool | None:
    """
    Checks if a packet pair is ordered correctly.
    :param packet_pair: The packet pair.
    :param idx: The index currently being checked for ordering.
    :return: None if no decision can be made, otherwise True or False.
    """
    packet1, packet2 = packet_pair

    # At least one of the packets is empty
    if idx > len(packet1) - 1:
        # No decision can be made if both packets are empty
        # If only packet 1 is empty, the pair is ordered correctly
        return None if idx > len(packet2) - 1 else True

    # Only packet 2 is empty, hence the pair is NOT ordered correctly
    if idx > len(packet2) - 1:
        return False

    p1, p2 = packet1[idx], packet2[idx]

    # Both packets are integers
    if isinstance(p1, int) and isinstance(p2, int):

        # No decision can be made, check the next index
        if p1 == p2:
            return are_ordered_correctly(packet_pair, idx + 1)

        # Different values, determine if ordered correctly
        return p1 < p2

    # Current value of packet 1 is an integer and needs to be converted
    if isinstance(p1, int):
        p1 = [p1]

    # Current value of packet 2 is an integer and needs to be converted
    elif isinstance(p2, int):
        p2 = [p2]

    # Both packets are lists
    current: bool = are_ordered_correctly((p1, p2))
    return current or (current is None and are_ordered_correctly(packet_pair, idx + 1))


# Read input for problem
input_file: str = os.path.join(os.path.dirname(__file__), 'input.txt')
pairs: list[str] = open(input_file).read().split('\n\n')
packet_pairs: list[PacketPair] = [parse_packet_pair(pair.splitlines()) for pair in pairs]

# Find pairs in right order
pairs_in_right_order: list[int] = [i + 1 for i, packet_pair in enumerate(packet_pairs)
                                   if are_ordered_correctly(packet_pair)]

print(f'part1: {sum(pairs_in_right_order)}')

# Flatten packet pairs and introduce divider packets
packets: list[Packet] = list(chain.from_iterable(packet_pairs))
packets.extend([[[2]], [[6]]])

# Sort packets
packets = quick_sort(packets)

# Find divider packets and compute decoder key
idx_divider_1 = packets.index([[2]]) + 1
idx_divider_2 = packets.index([[6]]) + 1
decoder_key = idx_divider_1 * idx_divider_2

print(f'part2: {decoder_key}')
