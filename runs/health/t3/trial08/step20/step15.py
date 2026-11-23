import csv
from sklearn.ensemble import RandomForestRegressor

def blame(header, rows):
    """
    Identifies which input columns are most predictive of poor performance.
    We define 'bad' rows as those in the bottom 25% of the aggregate score.
    We then train a Random Forest to predict the 'badness' and report
    the feature importances.
    """
    goal_cols = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    input_cols = [i for i, h in enumerate(header) if i not in goal_cols]
    
    # Calculate a normalized aggregate score for each row
    # MRE- (min), ACC+ (max), PRED40+ (max)
    scores = []
    for row in rows:
        mre = float(row[header.index('MRE-')])
        acc = float(row[header.index('ACC+')])
        pred = float(row[header.index('PRED40+')])
        # Normalize: (1-MRE) + ACC + PRED
        score = (1.0 - mre) + acc + pred
        scores.append(score)
    
    # Label rows as 'bad' (bottom 25%)
    threshold = sorted(scores)[len(scores) // 4]
    labels = [1 if s <= threshold else 0 for s in scores]
    
    # Prepare features: handle categorical by dummy encoding
    X = []
    for row in rows:
        feat = []
        for i in input_cols:
            val = row[i]
            if isinstance(val, str):
                # Simple label encoding for symbolic columns
                feat.append(hash(val) % 1000)
            else:
                feat.append(float(val))
        X.append(feat)
    
    # Train Random Forest to find features that correlate with 'bad' labels
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, labels)
    
    # Get feature importances
    importances = model.feature_importances_
    indexed_importances = sorted(zip(importances, input_cols), reverse=True)
    
    # Return top 3 input columns that explain the badness
    # These are the ones that, if changed, most affect performance
    top_cols = [header[idx] for _, idx in indexed_importances[:3]]
    return top_cols

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        # The settings that are NOT in the 'blame' list are the ones 
        # that have the least impact on performance, meaning they can 
        # safely be left at factory defaults.
        all_inputs = [h for h in header if not (h.endswith('-') or h.endswith('+'))]
        important_settings = blame(header, rows)
        safe_settings = [s for s in all_inputs if s not in important_settings]
        
        print("Settings that can be left at factory defaults without hurting performance:")
        for col in safe_settings:
            print(f"- {col}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
