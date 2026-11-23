import csv
import numpy as np

def spot(header, rows):
    """
    Identifies rows that look 'wrong' by detecting outliers in the data.
    We use the Isolation Forest approach (via standard deviation/z-score) 
    to find rows that deviate significantly from the mean of their columns.
    """
    # Convert rows to a numpy array for easier calculation
    # We only consider numeric columns for anomaly detection
    numeric_indices = [i for i, name in enumerate(header) if name[0].isupper()]
    
    data = []
    for row in rows:
        data.append([row[i] for i in numeric_indices])
    
    data = np.array(data)
    
    # Calculate Z-scores for each numeric column
    # A row is suspicious if it has a high average Z-score across columns
    means = np.mean(data, axis=0)
    stds = np.std(data, axis=0)
    
    # Avoid division by zero
    stds[stds == 0] = 1.0
    
    z_scores = np.abs((data - means) / stds)
    
    # Average Z-score per row
    row_scores = np.mean(z_scores, axis=1)
    
    # Get indices sorted by score descending (most suspicious first)
    suspicious_indices = np.argsort(row_scores)[::-1]
    
    # Return the top 10 most suspicious rows
    return suspicious_indices[:10].tolist()

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
            
    suspicious = spot(header, rows)
    
    print("Analysis: Identifying potentially erroneous data entries.")
    print("The following row indices are the most suspicious (most likely to contain typos):")
    for idx in suspicious:
        print(f"- Row index: {idx}")
    
    print("\nLogic: Rows were flagged based on high statistical deviation (Z-score) across numeric input fields.")
