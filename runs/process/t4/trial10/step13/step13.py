import csv
import pandas as pd
from step03 import certify

def analyze_shift(header, rows):
    """
    Analyzes if the 'Score-' goal shifted significantly.
    We split the data into two halves (first 400 vs last 400) 
    to simulate 'before' and 'after' the spring change.
    """
    df = pd.DataFrame(rows, columns=header)
    goal = 'Score-'
    
    # Split data into two halves
    before = df.iloc[:400][goal].tolist()
    after = df.iloc[400:800][goal].tolist()
    
    # Use the certify function from step03 to check for statistical significance
    is_same = certify(before, after)
    
    return before, after, is_same

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(val) for val in row] for row in reader]
        
        before, after, is_same = analyze_shift(header, rows)
        
        print("Analysis: Did the spring team decision change impact 'Score-'?")
        print(f"Average Score (Before): {sum(before)/len(before):.4f}")
        print(f"Average Score (After):  {sum(after)/len(after):.4f}")
        
        if is_same:
            print("Conclusion: The results are statistically the same. The change had no real impact.")
        else:
            print("Conclusion: The results are statistically different. The change caused a real shift.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
