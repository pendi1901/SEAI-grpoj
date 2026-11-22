import ezr
from statistics import mean
from step03 import certify
from load import loading_data


if __name__ == "__main__":
    header, rows = loading_data("pom3a.n1000.train.csv")
    table = ezr.Tbl([header] + rows)

    scores = [ezr.ydist(table, row) for row in rows]
    halfway = len(scores) // 2
    first = scores[:halfway]
    second = scores[halfway:]

    print("Comparing file halves, not known before/after dates.")
    print(f"First half mean distance: {mean(first):.4f}")
    print(f"Second half mean distance: {mean(second):.4f}")

    if certify(first, second):
        print("The groups are similar under this comparison.")
    else:
        print("The comparison detects a difference.")