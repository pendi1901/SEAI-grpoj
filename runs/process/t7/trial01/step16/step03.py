from load import loading_data
from statistics import mean, median
from comparisionchecker import same_checker

def certify(xs, ys):
    return same_checker(xs, ys)

if __name__ == "__main__":
    header, rows = loading_data("pom3a.n1000.train.csv")
    team_index = header.index("Team Size")
    cost_index = header.index("Cost-")
    team_sizes = []
    for row in rows : 
        team_sizes.append(row[team_index])
    
    cutoff = median(team_sizes)
    small_team = []
    large_team = []

    for row in rows:
        if row[team_index] <= cutoff:
            small_team.append(row[cost_index])
        else:
            large_team.append(row[cost_index])

    print("Small Team Cost: ", mean(small_team))
    print("Large Team Cost: ", mean(large_team))
    
    similarity_check = certify(small_team, large_team)

    if similarity_check:
        print("The two groups are similar")
    else:
        print("The two groups are not similar")