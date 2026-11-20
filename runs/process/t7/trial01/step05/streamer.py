import ezr 
 
def accepting_arow(header, row, seen):
    if(len(seen) < 20):
        return False
    table = ezr.Tbl([header] + seen)
    prev_scores  =[]
    for prev_row in seen:
        prev_scores.append(ezr.ydist(table, prev_row))

    prev_scores.sort()


    cuttoff_percentile = len(prev_scores)//10
    cutoff = prev_scores[cuttoff_percentile]

    current_score = ezr.ydist(table, row)
    return current_score <= cutoff
    