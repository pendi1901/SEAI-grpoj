import ezr
import step08

def fix(header, row, levers):
    """
    Suggests a change to a 'bad' row to improve its goal metrics.
    We use the global distribution (via the table) to calculate ydist.
    """
    # Load the full data to establish the context for ydist
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header_data = data[0]
    rows_data = data[1:]
    tbl = ezr.Tbl([header_data] + rows_data)
    
    best_change = {}
    # Calculate current distance
    current_ydist = ezr.ydist(tbl, row)
    best_ydist = current_ydist
    
    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Try changing the lever
        if isinstance(allowed, list):  # Symbolic
            for val in allowed:
                if val != original_val:
                    row[idx] = val
                    d = ezr.ydist(tbl, row)
                    if d < best_ydist:
                        best_ydist = d
                        best_change = {col_name: val}
                    row[idx] = original_val # Reset
        else:  # Numeric (low, high)
            low, high = allowed
            # Test boundaries and midpoint
            for val in [float(low), float((low + high) / 2), float(high)]:
                if val != original_val:
                    row[idx] = val
                    d = ezr.ydist(tbl, row)
                    if d < best_ydist:
                        best_ydist = d
                        best_change = {col_name: val}
                    row[idx] = original_val # Reset
        
    return best_change

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Levers excluding salary-related columns
    levers = {
        "businessTravel": ["Non-Travel", "Travel_Frequently", "Travel_Rarely"],
        "overTime": ["No", "Yes"],
        "TrainingTimesLastYear": (0, 6),
        "StockOptionLevel": (0, 3),
        "JobInvolvement": (1, 4),
        "EnvironmentSatisfaction": (1, 4)
    }
    
    # Identify a "bad" row (low tenure)
    idx_tenure = header.index("YearsAtCompany+")
    bad_rows = [r for r in rows if isinstance(r[idx_tenure], (int, float)) and r[idx_tenure] < 2]
    
    if bad_rows:
        sample_bad = bad_rows[0]
        suggestion = fix(header, sample_bad, levers)
        
        print("Analysis: Recommendations for improving employee retention without pay increases.")
        if suggestion:
            col, val = list(suggestion.items())[0]
            print(f"For the identified employee, we recommend changing '{col}' to '{val}'.")
            print("This change is predicted to improve the employee's alignment with organizational goals.")
        else:
            print("No effective non-monetary lever change found for this record.")
    else:
        print("No bad records found to analyze.")
