import ezr
from step09 import spot


def race(header, rows, label):
    """Compare three strategies for finding the best row under a labelling budget."""
    tbl = ezr.Tbl(iter([header] + rows))

    # --- Strategy 1: random sampling (must be one of them) -----------------
    def _random():
        chosen = set()
        while len(chosen) < 50 and len(rows) > 0:
            i = label(label.__self__ if hasattr(label, '__self__') else None)
            # We need to pick a row index. Use the label oracle on rows in order.
            pass

    # The `label` function is given by the harness; we wrap it so each call
    # labels one row and records which indices have been labelled.
    class _LabelState:
        def __init__(self, hdr, rs, lb):
            self.hdr = hdr
            self.rs = rs
            self.lb = lb
            self.seen = set()

        def pick(self):
            # Return the next unlabelled row index (or a random one if budget allows)
            return None  # filled in per strategy

    state = _LabelState(header, rows, label)

    # --- Strategy A: greedy best-first -------------------------------------
    def _greedy():
        chosen = set()
        # Start with a few random labels to seed centroids
        for i in range(min(4, len(rows))):
            idx = state.pick()  # will be overridden; we use the label directly
            pass

    # We need a clean implementation. Let's rewrite without relying on `state`
    # and instead track labelled indices ourselves using the provided `label`.
    # The harness provides `label(i)` which returns the true goal values for row i.
    # We must call it at most 50 times total across all strategies.

    class _Tracker:
        def __init__(self, hdr, rs, lb):
            self.hdr = hdr
            self.rs = rs
            self.lb = lb
            self.called = set()   # indices already labelled

        def label_row(self, i):
            if i not in self.called:
                self.called.add(i)
                return self.lb(i)
            return None  # already known

    tracker = _Tracker(header, rows, label)

    # --- Strategy A: greedy best-first -------------------------------------
    def _greedy_search():
        chosen = set()
        # Seed with a few random labels
        for i in range(min(4, len(rows))):
            if i not in tracker.called:
                tracker.label_row(i)

        best_idx = None
        best_yd = 1e30
        while len(tracker.called) < 50 and best_idx is None:
            # Pick the unlabelled row closest to current best centroid minus worst
            cb, cr = ezr.mids(ezr.clone(tbl, [tracker.label_row(i) for i in list(chosen)[:int(len(chosen)**0.5)])]), \
                            ezr.mids(ezr.clone(tbl, []))  # placeholder

        return None  # this approach is getting tangled; let's do it cleanly below


def race(header, rows, label):
    """Compare three strategies for finding the best row under a labelling budget."""
    tbl = ezr.Tbl(iter([header] + rows))

    class _Tracker:
        def __init__(self, hdr, rs, lb):
            self.hdr = hdr
            self.rs = rs
            self.lb = lb
            self.called = set()

        def label_row(self, i):
            if i not in self.called:
                self.called.add(i)
                return self.lb(i)
            return None

    # --- Strategy A: greedy best-first -------------------------------------
    def _greedy():
        trk = _Tracker(header, rows, label)
        chosen = set()
        # Seed with a few random labels to get initial centroids
        for i in range(min(4, len(rows))):
            if i not in trk.called:
                trk.label_row(i)

        best_idx = None
        best_yd = 1e30
        while len(trk.called) < 50 and best_idx is None:
            # Compute centroids of current labelled rows (best side)
            if not chosen:
                break
            seed_n = int(len(chosen) ** 0.5)
            seed_rows = list(chosen)[:seed_n]
            cb_centroid = ezr.mids(ezr.clone(tbl, [trk.label_row(i) for i in seed_rows]))

            # Pick the unlabelled row closest to best centroid minus worst centroid
            rest_centroid = ezr.mids(ezr.clone(tbl, []))  # placeholder; will be fixed

            todo = [i for i in range(len(rows)) if i not in trk.called]
            todo.sort(key=lambda z: (ezr.xdist(tbl, rows[z], cb_centroid) -
                                     ezr.xdist(tbl, rows[z], rest_centroid)))

            # Pick the first one
            idx = todo[0]
            lab = trk.label_row(idx)
            chosen.add(idx)
            if lab is not None:
                yd = ezr.ydist(tbl, lab)
                if yd < best_yd:
                    best_yd = yd
                    best_idx = idx

        return (best_idx, best_yd)

    # --- Strategy B: random sampling --------------------------------------
    def _random():
        trk = _Tracker(header, rows, label)
        chosen = set()
        for i in range(min(4, len(rows))):
            if i not in trk.called:
                trk.label_row(i)

        best_idx = None
        best_yd = 1e30
        while len(trk.called) < 50 and best_idx is None:
            todo = [i for i in range(len(rows)) if i not in trk.called]
            # Sort by closeness to worst centroid minus best centroid (opposite of greedy)
            cb_centroid = ezr.mids(ezr.clone(tbl, []))  # placeholder
            rest_centroid = ezr.mids(ezr.clone(tbl, []))  # placeholder

        return None


# Let's start fresh with a clean implementation.


def race(header, rows, label):
    """Compare three strategies for finding the best row under a labelling budget."""
    tbl = ezr.Tbl(iter([header] + rows))

    class _Tracker:
        def __init__(self, hdr, rs, lb):
            self.hdr = hdr
            self.rs = rs
            self.lb = lb
            self.called = set()

        def label_row(self, i):
            if i not in self.called:
                self.called.add(i)
                return self.lb(i)
            return None

    # --- Strategy A: greedy best-first -------------------------------------
    def _greedy():
        trk = _Tracker(header, rows, label)
        chosen = set()
        for i in range(min(4, len(rows))):
            if i not in trk.called:
                trk.label_row(i)

        best_idx = None
        best_yd = 1e30
        while len(trk.called) < 50 and best_idx is None:
            seed_n = int(len(chosen) ** 0.5) if chosen else 2
            seed_rows = list(chosen)[:seed_n]
            cb_centroid = ezr.mids(ezr.clone(tbl, [trk.label_row(i) for i in seed_rows]))

            # For the "rest" side, use a random sample of unlabelled rows to estimate worst centroid
            rest_sample = [i for i in range(len(rows)) if i not in trk.called][:seed_n]
            rest_centroid = ezr.mids(ezr.clone(tbl, [trk.label_row(i) for i in rest_sample]))

            todo = [i for i in range(len(rows)) if i not in trk.called]
            todo.sort(key=lambda z: (ezr.xdist(tbl, rows[z], cb_centroid) -
                                     ezr.xdist(tbl, rows[z], rest_centroid)))

            idx = todo[0]
            lab = trk.label_row(idx)
            chosen.add(idx)
            if lab is not None:
                yd = ezr.ydist(tbl, lab)
                if yd < best_yd:
                    best_yd = yd
                    best_idx = idx

        return (best_idx, best_yd)

    # --- Strategy B: random sampling --------------------------------------
    def _random():
        trk = _Tracker(header, rows, label)
        chosen = set()
        for i in range(min(4, len(rows))):
            if i not in trk.called:
                trk.label_row(i)

        best_idx = None
        best_yd = 1e30
        while len(trk.called) < 50 and best_idx is None:
            todo = [i for i in range(len(rows)) if i not in trk.called]
            # Pick randomly from unlabelled rows
            import random as _r
            idx = _r.choice(todo)
            lab = trk.label_row(idx)
            chosen.add(idx)
            if lab is not None:
                yd = ezr.ydist(tbl, lab)
                if yd < best_yd:
                    best_yd = yd
                    best_idx = idx

        return (best_idx, best_yd)

    # --- Strategy C: worst-first ------------------------------------------
    def _worst():
        trk = _Tracker(header, rows, label)
        chosen = set()
        for i in range(min(4, len(rows))):
            if i not in trk.called:
                trk.label_row(i)

        best_idx = None
        best_yd = 1e30
        while len(trk.called) < 50 and best_idx is None:
            # Pick the unlabelled row farthest from current best centroid (worst side)
            seed_n = int(len(chosen) ** 0.5) if chosen else 2
            seed_rows = list(chosen)[:seed_n]
            cb_centroid = ezr.mids(ezr.clone(tbl, [trk.label_row(i) for i in seed_rows]))

            # Use worst centroid (far from best) to pick rows that are bad
            rest_sample = [i for i in range(len(rows)) if i not in trk.called][:seed_n]
            rest_centroid = ezr.mids(ezr.clone(tbl, [trk.label_row(i) for i in rest_sample]))

            todo = [i for i in range(len(rows)) if i not in trk.called]
            # Sort by closeness to worst centroid (far from best) minus closeness to best
            todo.sort(key=lambda z: (ezr.xdist(tbl, rows[z], rest_centroid) -
                                     ezr.xdist(tbl, rows[z], cb_centroid)))

            idx = todo[0]
            lab = trk.label_row(idx)
            chosen.add(idx)
            if lab is not None:
                yd = ezr.ydist(tbl, lab)
                if yd < best_yd:
                    best_yd = yd
                    best_idx = idx

        return (best_idx, best_yd)

    # Run all three strategies and compare
    greedy_result = _greedy()
    random_result = _random()
    worst_result = _worst()

    results = {
        "greedy": greedy_result,
        "random": random_result,
        "worst": worst_result,
    }

    # Find the best result overall (lowest ydist)
    best_strategy = min(results.keys(), key=lambda s: results[s][1])
    winner_name = best_strategy
    winner_row = results[best_strategy][0]

    return {
        "winner": winner_name,
        "row": winner_row,
        "tried": ["greedy", "random", "worst"],
    }


if __name__ == "__main__":
    import csv
    with open("WA_Fn-UseC_-HR-Employee-Attrition.train.csv", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [next(reader) for _ in range(1470)]

    result = race(header, rows, label)
    print(f"Winner: {result['winner']}, Row: {result['row']}")
