import csv
import step09

def spot(header, rows):
    """
    Identifies rows that cannot be trusted for estimation.
    We define 'untrustworthy' as rows that are extreme outliers in the 
    input space, making them 'unlike anyone we have employed'.
    We reuse the logic from step09 which identifies rows with extreme 
    numeric values (Z-score > 3).
    """
    return step09.spot(header, rows)

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
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    suspicious_indices = spot(header, rows)
    
    print("Analysis: Identifying records that cannot be trusted for estimation.")
    print("These records represent employees 'unlike anyone we have employed' due to extreme input values.")
    print(f"Total suspicious records found: {len(suspicious_indices)}")
    print("Top 5 most suspicious row indices:")
    for i in range(min(5, len(suspicious_indices))):
        print(f"- Row {suspicious_indices[i]}")
