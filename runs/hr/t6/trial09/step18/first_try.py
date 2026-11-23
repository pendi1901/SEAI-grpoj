import ezr
import step08

def fix(header, row, levers):
    """
    Given a 'bad' row, recommend changes to levers to improve its ydist.
    We reuse the logic from step08, which simulates the impact of changing
    each lever and picks the one that results in the lowest ydist.
    """
    # Load data to build a reference table for ydist calculations
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    tbl = ezr.Tbl(data)
    
    # Use the logic from step08 to find the best lever change
    return step08.fix(header, row, levers)

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Define non-monetary levers
    # We exclude MonthlyIncome and PercentSalaryHike as per the prompt
    levers = {
        "businessTravel": ["Non-Travel", "Travel_Rarely", "Travel_Frequently"],
        "overTime": ["No", "Yes"],
        "TrainingTimesLastYear": (0, 6),
        "StockOptionLevel": (0, 3),
        "WorkLifeBalance": (1, 4),
        "EnvironmentSatisfaction": (1, 4),
        "JobInvolvement": (1, 4),
        "JobSatisfaction": (1, 4)
    }
    
    # Pick a "bad" row (high ydist) to demonstrate
    tbl = ezr.Tbl(data)
    sorted_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r), reverse=True)
    bad_row = sorted_rows[0]
    
    # Get recommendation
    change = fix(header, bad_row, levers)
    
    print("Analysis: Non-monetary recommendations for improving employee retention.")
    print("Method: Evaluating impact of changing work-life and environment levers.")
    if change:
        col, val = list(change.items())[0]
        print(f"Recommended change: Set '{col}' to '{val}'.")
    else:
        print("No single non-monetary lever change found to improve this specific record.")
    
    exit(0)
