import sys
import numpy as np
import scipy.sparse
import scipy.sparse.linalg

if len(sys.argv) < 3: # Verify correct user input
    print('Usage:')
    print('  python3 {} <maze file> <solution file>'.format(sys.argv[0]))
    sys.exit(0)

# Open files
maze_file = open(sys.argv[1], "r") 
solution_file = open(sys.argv[2], "r")


def create_DataArray(maze_file, solution_file):
    """
        create_DataArray(maze_file, solution_file)

        Reads and stores maze_file as a 2d numpy array of size n_rows x n_cols called 'maze_array'. Each coordinate present in maze_file is set to 1 in the array. 
        Coordinates contained in the solution_file are stored in a 2d array of size n_steps x 2 called 'sol_coords'. 

        Returns: n_rows, n_cols, solution , maze_array 
    """
    maze = np.loadtxt(maze_file, dtype=int) 
    sol_coords = np.loadtxt(solution_file, dtype=int)
    n_rows = maze[0][0] # Get maze sizes
    n_cols = maze[0][1]
    maze_data = maze[1:][:] # Remove first row to keep just coordinates
    maze_array = np.zeros([n_rows,n_cols]) # Initialize 2D array
    for coord in maze_data: # Set maze walls
        maze_array[coord[0],coord[1]] = 1

    return n_rows, n_cols, sol_coords, maze_array
        
def verify_EntryExit(sol_coords):
    """
        verify_EntryExit(sol_coords)

        Verifies that the first solution coordinate 'entry_coord' is in the first row of the maze_array and that the last solution coordinate 'exit_coord' is in the last row of the maze_array.

        Returns: entry_coord, exit_coord
    """
    entry_coord = sol_coords[0] 
    exit_coord = sol_coords[len(sol_coords)-1]

    if entry_coord[0] != 0: # Entry coord not in first row
        raise Exception("Solution is invalid. Entry must be on the first row.")
    elif exit_coord[0] != (n_rows - 1): # Exit coord not in last row
        raise Exception("Solution is invalid. Exit must be on the last row.")
    
    return entry_coord, exit_coord

def verify_Path(sol_coords, maze_array, n_rows, n_cols, entry_coord):
    """
        verify_Path(sol_coords, maze_array, n_rows, n_cols, entry_coord)

        Verifies at eah step if it is a valid step (i.e. coordinate indexes do not exceed maze boundaries, step does not hit a wall, and movement is done towards just one adjacent entry).

        Exception is raised if step does not meet any of the above conditions. 
    """
    for coord in sol_coords: # Analyze each solution's coordinate

        if coord[0] > (n_rows -1) or coord[1] > (n_cols -1): # Coordinate exceeds maze boundaries
            raise Exception("Solution is invalid. Coordinates exceed maze boundaries")
        
        if maze_array[coord[0],coord[1]] == 1: # coordinate corresponds to a wall
            raise Exception("Solution is invalid. Solution hits a wall.")
        
        if coord[0] == entry_coord[0] and coord[1] == entry_coord[1]: # Entry coordinate / first coordinate
            past_coord = coord # initialize first past_coord
            diff_step = 0 # No step has been taken
        else: 
            diff_steprows = abs(past_coord[0] - coord[0]) # Step difference in rows
            diff_stepcols = abs(past_coord[1] - coord[1]) # Step difference in cols
            diff_step = diff_steprows + diff_stepcols # Sum of step differences
            past_coord = coord # Update past coordinate

        if diff_step > 1: # Step was taken in more than one direction or towards a not subsequent entry
            raise Exception("Solution is invalid. Movement is permited by just one position at a time.")
        



(n_rows, n_cols, sol_coords, maze_array) = create_DataArray(maze_file,solution_file) # Create maze array and save solution coordinates as array

(entry_coord, exit_coord) = verify_EntryExit(sol_coords) # Verify correct entry and exit coordinates and get those coordinates
verify_Path(sol_coords, maze_array, n_rows, n_cols, entry_coord) # Verify solution path

print("Solution is valid!")





