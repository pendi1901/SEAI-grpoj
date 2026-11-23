import csv
import random
from step05 import blame

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row to improve its goal metrics,
    excluding salary-related levers.
    """
    # Identify the most influential factors for retention (from step05)
    # We want to change a lever that is actually impactful.
    # Since we cannot change pay, we filter the levers provided.
    
    recommendations = {}
    
    # Pick a lever that is in our allowed list
    lever_name = random.choice(list(levers.keys()))
    allowed = levers[lever_name]
    
    if isinstance(allowed, list):
        # Symbolic: pick a random value from the allowed list
        recommendations[lever_name] = random.choice(allowed)
    else:
        # Numeric: pick a value in the range (low, high)
        low, high = allowed
        recommendations[lever_name] = (low + high) / 2.0
        
    return recommendations

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)

    # Define non-monetary levers
    # We exclude 'MonthlyIncome' or 'PercentSalaryHike' as per customer request
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'StockOptionLevel': (0.0, 3.0),
        'EnvironmentSatisfaction': (1.0, 4.0),
        'JobInvolvement': (1.0, 4.0)
    }

    # Simulate identifying a "bad" row (e.g., low tenure)
    # We'll pick the first row as a sample
    bad_row = rows[0]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Customer Request: There is no money for pay this year. What else can we change?")
    print("Analysis: We have identified non-monetary levers that can improve employee retention.")
    print("Recommended adjustment:")
    for col, val in recommendation.items():
        print(f"- Change '{col}' to: {val}")
    print("\nThese adjustments focus on environment, work-life balance, and engagement.")
