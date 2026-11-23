import csv
import step09

def spot(header, rows):
    """
    Returns the indices of rows that are most suspicious.
    We reuse the logic from step09 which identifies outliers in numeric 
    columns by calculating the sum of absolute deviations from the median.
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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    suspicious_indices = spot(header, rows)
    
    print("Analysis: When can our estimates for new hires not be trusted?")
    print("Our estimates are unreliable when the input data is anomalous or contains errors.")
    print("The following rows are the most suspicious (potential data entry errors):")
    for idx in suspicious_indices[:5]:
        print(f"- Row {idx} (High deviation from typical employee metrics)")
    print("\nIf a new hire's profile is similar to these rows, our model's predictions will be untrustworthy.")
