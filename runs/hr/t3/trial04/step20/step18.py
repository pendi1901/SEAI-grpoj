import csv

def fix(header, row, levers):
    """
    Suggests changes to a 'bad' row to improve its retention metrics 
    without using salary-based levers.
    """
    recommendations = {}
    
    # Strategy: Focus on non-monetary levers that improve work-life balance
    # and job satisfaction, which are strong drivers of retention.
    
    # 1. If overtime is a lever, always prioritize reducing it.
    if 'overTime' in levers and row[header.index('overTime')] == 'Yes':
        recommendations['overTime'] = 'No'
    
    # 2. If business travel is a lever, reduce it to 'Non-Travel' to improve work-life balance.
    if 'businessTravel' in levers and row[header.index('businessTravel')] != 'Non-Travel':
        recommendations['businessTravel'] = 'Non-Travel'
        
    # 3. If training is a lever, increase it to the maximum allowed to improve engagement.
    if 'TrainingTimesLastYear' in levers:
        _, high = levers['TrainingTimesLastYear']
        recommendations['TrainingTimesLastYear'] = high
        
    # 4. If StockOptionLevel is a lever, increase it to improve long-term alignment.
    if 'StockOptionLevel' in levers:
        _, high = levers['StockOptionLevel']
        recommendations['StockOptionLevel'] = high

    # Fallback: If no specific logic triggered, pick the first available lever
    if not recommendations and levers:
        first_key = list(levers.keys())[0]
        val = levers[first_key]
        recommendations[first_key] = val[1] if isinstance(val, tuple) else val[0]
        
    return recommendations

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed)

    # Define non-monetary levers
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'StockOptionLevel': (0.0, 3.0)
    }

    # Identify a 'bad' row (low tenure)
    idx_tenure = header.index('YearsAtCompany+')
    bad_row = min(rows, key=lambda r: r[idx_tenure])
    
    changes = fix(header, bad_row, levers)
    
    print("Customer Inquiry: No budget for pay raises. What else can we change?")
    print("Recommendation: Focus on non-monetary levers to improve retention:")
    for col, val in changes.items():
        print(f"- Change '{col}' to {val}")
    print("\nThese changes reduce burnout and increase engagement without requiring salary adjustments.")
