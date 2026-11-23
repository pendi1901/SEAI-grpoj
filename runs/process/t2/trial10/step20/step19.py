import csv
import step09

def spot(header, rows):
    """
    Identifies rows that contain input values that are statistically 
    unlikely (outliers) using the logic from step09.
    """
    return step09.spot(header, rows)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
            suspicious_indices = spot(header, rows)
            
            print("Customer Inquiry: Tell me when I am asking about something you have never seen.")
            if not suspicious_indices:
                print("All provided setups appear to be within the expected range of historical data.")
            else:
                print(f"Found {len(suspicious_indices)} setups that contain unusual input values.")
                print("The most suspicious row indices are:", suspicious_indices[:5])
                print("These rows deviate significantly from the patterns observed in our historical data.")
                
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
