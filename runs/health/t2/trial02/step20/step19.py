import csv

def spot(header, rows):
    """
    Identifies rows containing input values that are 'far outside' 
    the range of what has been seen in the dataset.
    We use a Z-score approach for numeric inputs and a frequency-based 
    approach for symbolic inputs to detect outliers.
    """
    input_indices = [
        i for i, name in enumerate(header) 
        if not (name.endswith('-') or name.endswith('+'))
    ]
    
    # Calculate statistics for numeric inputs
    stats = {}
    for i in input_indices:
        if isinstance(rows[0][i], (int, float)):
            vals = [r[i] for r in rows if r[i] is not None]
            if not vals: continue
            mean = sum(vals) / len(vals)
            std = (sum((x - mean)**2 for x in vals) / len(vals))**0.5
            stats[i] = (mean, std)
        else:
            # For symbolic, track seen values
            stats[i] = set(r[i] for r in rows)

    scores = []
    for row_idx, row in enumerate(rows):
        anomaly_score = 0
        for i in input_indices:
            if i in stats:
                if isinstance(row[i], (int, float)):
                    mean, std = stats[i]
                    if std > 0:
                        z = abs(row[i] - mean) / std
                        # If Z-score > 3, it's statistically rare
                        if z > 3:
                            anomaly_score += z
                else:
                    # If symbolic value was never seen in training
                    if row[i] not in stats[i]:
                        anomaly_score += 10 
        
        if anomaly_score > 0:
            scores.append((anomaly_score, row_idx))
    
    # Sort by anomaly score descending
    scores.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scores]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
            rows.append(processed_row)

    suspicious = spot(header, rows)
    
    print("Customer Inquiry: 'A colleague suggests settings far outside anything we have tried. Tell me when you are being asked about something you have never seen.'")
    if suspicious:
        print(f"Answer: I have identified {len(suspicious)} rows that contain settings significantly outside the range of our historical data.")
        print("The indices of the most suspicious setups are:")
        print(suspicious[:5])
    else:
        print("Answer: No setups were found that deviate significantly from our historical data.")
