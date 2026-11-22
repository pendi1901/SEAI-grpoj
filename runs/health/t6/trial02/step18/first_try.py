import ezr
import step08

def fix(header, row, levers):
    """
    Finds the best single-lever change to improve the row's ydist.
    Reuses the logic from step08.py.
    """
    return step08.fix(header, row, levers)

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Define levers based on the problem description
    levers = {
        "N_estimators": (10.0, 200.0),
        "criterion": ["absolute_error", "poisson", "squared_error"],
        "Min_sample_leaves": (1.0, 20.0),
        "Min_impurity_decrease": (0.0, 10.0),
        "Max_depth": (1.0, 20.0)
    }
    
    # Identify a "bad" row (high ydist)
    tbl = ezr.Tbl([header] + rows)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Optimization Recommendation for bad configuration:")
    if recommendation:
        for col, val in recommendation.items():
            print(f"  Change '{col}' to {val}")
    else:
        print("  No single-lever change found to improve performance.")
