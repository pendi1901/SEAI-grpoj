import csv
import step05

def blame(header, rows):
    """
    Identifies input columns that correlate with poor performance.
    We define 'bad' rows as those in the bottom 25% of the overall score.
    We then calculate the difference in mean values of inputs between 
    the 'bad' rows and the 'good' rows.
    """
    # Reuse the logic from step05 which identifies the inputs most responsible
    # for poor performance.
    return step05.blame(header, rows)

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = [val if header[i] == 'criterion' else float(val) 
                                 for i, val in enumerate(row)]
                rows.append(processed_row)
        
        # The customer asks which settings can be left at factory defaults.
        # Settings that do not appear in the 'blame' list are those that 
        # do not significantly contribute to poor performance.
        all_inputs = [name for name in header if not (name.endswith('-') or name.endswith('+'))]
        blame_cols = blame(header, rows)
        
        safe_to_default = [col for col in all_inputs if col not in blame_cols]
        
        print("Settings that can be left at factory defaults without hurting performance:")
        for col in safe_to_default:
            print(f"- {col}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
