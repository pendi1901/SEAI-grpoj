import csv
import step01

def blame(header, rows):
    """
    Identifies input columns that correlate with poor performance.
    We define 'bad' rows as those in the bottom 25% of the overall score.
    We then calculate the difference in mean values of inputs between 
    the 'bad' rows and the 'good' rows.
    """
    # Identify goal indices and input indices
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('-') or name.endswith('+'))]

    # Use step01 logic to score rows
    # We need to invert the logic to find the worst rows
    n = len(rows)
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(row):
        # Simple score: lower MRE, higher ACC, higher PRED
        # We use raw values here for relative ranking
        return (-row[mre_idx] + row[acc_idx] + row[pred_idx])

    scored = sorted([(get_score(r), r) for r in rows], key=lambda x: x[0])
    
    # Bottom 25% vs Top 25%
    quarter = n // 4
    bad_rows = [x[1] for x in scored[:quarter]]
    good_rows = [x[1] for x in scored[-quarter:]]

    # Calculate "damage" score for each input
    # Damage = |mean(bad) - mean(good)| / std_dev(all)
    damages = []
    for i in input_indices:
        if isinstance(rows[0][i], str):
            # Symbolic: compare frequency of most common value
            bad_vals = [r[i] for r in bad_rows]
            good_vals = [r[i] for r in good_rows]
            # Simple heuristic: difference in probability of the most common bad value
            most_common = max(set(bad_vals), key=bad_vals.count)
            diff = abs(bad_vals.count(most_common)/len(bad_vals) - good_vals.count(most_common)/len(good_vals))
            damages.append((diff, header[i]))
        else:
            bad_vals = [r[i] for r in bad_rows]
            good_vals = [r[i] for r in good_rows]
            m_bad = sum(bad_vals) / len(bad_vals)
            m_good = sum(good_vals) / len(good_vals)
            # Normalize by range to make comparable
            all_vals = [r[i] for r in rows]
            diff = abs(m_bad - m_good) / (max(all_vals) - min(all_vals) + 1e-9)
            damages.append((diff, header[i]))

    # Return top 3 inputs that contribute most to the difference
    damages.sort(key=lambda x: x[0], reverse=True)
    return [d[1] for d in damages[:3]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = [val if header[i] == 'criterion' else float(val) 
                                 for i, val in enumerate(row)]
                rows.append(processed_row)
        
        blame_cols = blame(header, rows)
        print("The settings most responsible for poor performance are:")
        for col in blame_cols:
            print(f"- {col}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
