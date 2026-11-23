import csv
import pandas as pd
from scipy import stats
from step03 import certify

def compare_periods(header, rows):
    """
    Compares the performance of the first half of the data (pre-change)
    vs the second half (post-change).
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify goal columns
    goals = [col for col in header if col.endswith(('-', '+'))]
    
    # Calculate aggregate score for all rows
    scores = pd.DataFrame(index=df.index)
    for goal in goals:
        col_data = df[goal].astype(float)
        min_val, max_val = col_data.min(), col_data.max()
        normalized = (col_data - min_val) / (max_val - min_val + 1e-9)
        scores[goal] = 1 - normalized if goal.endswith('-') else normalized
    
    df['agg'] = scores.mean(axis=1)
    
    # Split into two periods
    mid = len(df) // 2
    pre_change = df.iloc[:mid]['agg'].tolist()
    post_change = df.iloc[mid:]['agg'].tolist()
    
    # Use the certify function from step03 to check for statistical difference
    is_same = certify(pre_change, post_change)
    
    return pre_change, post_change, is_same

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        pre, post, is_same = compare_periods(header, rows)
        
        print("Customer Inquiry: Did the change in team decision-making shift results?")
        print(f"Average Performance (Pre-change): {sum(pre)/len(pre):.4f}")
        print(f"Average Performance (Post-change): {sum(post)/len(post):.4f}")
        
        if is_same:
            print("Conclusion: The results are statistically the same. The change had no significant impact.")
        else:
            print("Conclusion: The results are statistically different. The change significantly altered performance.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
