import ezr
from itertools import islice

from step08 import fix
from load import loading_data, splitting_data
from neighbours import average_nearby_neighbours
from recommendations import candidate_changes


if __name__ == "__main__":
    header, rows = loading_data("Health-ClosedIssues0000.n1000.train.csv")
    train, hidden, actual = splitting_data(header, rows)
    error = header.index("MRE-")

    def error_value(row):
        return row[error]

    def observed_error(position):
        return error_value(actual[position])

    worst = max(range(len(actual)), key=observed_error)
    original = hidden[worst]
    controls = {}
    table = ezr.Tbl([header] + train)
    for column in table.x:
        values = []
        for row in train:
            if row[column.at] != "?":
                values.append(row[column.at])
        if isinstance(column, ezr.Num):
            controls[column.txt] = (min(values), max(values))
        else:
            controls[column.txt] = list(dict.fromkeys(values))

    error_header = [
        name + "X" if name.endswith(("+", "-")) and name != "MRE-" else name
        for name in header
    ]
    table = ezr.Tbl([header] + train)

    def predicted_error(row):
        return average_nearby_neighbours(table, train, row, error_value)

    before = after = predicted_error(original)
    changes = {}
    changed = original.copy()
    candidates = candidate_changes(error_header, train, original, controls)
    for suggestion in islice(candidates, 10):
        for name, value in suggestion.items():
            candidate = original.copy()
            candidate[header.index(name)] = value
            estimate = predicted_error(candidate)
            if estimate < after:
                after = estimate
                changes = {name: value}
                changed = candidate

    for name, value in changes.items():
        at = header.index(name)
        print(f"{name}: {original[at]} -> {value}")

    print("Settings changed:", len(changes))
    print(f"Predicted MRE-: {before:.4f} -> {after:.4f} (change {after - before:+.4f})")
    print("Neighbour estimates, not measured outcomes; suggestions target forecast error alone.")
    if after >= before:
        print("No candidate predicts lower MRE; keep the current setup.")
