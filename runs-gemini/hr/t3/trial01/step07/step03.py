import pandas as pd
import numpy as np
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the difference between two groups is statistically 
    insignificant (noise), False if they really differ.
    Uses Welch's t-test.
    """
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    # If p-value > 0.05, we fail to reject the null hypothesis (they are the same)
    return p_value > 0.05

if __name__ == "__main__":
    # Load the data
    df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.train.csv')
    
    # Identify the goal column related to tenure (YearsInCurrentRole+ is a good proxy for 'leaving sooner')
    # We want to see if 'OverTime' (Yes/No) affects 'YearsInCurrentRole+'
    target = 'YearsInCurrentRole+'
    
    # Split data based on OverTime
    overtime_yes = df[df['overTime'] == 'Yes'][target]
    overtime_no = df[df['overTime'] == 'No'][target]
    
    # Perform the certification
    is_noise = certify(overtime_yes.tolist(), overtime_no.tolist())
    
    print("Analysis: Does working overtime correlate with leaving a role sooner?")
    print("-" * 60)
    print(f"Average years in role (OverTime=Yes): {overtime_yes.mean():.2f}")
    print(f"Average years in role (OverTime=No):  {overtime_no.mean():.2f}")
    
    if is_noise:
        print("\nConclusion: The observed difference is likely just noise.")
        print("There is no statistically significant evidence that overtime impacts tenure.")
    else:
        print("\nConclusion: The difference is real.")
        print("Working overtime appears to have a statistically significant impact on tenure.")
    
    exit(0)
