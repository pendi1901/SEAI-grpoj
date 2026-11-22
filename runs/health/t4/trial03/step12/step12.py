import csv
from step02 import guess as base_guess

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows.
    """
    return base_guess(header, train, test)

def analyze_impact(header, rows):
    """
    Compares the performance of the full model vs a halved model.
    """
    # Identify N_estimators index
    n_est_idx = header.index('N_estimators')
    
    # Split data: full size vs halved size
    # We simulate "halving" by filtering rows where N_estimators is roughly half
    # of the max value found in the dataset.
    max_n = max(r[n_est_idx] for r in rows)
    
    full_model_rows = [r for r in rows if r[n_est_idx] > max_n * 0.75]
    half_model_rows = [r for r in rows if r[n_est_idx] <= max_n * 0.5]
    
    # Use the first 80% of each for training, remaining 20% for testing
    def get_split(data):
        split = int(len(data) * 0.8)
        train = data[:split]
        test = [r[:] for r in data[split:]]
        for r in test: r[0] = "?" # Mask MRE-
        return train, test

    train_full, test_full = get_split(full_model_rows)
    train_half, test_half = get_split(half_model_rows)
    
    # Get predictions
    preds_full = base_guess(header, train_full, test_full)
    preds_half = base_guess(header, train_half, test_half)
    
    # Calculate average MRE- (the first goal)
    avg_full = sum(preds_full) / len(preds_full)
    avg_half = sum(preds_half) / len(preds_half)
    
    return avg_full, avg_half

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
            rows.append(processed_row)
            
    avg_full, avg_half = analyze_impact(header, rows)
    
    print("Impact of halving the forecaster size:")
    print(f"Average MRE- (Full Size): {avg_full:.4f}")
    print(f"Average MRE- (Half Size): {avg_half:.4f}")
    diff = avg_half - avg_full
    print(f"The forecast error (MRE-) increases by approximately {diff:.4f} when halving the size.")
