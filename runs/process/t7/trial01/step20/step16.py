from itertools import zip_longest
from textwrap import wrap

from step06 import justify
from step15 import blame
from load import loading_data, splitting_data


if __name__ == "__main__":
    header, rows = loading_data("pom3a.n1000.train.csv")
    train, test, _ = splitting_data(header, rows, test_size=2)
    score_a, reason_a = justify(header, train, test[0])
    score_b, reason_b = justify(header, train, test[1])

    print(f"{'Setup A':<55} | Setup B")
    print(f"{'Estimated fraction beaten: ' + format(score_a, '.1%'):<55} | "
          f"Estimated fraction beaten: {score_b:.1%}")
    for left, right in zip_longest(wrap(reason_a, 55), wrap(reason_b, 55), fillvalue=""):
        print(f"{left:<55} | {right}")

    print("Top two inputs overall; these differences do not prove causation:")
    for name in blame(header, train):
        at = header.index(name)
        print(f"{name}: A = {test[0][at]:.3f}, B = {test[1][at]:.3f}")

    if score_a == score_b:
        print("The estimates tie; neither setup is preferred.")
    else:
        preferred = "A" if score_a > score_b else "B"
        print(f"The estimate favours {preferred} by {abs(score_a - score_b):.1%} "
              "of the reference set; this is not a guaranteed advantage.")
