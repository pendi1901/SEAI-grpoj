import csv

def flow(header, row, seen):
    """
    Decides whether to stop the search based on whether the current row
    is a new Pareto-optimal point. If the current row is not dominated by
    any previously seen row, it is considered an improvement.
    """
    if not seen:
        return True

    goals = []
    for i, name in enumerate(header):
        if name.endswith('-'):
            goals.append((i, -1))  # Minimize
        elif name.endswith('+'):
            goals.append((i, 1))   # Maximize

    def dominates(r1, r2):
        """Returns True if r1 dominates r2."""
        better_in_at_least_one = False
        for i, direction in goals:
            v1, v2 = float(r1[i]), float(r2[i])
            if direction == 1:
                if v1 < v2: return False
                if v1 > v2: better_in_at_least_one = True
            else:
                if v1 > v2: return False
                if v1 < v2: better_in_at_least_one = True
        return better_in_at_least_one

    # If the current row is not dominated by any row in 'seen', it's a new best
    for s in seen:
        if dominates(s, row):
            return False
    return True

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = [float(val) if val.replace('.', '', 1).isdigit() or 
                                 (val.startswith('-') and val[1:].replace('.', '', 1).isdigit()) 
                                 else val for val in row]
                rows.append(processed_row)

        seen = []
        stopped = False
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                # If we find a new Pareto-optimal point, we continue.
                # If we haven't found a new one in a while, we could stop.
                # Here we simply report the last improvement found.
                last_improvement_idx = i
            seen.append(row)
        
        print(f"The best setup (Pareto-optimal) was last improved at row {last_improvement_idx + 1}.")
        print("You can stop paying for runs after this point.")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
