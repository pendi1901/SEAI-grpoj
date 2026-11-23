import csv
import step09

def spot(header, rows):
    """
    Identifies rows that contain input values far outside the observed range
    (i.e., things we have never seen).
    """
    # We reuse the logic from step09 which identifies outliers in the input space.
    # This effectively flags rows with values that are statistically suspicious
    # or "never seen" compared to the distribution of the training data.
    return step09.spot(header, rows)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                # Convert numeric columns to float, keep symbolic as strings
                processed = []
                for i, val in enumerate(row):
                    if header[i] in ['N_estimators', 'Min_sample_leaves', 
                                     'Min_impurity_decrease', 'Max_depth']:
                        processed.append(float(val))
                    else:
                        processed.append(val)
                rows.append(processed)
        
        suspicious_indices = spot(header, rows)
        
        print("Analysis: Identifying settings far outside observed ranges.")
        if suspicious_indices:
            print(f"Found {len(suspicious_indices)} rows with unusual input values.")
            print("The most suspicious row indices are:")
            print(suspicious_indices[:5])
            print("These rows contain settings that deviate significantly from our historical data.")
        else:
            print("No unusual settings detected.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
