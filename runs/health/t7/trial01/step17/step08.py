from load import loading_data
from recommendations import suggested_changes
import ezr

def fix(header, row, controls) : 
    train_header,  train = loading_data("Health-ClosedIssues0000.n1000.train.csv")

    if train_header != header : 
        raise ValueError("columns in train don't match ")

    return suggested_changes(header, train, row, controls)

if __name__ == "__main__":
    header, rows  = loading_data("Health-ClosedIssues0000.n1000.train.csv")
    table = ezr.Tbl([header] + rows)

    def quality(row): 
        return ezr.ydist(table, row)
    
    bad_row = max(rows, key = quality)

    controls = {}

    for column in table.x : 
        if column.txt not in ["N_estimators", "criterion", "Min_sample_leaves", "Min_impurity_decrease", "Max_depth"] : 
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

    for name in ["N_estimators", "Max_depth"]:
        low, high = controls[name]
        controls[name] = (low, bad_row[header.index(name)])
    for name in ["Min_sample_leaves", "Min_impurity_decrease"]:
        low, high = controls[name]
        controls[name] = (bad_row[header.index(name)], high)
    controls["criterion"] = [bad_row[header.index("criterion")]]
    changes = fix(header, bad_row, controls)
    print("Model size cannot increase; actual run time still needs checking.")


    for name, value in changes.items():  
        position = header.index(name)
        print(f"{name} : {bad_row[position]} -> {value}")