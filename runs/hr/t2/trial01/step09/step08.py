import csv
import step01
import step06

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row to improve its tenure score.
    Iterates through each lever, tests the impact of changing the value,
    and returns the change that results in the highest score improvement.
    """
    best_change = {}
    best_score_gain = -1.0
    
    current_score = step06.get_score(header, row)
    
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Test variations
        variations = []
        if isinstance(allowed, tuple):  # Numeric range (low, high)
            # Test mid-point or boundaries
            variations = [allowed[0], allowed[1], (allowed[0] + allowed[1]) / 2]
        else:  # Symbolic list
            variations = allowed
            
        for val in variations:
            if val == original_val:
                continue
            
            # Create a copy and apply change
            new_row = list(row)
            new_row[idx] = val
            
            new_score = step06.get_score(header, new_row)
            gain = new_score - current_score
            
            if gain > best_score_gain:
                best_score_gain = gain
                best_change = {col_name: val}
                
    return best_change

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

    # Define levers based on customer request
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'PercentSalaryHike': (11.0, 25.0),
        'StockOptionLevel': (0.0, 3.0)
    }

    # Identify a 'bad' row (e.g., one with low tenure score)
    scores = [(step06.get_score(header, r), i) for i, r in enumerate(rows)]
    scores.sort()
    bad_row_idx = scores[0][1]
    bad_row = rows[bad_row_idx]

    recommendation = fix(header, bad_row, levers)
    
    print("Retention Strategy Recommendation:")
    print(f"For employee at index {bad_row_idx}, we recommend the following change:")
    for col, val in recommendation.items():
        print(f"  - Adjust '{col}' to: {val}")
    print("This change is designed to improve the employee's tenure score based on historical data.")
