from load import loading_data
from statistics import mean
from comparisionchecker import same_checker


def certify(xs, ys):
    return same_checker(xs, ys)


if __name__ == "__main__":
    header, rows = loading_data("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv")
    overtime = header.index("overTime")
    role = header.index("YearsInCurrentRole+")
    yes = []
    no = []
    for row in rows:
        if row[overtime] == "Yes":
            yes.append(row[role])
        elif row[overtime] == "No":
            no.append(row[role])
    print("Mean years in role with overtime:", mean(yes))
    print("Mean years in role without overtime:", mean(no))
    print("The groups are similar:", certify(yes, no))
    print("These are recorded years in role, not observed future leaving times.")
