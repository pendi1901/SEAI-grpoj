import ezr
from itertools import islice

from step08 import fix
from load import loading_data, splitting_data
from neighbours import average_nearby_neighbours
from recommendations import candidate_changes


if __name__ == "__main__":
    header, rows = loading_data("pom3a.n1000.train.csv")
    train, hidden, actual = splitting_data(header, rows)
    idle = header.index("Idle-")

    def idle_value(row):
        return row[idle]

    def observed_idle(position):
        return idle_value(actual[position])

    worst = max(range(len(actual)), key=observed_idle)
    original = hidden[worst]
    controls = {}
    for name in ["Plan", "Culture"]:
        at = header.index(name)
        values = [row[at] for row in train if row[at] != "?"]
        controls[name] = (min(values), max(values))

    idle_header = [
        name + "X" if name.endswith(("+", "-")) and name != "Idle-" else name
        for name in header
    ]
    table = ezr.Tbl([header] + train)

    def predicted_idle(row):
        return average_nearby_neighbours(table, train, row, idle_value)

    before = after = predicted_idle(original)
    changes = {}
    changed = original.copy()
    candidates = candidate_changes(idle_header, train, original, controls)
    for suggestion in islice(candidates, 10):
        candidate = original.copy()
        for name, value in suggestion.items():
            candidate[header.index(name)] = value
        estimate = predicted_idle(candidate)
        if estimate < after:
            after, changes, changed = estimate, suggestion, candidate

    for name, value in changes.items():
        at = header.index(name)
        print(f"{name}: {original[at]:.3f} -> {value:.3f}")

    team = header.index("Team Size")
    print(f"Team Size unchanged: {changed[team]:.3f}")
    print(f"Predicted Idle-: {before:.4f} -> {after:.4f} (change {after - before:+.4f})")
    print("Neighbour estimates, not measured outcomes; suggestions target Idle alone.")
    if after >= before:
        print("No candidate predicts lower Idle; keep the current setup.")
