import ezr
from load import loading_data, splitting_data
K=10
def guess(header, train, test):
    table = ezr.Tbl([header] + train)
    predictions = []
    goal_index = table.y[0].at
    for row in test: 
        def dist_btw_rows(training_row):
            return ezr.xdist(table, row, training_row)
            
        neighbours= sorted(train, key=dist_btw_rows)[:K]
        total = 0 
        for neighbour in neighbours:
            total += neighbour[goal_index]

        prediction  =total/len(neighbours)
        predictions.append(prediction)

    return predictions


if __name__ == "__main__":
    header, rows = loading_data("pom3a.n1000.train.csv")
    train, test, actual = splitting_data(header, rows)
    predictions = guess(header, train, test)
    print(predictions)

