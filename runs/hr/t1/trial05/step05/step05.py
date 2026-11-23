import csv

def blame(header, rows):
    """
    Identifies input columns that correlate with 'bad' performance.
    'Bad' is defined as having low values in goal columns ending in '+'.
    We calculate the correlation between each input column and the 
    average of the goal columns to find what explains the short stays.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+')]
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('+') or name.endswith('-'))]

    # Calculate a normalized score for each row (higher is better)
    def get_score(row):
        return sum(row[i] for i in goal_indices)

    # Calculate average score of the population to find 'bad' rows
    scores = [get_score(row) for row in rows]
    avg_score = sum(scores) / len(scores)
    
    # Focus on rows that are below average (the 'short stayers')
    bad_rows = [row for row in rows if get_score(row) < avg_score]
    if not bad_rows:
        return []

    # For each input column, calculate the average value in 'bad' rows
    # vs the average in the whole population.
    # We look for columns where the 'bad' rows have a distinct distribution.
    insights = []
    for i in input_indices:
        col_name = header[i]
        
        # Only consider numeric inputs for simple correlation
        if isinstance(rows[0][i], float):
            bad_avg = sum(r[i] for r in bad_rows) / len(bad_rows)
            all_avg = sum(r[i] for r in rows) / len(rows)
            # If the average in bad rows is significantly different, it's a candidate
            if all_avg != 0:
                diff = abs(bad_avg - all_avg) / all_avg
                insights.append((diff, col_name))
    
    # Sort by the magnitude of difference and return the top 3
    insights.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in insights[:3]]

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

    factors = blame(header, rows)
    
    print("Analysis: What explains short stays in the company?")
    print("The following input factors are most strongly associated with shorter tenure:")
    for factor in factors:
        print(f"- {factor}")
    print("\nThese columns show the greatest variance in employees who leave earlier than average.")
