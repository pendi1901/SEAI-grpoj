import csv
import pandas as pd
import numpy as np
from scipy import stats
from step03 import certify

def analyze_shift(header, rows):
    """
    Splits the data into two halves (before and after the 'spring' change)
    and compares the aggregate performance of the goal columns.
    """
    df = pd.DataFrame(rows, columns=header)
    goals = [col for col in header if col.endswith(('-', '+'))]
    
    # Calculate aggregate performance score for each row
    # Normalize goals to [0, 1]
    scores = pd.DataFrame(index=df.index)
    for goal in goals:
        col_min, col_max = df[goal].min(), df[goal].max()
        rng = col_max - col_min if col_max != col_min else 1.0
        norm = (df[goal] - col_min) / rng
        scores[goal] = (1 - norm) if goal.endswith('-') else norm
    
    df['aggregate_score'] = scores.mean(axis=1)
    
    # Split data into two halves
    mid = len(df) // 2
    before = df.iloc[:mid]['aggregate_score'].tolist()
    after = df.iloc[mid:]['aggregate_score'].tolist()
    
    # Check if distributions are statistically similar
    is_same = certify(before, after)
    
    return is_same, np.mean(before), np.mean(after)

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        is_same, mean_before, mean_after = analyze_shift(header, rows)
        
        print("Customer Inquiry: Did results shift after the spring change?")
        print(f"  Average Performance (Before): {mean_before:.4f}")
        print(f"  Average Performance (After):  {mean_after:.4f}")
        
        if is_same:
            print("  Conclusion: The difference is not statistically significant. The results are effectively the same.")
        else:
            print("  Conclusion: The difference is statistically significant. The results have truly shifted.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
