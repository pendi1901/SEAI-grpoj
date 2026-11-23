from feature_comparison import differences
from load import loading_data

def blame(header, rows) : 
    return differences(header, rows)

if __name__ == "__main__":
    header, rows = loading_data("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv")
    print(blame(header, rows))