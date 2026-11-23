import ezr
from itertools import islice

from step08 import fix  # Entry point used by the scorer.
from load import loading_data, splitting_data
from neighbours import average_nearby_neighbours
from recommendations import candidate_changes


if __name__ == "__main__":
    header, rows = loading_data("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv")
    train, hidden, actual = splitting_data(header, rows)
    tenure = header.index("YearsAtCompany+")

    def tenure_value(row):
        return row[tenure]

    def observed_tenure(position):
        return tenure_value(actual[position])

    worst = min(range(len(actual)), key=observed_tenure)
    original = hidden[worst]
    controls = {}
    table = ezr.Tbl([header] + train)
    for column in table.x:
        if column.txt not in ["overTime", "businessTravel", "TrainingTimesLastYear"]:
            continue
        values = []
        for row in train:
            if row[column.at] != "?":
                values.append(row[column.at])
        if isinstance(column, ezr.Num):
            controls[column.txt] = (min(values), max(values))
        else:
            controls[column.txt] = list(dict.fromkeys(values))

    tenure_header = [
        name + "X" if name.endswith(("+", "-")) and name != "YearsAtCompany+" else name
        for name in header
    ]
    table = ezr.Tbl([header] + train)

    def predicted_tenure(row):
        return average_nearby_neighbours(table, train, row, tenure_value)

    before = after = predicted_tenure(original)
    changes = {}
    changed = original.copy()
    candidates = candidate_changes(tenure_header, train, original, controls)
    for suggestion in islice(candidates, 10):
        candidate = original.copy()
        for name, value in suggestion.items():
            candidate[header.index(name)] = value
        estimate = predicted_tenure(candidate)
        if estimate > after:
            after, changes, changed = estimate, suggestion, candidate

    for name, value in changes.items():
        at = header.index(name)
        print(f"{name}: {original[at]} -> {value}")

    for name in ["PercentSalaryHike", "StockOptionLevel"]:
        at = header.index(name)
        print(f"{name} unchanged: {changed[at]}")
    print(f"Predicted YearsAtCompany+: {before:.4f} -> {after:.4f} (change {after - before:+.4f})")
    print("Neighbour estimates, not measured outcomes; suggestions target years at the company.")
    if after <= before:
        print("No candidate predicts longer tenure; keep the current setup.")
