import csv

def blame(header, rows):
    """
    Identifies input columns that have the least correlation with the goal 
    columns ('YearsAtCompany+', 'YearsInCurrentRole+', 'YearsWithCurrManager+').
    Columns with low correlation are candidates for removal.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('+') or name.endswith('-'))]
    
    # We define "relevance" as the average absolute correlation with all goal columns.
    # For numeric inputs, we use Pearson correlation.
    # For symbolic inputs, we use a simple variance-based heuristic (how much the 
    # distribution of the goal changes across categories).
    
    relevance_scores = []
    
    for i in input_indices:
        col_name = header[i]
        correlations = []
        
        for g_idx in goal_indices:
            # Extract valid pairs
            data = [(row[i], row[g_idx]) for row in rows if row[g_idx] != "?"]
            if not data:
                correlations.append(0)
                continue
                
            if isinstance(data[0][0], float):
                # Numeric correlation (Pearson-like)
                xs = [d[0] for d in data]
                ys = [d[1] for d in data]
                mx, my = sum(xs)/len(xs), sum(ys)/len(ys)
                num = sum((x - mx) * (y - my) for x, y in data)
                den = (sum((x - mx)**2 for x in xs) * sum((y - my)**2 for y in ys))**0.5
                correlations.append(abs(num / den) if den != 0 else 0)
            else:
                # Symbolic: compare variance of goal across categories
                cats = set(d[0] for d in data)
                if len(cats) < 2:
                    correlations.append(0)
                else:
                    # Calculate how much the mean of the goal varies by category
                    means = {c: [] for c in cats}
                    for x, y in data: means[x].append(y)
                    overall_mean = sum(d[1] for d in data) / len(data)
                    var_between = sum(len(means[c]) * (sum(means[c])/len(means[c]) - overall_mean)**2 for c in cats)
                    correlations.append(min(1.0, var_between / 10000)) # Normalized heuristic
        
        relevance_scores.append((sum(correlations) / len(correlations), col_name))
    
    # Return columns with the lowest relevance scores
    relevance_scores.sort()
    # Return the bottom 5 columns that have the least to do with the goals
    return [name for score, name in relevance_scores[:5]]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    useless_columns = blame(header, rows)
    print("Customer Analysis: Columns that have little impact on employee tenure.")
    print("You may consider stopping the collection of these fields:")
    for col in useless_columns:
        print(f"- {col}")
