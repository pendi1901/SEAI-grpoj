from streamer import accepting_arow
import random
from load import loading_data

def flow(header, row, seen):
    return accepting_arow(header, row, seen)

if __name__ == "__main__":
    header, rows = loading_data("Health-ClosedIssues0000.n1000.train.csv")
    randomizer = random.Random(1).sample(rows, 100)
    seen = []
    selected = randomizer[-1]
    for row in randomizer:
        if flow(header, row, seen):
            selected = row
            break
        seen.append(row)

    print(selected)
