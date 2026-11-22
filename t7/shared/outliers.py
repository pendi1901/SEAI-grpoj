import ezr
from neighbours import nearest_rows


def novelty_scores(header, known, rows, k=5):
    if not known:
        raise ValueError("At least one past setup is needed.")
    if k < 1:
        raise ValueError("k must be at least 1.")
    table = ezr.Tbl([header] + known)
    scores = []
    for row in rows:
        neighbours = nearest_rows(table, known, row, k)
        scores.append(ezr.xdist(table, row, neighbours[-1]))
    return scores


def abnormal(header, rows):
    table = ezr.Tbl([header] + rows)
    scores = []

    for row in rows:
        largest = 0

        for column in table.x:
            if not isinstance(column, ezr.Num) or column.sd == 0:
                continue

            value = row[column.at]
            if value == "?":
                continue

            distance = abs(value - column.mu) / column.sd
            largest = max(largest, distance)

        scores.append(largest)

    def oddness(position):
        return scores[position]

    return sorted(range(len(rows)), key=oddness, reverse=True)
