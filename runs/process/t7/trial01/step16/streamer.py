import ezr 
 
def accepting_arow(header, row, seen, warn=False):
    if(len(seen) < 20):
        return False
    table = ezr.Tbl([header] + seen)
    prev_scores  =[]
    for prev_row in seen:
        prev_scores.append(ezr.ydist(table, prev_row))

    prev_scores.sort()


    current_score = ezr.ydist(table, row)
    if warn:
        cutoff = prev_scores[-(len(prev_scores) // 10)]
        return current_score > cutoff

    cutoff = prev_scores[len(prev_scores) // 10]
    return current_score <= cutoff
    
