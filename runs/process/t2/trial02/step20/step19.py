import csv
from step09 import spot as step09_spot

def spot(header, rows):
    """
    Identifies rows that are outliers (never seen before).
    We reuse the logic from step09 which identifies rows that have values 
    more than 3 standard deviations away from the mean, effectively 
    flagging setups unlike anything seen in the historical data.
    """
    return step09_spot(header, rows)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        suspicious_rows = spot(header, rows)
        
        if not suspicious_rows:
            print("All setups are within the range of historical experience.")
        else:
            print(f"Found {len(suspicious_rows)} setups that are unlike anything previously run.")
            print("The most unusual setups (by row index) are:")
            for idx in suspicious_rows[:5]:
                print(f"- Row {idx}")
                
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
