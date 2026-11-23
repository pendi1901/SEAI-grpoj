import csv
from step02 import guess as original_guess

def guess(header, train, test):
    """
    Estimates the first goal (MRE-) for test rows.
    To answer the customer's question:
    1. We define 'halving the size' as halving the 'N_estimators' input.
    2. We compare the original test rows with 'halved' versions.
    """
    # The customer asks how much worse forecasts get if we halve the forecaster.
    # We use the existing KNN-based guess() from step02.
    return original_guess(header, train, test)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
            rows.append(processed_row)

    # Prepare data: Train on full set, test on a subset
    train_data = rows[:700]
    test_data = [list(r) for r in rows[700:750]]
    
    # Baseline: Predict MRE- for original test rows
    baseline_preds = guess(header, train_data, test_data)
    
    # Halved: Predict MRE- for test rows where N_estimators is halved
    n_idx = header.index('N_estimators')
    halved_test_data = [list(r) for r in test_data]
    for r in halved_test_data:
        r[n_idx] /= 2
        r[0] = r[1] = r[2] = "?"
        
    halved_preds = guess(header, train_data, halved_test_data)
    
    # Calculate average degradation
    diffs = [h - b for b, h in zip(baseline_preds, halved_preds)]
    avg_degradation = sum(diffs) / len(diffs)
    
    print("Customer Inquiry: Impact of halving N_estimators on MRE- forecast.")
    print(f"Average increase in MRE- (error) after halving N_estimators: {avg_degradation:.4f}")
    print("A positive value indicates performance degradation (higher error).")
    
    exit(0)
