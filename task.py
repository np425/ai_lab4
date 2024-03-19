from maze import MAZE, EMPTY, WALL, GOAL, print_values
from pprint import pprint

REWARD = {
    EMPTY: -1,
    WALL: -10,
    GOAL: 100
}

ACTION_PROB = 0.25

def neighbors(maze, origin_coord):
    res = []

    actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for a in actions:
        c = (origin_coord[0] + a[0], origin_coord[1] + a[1])
        if 0 <= c[0] < len(maze) and 0 <= c[1] < len(maze[0]):
            res.append(c)

    return res

def value_iteration(maze, theta=0.01):
    # Initialize values
    values = [[REWARD[node] for node in row] for row in maze]

    delta = theta + 1
    while delta > theta:
        delta = 0
        for x, row in enumerate(maze):
            for y, node in enumerate(row):
                if node != GOAL:
                    # Calculate the expected value
                    neighbors_values = [values[nx][ny] for (nx, ny) in neighbors(maze, (x, y))]
                    new_value = max(neighbors_values) * ACTION_PROB + REWARD[node]
                    old_value = values[x][y]

                    # Update the value
                    values[x][y] = new_value

                    # Update delta
                    delta = max(delta, abs(new_value - old_value))

    return values

def find_path(values, start_coord, goal_coord):
    current_coord = start_coord
    path = [current_coord]
    visited = set([current_coord])  # Set to store visited cells

    while current_coord != goal_coord:
        neighbors_list = neighbors(MAZE, current_coord)
        # Filter out wall cells and already visited cells from the list of neighbors
        neighbors_list = [neighbor for neighbor in neighbors_list if MAZE[neighbor[0]][neighbor[1]] != WALL and neighbor not in visited]
        
        if not neighbors_list:
            print("No valid neighbors, backtracking.")
            path.pop()  # Remove the last visited cell
            if not path:
                print("Cannot find a path to the goal.")
                return None
            current_coord = path[-1]  # Backtrack to the previous cell
            continue

        next_coord = max(neighbors_list, key=lambda coord: values[coord[0]][coord[1]])
        path.append(next_coord)
        visited.add(next_coord)  # Add the next cell to visited set
        current_coord = next_coord

    return path



# Perform value iteration
values = value_iteration(MAZE)

# Print the values
print_values(values)

# Find and print the path
pprint(find_path(values, (0, 0), (6, 6)))

