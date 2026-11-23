from load import loading_data, splitting_data
from statistics import mean
from step02 import guess


if __name__ == "__main__":
    header, rows = loading_data("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv")
    train, test, _ = splitting_data(header, rows, test_size=100)
    department = header.index("department")
    overtime = header.index("overTime")
    sales = []
    changed = []
    for row in test:
        if row[department] == "Sales":
            sales.append(row)
            copy = row.copy()
            copy[overtime] = "No"
            changed.append(copy)
    if sales:
        before = guess(header, train, sales)
        after = guess(header, train, changed)
        print("Sales employees compared:", len(sales))
        print(f"Predicted YearsAtCompany: {mean(before):.3f} -> {mean(after):.3f}")
        print("This compares model estimates; it does not prove overtime causes shorter stays.")
    else:
        print("No Sales employees in this sample.")
