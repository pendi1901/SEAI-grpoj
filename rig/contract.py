"""
contract.py: the function each skill must expose so it can be scored.

A program that only prints cannot be graded by a machine. So every step
file must also define one function, named after its skill, with the
signature below. The runner puts this text in the prompt; the scorer
imports the file and calls the function.

Shared conventions, stated once in the prompt:
  header  list of column names. A name starting in upper case is numeric,
          lower case symbolic; a name ending in - or + is a goal.
  rows    list of rows; a row is a list of cells in header order. Numeric
          cells are floats, symbolic cells are strings. A hidden cell is
          the string "?".
"""

SHARED = (
  "Conventions: `header` is the list of column names. `rows` is a list of "
  "rows; each row is a list of cells in header order, floats for numeric "
  "columns and strings for symbolic ones. A cell shown as \"?\" is hidden "
  "from you. A row is better when its goals are closer to their best "
  "(low for names ending in -, high for names ending in +).")

CONTRACT = {
  "remember": (
    "def remember(header, rows)\n"
    "  Returns a list of ints. "
    "  Return the positions (0-based) in `rows` of the rows you judge "
    "best. Return at least one and at most 5% of the rows."),
  "guess": (
    "def guess(header, train, test)\n"
    "  Returns a list of floats. "
    "  `train` rows are complete. In `test` rows every goal cell is \"?\". "
    "Return one number per test row: your estimate of the FIRST goal "
    "column for that row."),
  "certify": (
    "def certify(xs, ys)\n"
    "  Returns True or False. "
    "  `xs` and `ys` are lists of numbers. Return True if they are the "
    "same apart from noise, False if they really differ."),
  "flow": (
    "def flow(header, row, seen)\n"
    "  Returns True or False. "
    "  Rows arrive one at a time. `row` is the one that just arrived; "
    "`seen` is the list of rows that arrived before it. Return True to "
    "choose `row` and stop, False to let it go. You cannot go back."),
  "blame": (
    "def blame(header, rows)\n"
    "  Returns a list of strings. "
    "  Return the names of the input columns (not goals) that best "
    "explain why the worst rows are bad."),
  "justify": (
    "def justify(header, rows, row)\n"
    "  Returns a pair (number, string). "
    "  `rows` are complete. In `row` the goal cells are \"?\". Return "
    "(p, reason): p is the fraction, 0 to 1, of `rows` that `row` is "
    "better than; reason is one sentence a customer could read."),
  "choose": (
    "def choose(header, rows, label)\n"
    "  Returns an int. "
    "  Every goal cell in `rows` is \"?\". Calling label(i) returns the "
    "list of true goal values for rows[i]; you may label at most 50 "
    "different rows. Return the position of the best row you found."),
  "fix": (
    "def fix(header, row, levers)\n"
    "  Returns a dict. "
    "  `row` is a bad row. `levers` maps each column you are allowed to "
    "change to its allowed values: a list of strings for a symbolic "
    "column, a (low, high) pair for a numeric one. Return {column name: "
    "new value} for the change you recommend. Change at least one lever, "
    "only levers, and stay within the allowed values."),
  "spot": (
    "def spot(header, rows)\n"
    "  Returns a list of ints. "
    "  A few rows contain an input value that was entered wrongly. Return "
    "the positions of the rows you suspect, most suspicious first."),
  "race": (
    "def race(header, rows, label)\n"
    "  Returns a dict. "
    "  Every goal cell in `rows` is \"?\". label(i) returns the true goal "
    "values of rows[i]; at most 50 different rows may be labelled in "
    "total, across all strategies. Compare at least three ways of "
    "searching for the best row; one of them must pick rows at random "
    "and be named \"random\". Return {\"winner\": name of the best "
    "strategy, \"row\": position of the best row that strategy found, "
    "\"tried\": list of all strategy names}."),
}

# What a failed call earns: "crashing is not a way to sit out a round".
# gloss10 gives choose a chance level of 0.5, but that describes a skill
# as good as random search, not a crash; a program that picks one poor
# row scores about 0, so a failure must not earn more than that.
BASELINE = dict(remember=0, guess=0, certify=.5, flow=0, blame=0,
                justify=0, choose=0, fix=0, spot=0, race=0)


def prompt_text(skill):
  "The paragraph the runner adds to the prompt for this skill."
  return ("A test harness will import your file and call this function, "
          "so you must define it exactly:\n\n" + CONTRACT[skill] + "\n\n"
          + SHARED + "\n\nKeep everything that prints or reads the csv "
          "file under `if __name__ == \"__main__\":` so that importing "
          "the file prints nothing. Plain built-in types are all you need: "
          "do not import anything from `typing`.")
