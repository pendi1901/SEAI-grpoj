def choose(header, rows, label):
    """Interview up to 50 staff and return the position of the best one."""
    goal_cols = [c for c in header if c.endswith('+')]
    
    attrition_idx = None
    for i, col in enumerate(header):
        if col == 'attrition':
            attrition_idx = i
            break
    
    # Pick up to 50 employees who haven't left yet.
    candidates = []
    for i, row in enumerate(rows):
        if attrition_idx is not None and row[attrition_idx] == 'No':
            candidates.append(i)
    
    n_to_interview = min(50, len(candidates))
    chosen = candidates[:n_to_interview]
    
    best_pos = -1
    best_score = float('-inf')
    
    for pos in chosen:
        goals = label(pos)  # list of true goal values (len == len(goal_cols))
        score = sum(goals)
        
        if score > best_score:
            best_score = score
            best_pos = pos
    
    return best_pos


if __name__ == '__main__':
    import csv

    with open('WA_Fn-UseC_-HR-Employee-Attrition.train.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    result = choose(header, rows, label)
    print(
        f"Interviewed up to 50 staff. "
        f"The best arrangement keeps the employee at position {result}."
    )
