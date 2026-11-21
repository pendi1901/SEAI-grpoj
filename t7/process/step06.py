import ezr
from functools import partial
from load import loading_data, splitting_data
from neighbours import average_nearby_neighbours
K=5
def justify(header, rows, row) : 
    table = ezr.Tbl([header] + rows)
    distance_to_goal = partial(ezr.ydist, table)
    estimate = average_nearby_neighbours(table, rows, row, distance_to_goal, K)

    beaten = sum(distance_to_goal(r) > estimate for r in rows)

    reason  = (
        
        f"row {row} is estimated to be {estimate:.2f} "
        f"and beats {beaten}/{len(rows)} other rows"
    )
    
    return beaten/len(rows), reason

if __name__ == "__main__":
    header, rows = loading_data("pom3a.n1000.train.csv")
    train, test, actual = splitting_data(header, rows)
    p, reason = justify(header, train, test[0])
    print(p, reason)