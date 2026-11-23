import csv

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row (short tenure) to improve it,
    specifically avoiding 'MonthlyIncome' as requested by the customer.
    """
    recommendations = {}
    
    # Strategy:
    # 1. Prioritize reducing 'overTime' if it's 'Yes'.
    # 2. Adjust 'businessTravel' to 'Non-Travel' to reduce stress.
    # 3. Increase 'TrainingTimesLastYear' to invest in the employee.
    # 4. Adjust 'StockOptionLevel' as a non-monetary incentive.
    
    # We explicitly ignore 'MonthlyIncome' as per customer request.
    
    if 'overTime' in levers and row[header.index('overTime')] == 'Yes':
        if 'No' in levers['overTime']:
            recommendations['overTime'] = 'No'
            
    if 'businessTravel' in levers and 'businessTravel' not in recommendations:
        if 'Non-Travel' in levers['businessTravel']:
            recommendations['businessTravel'] = 'Non-Travel'
            
    if 'TrainingTimesLastYear' in levers and 'TrainingTimesLastYear' not in recommendations:
        low, high = levers['TrainingTimesLastYear']
        # Suggest increasing training to the max allowed
        recommendations['TrainingTimesLastYear'] = float(high)
        
    if 'StockOptionLevel' in levers and 'StockOptionLevel' not in recommendations:
        low, high = levers['StockOptionLevel']
        # Suggest increasing stock options
        recommendations['StockOptionLevel'] = float(high)
                
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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Define levers, excluding MonthlyIncome as requested
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'StockOptionLevel': (0.0, 3.0)
    }

    # Pick a 'bad' row (e.g., one with low YearsAtCompany+)
    goal_idx = header.index('YearsAtCompany+')
    bad_row = min(rows, key=lambda r: r[goal_idx])
    
    changes = fix(header, bad_row, levers)
    
    print("Retention Strategy (No Budget for Pay Increases):")
    print(f"Current Tenure: {bad_row[goal_idx]} years")
    print("Recommended non-monetary adjustments to improve retention:")
    for col, val in changes.items():
        print(f"- Change '{col}' to: {val}")
    print("\nLogic: Since pay increases are not possible, we focus on reducing work-life stress (OverTime, Travel) and increasing professional development (Training, Stock Options).")
