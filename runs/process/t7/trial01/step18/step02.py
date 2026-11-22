import ezr
from load import loading_data, splitting_data
from neighbours import average_nearby_neighbours
def guess(header, train, test):
    table = ezr.Tbl([header] + train)
    predictions = []
    goal_index = table.y[0].at
    def goal(row):
        return row[goal_index]
    for row in test: 
        prediction = average_nearby_neighbours(table, train, row, goal)
        predictions.append(prediction)
    return predictions


if __name__ == "__main__":
    header, rows = loading_data("pom3a.n1000.train.csv")
    train, test, actual = splitting_data(header, rows)
    predictions = guess(header, train, test)
    print(predictions)

