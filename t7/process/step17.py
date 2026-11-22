import random
from statistics import median

from step07 import choose
from load import loading_data, splitting_data


if __name__ == "__main__":
    random.seed(1)
    header, rows = loading_data("pom3a.n1000.train.csv")
    _, hidden, actual = splitting_data(header, rows, test_size=min(150, len(rows)))
    size = header.index("Size")
    risk = header.index("Criticality")
    size_cutoff = median(row[size] for row in hidden)
    risk_cutoff = median(row[risk] for row in hidden)
    positions = [i for i, row in enumerate(hidden)
                 if row[size] > size_cutoff and row[risk] > risk_cutoff]
    if not positions:
        raise ValueError("No setups are above both Size and Criticality medians.")

    subgroup = [hidden[i] for i in positions]
    goals = [i for i, name in enumerate(header) if name.endswith(("+", "-"))]
    asked = set()

    def label(position):
        original = positions[position]
        if original not in asked and len(asked) >= 50:
            raise ValueError("Trial budget exhausted.")
        asked.add(original)
        return [actual[original][at] for at in goals]

    winner = positions[choose(header, subgroup, label)]
    print(f"Large, high-risk means Size > {size_cutoff:.3f} "
          f"and Criticality > {risk_cutoff:.3f} in this candidate pool.")
    print("Eligible setups:", len(subgroup))
    print("Trials used:", len(asked))
    print("Chosen position in the original candidate pool:", winner)
    print("Chosen setup:", actual[winner])
