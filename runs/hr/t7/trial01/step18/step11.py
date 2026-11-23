import ezr 
from step01 import remember 
from load import loading_data
from neighbours import nearest_rows

if __name__ == "__main__" : 
    header, rows = loading_data("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv")
    proposal = rows[-1].copy()
    past = rows[:-1]
    table = ezr.Tbl([header] + past)
    for col in table.y : 
        proposal[col.at] = "?"

    near = nearest_rows(table, past, proposal, k =40)
    original_pos = {id(row) : position for position, row in enumerate(past)}


    print("Past Setups: ")
    for row in near : 
        print("Row", original_pos[id(row)])
        for col in table.y : 
            print(col.txt, "," , row[col.at])

    print("best setups among neighbours")
    best = remember(header, near)


    for position in best : 
        row = near[position]
        print(original_pos[id(row)])

