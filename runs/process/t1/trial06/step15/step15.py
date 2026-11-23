import csv

def blame(header, rows):
    """
    Identifies which input columns matter most to 'Cost-' and which can be ignored.
    We calculate the correlation between each input and the 'Cost-' goal.
    Inputs with high correlation are critical; those with near-zero correlation
    can be safely ignored.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i, name in enumerate(header) if i not in goal_indices]
    cost_idx = header.index('Cost-')

    # Calculate Pearson-like correlation: 
    # How much does the input change as Cost- changes?
    # We use the absolute difference in mean between the top 25% and bottom 25%
    # of rows sorted by Cost-.
    sorted_rows = sorted(rows, key=lambda r: r[cost_idx])
    n = len(sorted_rows)
    quarter = n // 4
    
    bottom_25 = sorted_rows[:quarter]
    top_25 = sorted_rows[-quarter:]
    
    impacts = []
    for i in input_indices:
        vals_bottom = [r[i] for r in bottom_25 if isinstance(r[i], (int, float))]
        vals_top = [r[i] for r in top_25 if isinstance(r[i], (int, float))]
        
        if not vals_bottom or not vals_top:
            impacts.append((0, header[i]))
            continue
            
        avg_bottom = sum(vals_bottom) / len(vals_bottom)
        avg_top = sum(vals_top) / len(vals_top)
        
        # The impact is the magnitude of the difference
        impacts.append((abs(avg_top - avg_bottom), header[i]))
    
    # Sort by impact descending
    impacts.sort(key=lambda x: x[0], reverse=True)
    
    # Return the names of the input columns
    return [name for impact, name in impacts]

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
        
        ranked_inputs = blame(header, rows)
        
        print("Analysis: Which project factors drive Cost-?")
        print(f"Most critical factors: {ranked_inputs[0]} and {ranked_inputs[1]}.")
        print(f"Factors you can safely stop worrying about: {ranked_inputs[-1]}.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
