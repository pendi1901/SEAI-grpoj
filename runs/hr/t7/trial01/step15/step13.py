from load import loading_data
from statistics import mean, median
from comparisionchecker import same_checker

def certify(xs, ys):
    return same_checker(xs, ys)

if __name__ == "__main__":
    header, rows = loading_data("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv")
    training_index = header.index("TrainingTimesLastYear")
    manager_index = header.index("YearsWithCurrManager+")
    training_counts = []
    for row in rows : 
        training_counts.append(row[training_index])
    
    cutoff = median(training_counts)
    less_training = []
    more_training = []

    for row in rows:
        if row[training_index] <= cutoff:
            less_training.append(row[manager_index])
        else:
            more_training.append(row[manager_index])

    print("Less training, years with manager: ", mean(less_training))
    print("More training, years with manager: ", mean(more_training))
    
    similarity_check = certify(less_training, more_training)

    if similarity_check:
        print("The two groups are similar")
    else:
        print("The two groups are not similar")