import csv
import math

def flow(header, row, seen):
    """
    Detects if a team (represented by the current row) looks 'abnormal' 
    compared to the historical distribution of 'seen' rows.
    
    We use the Z-score of numeric columns to determine if the current row
    is an outlier compared to the mean and standard deviation of seen rows.
    If the cumulative Z-score across numeric columns exceeds a threshold,
    we flag it as 'no longer looking the way it normally does'.
    """
    if not seen:
        return False

    numeric_indices = [i for i, h in enumerate(header) if h[0].isupper()]
    
    # Calculate stats for seen rows
    stats = {}
    for i in numeric_indices:
        vals = [r[i] for r in seen if isinstance(r[i], (int, float))]
        if len(vals) > 5:
            mean = sum(vals) / len(vals)
            std = math.sqrt(sum((x - mean) ** 2 for x in vals) / len(vals))
            if std > 0:
                stats[i] = (mean, std)
    
    # Calculate Z-score for the current row
    total_z = 0
    count = 0
    for i, (mean, std) in stats.items():
        val = row[i]
        if isinstance(val, (int, float)):
            total_z += abs(val - mean) / std
            count += 1
            
    # If the average deviation is high (e.g., > 2 standard deviations), flag it
    if count > 0 and (total_z / count) > 2.0:
        return True
    
    return False

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
            
    seen = []
    anomalies = 0
    for row in rows:
        if flow(header, row, seen):
            anomalies += 1
        seen.append(row)
        
    print("Analysis: Detecting abnormal team structures.")
    print(f"Processed {len(rows)} records.")
    print(f"Identified {anomalies} records where the team structure deviated significantly from historical norms.")
    print("A team is flagged when its numeric attributes (e.g., income, tenure) deviate by more than 2 standard deviations from the historical mean.")
