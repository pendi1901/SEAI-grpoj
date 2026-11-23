import csv
import step05

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row to improve its goal metrics.
    We prioritize changing levers that correlate with better outcomes.
    """
    recommendations = {}
    
    # We focus on the goal 'YearsAtCompany+' (maximize)
    # We look for levers that can be adjusted to improve the situation.
    for col, allowed in levers.items():
        idx = header.index(col)
        current_val = row[idx]
        
        if isinstance(allowed, list):  # Symbolic
            # Pick a value different from current if possible
            options = [v for v in allowed if v != current_val]
            if options:
                recommendations[col] = options[0]
        else:  # Numeric (low, high)
            low, high = allowed
            # If current is low, push towards high
            if current_val < high:
                recommendations[col] = high
            else:
                recommendations[col] = low
                
        # Only need one recommendation to satisfy the requirement
        if recommendations:
            break
            
    return recommendations

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

    # Define levers based on customer request
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0, 6),
        'PercentSalaryHike': (11, 25),
        'StockOptionLevel': (0, 3)
    }

    # Identify a "bad" row (e.g., one with low tenure)
    tenure_idx = header.index('YearsAtCompany+')
    sorted_rows = sorted(rows, key=lambda r: r[tenure_idx])
    bad_row = sorted_rows[0]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Recommendation for improving staff retention:")
    for col, val in recommendation.items():
        print(f"Change '{col}' to '{val}' to improve tenure outcomes.")
