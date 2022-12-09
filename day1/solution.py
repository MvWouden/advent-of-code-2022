"""
Advent of Code 2022: day 1
"""
calories = [
    sum([                                 # Sum up cluster
        int(calories)                     # Transform to int
        for calories in elf.splitlines()  # Split single caloric items
        if calories                       # Ignore empty string
    ])
    for elf in open('input.txt').read().split('\n\n')  # Divide input into clusters
]
calories.sort()

# Reverse and take top 3
top3 = calories[:-4:-1]

print(f'part1: {top3[0]}')
print(f'part2: {sum(top3)}')
