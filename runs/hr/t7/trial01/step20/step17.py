from load import loading_data, splitting_data
import random
from step07 import choose


if __name__ == "__main__":
    random.seed(1)
    header, rows = loading_data("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv")
    _, hidden, actual = splitting_data(header, rows, test_size=min(150, len(rows)))
    goals = [i for i, name in enumerate(header) if name.endswith(("+", "-"))]
    asked = set()
    role = header.index("jobRole")
    positions = [i for i, row in enumerate(hidden) if row[role] == "Laboratory Technician"]
    if not positions:
        raise ValueError("No Laboratory Technician records in this pool.")

    def label(position):
        original = positions[position]
        if original not in asked and len(asked) >= 50:
            raise ValueError("Trial budget exhausted.")
        asked.add(original)
        return [actual[original][at] for at in goals]

    winner = positions[choose(header, [hidden[i] for i in positions], label)]
    print("Eligible setups:", len(positions), "Trials:", len(asked))
    if len(asked) == len(positions):
        print("All eligible records were labelled; this run is exhaustive.")
    print("Chosen position:", winner, "Setup:", actual[winner])
