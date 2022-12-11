import os
import time

# Get all solution folders in the current directory
days = [f for f in os.listdir('.') if os.path.isdir(f) and f.startswith('day')]

# Run and time all solutions
print('-'*22)
print(f'| {"Day":3} | {"Time elapsed":12} |')
print('-'*22)
for day in days:
    start = time.time()
    os.system(f'python3 {day}/solution.py > /dev/null')
    end = time.time()
    print(f'| {day.replace("day", ""):>3} | {end - start:>12.3f} |')
print('-'*22)

