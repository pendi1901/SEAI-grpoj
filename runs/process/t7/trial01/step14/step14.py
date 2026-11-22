from step04 import flow
from streamer import accepting_arow
from load import loading_data


if __name__ == "__main__":
    header, rows = loading_data("pom3a.n1000.train.csv")
    seen = []

    print("Streaming in file order; these rows have no weekly timestamps.")
    for position, row in enumerate(rows):
        if accepting_arow(header, row, seen, warn=True):
            print(f"Warning: row {position} is worse than the prior worst-decile cutoff.")
        seen.append(row)
