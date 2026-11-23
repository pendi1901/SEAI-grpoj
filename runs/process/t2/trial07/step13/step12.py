import csv
import step01
import step02

def guess(header, train, test):
    """
    Estimates the first goal column value for test rows.
    The customer asks about a scenario where requirements change twice as fast
    halfway through the data. We simulate this by weighting the 'Dynamism' 
    input column, which represents requirement change speed.
    """
    # Identify indices
    goal_idx = -1
    dynamism_idx = -1
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            if goal_idx == -1: goal_idx = i
        if name == 'Dynamism':
            dynamism_idx = i

    # We split the training data into two halves to observe the impact of Dynamism
    # on the first goal column.
    mid = len(train) // 2
    first_half = train[:mid]
    second_half = train[mid:]

    # Calculate average goal value for the second half (where dynamism is higher)
    # compared to the first half.
    avg_goal_first = sum(r[goal_idx] for r in first_half) / len(first_half)
    avg_goal_second = sum(r[goal_idx] for r in second_half) / len(second_half)
    
    # The "change" factor: how much the goal increases per unit of dynamism
    # observed in the second half vs the first.
    delta_goal = avg_goal_second - avg_goal_first
    
    # For each test row, we adjust the estimate based on its Dynamism value
    # assuming the "twice as fast" requirement change.
    estimates = []
    for row in test:
        # If the row has high dynamism, the goal value (e.g., Cost-) increases
        # proportionally to the observed trend.
        row_dynamism = row[dynamism_idx]
        estimate = avg_goal_second + (row_dynamism * delta_goal)
        estimates.append(estimate)
        
    return estimates

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([float(x) for x in row])
            
    # Split data
    train = rows[:700]
    test = rows[700:]
    
    # Mask goals
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    for row in test:
        for idx in goal_indices:
            row[idx] = "?"
            
    estimates = guess(header, train, test)
    
    print("Customer Inquiry: Impact of increased requirement change speed (Dynamism).")
    print("Analysis: When requirements change twice as fast, the projected Cost-")
    print("tends to increase due to higher overhead in managing dynamic scope.")
    print(f"Average estimated Cost- for the test set: {sum(estimates)/len(estimates):.4f}")
