import ezr
from functools import partial
from load import loading_data, splitting_data
from neighbours import average_nearby_neighbours
K=5
def justify(header, rows, row) : 
    if not rows:
        raise ValueError("At least one reference row is needed.")
    table = ezr.Tbl([header] + rows)
    distance_to_goal = partial(ezr.ydist, table)
    estimate = average_nearby_neighbours(table, rows, row, distance_to_goal, K)

    beaten = sum(distance_to_goal(r) > estimate for r in rows)

    reason  = (
        
        f"Based on the average goal distance of its {min(K, len(rows))} "
        f"nearest past setups, this setup is estimated to beat "
        f"{beaten} of {len(rows)} reference setups."
    )
    
    return beaten/len(rows), reason

if __name__ == "__main__":
    header, rows = loading_data("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv")
    train, test, actual = splitting_data(header, rows)
    p, reason = justify(header, train, test[0])
    print(p, reason)
