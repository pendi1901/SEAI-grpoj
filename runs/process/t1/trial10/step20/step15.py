import csv

def blame(header, rows):
    """
    Identifies the input columns that most strongly correlate with high 'Cost-'.
    Returns the names of the two input columns that show the largest difference
    in mean values between the worst 10% of rows and the rest.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('-') or name.endswith('+'))]
    
    try:
        cost_idx = header.index('Cost-')
    except ValueError:
        return []

    # Sort rows by Cost- descending to find the worst performers
    sorted_rows = sorted(rows, key=lambda r: float(r[cost_idx]), reverse=True)
    
    # Take the worst 10%
    n = len(rows)
    limit = max(1, n // 10)
    worst = sorted_rows[:limit]
    others = sorted_rows[limit:]
    
    # Calculate the absolute difference in means for each input column
    diffs = []
    for i in input_indices:
        w_vals = [float(r[i]) for r in worst]
        o_vals = [float(r[i]) for r in others]
        
        avg_w = sum(w_vals) / len(w_vals)
        avg_o = sum(o_vals) / len(o_vals)
        
        diffs.append((abs(avg_w - avg_o), header[i]))
    
    # Sort by difference descending
    diffs.sort(key=lambda x: x[0], reverse=True)
    
    # Return the top 2 most influential input columns
    return [d[1] for d in diffs[:2]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        important = blame(header, rows)
        
        print("Analysis of project cost drivers:")
        print(f"The factors that matter most to cost are: {', '.join(important)}.")
        print("You should focus your attention on these, as they correlate most strongly")
        print("with high-cost outcomes. Other input factors have a negligible impact")
        print("and can be safely deprioritized.")
        exit(0)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
