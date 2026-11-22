import ezr
import step08

def fix(header, row, levers):
    """
    Recommends changes to non-monetary levers to improve retention metrics.
    Uses the logic from step08 to minimize ydist (distance to ideal goals).
    """
    # We exclude 'MonthlyIncome' and 'PercentSalaryHike' to respect the 
    # constraint that there is no money for pay increases.
    restricted_levers = {
        k: v for k, v in levers.items() 
        if k not in ["MonthlyIncome", "PercentSalaryHike"]
    }
    
    return step08.fix(header, row, restricted_levers)

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Define non-monetary levers
    levers = {
        "businessTravel": ["Non-Travel", "Travel_Rarely", "Travel_Frequently"],
        "overTime": ["No", "Yes"],
        "TrainingTimesLastYear": (0, 6),
        "StockOptionLevel": (0, 3),
        "WorkLifeBalance": (1, 4),
        "EnvironmentSatisfaction": (1, 4),
        "JobSatisfaction": (1, 4)
    }
    
    # Identify a "bad" row (high ydist)
    tbl = ezr.Tbl([header] + rows)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0])
    bad_row = scored[-1][1]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Retention Strategy Analysis: Non-Monetary Improvements")
    print("Given the budget constraints, we recommend the following adjustments:")
    for col, val in recommendation.items():
        print(f"- Adjust '{col}' to: {val}")
    print("-" * 60)
    print("These recommendations focus on improving job satisfaction and")
    print("work-life balance to optimize retention without salary increases.")
    
    exit(0)
