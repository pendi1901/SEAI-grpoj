import ezr
import step05

def blame(header, rows):
    """
    Identifies the input columns that most strongly correlate with the worst-performing rows.
    We reuse the logic from step05, which compares the distribution of input columns
    between the worst 25% and best 25% of rows.
    """
    # step05.blame already implements the logic to identify the top 3 culprits
    # based on the difference in means between the worst and best rows.
    # We return the top 2 as requested by the customer.
    culprits = step05.blame(header, rows)
    return culprits[:2]

if __name__ == "__main__":
    file_path = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(file_path)
    try:
        header = next(rows_gen)
        rows = list(rows_gen)
        
        # Get the top 2 factors that matter most to cost
        important_factors = blame(header, rows)
        
        # Identify all input columns to determine what can be ignored
        all_inputs = [name for name in header if not (name.endswith("-") or name.endswith("+"))]
        unimportant_factors = [name for name in all_inputs if name not in important_factors]
        
        print("Analysis of project factors affecting cost:")
        print(f"Most important factors to monitor: {', '.join(important_factors)}")
        print(f"Factors you can safely stop worrying about: {', '.join(unimportant_factors[:3])}...")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
    exit(0)
