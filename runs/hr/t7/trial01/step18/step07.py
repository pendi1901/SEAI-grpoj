from share import setup_trial, guided_search, best_positions
from load import loading_data, splitting_data
import ezr
import random

def choose(header, rows, label): 
    if not rows:
        raise RuntimeError("No rows to choose from")
    copy, trial, tested = setup_trial(header, rows, label)
    positions = guided_search(header, copy, trial, tested, budget=50)
    return best_positions(header, tested, positions)

if __name__ == "__main__":
    random.seed(1)
    header, rows = loading_data("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv")
    _, hidden, actual = splitting_data(header, rows , test_size = min(150, len(rows)))
    table = ezr.Tbl([header] + actual)
    goal_positions = [column.at for column in table.y]
    asked = set()
    def label(position): 
        if position not in asked and len(asked) >=50: 
            raise RuntimeError("trial budget exhausted")
        asked.add(position)
        return [actual[position][at] for at in goal_positions]
    winner = choose(header, hidden, label)

    print("Positions we've chosen", winner)
    print("Trials used ", len(asked))
    print("set up we're going with ",  actual[winner])