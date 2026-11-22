from load import loading_data
from statistics import mean, median
from comparisionchecker import same_checker

def certify(xs, ys):
    return same_checker(xs, ys)

if __name__ == "__main__":
    header, rows = loading_data("Health-ClosedIssues0000.n1000.train.csv")
    size_index = header.index("N_estimators")
    error_index = header.index("MRE-")
    sizes = []
    for row in rows : 
        sizes.append(row[size_index])
    
    cutoff = median(sizes)
    small = []
    large = []

    for row in rows:
        if row[size_index] <= cutoff:
            small.append(row[error_index])
        else:
            large.append(row[error_index])

    print("Small setup MRE: ", mean(small))
    print("Large setup MRE: ", mean(large))
    
    similarity_check = certify(small, large)

    if similarity_check:
        print("The two groups are similar")
    else:
        print("The two groups are not similar")