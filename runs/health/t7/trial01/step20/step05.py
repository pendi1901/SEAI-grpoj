from feature_comparison import differences
from load import loading_data

def blame(header, rows) : 
    return differences(header, rows)

if __name__ == "__main__":
    header, rows = loading_data("Health-ClosedIssues0000.n1000.train.csv")
    print(blame(header, rows))