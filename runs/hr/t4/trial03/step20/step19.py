import csv
import math
from step09 import spot as base_spot

def spot(header, rows):
    """
    Identifies rows that are 'unlike anyone we have employed'.
    We use the Mahalanobis distance logic from step09 to find rows that 
    deviate significantly from the numeric feature distribution of the 
    entire dataset. These are the rows where our model's estimates 
    cannot be trusted.
    """
    # The logic in step09 calculates the sum of squared z-scores for 
    # numeric features, which is a robust way to identify outliers 
    # (rows unlike the rest of the population).
    return base_spot(header, rows)

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    suspicious = spot(header, rows)
    
    print("Trust Analysis: Identifying records unlike existing employees.")
    print("Our model's estimates cannot be trusted for the following rows,")
    print("as they represent outliers in our historical data:")
    for idx in suspicious[:5]:
        print(f"- Row {idx}: Significant deviation from historical numeric feature norms.")
    
    exit(0)
