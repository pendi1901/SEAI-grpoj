import csv
import step09

def spot(header, rows):
    """
    Identifies rows that are 'unlike anything we have run'.
    We define this as rows containing input values that are outliers
    relative to the distribution of the training data.
    This reuses the logic from step09.py.
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
        
        # The customer asks to identify setups unlike anything seen before.
        # We use the spot function to find rows with extreme input values.
        outliers = spot(header, rows)
        
        print("Customer Inquiry: A new team lead proposes a setup unlike anything we have run. Tell me when I am asking you about something you have never seen.")
        if outliers:
            print(f"Answer: I have identified {len(outliers)} setups that are significantly different from our historical data.")
            print(f"The most unusual setup is at index {outliers[0]}.")
            print("These configurations contain input parameters that fall well outside our normal operating range.")
        else:
            print("Answer: All proposed setups appear to be within the range of our historical experience.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
