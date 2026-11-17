import pandas as pd
from scipy import stats


def certify(xs, ys):
    """Return True if xs and ys are statistically indistinguishable (same apart from noise)."""
    try:
        _, p = stats.ttest_ind(xs, ys)
        return p > 0.05
    except Exception:
        return False


if __name__ == "__main__":
    df = pd.read_csv('pom3a.train.csv')

    team_size_col = 'Team Size'
    cost_col = 'Cost-'

    group_means = {}
    for val, grp in df.groupby(team_size_col):
        group_means[val] = grp[cost_col].mean()

    print(f"Mean Cost- by Team Size:")
    for t, m in sorted(group_means.items()):
        print(f"  {t}: {m:.4f}")

    teams = list(group_means.keys())
    if len(teams) >= 2:
        xs = df.loc[df[team_size_col] == teams[0], cost_col].values
        ys = df.loc[df[team_size_col] == teams[-1], cost_col].values
        same = certify(xs, ys)
        print(f"\nAre small-team and big-team Cost- values the same apart from noise? {same}")
    else:
        print("\nNot enough team size groups to compare.")
