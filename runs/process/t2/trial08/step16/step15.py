import csv
import step05

def blame(header, rows):
    """
    Identifies input columns that correlate with high 'Cost-' values.
    We define 'worst' as the top 20% of rows with the highest 'Cost-' values.
    We then compare the distribution of each input column in these 'worst' 
    rows against the rest of the dataset.
    """
    cost_idx = header.index('Cost-')
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Sort rows by Cost- descending to find the worst
    sorted_rows = sorted(rows, key=lambda r: r[cost_idx], reverse=True)
    worst_rows = sorted_rows[:len(rows) // 5]
    other_rows = sorted_rows[len(rows) // 5:]
    
    def get_diff(idx):
        # Calculate the difference in means between worst and others
        worst_vals = [r[idx] for r in worst_rows]
        other_vals = [r[idx] for r in other_rows]
        avg_worst = sum(worst_vals) / len(worst_vals)
        avg_other = sum(other_vals) / len(other_vals)
        return abs(avg_worst - avg_other)

    # Rank inputs by how much they differ in the worst setups
    diffs = []
    for i in input_indices:
        diffs.append((get_diff(i), header[i]))
    
    diffs.sort(reverse=True)
    
    # Return the top 2 inputs that explain the variance
    return [name for _, name in diffs[:2]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
        
        reasons = blame(header, rows)
        
        # Identify columns to stop worrying about (those with the least impact)
        input_indices = [i for i, name in enumerate(header) 
                         if not (name.endswith('-') or name.endswith('+'))]
        
        # Calculate impact for all inputs to find the least significant
        all_impacts = []
        for i in input_indices:
            # Re-use logic for impact
            cost_idx = header.index('Cost-')
            sorted_rows = sorted(rows, key=lambda r: r[cost_idx], reverse=True)
            worst = sorted_rows[:len(rows) // 5]
            others = sorted_rows[len(rows) // 5:]
            w_vals = [r[i] for r in worst]
            o_vals = [r[i] for r in others]
            impact = abs((sum(w_vals)/len(w_vals)) - (sum(o_vals)/len(o_vals)))
            all_impacts.append((impact, header[i]))
        
        all_impacts.sort()
        ignored = [name for _, name in all_impacts[:2]]
        
        print("Customer Inquiry: Which facts matter most to cost, and which can I stop worrying about?")
        print(f"Answer: The primary factors driving cost are: {', '.join(reasons)}.")
        print(f"You can safely stop worrying about: {', '.join(ignored)}.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
