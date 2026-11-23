import csv
import random

def choose(header, rows, label):
    """
    Finds the best setup for a large, high-criticality project.
    We prioritize rows where 'Size' and 'Criticality' are high,
    then use a small budget of 50 labels to find the best among them.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    size_idx = header.index('Size')
    crit_idx = header.index('Criticality')

    def get_score(row_goals):
        s = 0
        for i, val in enumerate(row_goals):
            idx = goal_indices[i]
            s += val if header[idx].endswith('-') else (1.0 - val)
        return s

    # Filter for "large and high criticality" projects (top 25% in both)
    # We use a heuristic to identify candidates without labeling
    candidates = []
    for i, row in enumerate(rows):
        if row[size_idx] > 0.75 and row[crit_idx] > 0.75:
            candidates.append(i)

    # If not enough candidates, fall back to all rows
    if len(candidates) < 10:
        candidates = list(range(len(rows)))

    # Sample up to 50 candidates to find the best
    best_idx = -1
    best_score = float('inf')
    
    # Shuffle to ensure random exploration within the filtered set
    random.shuffle(candidates)
    
    for i in candidates[:50]:
        goals = label(i)
        score = get_score(goals)
        if score < best_score:
            best_score = score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        rows = []
        true_goals = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
            for row in reader:
                processed = []
                goals = []
                for i, val in enumerate(row):
                    if i in goal_indices:
                        goals.append(float(val))
                        processed.append("?")
                    else:
                        processed.append(float(val) if val.replace('.','',1).isdigit() else val)
                rows.append(processed)
                true_goals.append(goals)

        labeled_count = 0
        def label(i):
            global labeled_count
            labeled_count += 1
            if labeled_count > 50:
                raise Exception("Exceeded 50 labels!")
            return true_goals[i]

        best_idx = choose(header, rows, label)
        print(f"Analysis complete for large, high-criticality projects.")
        print(f"Best row found at index {best_idx} using {labeled_count} labels.")
        print("This setup minimizes risk and cost for large-scale, critical operations.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
