import ezr
def nearest_rows(table, rows, row, k): 
    def dist_btw_rows(training_row):
        return ezr.xdist(table, row, training_row)
        
    neighbours= sorted(rows, key=dist_btw_rows)[:k]
    return neighbours

def average_nearby_neighbours(table, rows, row, value , k=10) : 
    neighbours = nearest_rows(table, rows, row, k)
    total = 0 
    for neighbour in neighbours:
        total += value(neighbour)

    prediction  =total/len(neighbours)
    return prediction