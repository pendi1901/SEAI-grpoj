def spot(header, rows):
    goals_min = [c for c in header if c.endswith('-')]
    goals_max = [c for c in header if c.endswith('+')]

    suspicious = []

    for col in header:
        idx = header.index(col)

        # Skip goal columns (hidden with "?")
        if col.endswith('-') or col.endswith('+'):
            continue

        vals = [(i, row[idx]) for i, row in enumerate(rows) if row[idx] != '?']

        if not vals:
            continue

        is_numeric = True
        try:
            float(vals[0][1])
        except ValueError:
            is_numeric = False

        if not is_numeric:
            continue  # symbolic columns — skip for now

        nums = [float(v) for _, v in vals]
        n = len(nums)

        sorted_nums = sorted(nums)
        mid = n // 2
        median_val = sorted_nums[mid] if n % 2 == 0 else sorted_nums[(n - 1) // 2]

        abs_devs = [abs(x - median_val) for x in nums]
        abs_devs_sorted = sorted(abs_devs)
        mad_idx = (len(abs_devs_sorted) - 1) // 2
        mad_val = abs_devs_sorted[mad_idx]

        if mad_val == 0:
            continue

        for i, v in vals:
            diff = abs(float(v) - median_val)
            if diff > mad_val * 3:
                suspicious.append(i + 1)

    return sorted(suspicious, reverse=True)


if __name__ == "__main__":
    import csv

    with open("WA_Fn-UseC_-HR-Employee-Attrition.train.csv", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [next(reader) for _ in range(1470)]

    suspicious = spot(header, rows)
    print(f"Found {len(suspicious)} suspicious entries:")
    for pos in suspicious[:20]:
        print(f"  row {pos}")
