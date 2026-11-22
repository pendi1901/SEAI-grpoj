from load import loading_data, splitting_data
from step02 import guess


if __name__ == "__main__":
    header, rows = loading_data("Health-ClosedIssues0000.n1000.train.csv")
    train, hidden, _ = splitting_data(header, rows)
    original = hidden[0]
    changed = original.copy()
    at = header.index("N_estimators")
    minimum = min(row[at] for row in train)
    changed[at] = max(minimum, int(original[at] / 2))
    before, after = guess(header, train, [original, changed])
    print(f"Tree count: {original[at]} -> {changed[at]} (capped at training minimum)")
    print(f"Estimated MRE: {before:.4f} -> {after:.4f}; change {after-before:+.4f}")
    print("Tree count is a size proxy; this does not measure runtime or guarantee worse accuracy.")
