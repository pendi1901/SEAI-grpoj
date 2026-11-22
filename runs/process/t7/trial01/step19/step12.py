from step02 import guess
from load import loading_data, splitting_data


if __name__ == "__main__":
    header, rows = loading_data("pom3a.n1000.train.csv")
    train, test, _ = splitting_data(header, rows)
    original = test[0]
    changed = original.copy()
    dynamism = header.index("Dynamism")
    highest = max(row[dynamism] for row in train)
    requested = original[dynamism] * 2
    changed[dynamism] = min(requested, highest)

    if requested > highest:
        print("Dynamism capped at the highest training value.")

    print(f"Dynamism: {original[dynamism]:.3f} -> {changed[dynamism]:.3f}")
    print("Static comparison; this does not simulate a halfway change.")

    for goal in ["Cost-", "Idle-"]:
        at = header.index(goal)
        order = [at] + [i for i in range(len(header)) if i != at]
        names = [header[i] for i in order]
        training = [[row[i] for i in order] for row in train]
        scenarios = [[row[i] for i in order] for row in [original, changed]]
        before, after = guess(names, training, scenarios)
        print(f"{goal}: {before:.4f} -> {after:.4f} (change {after - before:+.4f})")
