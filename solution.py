assignments = []
digits = '123456789'
rows = 'ABCDEFGHI'
WITH_DIAGONAL = True

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
    units = create_units()
    for unit in units:
        for box_1 in unit:
            if len(values[box_1]) != 2:
                continue
            for box_2 in unit:
                if box_1 == box_2 or values[box_1] != values[box_2]:
                    continue
                for digit in values[box_1]:
                    for box in unit:
                        if digit in values[box] and box != box_1 and box != box_2:
                            values = assign_value(values, box, values[box].replace(digit,''))
    return values

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return ["{0}{1}".format(a, b) for a in A for b in B]

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
    boxes = cross(rows, digits)
    return dict(zip(boxes,grid))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    for row in rows:
        print('{0} {1} {2} | {3} {4} {5} | {6} {7} {8}'.format(
            values[row + str(1)], values[row + str(2)], values[row + str(3)],
            values[row + str(4)], values[row + str(5)], values[row + str(6)],
            values[row + str(7)], values[row + str(8)], values[row + str(9)]))
        if row in ['C','F']:
            print('---------------------')

def create_units(with_diagonal = WITH_DIAGONAL):
    '''
    Create a list with all the units that need to be verified.
    Args:
        with_diagonal(boolean) - Define if it is a diagonal Sudoku or not
    Returns:
        list with all the units
    '''
    boxes = cross(rows, digits)
    unit_horizontal = [["{0}{1}".format(row, digit) for digit in digits] for row in rows]
    unit_vertical = [["{0}{1}".format(row, digit) for row in rows] for digit in digits]
    if with_diagonal:
        unit_diagonal = [["{0}{1}".format(row, digit) for row, digit in list(zip(rows, digits))],
                        ["{0}{1}".format(row, digit) for row, digit in list(zip(rows, digits[::-1]))]]
    else:
        unit_diagonal = []
    digits_3by3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    rows_3by3 = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]
    unit_3by3 = []
    for row_group in rows_3by3:
        for digit_group in digits_3by3:
            unit_3by3.append(
                            ['{0}{1}'.format(row, digit)
                            for row in row_group for digit in digit_group])
    all_units = unit_horizontal + unit_vertical + unit_diagonal + unit_3by3
    return all_units

def include_options(values):
    """
    Include in the sudoku dictionary the options.
    Args:
        values(dict): The sudoku in dictionary form
    Return:
        values(dict): The sudoku in dictionary form but with possible values in each box
    """
    for box in values:
        if values[box] == '.':
            assign_value(values, box, '123456789')
    return values

def eliminate(values):
    """Eliminate values using the eliminate strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the defined values eliminated from peers.
    """
    units = create_units()
    for value in values:
        if len(values[value]) == 1:
            continue
        for unit in units:
            if value in unit:
                for box in unit:
                    if len(values[box]) == 1 and box != value:
                        assign_value(values, value, values[value].replace(values[box],''))
    return values

def only_choice(values):
    """Eliminate values using the only choice strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the only choice defined.
    """
    units = create_units()
    for digit in digits:
        for unit in units:
            boxes_with_digit = [box for box in unit if digit in values[box]]
            if len(boxes_with_digit) == 1:
                assign_value(values, boxes_with_digit[0], digit)
                values[boxes_with_digit[0]] = digit
    return values

def reduce_puzzle(values):
    re_do = True
    while re_do:
        values_old = values.copy()
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        re_do = not values_old == values
    boxes_empty = [value for value in values if len(values[value]) == 0]
    if boxes_empty != []:
        return False
    return values

def search(values):
    # Verify if it is already done
    boxes = [value for value in values if len(values[value]) > 1]
    if boxes == []:
        return values
    # Choose the box to start guessing
    box_to_use = boxes[0]
    for box in boxes:
        box_to_use = (box if len(values[box]) < len(values[box_to_use]) else
                        box_to_use)
    for digit in values[box_to_use]:
        sudoku = values.copy()
        sudoku[box_to_use] = digit
        sudoku = reduce_puzzle(sudoku)
        if not sudoku:
            continue
        boxes = [value for value in sudoku if len(sudoku[value]) > 1]
        if boxes == []:
            return sudoku
        sudoku = search(sudoku)
        if not sudoku:
            continue
        return sudoku
    return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    sudoku = include_options(grid_values(grid))
    return search(reduce_puzzle(sudoku))


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    print('Sudoku to be solved:')
    display(grid_values(diag_sudoku_grid))
    print('Sudoku solved:')
    display(solve(diag_sudoku_grid))
    print("Done!")

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
