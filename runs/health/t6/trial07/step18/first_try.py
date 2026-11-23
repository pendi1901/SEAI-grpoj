import ezr
import step08

def fix(header, row, levers):
    """
    Finds the single best change to a 'bad' row that improves its ydist,
    staying within the provided lever constraints.
    """
    # Reuse the logic from step08 which already implements the search
    # for the best single lever change.
    return step08.fix(header, row, levers)

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Define levers based on column types found in the data
    levers = {
        "N_estimators": (50.0, 200.0),
        "criterion": ["absolute_error", "poisson", "squared_error"],
        "Min_sample_leaves": (1.0, 20.0),
        "Min_impurity_decrease": (0.0, 10.0),
        "Max_depth": (1.0, 20.0)
    }
    
    # Pick a "bad" row (one with high ydist)
    tbl = ezr.Tbl([header] + rows)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    recommendation = fix(header, bad_row, levers)
    
    print("--- Single Lever Optimization ---")
    print(f"Original bad setup: {bad_row}")
    if recommendation:
        col_name = list(recommendation.keys())[0]
        new_val = recommendation[col_name]
        print(f"Recommended change: Set '{col_name}' to {new_val}.")
        print("This single change minimizes the distance to ideal performance goals.")
    else:
        print("No single lever change found that improves performance.")
    
    exit(0)
