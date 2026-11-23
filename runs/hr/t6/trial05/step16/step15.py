import ezr
import step05

def blame(header, rows):
    """
    Identifies input columns that have nothing to do with how long people stay.
    We define 'nothing to do' as columns that show no statistically significant 
    difference between the best-performing and worst-performing employees.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Sort rows by ydist (ascending: best to worst)
    sorted_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r))
    
    n = len(sorted_rows) // 4
    best = sorted_rows[:n]
    worst = sorted_rows[-n:]
    
    irrelevant = []
    
    # Iterate over all input columns (excluding goals)
    for col in tbl.x:
        if isinstance(col, ezr.Num):
            xs = [r[col.at] for r in best if r[col.at] != "?"]
            ys = [r[col.at] for r in worst if r[col.at] != "?"]
            # If the distributions are the same, the column is irrelevant
            if len(xs) > 1 and len(ys) > 1:
                if ezr.same(xs, ys):
                    irrelevant.append(col.txt)
        else:
            # For symbols, compare distributions
            best_col = ezr.Sym(col.txt, col.at)
            worst_col = ezr.Sym(col.txt, col.at)
            for r in best: ezr.add(best_col, r[col.at])
            for r in worst: ezr.add(worst_col, r[col.at])
            
            # If the most common symbol is the same, it's a candidate for irrelevance
            if ezr.mid(best_col) == ezr.mid(worst_col):
                irrelevant.append(col.txt)
                
    return irrelevant

if __name__ == "__main__":
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Get columns that have no significant impact on performance
    unimportant_cols = blame(header, rows)
    
    print("Analysis: Which columns have nothing to do with employee tenure?")
    print("The following input columns show no significant difference between")
    print("the best-performing and worst-performing employees and could be dropped:")
    for col in unimportant_cols:
        print(f"- {col}")
    
    exit(0)
