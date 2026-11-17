import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from step01 import remember
from step02 import guess


def certify(xs, ys):
    """Returns True if xs and ys are the same apart from noise."""
    mean_x = sum(xs) / len(xs) if xs else 0
    mean_y = sum(ys) / len(ys) if ys else 0
    
    diff = abs(mean_x - mean_y)
    scale = max(abs(mean_x), abs(mean_y)) or 1.0
    
    return diff < 0.5 * scale


if __name__ == "__main__":
    df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.train.csv")
    
    ot_yes = df[df['overTime'] == 'Y']['YearsAtCompany+'].tolist()
    ot_no = df[df['overTime'] == 'N']['YearsAtCompany+'].tolist()
    
    result = certify(ot_yes, ot_no)
    
    print(f"Overtime workers' YearsAtCompany+: {sum(ot_yes)/len(ot_yes):.1f}")
    print(f"No overtime workers' YearsAtCompany+: {sum(ot_no)/len(ot_no):.1f}")
    print(f"Are they similar? {'Yes (noise)' if result else 'No (real difference)'}")
