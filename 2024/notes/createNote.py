import os
from datetime import datetime

day = str(datetime.now().day)

# Checks if the note already exists
for file in os.listdir("./"):
    if file == f"day{day:0>2}.md":
        print(f"day{day:0>2}.md already exists!")
        exit(1)

part1 = ""
part2 = ""

# Checks if the day's dir exists (doesn't check for part1.py and part2.py)
for dir in os.listdir("../code"):
    if dir != f"Day{day:0>2}":
        continue

    part1 = open(f"../code/Day{day:0>2}/part1.py").read()
    part2 = open(f"../code/Day{day:0>2}/part2.py").read()

with open(f"day{day:0>2}.md", "w") as f:
    f.write(
        f"""# [Day {day} - TITLE](https://adventofcode.com/2024/day/{day})

> [<- Previous](day{int(day) - 1:0>2}.md) | [Next ->](day{int(day) + 1:0>2}.md)

General comments about the problem

|                | Part A | Part B | Total |
| -------------- | :----: | :----: | :---: |
| Coding Time    |        |        |       |
| Execution Time |        |        |       |

## Part A

General comments about part A

> [!TIP]
> Insights on the problem

```python
{part1}
```

### Addendum

A possible lookback to improve the code's readability and efficiency

```python
# optimized, improved code
```

## Part B

General comments about part B

> [!TIP]
> Insights on the problem

```python
{part2}
```

### Addendum

A possible lookback to improve the code's readability and efficiency

```python
# optimized, improved code
```
    """
    )

    print(f"Created note day{day:0>2}.md")
