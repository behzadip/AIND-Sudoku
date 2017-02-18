import itertools

def cross(A, B):
        "Cross product of elements in A and elements in B."
        return [s+t for s in A for t in B]

# Initialize assignments and Sudoku board boxes
assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
# List of row units
row_units = [cross(r, cols) for r in rows]
# List of column units
column_units = [cross(rows, c) for c in cols]
# List of 9 3x3 squares within main board
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# List of two diagonal units encoded manually
diag_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
# Create list of all units
unitlist = row_units + column_units + square_units + diag_units
# Dictionary of a list of units each box is a member of
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
# Remove repetition from above dictionary to include unique co-unit members for each box
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    # Going through each individual unit
    for unit in unitlist:
        # Narrow down candidates to be further investigated (boxes with two possible values)
        candidates = [values[key] for key in unit if len(values[key])==2]
        # Check if they are more than one box with identical two possible values
        switches = set([can for can in candidates if candidates.count(can)>1])
        # For each pair remove these two values from its co-unit members possibile values
        for switch in switches:
            for key in unit:
                # Check not to remove the values from naked twin boxes themselves 
                if values[key] != switch:
                    # Remove two options from their possibilities
                    values = assign_value(values, key, values[key].replace(switch[0], ''))
                    values = assign_value(values, key, values[key].replace(switch[1], ''))
    return values

''' OPTIONAL STRATEGIES
    Below is hidden_twins function which implements the hidden twins strategy based on following link
    http://www.sudokudragon.com/tutorialhiddentwins.htm
'''
def hidden_twins(values):
    """Eliminate values using the hidden twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the hidden twins identified.
    """
    # Find all instances of hidden twins
    # Going through each individual unit
    for unit in unitlist:
        # Goes through all possible pair of digits 
        for digit1,digit2 in itertools.combinations('123456789', 2): 
            # Record boxes that have both digits as their possibile values
            switches = [key for key in unit if digit1 in values[key] and digit2 in values[key]]
            # In case there are only two boxes, a possible hidden twin has been found
            if len(switches)==2:
                # Checks whether either of the two digits is among possible values for peers of them
                sanity = [not(digit1 in values[key] or digit2 in values[key]) for key in unit if key not in switches]
                if all(sanity):
                    # In case these digits were not found in any of their peers a Hidden Twins is found
                    # Assignining the pair of digit as the their only available values
                    values = assign_value(values, switches[0], digit1+digit2)
                    values = assign_value(values, switches[1], digit1+digit2)
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    # Sanity check if they are 81 boxes
    assert len(grid) == 81
    # Assign values to boxes in order replacing blank values with all possible numbers
    values = dict(zip(boxes, grid))
    for box in boxes:
        if values[box] == '.':
            values[box] = '123456789'
    return values

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    # Go through all boxes
    for key in boxes:
        # If it has only one possible value
        if len(values[key]) == 1:
            # Go through all its peers and remove this value from their possible values
            for peer in peers[key]:
                if len(values[peer]) > 1 and values[key] in values[peer]:
                    values = assign_value(values, peer, values[peer].replace(values[key],''))
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    # Go through each unit
    for unit in unitlist:
        # For each digit make a list of all the boxes which has the digit as their possible values
        for num in '123456789':
            count = [key for key in unit if num in values[key]]
            # Assign the digit to a box if it is the only box in above list
            if len(count) == 1:
                values = assign_value(values, count[0], num)
    return values

def reduce_puzzle(values):
    """Reduce the possible values for applicable boxes.
    Apply eliminate, only choice, and naked twins functions over and over again while
    it's making progress. Stops when the board did not change after applying 
    these three functions.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after reducing possible values. Return False
    if there are boxes with no possible values.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, try naked twins and hidden twins strategies.
        stalled = solved_values_before == solved_values_after
        if stalled:
            # Use Hidden Twins strategy
            values = hidden_twins(values)
            # Use Naked Twins strategy
            values = naked_twins(values)
            # Check how many boxes have a determined value, to compare
            solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
            # If no new values were added again, stop the loop.
            stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    # Return False if reduce puzzle were unsuccessful
    if not values:
        return False
    # Choose one of the unfilled squares with the fewest possibilities
    # List number of all possible values greater than 1 for each box
    lengths = [(len(values[k]), k) for k in boxes if len(values[k]) > 1]
    # Return one box with minimum number of possibilities if exists to expand
    if lengths:
        key = min(lengths)[1]
    # Found the solution if no expansion key found
    else:
        return values # Solved

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!        
    for val in values[key]:
        # Copy a new Sudoku game by assigning one of the possible values to the expansion key
        temp = values.copy()
        temp[key] = val
        solution = search(temp)
        # Return solution if it exists
        if solution:
            return solution

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)    
    return search(values)
    
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
