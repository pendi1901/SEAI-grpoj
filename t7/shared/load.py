import ezr

def loading_data(file):
    data = list(ezr.csv(file))
    header = data[0]
    rows = data[1:]

    return header, rows
    