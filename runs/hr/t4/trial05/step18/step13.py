import csv
from step03 import certify

def analyze_training_impact(header, rows):
    """
    Analyzes if 'TrainingTimesLastYear' correlates with 'YearsWithCurrManager+'.
    We split the population into two groups: those with training above the median
    and those with training at or below the median.
    """
    train_idx = header.index('TrainingTimesLastYear')
    manager_idx = header.index('YearsWithCurrManager+')
    
    training_values = [r[train_idx] for r in rows]
    median_training = sorted(training_values)[len(training_values) // 2]
    
    more_training = [r[manager_idx] for r in rows if r[train_idx] > median_training]
    less_training = [r[manager_idx] for r in rows if r[train_idx] <= median_training]
    
    # Use the certify function from step03 to check if the difference is noise
    is_noise = certify(more_training, less_training)
    
    return is_noise, more_training, less_training

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    is_noise, more, less = analyze_training_impact(header, rows)
    
    print("Analysis: Do people with more training stay longer with their manager?")
    if is_noise:
        print("Result: The observed difference is likely just noise (not statistically significant).")
    else:
        avg_more = sum(more) / len(more)
        avg_less = sum(less) / len(less)
        print(f"Result: There is a statistically significant difference.")
        print(f"Average years with manager (more training): {avg_more:.2f}")
        print(f"Average years with manager (less training): {avg_less:.2f}")
        if avg_more > avg_less:
            print("Conclusion: More training is associated with longer tenure with the manager.")
        else:
            print("Conclusion: More training is not associated with longer tenure with the manager.")
