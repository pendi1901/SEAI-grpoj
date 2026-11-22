import csv
import step09

def spot(header, rows):
    """
    Identifies rows that are 'unlike anyone we have employed'.
    We define this as rows that have input values significantly different
    from the historical distribution (outliers).
    
    We reuse the logic from step09, which calculates z-scores for numeric
    input columns and flags rows with extreme values.
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
    
    print("Trust Analysis: Identifying 'Unusual' Hires")
    if not suspicious_indices:
        print("All records appear consistent with historical data.")
    else:
        print(f"Detected {len(suspicious_indices)} records that are statistically 'unlike' our history.")
        print("Our estimates for these specific employees may be less reliable.")
        print("Top 5 most unusual row indices:")
        for idx in suspicious_indices[:5]:
            print(f" - Row {idx}")
