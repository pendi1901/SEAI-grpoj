import csv
from step03 import certify
from step02 import guess as guess_k5
from step12 import guess as guess_k2

def compare_rules(header, rows):
    """
    Compares the performance of two different rules (k=5 vs k=2)
    to see if the difference is statistically significant.
    """
    # Use a subset for testing
    train_data = rows[:700]
    test_data = rows[700:800]
    
    # Get predictions
    preds_k5 = guess_k5(header, train_data, test_data)
    preds_k2 = guess_k2(header, train_data, test_data)
    
    # The certify function from step03 uses a t-test to check if the 
    # difference between two distributions is noise.
    is_noise = certify(preds_k5, preds_k2)
    
    return is_noise

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    is_noise = compare_rules(header, rows)
    
    print("Comparing the two built-in rules (k=5 vs k=2):")
    if is_noise:
        print("The difference is statistically insignificant. You can stop arguing about it.")
    else:
        print("The difference is statistically significant. The choice of rule matters.")
    
    exit(0)
