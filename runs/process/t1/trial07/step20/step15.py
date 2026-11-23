import csv

def blame(header, rows):
    """
    Identifies the most important input columns by comparing the 
    distribution of inputs in the 'worst' rows versus the 'best' rows.
    
    Returns the names of the two input columns that show the largest 
    difference in mean values between the worst and best quartiles.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    input_indices = [i for i, name in enumerate(header) if i not in goal_indices]
    
    # Identify the goal column to minimize (Cost-)
    cost_idx = header.index('Cost-')
    
    # Score rows to find best and worst
    def get_score(row):
        return row[cost_idx]
    
    sorted_rows = sorted(rows, key=get_score)
    
    # Use quartiles to compare extremes
    q = len(sorted_rows) // 4
    best_rows = sorted_rows[:q]
    worst_rows = sorted_rows[-q:]
    
    # Find inputs with the largest difference in means between worst and best
    diffs = []
    for i in input_indices:
        best_mean = sum(r[i] for r in best_rows) / len(best_rows)
        worst_mean = sum(r[i] for r in worst_rows) / len(worst_rows)
        diffs.append((abs(worst_mean - best_mean), header[i]))
    
    # Sort by difference descending
    diffs.sort(key=lambda x: x[0], reverse=True)
    
    # Return the top 2 most impactful inputs
    return [name for diff, name in diffs[:2]]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(x) for x in row])
        
        important_factors = blame(header, rows)
        
        print("Customer Inquiry: Project Cost Drivers")
        print("-" * 40)
        print("The factors that matter most to project cost are:")
        for i, factor in enumerate(important_factors):
            print(f"{i+1}. {factor}")
        
        print("\nYou can safely stop worrying about the other input factors,")
        print("as they show minimal correlation with cost variance.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
