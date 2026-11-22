from load import loading_data, splitting_data
import random
from statistics import median
from step07 import choose


if __name__ == "__main__":
    random.seed(1)
    header, rows = loading_data("Health-ClosedIssues0000.n1000.train.csv")
    _, hidden, actual = splitting_data(header, rows, test_size=min(150, len(rows)))
    goals = [i for i, name in enumerate(header) if name.endswith(("+", "-"))]
    asked = set()
    count, depth = header.index("N_estimators"), header.index("Max_depth")
    count_limit = median(row[count] for row in hidden)
    depth_limit = median(row[depth] for row in hidden)
    positions = [i for i, row in enumerate(hidden)
                 if row[count] <= count_limit and row[depth] <= depth_limit]
    if not positions:
        raise ValueError("No setups meet both size limits.")

    def label(position):
        original = positions[position]
        if original not in asked and len(asked) >= 50:
            raise ValueError("Trial budget exhausted.")
        asked.add(original)
        return [actual[original][at] for at in goals]

    winner = positions[choose(header, [hidden[i] for i in positions], label)]
    print("Size caps:", count_limit, "trees and depth", depth_limit)
    print("Eligible setups:", len(positions), "Trials:", len(asked))
    print("Chosen position:", winner, "Setup:", actual[winner])
    print("Size limits are proxies; nightly runtime feasibility has not been measured.")
