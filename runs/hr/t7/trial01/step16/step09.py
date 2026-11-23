from outliers import abnormal
from load import loading_data
import random
import ezr

def spot(header, rows) : 
    return abnormal(header, rows)


if __name__ == "__main__" : 
    header, rows = loading_data("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv")
    rand = random.Random(1)
    selected = rand.sample(rows, min(100, len(rows)))
    sample = []

    for row in selected : 
        sample.append(row.copy())

    table = ezr.Tbl([header] + sample)

    numeric_columns = []
    for column in table.x: 
        if isinstance(column, ezr.Num) and column.sd > 0 : 
            numeric_columns.append(column)
    if not numeric_columns : 
        raise ValueError("no numeric columns")
    
    error_position = rand.randrange(len(sample))
    column = rand.choice(numeric_columns)

    wrong_value = column.mu + 6 * column.sd
    sample[error_position][column.at] = wrong_value

    suspects = spot(header, sample)
    error_rank = suspects.index(error_position) + 1

    print(f"Changed {column.txt} in row {error_position} to {wrong_value:.2f}")
    print(f"Top 10 suspicious rows: {suspects[:10]}")
    print(f"The changed row ranked #{error_rank}")

