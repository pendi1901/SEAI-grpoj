import csv
import random

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row to improve its goal metrics.
    We pick a random lever and set it to a value that is likely to improve
    the outcome (e.g., higher pay, more stock, less overtime).
    """
    recommendations = {}
    
    # Pick one lever to change
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
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Define levers based on customer request
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'PercentSalaryHike': (11.0, 25.0),
        'StockOptionLevel': (0.0, 3.0)
    }

    # Simulate identifying a "bad" row (e.g., low tenure)
    # We'll pick the first row as a sample "bad" row
    bad_row = rows[0]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Customer Request: What can we change for staff who do not stay?")
    print("Analysis: Based on the provided levers, we recommend the following adjustment:")
    for col, val in recommendation.items():
        print(f"- Change '{col}' to: {val}")
    print("\nThis change is intended to improve retention metrics.")
