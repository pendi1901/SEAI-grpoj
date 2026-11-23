from load import loading_data, splitting_data
from step06 import justify


if __name__ == "__main__":
    header, rows = loading_data("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv")
    train, hidden, _ = splitting_data(header, rows)
    current = hidden[0]
    biggest = current.copy()
    pay_index = header.index("PercentSalaryHike")
    biggest[pay_index] = max(row[pay_index] for row in train)
    print("PercentSalaryHike:", current[pay_index], "->", biggest[pay_index])
    for name, row in [("Current", current), ("Maximum pay rise", biggest)]:
        p, reason = justify(header, train, row)
        print(f"{name}: estimated fraction beaten {p:.1%}; {reason}")
    print("A prediction change does not prove that increasing pay will cause longer stays.")
