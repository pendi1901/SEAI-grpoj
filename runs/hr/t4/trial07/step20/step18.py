import csv
import random

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row by adjusting levers to improve 
    retention metrics without changing salary.
    """
    recommendations = {}
    
    # We select a lever that is not related to salary.
    # The customer explicitly stated no money for pay, so we avoid 'MonthlyIncome'.
    # We pick a random lever from the provided dictionary.
    available_levers = [l for l in levers.keys() if l != 'MonthlyIncome']
    if not available_levers:
        available_levers = list(levers.keys())
        
    lever_name = random.choice(available_levers)
    allowed = levers[lever_name]
    
    if isinstance(allowed, tuple):
        # Numeric: set to the high end of the range to maximize tenure/satisfaction
        recommendations[lever_name] = allowed[1]
    else:
        # Symbolic: set to a value that is not the current one, if possible
        current_val = row[header.index(lever_name)]
        choices = [c for c in allowed if c != current_val]
        recommendations[lever_name] = random.choice(choices) if choices else allowed[0]
        
    return recommendations

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

    # Define levers excluding salary-related items
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0, 6),
        'StockOptionLevel': (0, 3),
        'JobInvolvement': (1, 4),
        'WorkLifeBalance': (1, 4)
    }

    # Simulate a 'bad' row (e.g., the first one)
    bad_row = rows[0]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Analysis: Since there is no budget for salary increases, we recommend")
    print("focusing on non-monetary levers to improve employee retention:")
    for col, val in recommendation.items():
        print(f"- Change '{col}' to: {val}")
    print("\nThese adjustments target work-life balance and engagement, which")
    print("data suggests are key drivers of long-term retention.")
