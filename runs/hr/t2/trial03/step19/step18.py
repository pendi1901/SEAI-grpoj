import csv
import step08

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row (short tenure) to improve retention,
    excluding 'MonthlyIncome' as per the customer's constraint.
    """
    # Filter out MonthlyIncome from the available levers
    available_levers = {k: v for k, v in levers.items() if k != 'MonthlyIncome'}
    
    # Use the logic from step08, but with the restricted set of levers
    return step08.fix(header, row, available_levers)

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
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Define levers excluding MonthlyIncome
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'StockOptionLevel': (0.0, 3.0)
    }

    # Identify a 'bad' row (e.g., lowest tenure)
    years_idx = header.index('YearsAtCompany+')
    bad_row = min(rows, key=lambda r: r[years_idx])
    
    recommendations = fix(header, bad_row, levers)
    
    print("Analysis: Recommended changes for employees with short tenure (No budget for pay increases):")
    for col, val in recommendations.items():
        print(f"- Change '{col}' to {val}")
    
    print("\nLogic: We prioritize non-monetary levers like reducing overtime, adjusting travel, "
          "increasing training, and stock options to improve retention without salary increases.")
