import csv
import step09

def spot(header, rows):
    """
    Identifies rows that are 'outliers' based on the Mahalanobis-like distance
    of their input values from the centroid of all input values.
    This reuses the logic from step09 to detect rows that are 'unlike anything 
    we have run'.
    """
    return step09.spot(header, rows)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                # Convert numeric columns to float, keep symbolic as is
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        suspicious_indices = spot(header, rows)
        
        print("Analysis: Identifying setups that are unlike anything we have run.")
        if suspicious_indices:
            print(f"I have identified {len(suspicious_indices)} setups that appear unusual.")
            print("The most suspicious row indices (in order of concern) are:")
            print(suspicious_indices[:10])
        else:
            print("All setups appear to be within the expected range of historical data.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
