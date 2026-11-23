import csv
from step09 import spot as original_spot

def spot(header, rows):
    """
    Identifies rows that are 'unlike anything we have run'.
    We use the logic from step09 (distance from median) to identify
    anomalous/unseen configurations.
    """
    return original_spot(header, rows)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        suspicious_indices = spot(header, rows)
        
        print("Customer Inquiry: Identifying setups unlike anything we have run.")
        print("Analysis: We compared all records against the median values of the dataset.")
        print("The following row indices represent configurations that are significantly")
        print("different from our historical data (most anomalous first):")
        print(suspicious_indices[:5])
        print("\nThese rows represent setups that deviate from our known operational patterns.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
