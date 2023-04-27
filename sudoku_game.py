import pygame
# needed so we can use the solver to see when the user is done is it similar to the solved version 
# and is the numbers valid
from sudoku_solver import solve_grid, valid_grid
import time
import random

pygame.font.init()


# Class for the Grid
class Grid:
    board_easy = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    board_medium = [[0, 0, 0, 0, 9, 0, 5, 0, 1],
                    [0, 0, 0, 0, 0, 0, 0, 2, 0],
                    [8, 3, 0, 0, 2, 0, 0, 0, 0],
                    [0, 0, 4, 0, 1, 6, 7, 5, 0],
                    [3, 0, 0, 0, 7, 5, 0, 1, 8],
                    [0, 5, 0, 0, 0, 0, 0, 9, 0],
                    [4, 1, 0, 0, 0, 0, 9, 0, 2],
                    [7, 0, 3, 0, 0, 0, 1, 0, 0],
                    [0, 2, 0, 6, 5, 0, 0, 0, 4]]

    board_hard = [[6, 4, 9, 8, 0, 1, 0, 0, 0],
                  [8, 0, 7, 0, 0, 0, 6, 0, 0],
                  [0, 0, 0, 0, 7, 0, 0, 0, 4],
                  [1, 8, 0, 0, 6, 0, 4, 0, 9],
                  [0, 0, 0, 0, 1, 0, 3, 7, 0],
                  [0, 0, 0, 0, 0, 0, 5, 0, 0],
                  [7, 0, 0, 0, 8, 0, 0, 9, 0],
                  [0, 0, 0, 3, 0, 0, 7, 0, 5],
                  [0, 9, 6, 0, 5, 0, 0, 3, 0]]

    # chooses a random level of sudoku
    game_board = random.choice([board_easy, board_medium, board_hard])

    # gives appropiate properties of the entire grid
    def __init__(self, rows, colm, width, height):
        self.rows = rows
        self.colm = colm
        self.slot = [[Slot(self.game_board[i][j], i, j, width, height) for j in range(colm)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model_grid = None
        self.selected = None

    # Used to sketch a temp value in a slot that was clicked
    def sketch(self, val):
        row, col = self.selected
        self.slot[row][col].set_temp(val)

    def draw(self, win):
        # Draws Grid Lines
        spacing = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(win, (255, 255, 255), (0, i * spacing), (self.width, i * spacing), thickness)
            pygame.draw.line(win, (255, 255, 255), (i * spacing, 0), (i * spacing, self.height), thickness)

        # Draws Slots
        for i in range(self.rows):
            for j in range(self.colm):
                self.slot[i][j].draw(win)

    # the grid model is a seperate board that is sent to the solver portion to solve it with
    # integer values and not values that have been drawn in 
    def update_model_grid(self):
        self.model_grid = [[self.slot[i][j].value for j in range(self.colm)] for i in range(self.rows)]

    # allows the user to select only the appropiate slots that are given
    def select_slot(self, row, col):
        # Reset any other slots
        for i in range(self.rows):
            for j in range(self.colm):
                self.slot[i][j].selected = False
        self.slot[row][col].selected = True
        self.selected = (row, col)

    # checks if a number that has been placed is valid and actually leds to solving the game
    def num_place(self, val):
        row, col = self.selected
        if self.slot[row][col].value == 0:
            self.slot[row][col].set(val)
            self.update_model_grid()
            # heyy, those two functions look hella familiar, well because it's from the solver portion 
            # we did before, we use those two functions to dicdate a well-placed number
            if valid_grid(self.model_grid, val, (row, col)) and solve_grid(self.model_grid):
                return True
            else:
                self.slot[row][col].set(0)
                self.slot[row][col].set_temp(0)
                self.update_model_grid()
                return False

    # only allows for areas where its zero to be mutated so it can be deleted if needed
    # also stops slots where there was originally a number to not be mutated
    def clear_slot(self):
        row, col = self.selected
        if self.slot[row][col].value == 0:
            self.slot[row][col].set_temp(0)

    # returns the position of the slot that has been mouse clicked
    def click(self, posn):
        if posn[0] < self.width and posn[1] < self.height:
            spacing = self.width / 9
            x = posn[0] // spacing
            y = posn[1] // spacing
            return (int(y), int(x))
        else:
            return None

    # makes sure there is no more empty slots left in either the rows or columns
    def game_over(self):
        for i in range(self.rows):
            for j in range(self.colm):
                if self.slot[i][j].value == 0:
                    return False
        return True


# class for the individial slots in the board
class Slot:
    rows = 9
    cols = 9

    # gives appropiate properties of a slot
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        # if the slot is selected or not, default is False, Ofc
        self.selected = False

    # basically draws the indivial boxes and shows if it is selected to add a number
    # it'll also draw the number on that selected slot
    def draw(self, win):
        # allows for font
        game_font = pygame.font.SysFont("arial", 40)

        # gives the gap/borderline so its not messy
        spacing = self.width / 9
        x = self.col * spacing
        y = self.row * spacing

        # this uses pygame module to render out the numbers and map it onto the board
        if self.temp != 0 and self.value == 0:
            text = game_font.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = game_font.render(str(self.value), 1, (255, 255, 255))
            win.blit(text, (x + (spacing / 2 - text.get_width() / 2), y + (spacing / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, spacing, spacing), 3)

    # sets a value to the slot
    def set(self, val):
        self.value = val

    # creates a temp value that will be set to a value
    def set_temp(self, val):
        self.temp = val


# basically just re-draws the board with the accurate modified state
# Adds time to see how long it's been for each round
# Also adds a strike icon when an incorrect number is given
def window_update(win, game_board, time, strikes):
    win.fill((0, 0, 0))
    # Draws time
    game_font = pygame.font.SysFont("arial", 40)
    text = game_font.render("Time: " + format_time(time), 1, (255, 255, 255))
    win.blit(text, (350, 550))
    # Draws Strikes
    text = game_font.render("X " * strikes, 1, (0, 255, 0))
    win.blit(text, (20, 560))
    # Draws grid
    game_board.draw(win)


# creates a universal timer
def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60
    timer = " " + str(minute) + ":" + str(sec)
    return timer


def main():
    win = pygame.display.set_mode((550, 600))
    pygame.display.set_caption("Sudoku Game")
    game_board = Grid(9, 9, 550, 550)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)
        # allows for the numbers to initialized to its appropiate key number
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    game_board.clear_slot()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = game_board.selected
                    # if there are no more zeroes and its solved then it's done
                    if game_board.slot[i][j].temp != 0:
                        if game_board.num_place(game_board.slot[i][j].temp):
                            print("Freaking Hell, That's Correct, Continue Smart Boy/Girl")
                        else:
                            # Continous to add a strike till you lose
                            print("You Freaking Guy, That's Wrong, Try Again")
                            strikes += 1
                        key = None
                        # prints when game is over
                        if game_board.game_over():
                            print("That's All Man, Game over, YOU WONNN")
                            run = False
                        # gives a limit to strikes before game is over
                        if strikes > 5:
                            print("YOU LOSTTTTT")
                            run = False
            # controls the mouse clicking portion so when something is clicked, it actually works
            if event.type == pygame.MOUSEBUTTONDOWN:
                posn = pygame.mouse.get_pos()
                clicked = game_board.click(posn)
                if clicked:
                    game_board.select_slot(clicked[0], clicked[1])
                    key = None

        if game_board.selected and key != None:
            game_board.sketch(key)

        window_update(win, game_board, play_time, strikes)
        pygame.display.update()


# calling main and also allowing for the game to quit
main()
pygame.quit()
