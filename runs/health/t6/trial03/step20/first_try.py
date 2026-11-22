import ezr
import random
import step10

def race(header, rows, label):
    """
    Compares three strategies for finding the best setup within a 50-label budget.
    Strategies:
    1. random: Picks rows at random.
    2. acquire: Uses ezr's active learning.
    3. greedy: Picks rows that are closest to the current best known row in input space.
    
    This implementation reuses the logic from step10 to ensure consistency.
    """
    return step10.race(header, rows, label)

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]

    # Define the label function for the harness
    # The harness expects us to use the true goals from the original rows
    def label(i):
        return [rows[i][j] for j, col in enumerate(header) if col[-1] in "+-"]

    # Run the race
    result = race(header, rows, label)
    
    print("Strategy Comparison Analysis:")
    print(f"The winning strategy is: {result['winner']}.")
    print(f"The best configuration found was at index {result['row']}.")
    print(f"Strategies compared: {', '.join(result['tried'])}.")
    
    if result['winner'] == 'random':
        print("Result: The random strategy performed best, suggesting the search space is flat.")
    else:
        print(f"Result: {result['winner']} outperformed random, confirming the value of guided search.")
        
    exit(0)
