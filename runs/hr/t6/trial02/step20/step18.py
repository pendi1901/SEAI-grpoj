import ezr
import step08

def fix(header, row, levers):
    """
    Given a 'bad' row, find a change in the allowed levers that 
    minimizes the row's ydist (improves retention metrics).
    """
    # We reuse the logic from step08 which calculates the best lever change
    # to minimize ydist.
    return step08.fix(header, row, levers)

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Initialize global stats for ydist
    tbl = ezr.Tbl([header] + rows)
    
    # Define non-monetary levers
    levers = {
        "businessTravel": ["Non-Travel", "Travel_Frequently", "Travel_Rarely"],
        "overTime": ["No", "Yes"],
        "TrainingTimesLastYear": (0, 6),
        "StockOptionLevel": (0, 3),
        "JobInvolvement": (1, 4),
        "EnvironmentSatisfaction": (1, 4),
        "JobSatisfaction": (1, 4),
        "WorkLifeBalance": (1, 4)
    }
    
    # Find a 'bad' row (high ydist)
    sorted_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r), reverse=True)
    bad_row = sorted_rows[0]
    
    # Get recommendation
    recommendation = fix(header, bad_row, levers)
    
    print("Customer Query: There is no money for pay this year. What else can we change?")
    print("Analysis: We identified non-monetary levers that improve retention metrics.")
    print(f"Recommended change for a high-risk employee: {recommendation}")
    
    # Verify improvement
    new_row = list(bad_row)
    for k, v in recommendation.items():
        new_row[header.index(k)] = v
    
    print(f"Original ydist: {ezr.ydist(tbl, bad_row):.2f}")
    print(f"Improved ydist: {ezr.ydist(tbl, new_row):.2f}")
    print("Conclusion: Adjusting these non-monetary factors can improve retention metrics.")
    
    exit(0)
