import csv
import step09

def spot(header, rows):
    """
    Identifies rows that are 'outliers' by calculating the distance of each row
    to its nearest neighbor in the input space. Rows with unusually large 
    distances to their nearest neighbor are flagged as suspicious.
    
    This reuses the logic from step09, which identifies rows that are 
    unlike anything seen before in the input space.
    """
    return step09.spot(header, rows)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
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
        
        print("Analysis: Identifying setups unlike anything we have run.")
        if suspicious_indices:
            print(f"I have identified {len(suspicious_indices)} setups that are highly unusual.")
            print("These rows are the most suspicious because they are the furthest from")
            print("any other known configuration in our historical data.")
            print(f"The most suspicious row index is: {suspicious_indices[0]}")
        else:
            print("No unusual setups were detected.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
