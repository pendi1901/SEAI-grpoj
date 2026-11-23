import csv
import step09

def spot(header, rows):
    """
    Identifies rows that are 'unlike anyone we have employed' by checking
    if their input values are extreme outliers compared to the rest of the
    dataset. We use the logic from step09 to flag logical inconsistencies,
    and extend it to flag rows with extreme values in numeric inputs.
    """
    # Start with the suspicious logical inconsistencies from step09
    suspicious = []
    
    # Calculate means and standard deviations for numeric input columns
    # to identify statistical outliers (values > 3 std devs from mean)
    numeric_indices = [i for i, name in enumerate(header) 
                       if name[0].isupper() and not (name.endswith('+') or name.endswith('-'))]
    
    stats = {}
    for idx in numeric_indices:
        vals = [r[idx] for r in rows if isinstance(r[idx], (int, float))]
        if not vals: continue
        avg = sum(vals) / len(vals)
        std = (sum((x - avg) ** 2 for x in vals) / len(vals)) ** 0.5
        stats[idx] = (avg, std)

    # Score rows based on how many extreme values they contain
    for i, row in enumerate(rows):
        score = 0
        # Add score from logical inconsistencies (step09)
        score += len(step09.spot(header, [row])) * 5
        
        # Add score for statistical outliers
        for idx, (avg, std) in stats.items():
            if std > 0 and abs(row[idx] - avg) > (3 * std):
                score += 1
        
        if score > 0:
            suspicious.append((score, i))
            
    # Sort by score descending (most suspicious first)
    suspicious.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in suspicious]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    suspects = spot(header, rows)
    
    print("Analysis: Identifying records that are 'unlike' our historical data.")
    print("These records contain either logical inconsistencies or extreme statistical outliers.")
    print("Our estimates for these rows cannot be trusted:")
    for i in suspects[:10]:
        print(f"- Row {i} is highly suspicious.")
