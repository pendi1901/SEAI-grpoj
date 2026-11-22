import csv
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the difference between two groups is not statistically 
    significant (p > 0.05), suggesting the difference is likely noise.
    """
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    return p_value > 0.05

def analyze_attrition_tenure(header, rows):
    """
    Compares 'YearsAtCompany+' for employees who work overtime vs those who don't.
    """
    idx_overtime = header.index('overTime')
    idx_tenure = header.index('YearsAtCompany+')
    
    overtime_yes = [row[idx_tenure] for row in rows if row[idx_overtime] == 'Yes']
    overtime_no = [row[idx_tenure] for row in rows if row[idx_overtime] == 'No']
    
    avg_yes = sum(overtime_yes) / len(overtime_yes)
    avg_no = sum(overtime_no) / len(overtime_no)
    
    is_noise = certify(overtime_yes, overtime_no)
    
    print(f"Average tenure (Overtime=Yes): {avg_yes:.2f} years")
    print(f"Average tenure (Overtime=No): {avg_no:.2f} years")
    if is_noise:
        print("Conclusion: The difference is likely just noise.")
    else:
        print("Conclusion: The difference is statistically significant.")
    return is_noise

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
    
    analyze_attrition_tenure(header, rows)
