import ezr

def certify(xs, ys):
    """Returns True if xs and ys are the same apart from noise."""
    return (ezr.stats.cohen(xs, ys) 
            and ezr.stats.cliffs(xs, ys) 
            and ezr.stats.ks(xs, ys))

if __name__ == "__main__":
    tbl = ezr.Tbl(open("WA_Fn-UseC_-HR-Employee-Attrition.train.csv", encoding="utf-8-sig"))
    
    overtime_ycr = []
    non_overtime_ycr = []
    for row in tbl.rows:
        if row[22] == "Y":
            overtime_ycr.append(row[32])
        else:
            non_overtime_ycr.append(row[32])
    
    result = certify(overtime_ycr, non_overtime_ycr)
    print(f"Overtime workers stay in their current role {'similarly' if result else 'differently'} to those who don't work overtime.")
