import ezr


def flow(header, row, seen):
    tbl = ezr.Tbl([header] + seen + [row])
    ydist_row = ezr.ydist(tbl, row)
    if ydist_row <= 0.5:
        return True
    return False


if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__), "Health-ClosedIssues0000.train.csv")
    rows = list(ezr.csv(path))
    header = rows[0]
    data_rows = rows[1:]

    for i, row in enumerate(data_rows):
        if flow(header, row, data_rows[:i]):
            print(f"Row {i} is good enough to ship (ydist={ezr.ydist(ezr.Tbl([header]+data_rows[:i+1]), row):.4f})")
            break
    else:
        print("No row was good enough.")
