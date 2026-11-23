import csv

def blame(header, rows):
    """
    Identifies input columns that correlate with low tenure (short stays).
    'Worst' rows are defined as those with the lowest sum of goal columns.
    We compare the average of input features in the bottom 20% of tenure 
    against the rest of the population to find the most significant differences.
    """
    goal_indices = [i for i, h in enumerate(header) if '+' in h or '-' in h]
    input_indices = [i for i, h in enumerate(header) if '+' not in h and '-' not in h]

    def get_tenure_score(row):
        # Higher is better tenure. We want to find why tenure is low.
        return sum(row[i] for i in goal_indices if '+' in header[i]) - \
               sum(row[i] for i in goal_indices if '-' in header[i])

    # Sort rows by tenure score
    scored_rows = sorted(rows, key=get_tenure_score)
    
    # Bottom 20% are the 'worst' (short stays)
    cutoff = max(1, int(len(rows) * 0.2))
    worst = scored_rows[:cutoff]
    rest = scored_rows[cutoff:]

    # Calculate mean difference for numeric inputs
    diffs = []
    for i in input_indices:
        if isinstance(worst[0][i], (int, float)):
            m_worst = sum(r[i] for r in worst) / len(worst)
            m_rest = sum(r[i] for r in rest) / len(rest)
            # We look for features where the worst group deviates most
            diffs.append((abs(m_worst - m_rest), header[i]))

    # Return the top 3 input columns that differentiate the short-stay group
    diffs.sort(key=lambda x: x[0], reverse=True)
    return [d[1] for d in diffs[:3]]

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

    results = blame(header, rows)
    print("Input columns that best explain short stays:")
    for col in results:
        print(f"- {col}")
