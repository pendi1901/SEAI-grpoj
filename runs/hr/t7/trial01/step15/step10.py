from load import loading_data, splitting_data
from share import setup_trial, guided_search, random_search, knn_search, best_positions
import ezr
import random


def race(header, rows, labels) : 
    if not rows: 
        raise ValueError("no rows available to search")
    copy, trial, tested = setup_trial(header, rows, labels)
    strategies = [("random", random_search, 17), ("guided", guided_search, 17), ("knn",knn_search, 16)]
    found_by = {}
    tried = []


    for name, search, allocation in strategies : 
        budget = min(allocation, 50-len(tested))
        positions = search(header, copy, trial, tested, budget)
        for position in positions : 
            found_by[position]= name
        tried.append(name)
    best_row = best_positions(header, tested)

    return {"winner": found_by[best_row], "row" : best_row, "tried" : tried}


if __name__ == "__main__" : 
    random.seed(1)
    header, rows = loading_data("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv")
    sample_size = min(150, len(rows))
    _, hidden, actual = splitting_data(header, rows, sample_size)

    table = ezr.Tbl([header] + actual)
    asked = set()

    def label(position) : 
        if position not in asked and len(asked) >= 50 : 
            raise ValueError("trial's budget exhausted")
        asked.add(position)
        goals = []
        for column in table.y : 
            goals.append(actual[position][column.at])
        return goals
    
    result= race(header, hidden, label)
    winner = result["winner"]
    position = result["row"]

    print("Tried Strategies: ", result["tried"] )
    print("Winning strategy: ", winner )
    print("Position chosen: ", position)
    print("Trials used till now: ", len(asked))
    print("Chosen setup: ", actual[position] )
