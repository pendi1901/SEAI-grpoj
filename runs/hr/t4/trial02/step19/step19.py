import csv
import math
from step09 import spot as base_spot

def spot(header, rows):
    """
    Identifies rows that are 'unlike anyone we have employed' by calculating
    the Z-score of numeric inputs. Rows with values significantly outside 
    the distribution (Z > 3) are flagged as potential outliers or 
    untrustworthy estimates.
    """
    # We reuse the logic from step09 which identifies rows that deviate 
    # significantly from the historical norms of the dataset.
    return base_spot(header, rows)

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
            
    suspects = spot(header, rows)
    
    print("Analysis: Identifying rows where estimates cannot be trusted.")
    print("We flag rows that contain input values significantly outside the historical distribution.")
    print(f"Found {len(suspects)} rows that are 'unlike anyone we have employed'.")
    print("Top 5 most suspicious row indices (where estimates are least reliable):")
    for idx in suspects[:5]:
        print(f"- Row {idx}")
    print("\nThese rows represent outliers where our predictive models lack sufficient")
    print("historical context to provide a reliable estimate.")
