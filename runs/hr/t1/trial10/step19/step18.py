import csv

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row to improve retention metrics (YearsAtCompany+)
    without using pay-related levers (like PercentSalaryHike).
    
    Strategy: Focus on non-monetary levers that correlate with higher tenure:
    1. Reduce 'overTime' if possible.
    2. Adjust 'businessTravel' to 'Travel_Rarely' or 'Non-Travel'.
    3. Increase 'TrainingTimesLastYear' to the maximum allowed.
    4. Increase 'StockOptionLevel' (if considered non-monetary/equity-based).
    """
    recommendations = {}
    
    # Filter out pay-related levers if they exist in the input
    non_pay_levers = {k: v for k, v in levers.items() if 'Salary' not in k and 'Income' not in k}
    
    # 1. Try to reduce Overtime
    if 'overTime' in non_pay_levers and 'overTime' in header:
        idx = header.index('overTime')
        if row[idx] == 'Yes' and 'No' in non_pay_levers['overTime']:
            recommendations['overTime'] = 'No'
            
    # 2. Try to reduce Business Travel stress
    if 'businessTravel' in non_pay_levers and 'businessTravel' in header:
        idx = header.index('businessTravel')
        if row[idx] == 'Travel_Frequently' and 'Travel_Rarely' in non_pay_levers['businessTravel']:
            recommendations['businessTravel'] = 'Travel_Rarely'
            
    # 3. Maximize Training (Growth opportunity)
    if 'TrainingTimesLastYear' in non_pay_levers and 'TrainingTimesLastYear' in header:
        idx = header.index('TrainingTimesLastYear')
        low, high = non_pay_levers['TrainingTimesLastYear']
        if row[idx] < high:
            recommendations['TrainingTimesLastYear'] = high
            
    # 4. If no other changes, pick the first available non-pay lever
    if not recommendations and non_pay_levers:
        first_key = list(non_pay_levers.keys())[0]
        val = non_pay_levers[first_key]
        recommendations[first_key] = val[1] if isinstance(val, tuple) else val[0]
        
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
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    # Define levers excluding salary-based ones
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'StockOptionLevel': (0.0, 3.0)
    }
    
    # Example: Fix the first row
    bad_row = rows[0]
    changes = fix(header, bad_row, levers)
    
    print("Retention Improvement Recommendations (Non-Monetary):")
    if not changes:
        print("No non-monetary levers could be optimized.")
    else:
        for col, val in changes.items():
            print(f"- Change '{col}' to {val}")
    
    print("\nConclusion: Since salary increases are not possible, we focus on improving")
    print("work-life balance (reducing overtime/travel) and professional development")
    print("(training) to increase employee retention.")
