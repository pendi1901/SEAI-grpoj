import csv
import step01

def blame(header, rows):
    """
    Identifies input columns that correlate with high 'Idle-' values.
    We compare the top 25% worst rows (by 'Idle-') against the rest.
    """
    idle_idx = header.index('Idle-')
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Sort rows by 'Idle-' descending to find the worst
    sorted_rows = sorted(rows, key=lambda r: r[idle_idx], reverse=True)
    worst = sorted_rows[:len(rows) // 4]
    rest = sorted_rows[len(rows) // 4:]
    
    def get_avg(data, idx):
        vals = [r[idx] for r in data if isinstance(r[idx], (int, float))]
        return sum(vals) / len(vals) if vals else 0

    # Find inputs where the average in 'worst' is significantly higher than in 'rest'
    # We look for the largest delta in normalized space
    deltas = []
    for i in input_indices:
        avg_worst = get_avg(worst, i)
        avg_rest = get_avg(rest, i)
        deltas.append((avg_worst - avg_rest, header[i]))
    
    # Return the top 2 inputs that contribute most to the 'Idle-' increase
    deltas.sort(reverse=True)
    return [name for delta, name in deltas[:2]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([float(x) for x in row])
            
    reasons = blame(header, rows)
    
    print("Customer Inquiry: Why do our worst setups leave so many people waiting around?")
    print(f"Analysis: The setups with the highest 'Idle-' values are most strongly associated with: {', '.join(reasons)}.")
    print("These factors appear to drive inefficiency in your current process.")
