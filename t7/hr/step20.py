import random
import ezr

from load import loading_data, splitting_data
from share import run_race, biggest_raises, random_search, guided_search, knn_search


def race(header, rows, label):
    strategies = [
        ("biggest raises", biggest_raises, 13),
        ("random", random_search, 13),
        ("guided", guided_search, 12),
        ("knn", knn_search, 12),
    ]
    return run_race(header, rows, label, strategies)


if __name__ == "__main__":
    random.seed(1)
    header, rows = loading_data("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv")
    _, hidden, actual = splitting_data(header, rows, test_size=min(150, len(rows)))
    goals = [i for i, name in enumerate(header) if name.endswith(("+", "-"))]
    asked = []

    def label(position):
        if position not in asked:
            if len(asked) >= 50:
                raise ValueError("Trial budget exhausted.")
            asked.append(position)
        return [actual[position][at] for at in goals]

    result = race(header, hidden, label)
    table = ezr.Tbl([header] + [actual[i] for i in asked])

    def quality(position):
        return ezr.ydist(table, actual[position])

    baseline = min(asked[:13], key=quality)
    print("Strategies tried:", result["tried"])
    print("Winning strategy:", result["winner"])
    print("Chosen position:", result["row"])
    print("Trials used:", len(asked))
    print(f"Best biggest-raise distance: {quality(baseline):.4f}")
    print(f"Race winner distance: {quality(result['row']):.4f} (lower is better)")
    print("The baseline gets 13 labels; the race winner is selected from all 50.")
    print("One shared-budget run; this does not establish a general strategy advantage.")

    print("Lower TotalWorkingYears breaks pay-rise ties; it is a proxy for newest staff.")
