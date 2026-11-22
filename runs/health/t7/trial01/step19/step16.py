from load import loading_data, splitting_data
from step06 import justify


if __name__ == "__main__":
    header, rows = loading_data("Health-ClosedIssues0000.n1000.train.csv")
    train, hidden, _ = splitting_data(header, rows)
    current = hidden[0]
    biggest = current.copy()
    for name in ["N_estimators", "Max_depth"]:
        at = header.index(name)
        biggest[at] = max(row[at] for row in train)
        print(name, ":", current[at], "->", biggest[at])
    for name, row in [("Current", current), ("Biggest/deepest", biggest)]:
        p, reason = justify(header, train, row)
        print(f"{name}: estimated fraction beaten {p:.1%}; {reason}")
    print("Observed maxima are not machine limits; larger is not guaranteed more accurate.")
