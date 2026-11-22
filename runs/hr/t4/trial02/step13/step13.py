import csv
from step03 import certify

def analyze_training_impact(header, rows):
    """
    Analyzes if 'TrainingTimesLastYear' correlates with 'YearsWithCurrManager+'.
    We split the data into two groups: those with training above the median
    and those with training at or below the median.
    """
    train_idx = header.index('TrainingTimesLastYear')
    years_idx = header.index('YearsWithCurrManager+')
    
    training_vals = [row[train_idx] for row in rows]
    median_training = sorted(training_vals)[len(training_vals) // 2]
    
    more_training = [row[years_idx] for row in rows if row[train_idx] > median_training]
    less_training = [row[years_idx] for row in rows if row[train_idx] <= median_training]
    
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
        print("Result: The difference is statistically insignificant (noise).")
    else:
        print("Result: There is a statistically significant difference.")
        
    print(f"Mean years with manager (More training): {sum(more)/len(more):.2f}")
    print(f"Mean years with manager (Less training): {sum(less)/len(less):.2f}")
