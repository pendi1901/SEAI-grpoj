import csv

def remember(header, rows):
    """
    Identifies staff who stay 'unusually long'.
    'YearsAtCompany+' is a goal to maximize.
    We define 'unusually long' as the top 5% of employees by tenure.
    """
    # Find index for YearsAtCompany+
    try:
        idx = header.index("YearsAtCompany+")
    except ValueError:
        return [0]

    # Extract tenure and original index
    tenures = []
    for i, row in enumerate(rows):
        try:
            val = float(row[idx])
            tenures.append((val, i))
        except (ValueError, TypeError):
            continue

    # Sort by tenure descending
    tenures.sort(key=lambda x: x[0], reverse=True)

    # Return top 5% (or at least 1)
    limit = max(1, len(rows) // 20)
    return [item[1] for item in tenures[:limit]]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            # Convert numeric columns (starting with uppercase) to floats
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

    indices = remember(header, rows)
    
    print("Working arrangements of staff with the longest tenure:")
    print(f"{'Years':<10} | {'Business Travel':<20} | {'OverTime':<10}")
    print("-" * 45)
    
    travel_idx = header.index("businessTravel")
    ot_idx = header.index("overTime")
    tenure_idx = header.index("YearsAtCompany+")
    
    for i in indices:
        row = rows[i]
        print(f"{row[tenure_idx]:<10} | {row[travel_idx]:<20} | {row[ot_idx]:<10}")
