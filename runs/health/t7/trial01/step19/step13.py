from load import loading_data
from statistics import mean
from itertools import combinations
from step03 import certify


if __name__ == "__main__":
    header, rows = loading_data("Health-ClosedIssues0000.n1000.train.csv")
    rule, error = header.index("criterion"), header.index("MRE-")
    groups = {}
    for row in rows:
        groups.setdefault(row[rule], []).append(row[error])
    names = sorted(groups)
    print(f"The training data contains {len(names)} criteria; comparing each pair.")
    for name in names:
        print(name, "mean MRE:", round(mean(groups[name]), 4))
    for first, second in combinations(names, 2):
        print(first, "vs", second, "similar apart from noise:",
              certify(groups[first], groups[second]))
    print("Other settings also vary; this is an association, not a controlled rule comparison.")
