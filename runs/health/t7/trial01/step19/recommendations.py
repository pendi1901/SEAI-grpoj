import ezr
from neighbours import nearest_rows

def allowed_changes(header, row, controls):
    for name, allowed in controls.items(): 
        position = header.index(name)
        current = row[position]

        if isinstance(allowed, tuple) : 
            low, high  = allowed
            values  = [(low+high)/2 , low, high]
        else:
            values = allowed
        
        for value in values: 
            if value!= current: 
                yield{name: value}

def candidate_changes(header, train, row, controls):
    table  = ezr.Tbl([header] + train)
    def quality(training_rows) : 
        return ezr.ydist(table, training_rows)
    ranked  = sorted(train, key = quality)
    count = len(train)//4
    good_rows  = ranked[:count]

    matching_header = header.copy()


    for name in controls : 
        position = header.index(name)
        matching_header[position] +="X"

    matching_table = ezr.Tbl([matching_header]+ train)


    if matching_table.x: 
        good_rows = nearest_rows(matching_table, good_rows, row, k = len(good_rows))
    
    for neighbour in good_rows: 
        changes = {}
        for name, allowed in controls.items(): 
            position = header.index(name)
            value = neighbour[position]

            if value == "?": 
                continue
            if isinstance(allowed, tuple) : 
                low, high = allowed
                value  = max(low, min(value, high))
            elif value not in allowed:  
                continue
            if value!= row[position]: 
                changes[name] = value
        if changes:
            yield changes
    yield from allowed_changes(header, row, controls)


def suggested_changes(header, train, row, controls):
    changes = next(candidate_changes(header, train, row, controls), None)
    if changes is None:
        raise ValueError("no allowed changes are available")
    return changes
