import csv
import step05

def blame(header, rows):
    """
    Identifies input columns that have 'nothing to do' with tenure.
    We define these as columns that show the least difference between 
    the 'worst' 20% of employees and the rest of the population.
    """
    goal_indices = [i for i, h in enumerate(header) if '+' in h or '-' in h]
    input_indices = [i for i, h in enumerate(header) if '+' not in h and '-' not in h]

    def get_tenure_score(row):
        # Higher is better tenure.
        return sum(row[i] for i in goal_indices if '+' in header[i]) - \
               sum(row[i] for i in goal_indices if '-' in header[i])

    # Sort rows by tenure score
    scored_rows = sorted(rows, key=get_tenure_score)
    
    # Bottom 20% are the 'worst' (short stays)
    cutoff = max(1, int(len(rows) * 0.2))
    worst = scored_rows[:cutoff]
    rest = scored_rows[cutoff:]

    # Calculate mean difference for all input columns
    # We look for features where the difference is minimal (near zero)
    diffs = []
    for i in input_indices:
        col_name = header[i]
        if isinstance(worst[0][i], (int, float)):
            m_worst = sum(r[i] for r in worst) / len(worst)
            m_rest = sum(r[i] for r in rest) / len(rest)
            diffs.append((abs(m_worst - m_rest), col_name))
        else:
            # For symbolic, compare frequency distributions
            worst_vals = [r[i] for r in worst]
            rest_vals = [r[i] for r in rest]
            # Simple metric: overlap in distribution
            unique = set(worst_vals + rest_vals)
            overlap = 0
            for val in unique:
                p_worst = worst_vals.count(val) / len(worst_vals)
                p_rest = rest_vals.count(val) / len(rest_vals)
                overlap += min(p_worst, p_rest)
            diffs.append((1.0 - overlap, col_name))

    # Sort by difference ascending (smallest difference = least relevant)
    diffs.sort(key=lambda x: x[0])
    
    # Return the top 5 columns that have the least impact on tenure
    return [d[1] for d in diffs[:5]]

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
    print("Input columns that have the least correlation with tenure (candidates for removal):")
    for col in results:
        print(f"- {col}")
