import csv
from step01 import remember

def blame(header, rows):
    """
    Identifies input columns that correlate most strongly with the 'Idle-' goal.
    We define 'worst' as rows in the top 25% of 'Idle-' values.
    We compare the average of these inputs against the population average.
    """
    idle_idx = header.index('Idle-')
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Sort rows by Idle- to find the worst 25%
    sorted_rows = sorted(rows, key=lambda r: float(r[idle_idx]), reverse=True)
    worst_rows = sorted_rows[:len(rows) // 4]
    
    # Calculate average of inputs for the whole population and the worst rows
    def get_avg(data, idx):
        return sum(float(r[idx]) for r in data) / len(data)
    
    diffs = []
    for i in input_indices:
        pop_avg = get_avg(rows, i)
        worst_avg = get_avg(worst_rows, i)
        # We look for inputs where the worst rows deviate most from the population
        diffs.append((abs(worst_avg - pop_avg), header[i]))
    
    # Return the top 3 inputs that explain the bad idle performance
    diffs.sort(key=lambda x: x[0], reverse=True)
    return [name for _, name in diffs[:3]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        reasons = blame(header, rows)
        
        print("Customer Inquiry: Why do our worst setups leave so many people waiting around?")
        print("Analysis: We compared the input parameters of the worst 25% of setups (by 'Idle-')")
        print("against the general population.")
        print(f"The primary factors contributing to high idle time are: {', '.join(reasons)}.")
        print("These parameters show the most significant deviation in poorly performing setups.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
