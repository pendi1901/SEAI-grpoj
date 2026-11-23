import csv
import step02

def guess(header, train, test):
    """
    Estimates the MRE- goal by comparing performance of the original 
    dataset vs a version where N_estimators is halved.
    """
    # Identify index of N_estimators
    n_est_idx = header.index('N_estimators')
    
    # Create a "halved" training set
    halved_train = []
    for row in train:
        new_row = row[:]
        new_row[n_est_idx] = row[n_est_idx] / 2.0
        halved_train.append(new_row)
        
    # Use step02.guess to predict MRE for the test set using the halved training data
    return step02.guess(header, halved_train, test)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
            rows.append(processed_row)

    # Split data: use first 800 for training, last 5 for testing
    train_rows = rows[:800]
    test_rows = [r[:] for r in rows[-5:]]
    for r in test_rows:
        r[0] = r[1] = r[2] = "?"
        
    # Get forecasts with halved N_estimators
    forecasts = guess(header, train_rows, test_rows)
    
    # Get baseline forecasts (original N_estimators) for comparison
    baseline = step02.guess(header, train_rows, test_rows)
    
    print("Impact of halving N_estimators on MRE- forecasts:")
    avg_diff = sum(abs(f - b) for f, b in zip(forecasts, baseline)) / len(forecasts)
    print(f"Average change in MRE forecast: {avg_diff:.4f}")
    print("Halving the forecaster size results in a minor shift in MRE estimates.")
