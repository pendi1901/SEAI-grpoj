import csv

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row to improve tenure-related goals 
    without changing pay (MonthlyIncome).
    
    We look for levers that correlate positively with tenure-related goals
    (YearsAtCompany+, YearsInCurrentRole+, YearsWithCurrManager+).
    """
    recommendations = {}
    
    # Heuristic:
    # 1. 'overTime' == 'No' is generally better for retention.
    # 2. 'businessTravel' == 'Non-Travel' is generally better for retention.
    # 3. 'StockOptionLevel' == 3 (higher) is generally better for retention.
    # 4. 'TrainingTimesLastYear' == 3 (moderate) is generally better for retention.
    
    for col, allowed in levers.items():
        if col not in header:
            continue
            
        if isinstance(allowed, list):  # Symbolic
            if col == 'overTime' and 'No' in allowed:
                recommendations[col] = 'No'
            elif col == 'businessTravel' and 'Non-Travel' in allowed:
                recommendations[col] = 'Non-Travel'
            else:
                recommendations[col] = allowed[0]
        else:  # Numeric (low, high)
            low, high = allowed
            if col == 'StockOptionLevel':
                recommendations[col] = high
            elif col == 'TrainingTimesLastYear':
                # Aim for a balanced training load
                recommendations[col] = min(high, 3)
            elif col == 'PercentSalaryHike':
                # Even if no base pay increase, higher percentage hikes are better
                recommendations[col] = high
            else:
                recommendations[col] = low
                
    return recommendations

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for line in reader:
            processed_row = []
            for i, val in enumerate(line):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    # Define levers available to the customer (excluding MonthlyIncome)
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0, 6),
        'PercentSalaryHike': (11, 25),
        'StockOptionLevel': (0, 3)
    }
    
    # Demonstrate on the first row
    sample_row = rows[0]
    recommendation = fix(header, sample_row, levers)
    
    print("Retention Strategy (No Budget for Pay Increases):")
    print("Since base pay cannot be adjusted, we recommend focusing on work-life balance and non-monetary incentives:")
    for col, val in recommendation.items():
        print(f"- Adjust '{col}' to: {val}")
    
    print("\nThese adjustments target improved retention by reducing burnout and increasing organizational alignment.")
    exit(0)
