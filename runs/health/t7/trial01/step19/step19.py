from step09 import spot
from load import loading_data, splitting_data
from outliers import novelty_scores


if __name__ == "__main__":
    header, rows = loading_data("Health-ClosedIssues0000.n1000.train.csv")
    train, hidden, _ = splitting_data(header, rows, test_size=20)
    scores = novelty_scores(header, train, hidden)
    def novelty(position):
        return scores[position]

    ranked = sorted(range(len(hidden)), key=novelty, reverse=True)

    print("Most unfamiliar candidates by distance to their fifth-nearest past setup:")
    for position in ranked[:5]:
        print(f"Candidate {position}: distance {scores[position]:.3f}")
    print("Larger distances mean less familiar input combinations, not proven errors.")
