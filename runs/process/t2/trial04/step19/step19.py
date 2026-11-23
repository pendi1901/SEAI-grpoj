import csv
import math
import step09

def spot(header, rows):
    """
    Identifies rows that are 'outliers' by calculating the distance 
    of each row to the centroid of the input columns. 
    This identifies setups that are 'unlike anything we have run'.
    """
    # We reuse the logic from step09 which calculates the distance 
    # of each row to the centroid of the input columns.
    # Rows with the largest distances are the most 'unseen' or 'unlike' 
    # the historical data.
    return step09.spot(header, rows)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                # Convert numeric columns to float
                processed_row = [float(val) for val in row]
                rows.append(processed_row)
        
        suspicious_indices = spot(header, rows)
        
        print("Analysis: Identifying setups unlike anything seen in historical data.")
        print(f"Found {len(suspicious_indices)} setups that are significantly different from the norm.")
        print("The most unusual setups (by row index) are:")
        print(suspicious_indices[:5])
        print("These configurations represent novel or potentially erroneous data points.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
