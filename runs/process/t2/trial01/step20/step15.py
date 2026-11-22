import csv
from step05 import blame as base_blame

def blame(header, rows):
    """
    Identifies input columns that matter most to cost (by identifying which
    inputs are most deviant in the worst-performing setups) and implicitly
    suggests that inputs not identified are less critical.
    """
    # The logic in step05.py already identifies the top 2 drivers of bad performance.
    # We reuse this logic as it satisfies the requirement to find what matters most.
    return base_blame(header, rows)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                # Convert numeric columns to float
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        important_inputs = blame(header, rows)
        
        # Identify all input columns
        all_inputs = [name for name in header if not (name.endswith('-') or name.endswith('+'))]
        
        # Determine what can be ignored (those not in the top 2)
        ignored_inputs = [name for name in all_inputs if name not in important_inputs]
        
        print("Customer Inquiry: Which facts matter most to cost, and which can I stop worrying about?")
        print(f"Answer: The most critical factors affecting cost are: {', '.join(important_inputs)}.")
        print(f"You can likely deprioritize monitoring: {', '.join(ignored_inputs[:3])} (and others).")
        print("These findings are based on analyzing the input deviations in the worst-performing project setups.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
