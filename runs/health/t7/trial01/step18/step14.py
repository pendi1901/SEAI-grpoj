from load import loading_data
from step04 import flow


def stopped_improving(header, row, seen, patience=20):
    if patience < 1:
        raise ValueError("Patience must be positive.")
    if len(seen) < patience:
        return False
    at = header.index("MRE-")
    history = seen + [row]
    best_before = min(previous[at] for previous in history[:-patience])
    return min(previous[at] for previous in history[-patience:]) >= best_before


if __name__ == "__main__":
    header, rows = loading_data("Health-ClosedIssues0000.n1000.train.csv")
    seen = []
    print("File-order illustration; no nightly timestamps are available.")
    for position, row in enumerate(rows):
        if stopped_improving(header, row, seen):
            print(f"Arrival {position}: no new best MRE in 20 arrivals; consider stopping.")
            break
        seen.append(row)
    else:
        print("No stopping signal in this stream.")
    print("A patience heuristic does not prove that future runs cannot improve.")
