import ezr
import step08

def fix(header, row, levers):
    """
    Suggests a change to one of the provided levers to improve the row's ydist,
    excluding 'MonthlyIncome' as per the customer's constraint.
    """
    # Filter out MonthlyIncome from the allowed levers
    allowed_levers = {k: v for k, v in levers.items() if k != "MonthlyIncome"}
    
    # Use the logic from step08 to find the best improvement
    return step08.fix(header, row, allowed_levers)

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Define levers excluding MonthlyIncome
    levers = {
        "businessTravel": ["Non-Travel", "Travel_Frequently", "Travel_Rarely"],
        "overTime": ["No", "Yes"],
        "TrainingTimesLastYear": (0, 6),
        "PercentSalaryHike": (11, 25),
        "StockOptionLevel": (0, 3),
        "JobInvolvement": (1, 4),
        "WorkLifeBalance": (1, 4)
    }
    
    # Identify a "bad" row (high ydist)
    tbl = ezr.Tbl([header] + rows)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0])
    bad_row = scored[-1][1]
    
    suggestion = fix(header, bad_row, levers)
    
    print("Analysis: Recommended changes for employee retention (excluding pay).")
    if suggestion:
        col, val = list(suggestion.items())[0]
        print(f"Recommendation: Change '{col}' to '{val}'.")
        print("Logic: This change optimizes the employee's goal-distance metrics "
              "without requiring any salary adjustments.")
    else:
        print("No improvement found within the provided non-monetary levers.")
