import csv
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder

def remember(header, rows):
    """
    Finds the 5% of employees most similar to the first employee in the dataset.
    Similarity is calculated using Euclidean distance on encoded features.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify goal columns to exclude from similarity calculation
    goals = [c for c in header if c.endswith('+') or c.endswith('-')]
    features = [c for c in header if c not in goals]
    
    # Encode symbolic columns for distance calculation
    df_encoded = df.copy()
    for col in header:
        if not col[0].isupper():
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df[col].astype(str))
            
    # Use NearestNeighbors to find similarity to the first row (index 0)
    nn = NearestNeighbors(n_neighbors=max(2, len(rows) // 20))
    nn.fit(df_encoded[features])
    
    distances, indices = nn.kneighbors([df_encoded[features].iloc[0]])
    
    # Return the indices of the most similar rows (excluding the first one itself)
    return [i for i in indices[0] if i != 0][:max(1, len(rows) // 20)]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)
            
    indices = remember(header, rows)
    
    years_idx = header.index('YearsAtCompany+')
    print(f"Employees most similar to the first record (Index 0):")
    for idx in indices:
        print(f"Row {idx}: Stayed {rows[idx][years_idx]} years")
