import csv
import step03

def certify(xs, ys):
    """
    Returns True if the difference between two distributions is likely noise,
    False if they are statistically distinct. Uses the A12 effect size test.
    """
    return step03.certify(xs, ys)

def compare_criteria(header, rows):
    """
    Compares the performance (composite score) of different 'criterion' settings.
    We focus on the two most common criteria to see if they differ significantly.
    """
    # Identify indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    crit_idx = header.index('criterion')

    # Calculate composite score for all rows
    mres = [r[mre_idx] for r in rows]
    accs = [r[acc_idx] for r in rows]
    preds = [r[pred_idx] for r in rows]
    
    min_mre, max_mre = min(mres), max(mres)
    min_acc, max_acc = min(accs), max(accs)
    min_pred, max_pred = min(preds), max(preds)

    def get_score(row):
        s1 = (1 - (row[mre_idx] - min_mre) / (max_mre - min_mre)) if max_mre > min_mre else 0.5
        s2 = (row[acc_idx] - min_acc) / (max_acc - min_acc) if max_acc > min_acc else 0.5
        s3 = (row[pred_idx] - min_pred) / (max_pred - min_pred) if max_pred > min_pred else 0.5
        return (s1 + s2 + s3) / 3

    # Group scores by criterion
    groups = {}
    for row in rows:
        crit = row[crit_idx]
        groups.setdefault(crit, []).append(get_score(row))

    # Compare the two most frequent criteria
    sorted_criteria = sorted(groups.keys(), key=lambda k: len(groups[k]), reverse=True)
    if len(sorted_criteria) < 2:
        return True, "Insufficient variety in criteria to compare."

    c1, c2 = sorted_criteria[0], sorted_criteria[1]
    is_noise = certify(groups[c1], groups[c2])
    
    msg = f"Comparing '{c1}' vs '{c2}': "
    if is_noise:
        msg += "The difference is statistically negligible (noise)."
    else:
        msg += "The difference is statistically significant."
        
    return is_noise, msg

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        is_noise, analysis = compare_criteria(header, rows)
        print(analysis)
        if is_noise:
            print("Conclusion: You can stop arguing; the choice of criterion does not matter.")
        else:
            print("Conclusion: The choice of criterion makes a real difference.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
