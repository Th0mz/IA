def smallest_radius_successor (self, number):
    max_radius = max(number - 1,   self.size ** 2 - number)
    for radius in range(1, max_radius):
        if (not self.is_available_value(number - radius) and number - radius >= 1):
            return (radius, number - radius) 
        elif (not self.is_available_value(number + radius) and number + radius <= self.size**2):
            return (radius, number + radius)
            
    return None

def is_in_sequence_range(row, col, number):
    radius, adj_number = self.smallest_radius_successor(number)
    adj_position = get_number_position(adj_number)
    adj_row, adj_col = adj_position

    # manhattan distance must be smaller than the difference bettween the
    # 2 adjacent values in order to be able to connect the 2 values
    if not abs(row - adj_row) + abs(col - adj_col) <= radius:
        return False

    # check if there is a blank path from the postion to the
    # adjacent position
    stack = [(row, col)]
    depths = [0]
    while stack != []:
        row, col = stack.pop()
        depth = depths.pop()

        # check if the path size is bigger
        # than the radius 
        if (depth > radius):
            continue

        if (adj_row == row and adj_col == col):
            return True
        
        adjacencies = self.get_adjacencies(row, col)
        for adjency in adjacencies:
            if (self.is_blank_position(row, col)):
                stack = [adjency] + stack
                depths = [depth + 1] + depths
        
    return False