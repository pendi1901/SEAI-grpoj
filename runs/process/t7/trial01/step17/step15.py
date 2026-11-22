from feature_comparison import differences
from load import loading_data


def blame(header, rows):
    return differences(header, rows)[:2]


if __name__ == "__main__":
    header, rows = loading_data("pom3a.n1000.train.csv")
    print("Inputs that differ most between the best and worst setups:")
    for name in blame(header, rows):
        print(f"- {name}")
