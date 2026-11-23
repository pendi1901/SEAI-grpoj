from load import loading_data
from step04 import flow  # Entry point used by the scorer.
from outliers import novelty_scores


if __name__ == "__main__":
    header, rows = loading_data("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv")
    department = header.index("department")
    team = [row for row in rows if row[department] == "Research & Development"]
    known = team[:100]
    if len(known) < 20:
        raise ValueError("Not enough reference rows for this department.")
    distances = []
    for position, row in enumerate(known):
        others = known[:position] + known[position + 1:]
        distances.append(novelty_scores(header, others, [row])[0])
    distances.sort()
    cutoff = distances[int(0.95 * (len(distances) - 1))]
    print("File-order example for Research & Development; no monthly history is available.")
    flagged = 0
    for row in team[100:]:
        distance = novelty_scores(header, known, [row])[0]
        if distance > cutoff:
            flagged += 1
    print("Records flagged for review:", flagged, "of", len(team[100:]))
    print("These are unfamiliar records within a department, not proof that the whole team changed.")
