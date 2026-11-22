import csv
from step02 import guess as knn_guess

def guess(header, train, test):
    """
    Estimates the first goal column for test rows.
    The customer asks about the effect of requirements changing twice as fast.
    In the pom3a dataset, 'Dynamism' represents the rate of change.
    We simulate the scenario by adjusting 'Dynamism' in the test set
    and using the trained model to predict the impact on the first goal.
    """
    # Identify index of 'Dynamism'
    dyn_idx = header.index('Dynamism')
    
    # Create a modified test set where Dynamism is doubled (capped at 1.0)
    modified_test = []
    for row in test:
        new_row = list(row)
        if isinstance(new_row[dyn_idx], float):
            new_row[dyn_idx] = min(1.0, new_row[dyn_idx] * 2.0)
        modified_test.append(new_row)
        
    return knn_guess(header, train, modified_test)

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) if val.replace('.','',1).isdigit() or (val.startswith('-') and val[1:].replace('.','',1).isdigit()) else val for val in row])
        
        # Split data
        split = int(len(rows) * 0.8)
        train_data = rows[:split]
        test_data = rows[split:]
        
        # Mask goals
        goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
        masked_test = []
        for row in test_data:
            new_row = list(row)
            for idx in goal_indices:
                new_row[idx] = "?"
            masked_test.append(new_row)
            
        predictions = guess(header, train_data, masked_test)
        
        avg_pred = sum(predictions) / len(predictions)
        print("Analysis: Impact of doubling requirement change rate (Dynamism) on the first goal.")
        print(f"The estimated average value for the first goal ({header[goal_indices[0]]}) under increased dynamism is: {avg_pred:.4f}")
        print("Increasing dynamism generally forces higher resource allocation, impacting cost and idle time.")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
