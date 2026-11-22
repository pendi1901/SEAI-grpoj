from load import loading_data, splitting_data
import random
import sys
from step10 import race


if __name__ == "__main__":
    random.seed(1)
    header, rows = loading_data("Health-ClosedIssues0000.n1000.train.csv")
    _, hidden, actual = splitting_data(header, rows, test_size=min(150, len(rows)))
    goals = [i for i, name in enumerate(header) if name.endswith(("+", "-"))]
    asked = set()

    def label(position):
        if position not in asked and len(asked) >= 50:
            raise ValueError("Trial budget exhausted.")
        asked.add(position)
        return [actual[position][at] for at in goals]
    result = race(header, hidden, label)
    chosen = actual[result["row"]]
    print("Source-project shared-budget race:", result, "Trials:", len(asked))
    if len(sys.argv) < 2:
        print("Cross-project comparison requires a second project's training CSV as an argument.")
        print("No second-project result is claimed from this dataset alone.")
    else:
        other_header, other = loading_data(sys.argv[1])
        if other_header != header:
            raise ValueError("The second project must use the same columns.")
        inputs = [i for i, name in enumerate(header) if not name.endswith(("+", "-", "X"))]
        matches = [row for row in other if all(row[i] == chosen[i] for i in inputs)]
        if not matches:
            print("The chosen settings were not tried on the second project; transfer is unmeasured.")
        else:
            error = header.index("MRE-")
            transferred = sum(row[error] for row in matches) / len(matches)
            random_mean = sum(row[error] for row in other) / len(other)
            print(f"Second-project MRE: chosen settings {transferred:.4f}; random-row expectation {random_mean:.4f}")
            print("Chosen settings beat random in mean MRE:", transferred < random_mean)
