import csv
import step09

def spot(header, rows):
    """
    Identifies rows that look wrong by checking for outliers in numeric columns.
    We use the logic from step09 to flag rows where any value is more than 
    3 standard deviations from the mean. This identifies rows that are 
    statistically 'unlike' the rest of the population.
    """
    return step09.spot(header, rows)

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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    suspects = spot(header, rows)
    
    print("Analysis: Identifying rows that cannot be trusted.")
    print("These rows contain input values that are extreme outliers (3+ standard deviations).")
    print(f"We identified {len(suspects)} suspicious rows.")
    print("Top 5 most suspicious row indices (where estimates are least reliable):")
    for idx in suspects[:5]:
        print(f"- Row {idx}")
    print("\nLogic: If a new hire's profile is significantly different from the historical data "
          "(outlier), our model's estimates for them are less trustworthy.")
