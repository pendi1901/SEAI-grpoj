import ezr

def loading_data(file):
    data = list(ezr.csv(file))
    header = data[0]
    rows = data[1:]

    return header, rows
    
def splitting_data(header, rows, test_size=10): 
    train = rows[:-test_size]
    actual = rows[-test_size:]
    test =   []
    for row in actual:
        hidden = row.copy()
        for i, name in enumerate(header):
            if name.endswith("+") or name.endswith("-"):
                hidden[i] = "?"

        test.append(hidden)
    return train, test, actual