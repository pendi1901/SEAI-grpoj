import ezr

def differences(header, rows) : 
    def score(row): 
        return ezr.ydist(table, row)
    def gap_lambda(item): 
        return item[0]
    table = ezr.Tbl([header] + rows)
    sorted_rows = sorted(rows, key=score)
    max_size = len(rows)//4

    good = ezr.Tbl([header] + sorted_rows[:max_size])
    bad  = ezr.Tbl([header] + sorted_rows[-max_size:])

    diff = []
    for column in table.x : 
        good_col = good.cols[column.at]
        bad_col  = bad.cols[column.at]

        if isinstance(column, ezr.Num): 
            values_good = ezr.norm(column, good_col.mu)
            values_bad = ezr.norm(column, bad_col.mu)
            gap = abs(values_good - values_bad)
        else: 
            gap = 0
            
            for value in column.has : 
                count_good = good_col.has.get(value, 0)
                count_bad  = bad_col.has.get(value, 0)

                fraction_good = count_good / max(good_col.n, 1)
                fraction_bad  = count_bad  / max(bad_col.n, 1)

                gap+= abs(fraction_good - fraction_bad)

            gap = gap/2
        if gap > 0 : 
            diff.append((gap, column.txt))

    diff.sort(key=gap_lambda, reverse=True)
    peak_three = []
    for gap, name in diff[:3]: 
        peak_three.append(name)
    return peak_three
