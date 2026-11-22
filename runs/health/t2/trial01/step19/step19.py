import csv
import step09

def spot(header, rows):
    """
    Identifies rows that are 'failed runs' or 'outliers' based on input values.
    This reuses the logic from step09, which calculates Z-scores for numeric 
    inputs to detect extreme values that deviate from the population.
    """
    return step09.spot(header, rows)

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        rows = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = []
                for i, val in enumerate(row):
                    if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                     'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                        processed_row.append(float(val))
                    else:
                        processed_row.append(val)
                rows.append(processed_row)
        
        suspicious_indices = spot(header, rows)
        
        print("Analysis: Identifying configurations that are far outside the norm.")
        if suspicious_indices:
            print(f"I found {len(suspicious_indices)} configurations that contain extreme or unusual input values.")
            print("These are the most suspicious row indices (most extreme first):")
            print(suspicious_indices[:10])
            print("\nRecommendation: Review these configurations for data entry errors or extreme parameter settings.")
        else:
            print("No suspicious configurations were found.")
            
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
