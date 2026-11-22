import ezr
from load import loading_data

def remember(header, rows):

    def distance_to_goal(i):
        return ezr.ydist(table, rows[i])
    
    if not rows:
        return []

    table = ezr.Tbl([header] + rows)
    positions = list(range(len(rows)))
    positions.sort(key=distance_to_goal)
    # we need to get the top 5% rows here
    count = len(rows)//20
    return positions[:count]



if __name__ == "__main__":
    header, rows = loading_data("Health-ClosedIssues0000.n1000.train.csv")
    selected = remember(header, rows)
    print(selected)
