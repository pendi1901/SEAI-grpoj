from load import loading_data
from recommendations import suggested_changes
import ezr

def fix(header, row, controls) : 
    train_header,  train = loading_data("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv")

    if train_header != header : 
        raise ValueError("columns in train don't match ")

    return suggested_changes(header, train, row, controls)

if __name__ == "__main__":
    header, rows  = loading_data("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv")
    table = ezr.Tbl([header] + rows)

    def quality(row): 
        return ezr.ydist(table, row)
    
    bad_row = max(rows, key = quality)

    controls = {}

    for column in table.x : 
        if column.txt not in ["overTime", "businessTravel", "TrainingTimesLastYear", "PercentSalaryHike", "StockOptionLevel"] : 
            continue
        values=  []
        for row in rows: 
            value = row[column.at]
            if value != "?" : 
                values.append(value)
        if not values: 
            continue

        if isinstance(column, ezr.Num) : 
            controls[column.txt] = (min(values), max(values))
        else: 
            controls[column.txt] = list(dict.fromkeys(values))

    changes = fix(header, bad_row, controls)


    for name, value in changes.items():  
        position = header.index(name)
        print(f"{name} : {bad_row[position]} -> {value}")