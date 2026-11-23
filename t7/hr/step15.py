from feature_comparison import differences
from load import loading_data


def blame(header, rows):
    return differences(header, rows, limit=None)[-2:]


if __name__ == "__main__":
    header, rows = loading_data("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv")
    print("Inputs with the smallest differences between long and short stays:")
    for name in blame(header, rows):
        print(f"- {name}")

    print("Small differences do not prove that a field is useless.")
