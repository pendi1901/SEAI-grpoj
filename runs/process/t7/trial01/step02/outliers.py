import ezr


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
