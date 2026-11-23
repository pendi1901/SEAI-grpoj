import csv

def spot(header, rows):
    """
    Identifies rows that contain 'unseen' or 'suspicious' data.
    We define suspicious as values that fall outside the observed range 
    of the training data (0.0 to 1.0).
    """
    suspicious = []
    
    # Identify numeric columns
    numeric_indices = [i for i, col in enumerate(header) if not col.islower()]
    
    for row_idx, row in enumerate(rows):
        anomaly_count = 0
        for col_idx in numeric_indices:
            val = row[col_idx]
            # Check for values outside the standard [0, 1] range
            # or values that are clearly erroneous (e.g., negative or > 1)
            if isinstance(val, (int, float)):
                if val < 0.0 or val > 1.0:
                    anomaly_count += 1
        
        if anomaly_count > 0:
            suspicious.append((row_idx, anomaly_count))
            
    # Sort by number of anomalies found, descending
    suspicious.sort(key=lambda x: x[1], reverse=True)
    
    return [item[0] for item in suspicious]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        suspicious_indices = spot(header, rows)
        
        print("Customer Inquiry: Anomaly Detection")
        if not suspicious_indices:
            print("All provided setups appear to be within the expected historical range.")
        else:
            print(f"We detected {len(suspicious_indices)} setups that contain values unlike anything seen in our history.")
            print("The most suspicious setups (by index) are:")
            print(suspicious_indices[:10])
            print("\nThese setups contain parameters that deviate from our standard operating range.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
