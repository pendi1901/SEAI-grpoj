import csv
import step02

def remember(header, rows):
    """
    Finds the 5% of rows most similar to the first row (the 'target').
    Similarity is defined by the inverse of the Euclidean distance on 
    numeric input columns, as established in step02.
    """
    # Identify numeric input columns (excluding goals and symbolic)
    input_indices = [
        i for i, name in enumerate(header) 
        if name[0].isupper() and '+' not in name and '-' not in name
    ]

    def get_dist(row1, row2):
        dist = 0
        for i in input_indices:
            dist += (row1[i] - row2[i]) ** 2
        return dist ** 0.5

    # Target is the first row
    target = rows[0]
    
    # Calculate distances to all other rows
    distances = []
    for i in range(1, len(rows)):
        d = get_dist(target, rows[i])
        distances.append((d, i))
    
    # Sort by distance ascending (closest first)
    distances.sort(key=lambda x: x[0])
    
    # Return top 5% (800 rows * 0.05 = 40 rows)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in distances[:limit]]

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

    best_indices = remember(header, rows)
    
    idx_years = header.index('YearsAtCompany+')
    
    print("Employees most similar to the first record and their tenure:")
    print(f"{'Index':<10} | {'YearsAtCompany':<15}")
    print("-" * 30)
    
    for i in best_indices:
        print(f"{i:<10} | {rows[i][idx_years]:<15}")
