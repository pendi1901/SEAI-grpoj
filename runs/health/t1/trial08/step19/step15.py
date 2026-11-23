import csv

def blame(header, rows):
    """
    Identifies input columns that correlate with 'bad' performance.
    A row is 'bad' if its goals (MRE-, ACC+, PRED40+) are poor.
    We calculate a 'badness' score for each row and correlate it with input settings.
    Settings that do not correlate with badness are candidates for factory defaults.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    input_cols = [i for i, name in enumerate(header) if name not in ['MRE-', 'ACC+', 'PRED40+']]
    
    # Calculate badness: High MRE, Low ACC, Low PRED
    # Normalize: MRE + (1-ACC) + (1-PRED)
    def get_badness(row):
        return row[mre_idx] + (1.0 - row[acc_idx]) + (1.0 - row[pred_idx])

    # Sort rows by badness and take the worst 20%
    rows_with_badness = sorted([(get_badness(r), r) for r in rows], key=lambda x: x[0], reverse=True)
    worst_rows = [r for _, r in rows_with_badness[:len(rows)//5]]
    
    # For each input column, calculate the absolute difference in mean between 
    # the worst rows and the whole dataset.
    # Low impact means the setting is likely neutral (safe for factory default).
    impacts = []
    for i in input_cols:
        col_name = header[i]
        if isinstance(rows[0][i], str):
            # For symbolic, check if distribution in worst rows matches overall
            # We use a simple frequency deviation
            all_vals = [r[i] for r in rows]
            worst_vals = [r[i] for r in worst_rows]
            # Impact = difference in frequency of the most common value
            mode_all = max(set(all_vals), key=all_vals.count)
            freq_all = all_vals.count(mode_all) / len(all_vals)
            freq_worst = worst_vals.count(mode_all) / len(worst_vals)
            impacts.append((abs(freq_worst - freq_all), col_name))
        else:
            avg_all = sum(r[i] for r in rows) / len(rows)
            avg_worst = sum(r[i] for r in worst_rows) / len(worst_rows)
            # Normalize impact by range to make it comparable
            col_vals = [r[i] for r in rows]
            col_range = max(col_vals) - min(col_vals)
            impact = abs(avg_worst - avg_all) / (col_range if col_range > 0 else 1)
            impacts.append((impact, col_name))
            
    # Return names of inputs sorted by impact (ascending: least impact first)
    impacts.sort(key=lambda x: x[0])
    return [name for _, name in impacts]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)
            
    blame_list = blame(header, rows)
    
    print("Analysis: Which settings are safe to leave at factory defaults?")
    print("The following settings have the least impact on poor performance and are safest to keep as defaults:")
    for i, name in enumerate(blame_list):
        print(f"{i+1}. {name}")
    print("\nSettings at the top of this list show the least correlation with bad outcomes.")
