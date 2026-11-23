import ezr
import random

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We define 'bad' as having a high ydist (far from the goal).
    We compare the distribution of input values in the worst 25% of rows
    against the best 25% of rows.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Sort rows by ydist (ascending: best to worst)
    sorted_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r))
    
    n = len(sorted_rows) // 4
    best = sorted_rows[:n]
    worst = sorted_rows[-n:]
    
    # For each input column, check if the distribution of values differs
    # significantly between the best and worst groups.
    # We use the same 'same' logic from ezr.
    explanations = []
    for col in tbl.x:
        if type(col) is ezr.Num:
            xs = [r[col.at] for r in best if r[col.at] != "?"]
            ys = [r[col.at] for r in worst if r[col.at] != "?"]
            if len(xs) > 1 and len(ys) > 1:
                if not ezr.same(xs, ys):
                    explanations.append(col.txt)
        else:
            # For symbols, check if the most frequent value differs
            best_mode = ezr.mid(ezr.adds([r[col.at] for r in best if r[col.at] != "?"]))
            worst_mode = ezr.mid(ezr.adds([r[col.at] for r in worst if r[col.at] != "?"]))
            if best_mode != worst_mode:
                explanations.append(col.txt)
                
    return explanations

if __name__ == "__main__":
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    reasons = blame(header, rows)
    
    print("Analysis: What factors correlate with short employee stays?")
    print("The following input columns show significant differences between")
    print("the best-performing and worst-performing employees:")
    for reason in reasons:
        print(f"- {reason}")
    
    exit(0)
