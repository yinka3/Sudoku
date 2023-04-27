import random
board_easy = [[7,8,0,4,0,0,1,2,0],
              [6,0,0,0,7,5,0,0,9],
              [0,0,0,6,0,1,0,7,8],
              [0,0,7,0,4,0,2,6,0],
              [0,0,1,0,5,0,9,3,0],
              [9,0,4,0,6,0,0,0,5],
              [0,7,0,3,0,0,0,1,2],
              [1,2,0,0,0,7,4,0,0],
              [0,4,9,2,0,6,0,0,7]]


board_medium = [[0,0,0,0,9,0,5,0,1],
                [0,0,0,0,0,0,0,2,0],
                [8,3,0,0,2,0,0,0,0],
                [0,0,4,0,1,6,7,5,0],
                [3,0,0,0,7,5,0,1,8],
                [0,5,0,0,0,0,0,9,0],
                [4,1,0,0,0,0,9,0,2],
                [7,0,3,0,0,0,1,0,0],
                [0,2,0,6,5,0,0,0,4]]


board_hard = [[6,4,9,8,0,1,0,0,0],
              [8,0,7,0,0,0,6,0,0],
              [0,0,0,0,7,0,0,0,4],
              [1,8,0,0,6,0,4,0,9],
              [0,0,0,0,1,0,3,7,0],
              [0,0,0,0,0,0,5,0,0],
              [7,0,0,0,8,0,0,9,0],
              [0,0,0,3,0,0,7,0,5],
              [0,9,6,0,5,0,0,3,0]]


game_board = random.choice([board_easy, board_medium, board_hard])

def print_grid(grid):
    #loops through the length of the columns
    for i in range(len(grid)):
        # Allows for the line to printed after every 3 rows for seperation
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")
        #loops through the length of the rows
        for j in range(len(grid[0])):
            # Allows for the line to printed after every 3 column for seperation
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            # check if its the last position of the board
            if j == 8:
                print(grid[i][j])
            else:
                print(str(grid[i][j]) + " ", end="")

# Find the empty spaces aka 0
def find_emptyspace(grid):
     #loops through the length of the columns
    for i in range(len(grid)):
         #loops through the length of the rows
        for j in range(len(grid[0])):
            # check each position and see if it is 0
            if grid[i][j] == 0:
                # return column and row
                return (i, j)
    # if there is no empty spaces or "0" then return None
    return None
            
# Basically where the backtracking algorithm comes, with the use of recursion

def solve_grid(grid):
    # start with the base case recursion
    # initialize a "find" variable to the find_emptyspace function
    find = find_emptyspace(grid)
    # so if find_emptyspace is not the case aka if it returns None in the find_emptyspace function
    # which triggers the if statement and then you found the solution(YAY THATS IT, SIKEEE I LIED)
    if not find:
        return True
    else:
        # initialize a "row, colm" variable to the find variable, making a copy of the find_emptyspace function
        row, colm = find
     
    # loop through nums 1-10 inclusively(IDK if I spelled that right) to see which one matches for a solution
    for i in range(1,10):
        # Uses the valid_grid function to test all the numbers in each row and colm to see if they are valid
        if valid_grid(grid, i, (row, colm)):
            # if the numbers are valid in the approriate row and colm then it is added to the board
            grid[row][colm] = i
            # Now where recursion comes into play (salute emoji) 
            # calls on solve_grid to basically continouslly try to see if the number makes it valid
            if solve_grid(grid):
                return True
            # go to my comment on the return False first
            # if return False is issued, then we use the backtracking part but making that position an empty space
            # by euqalling it to 0 and then we try over again with a new number
            grid[row][colm] = 0
    # if looped through all the numbers for the row and colm and it does not solve it then return False
    # Now go back to the other line of code(line 49-50 I believe)
    return False
    
    
# Check if the numbers given, will it give a valid board
def valid_grid(grid, num, posn):
     #loops through the length of the rows
    for i in range(len(grid[0])):
        # Check each element in the row to see if it equal to the number added
        # Also if the position that was just entered is the same as the new current position, then it'll be skipped
        if grid[posn[0]][i] == num and posn[1] != i:
            return False
        
    #loops through the length of the columns, does the same thing as previous code but now with the columns
    for i in range(len(grid)):
        if grid[i][posn[1]] == num and posn[0] != i:
            return False
    
    # Check each "section" of the grid, a sudoku board traditionally has 9 sections with 9 numbers in each section
    # Really dont know how to explain this than to say, uses integer math to break up a 9x9 grid to then make 
    # sections aka a bigger matrix of (3x3), where the first section is (0,0), next is (0,1), then (0,2), etc...
    sect_x = posn[1] // 3
    sect_y = posn[0] // 3
    
    # loop through each elements of each section, first points out with section its in then go through all the elments
    # in that section
    for i in range(sect_y * 3, sect_y * 3 + 3):
        for j in range(sect_x * 3, sect_x * 3 + 3):
            # Does the same checking as earlier when finding the rows and columns
            if grid[i][j] == num and (i,j) != posn:
                return False
            
    # If all the values are checking off in each "test" then you know the board is valid
    return True

print_grid(game_board)
solve_grid(game_board)
print("__________________________")
print_grid(game_board)
