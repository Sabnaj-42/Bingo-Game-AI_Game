import numpy as np
from pygame import Color
import pygame
import random
import time
import os
import sys

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()
pygame.font.init()
pygame.display.set_caption("SCORE!")

# GLOBAL CONSTANTS
BLOCK_SIZE = 60
WHITE = (255, 255, 255)
MARGIN = 10
N_BLOCKS = 9 # SIZE OF GRID SQUARE
RANGE = 81  # RANGE OF NUMBERS

if RANGE < N_BLOCKS * N_BLOCKS:
    RANGE = N_BLOCKS * N_BLOCKS

# GLOBAL VARIABLES
PLAY_HOVER = True
GRID_HOVER = True
PLAY = True

# COLORS
ACCENT = (130, 30, 30)
NUM_CLR = (0, 0, 0)
MENU_CLR = (0, 0, 0)

# GAME WINDOW 
WIDTH = (BLOCK_SIZE * N_BLOCKS) + (MARGIN * N_BLOCKS) + MARGIN
HEIGHT = (BLOCK_SIZE * N_BLOCKS) + (MARGIN * N_BLOCKS) + MARGIN + 75
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets/Images", "mainbg.jpg")), (WIDTH, HEIGHT))
BGAI = pygame.transform.scale(pygame.image.load(os.path.join("assets/Images", "winnn.jpg")), (WIDTH, HEIGHT))
BGwin = pygame.transform.scale(pygame.image.load(os.path.join("assets/Images", "aiwin.jpg")), (WIDTH, HEIGHT))
Splashh = pygame.transform.scale(pygame.image.load(os.path.join("assets/Images", "splashscreen.jpg")), (WIDTH, HEIGHT))

CIRCLE = pygame.transform.scale(pygame.image.load(os.path.join("assets/Images", "circle.png")),
                                (BLOCK_SIZE, BLOCK_SIZE))

# LOADING AUDIO
HOVER = os.path.join("assets/Audio", "hover.mp3")
SCRATCH = os.path.join("assets/Audio", "scratch.mp3")
REV_SCRATCH = os.path.join("assets/Audio", "reverse_scratch.mp3")
MENU_CLICK = os.path.join("assets/Audio", "menu_click.mp3")
GET_LETTER = os.path.join("assets/Audio", "letter.mp3")
WIN_GAME = os.path.join("assets/Audio", "positive.wav")
LOSE_GAME = os.path.join("assets/Audio", "negative.wav")
EXIT = os.path.join("assets/Audio", "exit.mp3")

# LOADING FONTS
NUM_FONT = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Light.ttf"), 35)
NUM_FONT_2 = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Medium.ttf"), 35)
MENU_FONT = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Light.ttf"), 60)
MENU_FONT_2 = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Medium.ttf"), 60)
SCRATCH_FONT = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Medium.ttf"), 50)
New_font = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Medium.ttf"), 30)
newww = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Medium.ttf"), 17)

# Define the font size

FONT_SIZE = 60
FONT_SIZE_2 = 54
FONT_SIZE_3 = 40

# Create the font object with the desired size
GRID_FONT = pygame.font.Font(None, FONT_SIZE)
GRID_FONT_2 = pygame.font.Font(None, FONT_SIZE_2)
GRID_FONT_3 = pygame.font.Font(None, FONT_SIZE_3)




grid_input_text = "Choose Grid Number"
input_active = False


#function for difficulties selection

def select_grid_number(RANGE, difficulty):
    global N_BLOCKS, grid_input_text, input_active

    menu = True
    while menu:
        WIN.blit(BG, (0, 0))

        # GRID NUMBER TEXT
        grid_text = GRID_FONT.render("Grid Number", 1, MENU_CLR)
        grid_rect = grid_text.get_rect()
        grid_rect.x = int(WIDTH / 2 - grid_rect.width / 2)
        grid_rect.y = int(HEIGHT / 7)

        if hover(grid_rect):
            grid_text = GRID_FONT_2.render("Grid Number", 1, ACCENT)

        WIN.blit(grid_text, (grid_rect.x, grid_rect.y))

        # Render the input field text
        grid_input_text_surface = GRID_FONT_3.render(grid_input_text, True, MENU_CLR)
        grid_input_rect = grid_input_text_surface.get_rect()
        grid_input_rect.center = (int(WIDTH / 2), int(HEIGHT / 4 + grid_rect.height + 100))
        input_box_rect = pygame.Rect(
            grid_input_rect.left - 5,
            grid_input_rect.top - 5,
            grid_input_rect.width + 10,
            grid_input_rect.height + 10
        )
        pygame.draw.rect(WIN, ACCENT, input_box_rect, 2)
        WIN.blit(grid_input_text_surface, grid_input_rect)

        # Display the current value of N_BLOCKS
        current_grid_text = GRID_FONT_3.render("*** Choose among 3-9 ***", 1, MENU_CLR)
        current_grid_rect = current_grid_text.get_rect()
        current_grid_rect.x = int(WIDTH / 2 - current_grid_rect.width / 2)
        current_grid_rect.y = int(HEIGHT / 2 + grid_rect.height + 130)
        WIN.blit(current_grid_text, (current_grid_rect.x, current_grid_rect.y))

        # CLICK EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the grid number input field is clicked
                if grid_input_rect.collidepoint(event.pos):
                    input_active = True
                    grid_input_text = ""
                else:
                    input_active = False
                    grid_input_text = "Choose Grid Number"

            if input_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        # Update N_BLOCKS with the user's input
                        N_BLOCKS = int(grid_input_text)
                        RANGE = N_BLOCKS * N_BLOCKS
                        print(N_BLOCKS)
                        pygame.display.flip()
                        # Call the main function to start the game with selected difficulty and grid size
                        main(RANGE, difficulty)
                    except ValueError:
                        # Handle invalid input
                        pass
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    # Remove the last character from the input string
                    grid_input_text = grid_input_text[:-1]
                else:
                    # Add the pressed key to the input string
                    grid_input_text += event.unicode

        pygame.display.flip()



def difficulty_menu(RANGE):
    global PLAY_HOVER, EASY_HOVER, MEDIUM_HOVER, HARD_HOVER

    # Initialize hover variables
    EASY_HOVER = True
    MEDIUM_HOVER = True
    HARD_HOVER = True

    menu = True
    while menu:
        WIN.blit(BG, (0, 0))

        # EASY TEXT
        easy_text = GRID_FONT.render("Easy", 1, MENU_CLR)
        easy_rect = easy_text.get_rect()
        easy_rect.x = int(WIDTH / 2 - easy_rect.width / 2)
        easy_rect.y = int(HEIGHT / 3 - easy_rect.height / 3)

        if hover(easy_rect):
            if EASY_HOVER:
                play_sound(HOVER)
                EASY_HOVER = False
            easy_text = GRID_FONT.render("Easy", 1, ACCENT)
        else:
            EASY_HOVER = True

        WIN.blit(easy_text, (easy_rect.x, easy_rect.y))

        # MEDIUM TEXT
        medium_text = GRID_FONT.render("Medium", 1, MENU_CLR)
        medium_rect = medium_text.get_rect()
        medium_rect.x = int(WIDTH / 2 - medium_rect.width / 2)
        medium_rect.y = int(HEIGHT / 2 - medium_rect.height / 2)

        if hover(medium_rect):
            if MEDIUM_HOVER:
                play_sound(HOVER)
                MEDIUM_HOVER = False
            medium_text = GRID_FONT.render("Medium", 1, ACCENT)
        else:
            MEDIUM_HOVER = True

        WIN.blit(medium_text, (medium_rect.x, medium_rect.y))

        # HARD TEXT
        hard_text = GRID_FONT.render("Hard", 1, MENU_CLR)
        hard_rect = hard_text.get_rect()
        hard_rect.x = int(WIDTH / 2 - hard_rect.width / 2)
        hard_rect.y = int(HEIGHT / 1.5 - hard_rect.height / 1.5)

        if hover(hard_rect):
            if HARD_HOVER:
                play_sound(HOVER)
                HARD_HOVER = False
            hard_text = GRID_FONT.render("Hard", 1, ACCENT)
        else:
            HARD_HOVER = True

        WIN.blit(hard_text, (hard_rect.x, hard_rect.y))

        # CLICK ON DIFFICULTY
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if hover(easy_rect):
                    play_sound(MENU_CLICK)
                    time.sleep(0.5)
                    select_grid_number(RANGE, 'Easy')
                elif hover(medium_rect):
                    play_sound(MENU_CLICK)
                    time.sleep(0.5)
                    select_grid_number(RANGE, 'Medium')
                elif hover(hard_rect):
                    play_sound(MENU_CLICK)
                    time.sleep(0.5)
                    select_grid_number(RANGE, 'Hard')

        pygame.display.flip()




def main_menu(RANGE):
    global PLAY_HOVER, GRID_HOVER, DIFFICULTY_HOVER, grid_input_text, input_active

    splash_screen_duration = 3  # in seconds
    splash_screen_end_time = time.time() + 3

    menu = True
    while menu:
        if time.time() > splash_screen_end_time:
            break
        alpha = int(255 * (1 - (time.time() - splash_screen_end_time) / splash_screen_duration))
        Splashh.set_alpha(alpha)  # Set the alpha value for transparency
        WIN.blit(Splashh, (0, 0))
        pygame.display.flip()

    menu = True
    while menu:
        WIN.blit(BG, (0, 0))

        # PLAY TEXT
        play_text = GRID_FONT.render("<<PLAY>>", 1, MENU_CLR)
        play_rect = play_text.get_rect()
        play_rect.x = int(WIDTH / 2 - play_rect.width / 2)
        play_rect.y = int(HEIGHT / 1.9 - play_rect.height / 1.9)

        if hover(play_rect):
            if PLAY_HOVER:
                play_sound(HOVER)
                PLAY_HOVER = False
            play_text = GRID_FONT.render("<<PLAY>>", 1, ACCENT)
        else:
            PLAY_HOVER = True

        WIN.blit(play_text, (play_rect.x, play_rect.y))

        # DIFFICULTY TEXT
        difficulty_text = GRID_FONT.render("Difficulty", 1, MENU_CLR)
        difficulty_rect = difficulty_text.get_rect()
        difficulty_rect.x = int(WIDTH / 2 - difficulty_rect.width / 2)
        difficulty_rect.y = int(HEIGHT / 2 + play_rect.height)

        if hover(difficulty_rect):
            if DIFFICULTY_HOVER:
                play_sound(HOVER)
                DIFFICULTY_HOVER = False
            difficulty_text = GRID_FONT.render("Difficulty", 1, ACCENT)
        else:
            DIFFICULTY_HOVER = True

        WIN.blit(difficulty_text, (difficulty_rect.x, difficulty_rect.y))

        # CLICK EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if hover(play_rect):
                    play_sound(MENU_CLICK)
                    time.sleep(0.5)
                    difficulty_menu(RANGE)  # Navigate to difficulty menu

        pygame.display.flip()





'''
def end_screen(AI):
    global PLAY_HOVER, PLAY

    if PLAY:
        play_sound(WIN_GAME)
        PLAY = False

    # DISPLAYING TEXT
    if AI==1:
        win_text = MENU_FONT.render("AI WINS!", 1, ACCENT)
    elif AI==0:
        win_text = MENU_FONT.render("YOU WIN!", 1, ACCENT)
    else:
        win_text = MENU_FONT.render("TIE!", 1, ACCENT)
    win_rect = win_text.get_rect()
    win_rect.x = int(WIDTH / 2 - win_rect.width / 2)
    win_rect.y = int((HEIGHT - 75) / 2 - win_rect.height / 2)

    rest_text = MENU_FONT.render("RESTART", 1, MENU_CLR)
    rest_rect = rest_text.get_rect()
    rest_rect.x = int(WIDTH / 2 - rest_rect.width / 2)
    rest_rect.y = int((HEIGHT - 75) / 2 + win_rect.height + 10)

    # MAKING RESTART INTERACTIVE
    if hover(rest_rect):
        if PLAY_HOVER:
            play_sound(HOVER)
            PLAY_HOVER = False
        rest_text = MENU_FONT_2.render("RESTART", 1, ACCENT)
    else:
        PLAY_HOVER = True

    WIN.blit(BG, (0, 0))
    WIN.blit(win_text, (win_rect.x, win_rect.y))
    WIN.blit(rest_text, (rest_rect.x, rest_rect.y))

    # CLICK ON RESTART
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if hover(rest_rect):
                play_sound(MENU_CLICK)

                time.sleep(0.5)
                main_menu(RANGE)

    pygame.display.flip()
'''
def end_screen(AI, ai_grid):
    global PLAY_HOVER, PLAY

    if PLAY:
        play_sound(WIN_GAME)
        PLAY = False

    # DISPLAYING TEXT
    if AI == 1:
        win_text = MENU_FONT.render("AI WINS!", 1, ACCENT)
    elif AI == 0:
        win_text = MENU_FONT.render("YOU WIN!", 1, ACCENT)
    else:
        win_text = MENU_FONT.render("TIE!", 1, ACCENT)
    win_rect = win_text.get_rect()
    win_rect.center = (WIDTH // 2, HEIGHT // 2 - 40)

    rest_text = New_font.render("RESTART", 1, MENU_CLR)
    rest_rect = rest_text.get_rect()
    rest_rect.center = (WIDTH // 2, HEIGHT // 2 + 20)

    ai_text = New_font.render("SHOW AI GRID", 1, MENU_CLR)
    ai_rect = ai_text.get_rect()
    ai_rect.center = (WIDTH // 2, HEIGHT // 2 + 60)

    # MAKING RESTART INTERACTIVE
    if hover(rest_rect):
        if PLAY_HOVER:
            play_sound(HOVER)
            PLAY_HOVER = False
        rest_text = New_font.render("RESTART", 1, ACCENT)
    else:
        PLAY_HOVER = True

    # MAKING AI GRID INTERACTIVE
    if hover(ai_rect):
        if PLAY_HOVER:
            play_sound(HOVER)
            PLAY_HOVER = False
        ai_text = New_font.render("SHOW AI GRID", 1, ACCENT)
    else:
        PLAY_HOVER = True

    WIN.blit(BGwin, (0, 0))
    WIN.blit(win_text, win_rect)
    WIN.blit(rest_text, rest_rect)
    WIN.blit(ai_text, ai_rect)

    # CLICK ON RESTART
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if hover(rest_rect):
                play_sound(MENU_CLICK)
                time.sleep(0.5)
                main_menu(RANGE)

            if hover(ai_rect):
                play_sound(MENU_CLICK)
                time.sleep(0.5)
                show_ai_grid(ai_grid)

    pygame.display.flip()
    
'''   
def show_ai_grid(ai_grid):
    # Create a new window to show the AI grid values
    ai_win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AI Grid")
    
    # Positioning the AI grid values caption
    ai_text = New_font.render("AI GRID VALUES", 1, ACCENT)
    ai_rect = ai_text.get_rect()
    ai_rect.topleft = (205, 10)  # Adjust the y-coordinate to create space for numbers

    back_text = newww.render("BACK", 1, MENU_CLR)
    back_rect = back_text.get_rect()
    back_rect.bottomright = (WIDTH - 5, HEIGHT - 5)

    while True:
        # Handle events in the new window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if hover(back_rect):
                    play_sound(MENU_CLICK)
                    time.sleep(0.5)
                    return

        ai_win.blit(BGAI, (0, 0))
        ai_win.blit(ai_text, ai_rect)

        # Display the AI grid values
        for column in range(N_BLOCKS):
            for row in range(N_BLOCKS):
                x = (MARGIN + BLOCK_SIZE) * column + MARGIN
                y = (MARGIN + BLOCK_SIZE) * row + MARGIN

                value = ai_grid[row, column]
                if value == 10000:
                    value_text = New_font.render("*", 1, ACCENT)  # Render "*" in red color
                else:
                    value_text = New_font.render(str(value), 1, NUM_CLR)  # Render numbers in black color

                value_rect = pygame.Rect(x, y + ai_rect.height + 20, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(ai_win, WHITE, value_rect)  # Draw a white rectangle around the number

                value_rect_center = value_text.get_rect(center=value_rect.center)
                ai_win.blit(value_text, value_rect_center)

        ai_win.blit(back_text, back_rect)
        pygame.display.flip()

'''
 
def show_ai_grid(ai_grid):
    # Create a new window to show the AI grid values
    ai_win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AI Grid")
    
    # Positioning the AI grid values caption
    ai_text = New_font.render("AI GRID VALUES", 1, ACCENT)
    ai_rect = ai_text.get_rect()  # Center the text horizontally and vertically
    ai_rect.topleft = (205, 10)
    back_text = newww.render("BACK", 1, MENU_CLR)
    back_rect = back_text.get_rect()
    back_rect.bottomright = (WIDTH - 5, HEIGHT - 5)

    while True:
        # Handle events in the new window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if hover(back_rect):
                    play_sound(MENU_CLICK)
                    time.sleep(0.5)
                    return

        ai_win.blit(BGAI, (0, 0))
        ai_win.blit(ai_text, ai_rect)

        # Calculate the center of the window
        window_center_x = WIDTH // 2
        window_center_y = HEIGHT // 2

        # Calculate the starting position for drawing the grid
        grid_width = (BLOCK_SIZE + MARGIN) * N_BLOCKS
        grid_height = (BLOCK_SIZE + MARGIN) * N_BLOCKS
        grid_start_x = window_center_x - (grid_width // 2)
        grid_start_y = window_center_y - (grid_height // 2)

        # Display the AI grid values
        for column in range(N_BLOCKS):
            for row in range(N_BLOCKS):
                x = grid_start_x + (MARGIN + BLOCK_SIZE) * column
                y = grid_start_y + (MARGIN + BLOCK_SIZE) * row

                value = ai_grid[row, column]
                if value == 10000:
                    value_text = New_font.render("*", 1, ACCENT)  # Render "*" in red color
                else:
                    value_text = New_font.render(str(value), 1, NUM_CLR)  # Render numbers in black color

                value_rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(ai_win, WHITE, value_rect)  # Draw a white rectangle around the number

                value_rect_center = value_text.get_rect(center=value_rect.center)
                ai_win.blit(value_text, value_rect_center)

        ai_win.blit(back_text, back_rect)
        pygame.display.flip()


    
def hover(rect):
    if rect.collidepoint(pygame.mouse.get_pos()):
        return True
    return False


def play_sound(sound, volume=1.0):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()

'''
def show_numbers(grid1, grid2):
    for column in range(N_BLOCKS):
        for row in range(N_BLOCKS):
            x = (MARGIN + BLOCK_SIZE) * column + MARGIN
            y = (MARGIN + BLOCK_SIZE) * row + MARGIN

            if grid2[row, column] == 1:
                scratch = SCRATCH_FONT.render("/",1,ACCENT)
                WIN.blit(scratch, (x+15, y))

            text = NUM_FONT.render(str(grid1[row, column]), 1, NUM_CLR)
            text_rect = text.get_rect()
            text_rect.x = int(x + (BLOCK_SIZE / 2) - text_rect.width / 2)
            text_rect.y = int(y + (BLOCK_SIZE / 2) - text_rect.height / 2)

            if hover(text_rect):
                text = NUM_FONT_2.render(str(grid1[row, column]), 1, ACCENT)

            WIN.blit(text, (text_rect.x, text_rect.y))
'''
def show_numbers(grid1, grid2,ai_number):
    for column in range(N_BLOCKS):
        for row in range(N_BLOCKS):
            x = (MARGIN + BLOCK_SIZE) * column + MARGIN
            y = (MARGIN + BLOCK_SIZE) * row + MARGIN
            grid_rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(WIN, WHITE, grid_rect)
            if grid2[row, column] == 1:
                scratch = SCRATCH_FONT.render("/",1,ACCENT)
                WIN.blit(scratch, (x+15, y))

            text = NUM_FONT.render(str(grid1[row, column]), 1, NUM_CLR)
            text_rect = text.get_rect()
            text_rect.x = int(x + (BLOCK_SIZE / 2) - text_rect.width / 2)
            text_rect.y = int(y + (BLOCK_SIZE / 2) - text_rect.height / 2)

            if hover(text_rect):
                text = NUM_FONT_2.render(str(grid1[row, column]), 1, ACCENT)

            WIN.blit(text, (text_rect.x, text_rect.y))
            if grid1[row][column]==ai_number:
                radius = BLOCK_SIZE // 2 - 2
                center_x = x + BLOCK_SIZE // 2
                center_y = y + BLOCK_SIZE // 2
                pygame.draw.circle(WIN,ACCENT, (center_x, center_y), radius, 3)
            






def show_letters(n1, n2):
    word = "SCORE"

    if n2 > 0:
        bingo = MENU_FONT.render(str(word[0:n2]), 1, ACCENT)
        bingo_rect = bingo.get_rect()
        bingo_rect.x = int(WIDTH / 2 - (bingo_rect.width / 2 + (45 / 2)))
        bingo_rect.y = int(HEIGHT - bingo_rect.height)

        WIN.blit(bingo, (bingo_rect.x, bingo_rect.y))

    if n1 != n2:
        play_sound(GET_LETTER, 0.15)


    
    

WIN_SIZE = (800, 600)
EMPTY = 0
AI_MARK = 10000
PLAYER_MARK = 1







import numpy as np

EMPTY = 0
AI_MARK = 10000
PLAYER_MARK = 10000

def evaluate_score(ai_grid,move,roww,coll):
    # Evaluate the score of a given grid
    distance = 0
    score = 0
    win_score=0
    max_win_score=0
    #roww = 0  # Initialize roww before the loop
    #coll = 0  # Initialize coll before the loop
    #for row in range(N_BLOCKS):
     #   for col in range(N_BLOCKS):
          #  if ai_grid[row, col] == move:
           #     roww = row
              #  coll = col
    for r in range(N_BLOCKS):
        for c in range(N_BLOCKS):
            if ai_grid[r, c] == 10000:
                distance = distance + abs(roww - r) + abs(coll - c)
                #print("roww: ",roww," r: ",r," coll: ",coll," c: ",c)
                #print("distance: ",distance)

    # Rows and columns
    max_row_marks = 0
    max_col_marks = 0
    for i in range(N_BLOCKS):
        if all(ai_grid[i, :] == 10000):
            win_score += 1
                            

                    # Check columns
    for j in range(N_BLOCKS):
        if all(ai_grid[:, j] == 10000):
            win_score += 1

                    # Check diagonal 1
    if all(ai_grid.diagonal() == 10000):
           win_score += 1

                    # Check diagonal 2
    if all(np.fliplr(ai_grid).diagonal() == 10000):
           win_score += 1

                    # Check 3x2 or 2x3 grids
    for i in range(N_BLOCKS - 1):
          for j in range(N_BLOCKS - 2):
                # Check for a 2x3 grid
               if(ai_grid[i:i+2, j:j+3] == 10000).all():
                    win_score += 6
        # 3x2 GRIDS
    for i in range(N_BLOCKS - 2):
          for j in range(N_BLOCKS - 1):
                # Check for a 3x2 grid
               if(ai_grid[i:i+3, j:j+2] == 10000).all():
                    win_score += 6

    for i in range(N_BLOCKS):
        row_marks = (ai_grid[i, :] == AI_MARK).sum()
        col_marks = (ai_grid[:, i] == AI_MARK).sum()

        if row_marks > max_row_marks:
            max_row_marks = row_marks
            #score += 1
        if col_marks > max_col_marks:
            max_col_marks = col_marks
            #score += 1

    # Diagonals
    diagonal_marks = (ai_grid.diagonal() == AI_MARK).sum()
    reverse_diagonal_marks = (np.fliplr(ai_grid).diagonal() == AI_MARK).sum()
    """
    if diagonal_marks > max_row_marks:
        max_row_marks = diagonal_marks
        score += 1
    if reverse_diagonal_marks > max_row_marks:
        max_row_marks = reverse_diagonal_marks
        score += 1
    """
    max_grid_score_3x2 = 0
    grid_score_3x2 = 0
    
    # Check 3x2 or 2x3 grids
    for i in range(N_BLOCKS - 1):
        for j in range(N_BLOCKS - 2):
            # Check for a 2x3 grid
            grid_score_3x2= (ai_grid[i:i+2, j:j+3] == AI_MARK).sum()*5
            if grid_score_3x2> max_grid_score_3x2:
                max_grid_score_3x2= grid_score_3x2
            
    max_grid_score_2x3 = 0
    grid_score_2x3 = 0
    for i in range(N_BLOCKS - 2):
        for j in range(N_BLOCKS - 1):
            grid_score_2x3= (ai_grid[i:i+3, j:j+2] == AI_MARK).sum()*5
            if grid_score_2x3> max_grid_score_2x3:
                max_grid_score_2x3= grid_score_2x3
    for i in range(N_BLOCKS):
        for j in range(N_BLOCKS):
            # Check for a 2x3 grid
            if win_score> max_win_score:
                max_win_score= win_score       
    score = score + max_row_marks + max_col_marks + diagonal_marks + reverse_diagonal_marks + max_grid_score_3x2 + max_grid_score_2x3+max_win_score
    #print("move",move)
    #print("score",score)
    score = score/distance
    
    
    #print("max_row_marks",max_row_marks)
    #print("max_col_marks",max_col_marks)
    #print("diagonal_marks",diagonal_marks)
    #print("reverse_diagonal_marks",reverse_diagonal_marks)
    #print("max_grid_score_3x2",max_grid_score_3x2)
    #print("max_grid_score_2x3",max_grid_score_2x3)
    #print("distance",distance)
    #print("move",move)
    #print("score",score)
    
    

    return score

def get_moves_to_complete(grid):
    # Get the number of moves required to complete a 3x2 or 2x3 grid
    empty_cells = (grid != 10000).sum()
    return empty_cells

def is_terminal_state(ai_grid,move,roww,coll):
    # Check if the game has ended in a terminal state
    return evaluate_score(ai_grid,move,roww,coll) > 0 or (ai_grid == 10000).sum() == 0

def get_available_moves(ai_grid):
    # Get the available moves in the grid
    return np.where(ai_grid != 10000)[0]

def make_move(ai_grid, move, player):
    # Make a move in the grid
    #N_BLOCKS = 6
    new_grid = ai_grid.copy()
    for row in range(N_BLOCKS):
        for col in range(N_BLOCKS):
            if new_grid[row, col] == move:
                new_grid[row, col] = 10000
    
    return new_grid

def minimax(ai_grid, depth, alpha, beta, maximizing_player,move,roww,coll):
    if depth == 0 or is_terminal_state(ai_grid,move,roww,coll):
        return evaluate_score(ai_grid,move,roww,coll)
    #print("depth" ,  depth)

    if maximizing_player:
        max_eval = float('-inf')
        moves = get_available_moves(ai_grid)
        moves = order_moves(ai_grid, moves)
        # Order moves based on completing 3x2 or 2x3 grids
        #print ("moves",moves)
        for move in moves:
            new_grid = make_move(ai_grid, move, AI_MARK)
            eval = minimax(new_grid, depth - 1, alpha, beta, False,move,roww,coll)
            #print("move: ",move,"max eval: ",eval,"depth:", depth)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        moves = get_available_moves(ai_grid)
        # Order moves based on completing 3x2 or 2x3 grids
        moves = order_moves(ai_grid, moves)
        for move in moves:
            new_grid = make_move(ai_grid, move, PLAYER_MARK)
            eval = minimax(new_grid, depth - 1, alpha, beta, True,move,roww,coll)
            #print("move: ",move,"min eval: ",eval,"depth:", depth)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
    


#Genetic Algorithm
import random

def initialize_population(pop_size, ai_grid):
    population = []
    moves = get_available_moves(ai_grid)
    for _ in range(pop_size):
        move = random.choice(moves)
        population.append(move)
    return population

def fitness_function(ai_grid, move, roww, coll):
    new_grid = make_move(ai_grid, move, AI_MARK)
    score = evaluate_score(new_grid, move, N_BLOCKS, N_BLOCKS)
    return score

def selection(population, fitnesses, num_parents):
    selected = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)
    return [move for move, fitness in selected[:num_parents]]

def crossover(parent1, parent2):
    # For simplicity, we just take the first parent move
    return parent1

def mutation(move, moves, mutation_rate=0.1):
    if random.random() < mutation_rate:
        return random.choice(moves)
    return move

def genetic_algorithm(ai_grid, roww, coll, pop_size=10, generations=10, num_parents=5, mutation_rate=0.1):
    population = initialize_population(pop_size, ai_grid)
    moves = get_available_moves(ai_grid)
    print("GENETIC ALGORITHM")
    
    for _ in range(generations):
        fitnesses = [fitness_function(ai_grid, move, N_BLOCKS, N_BLOCKS) for move in population]
        
        parents = selection(population, fitnesses, num_parents)
        
        next_population = []
        
        for _ in range(pop_size):
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            
            offspring = crossover(parent1, parent2)
            offspring = mutation(offspring, moves, mutation_rate)
            
            next_population.append(offspring)
        
        population = next_population
    
    # Return the best move
    fitnesses = [fitness_function(ai_grid, move, roww, coll) for move in population]
    best_move = population[fitnesses.index(max(fitnesses))]
    
    return best_move




def order_moves(ai_grid, moves):
    # Order moves based on completing 3x2 or 2x3 grids
    ordered_moves = []
    dit = {}
    for move in moves:
        new_grid = make_move(ai_grid, move, AI_MARK)
        xxx = max(check_3x2_grid(new_grid,move), check_2x3_grid(new_grid,move))
        dit[move] =  xxx
    #sorted_dict = sorted(dit.items(), key=lambda x: x[1])  # Sort the dictionary by values
    #first_element = sorted_dict[0].move()
    #sorted_keys = sorted(dit.keys())
    #first_key = sorted_keys[0]
    sorted_moves = sorted(dit.items(), key=lambda x: x[1], reverse=True)  # Sort the moves based on their values

    for move, value in sorted_moves:
        ordered_moves.append(move)
        
    """
        if check_3x2_grid(new_grid) or check_2x3_grid(new_grid):
            ordered_moves.insert(0, move)  # Add move to the beginning of the list
        else:
            ordered_moves.append(move)  # Add move to the end of the list
    """
    return ordered_moves
def check_3x2_grid(grid,move):
    # Check if the grid has a 3x2 pattern of AI marks
    best_match_score = 0
    distance = 0
    best_future_moves = float('inf')
    roww = 0  # Initialize roww before the loop
    coll = 0  # Initialize coll before the loop
    for row in range(N_BLOCKS):
       for col in range(N_BLOCKS):
           if grid[row, col] == move:
               roww = row
               coll = col
    for r in range(N_BLOCKS):
       for c in range(N_BLOCKS):
           if grid[r, c] == 10000:
               distance = distance + abs(roww - r) + abs(coll - c)

    for i in range(N_BLOCKS - 2):
        for j in range(N_BLOCKS - 1):
            match_score = (grid[i:i+3, j:j+2] == AI_MARK).sum()
            future_moves = get_moves_to_complete(grid[i:i+3, j:j+2])

            if match_score > best_match_score:
                best_match_score = match_score
                best_future_moves = future_moves
    best_match_score = best_match_score/distance

    return best_match_score

def check_2x3_grid(grid,move):
    # Check if the grid has a 2x3 pattern of AI marks
    best_match_score = 0
    distance = 0
    best_future_moves = float('inf')
    roww = 0  # Initialize roww before the loop
    coll = 0  # Initialize coll before the loop
    for row in range(N_BLOCKS):
       for col in range(N_BLOCKS):
           if grid[row, col] == move:
               roww = row
               coll = col
    for r in range(N_BLOCKS):
       for c in range(N_BLOCKS):
           if grid[r, c] == 10000:
               distance = distance + abs(roww - r) + abs(coll - c)

    for i in range(N_BLOCKS - 1):
        for j in range(N_BLOCKS - 2):
            match_score = (grid[i:i+2, j:j+3] == AI_MARK).sum()
            future_moves = get_moves_to_complete(grid[i:i+2, j:j+3])

            if match_score > best_match_score :
                best_match_score = match_score
                best_future_moves = future_moves
    best_match_score = best_match_score/distance

    return best_match_score

def get_best_move(ai_grid, moves, strategy='minimax'):
    best_score = float('-inf')
    best_move = None
    roww = 0  # Initialize roww before the loop
    coll = 0  # Initialize coll before the loop
    for move in moves:
        for row in range(N_BLOCKS):
            for col in range(N_BLOCKS):
                if ai_grid[row, col] == move:
                    roww = row
                    coll = col
        
        if strategy == 'minimax':
            new_grid = make_move(ai_grid, move, AI_MARK)
            score = minimax(new_grid, depth=5, alpha=float('-inf'), beta=float('inf'), maximizing_player=False, move=move, roww=roww, coll=coll)
        elif strategy == 'genetic_algorithm':
            score = genetic_algorithm(ai_grid, moves,N_BLOCKS,N_BLOCKS)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

        if score > best_score:
            best_score = score
            best_move = move

    return best_move






def AI_move(player_grid, grid2, ai_grid, clicked, diag_pos, difficulty):
    ai_score = 0
    moves = []
    for row in range(N_BLOCKS):
        for col in range(N_BLOCKS):
            if grid2[row, col] == 0:
                moves.append(player_grid[row, col])

    if difficulty == 'Easy':
        ai_number = get_best_move(ai_grid, moves, strategy='genetic_algorithm')
    elif difficulty == 'Medium':
        ai_number = get_best_move(ai_grid, moves, strategy='minimax')
    else:
        raise ValueError(f"Unknown difficulty: {difficulty}")

    print("AI selected number:", ai_number)  # Print the number selected by the AI

    for row in range(N_BLOCKS):
        for col in range(N_BLOCKS):
            if player_grid[row, col] == ai_number:
                grid2[row, col] = 1

                # ADD TO D1
                if row == col:
                    clicked.append("d1")

                # ADD TO D2
                if [row, col] in diag_pos:
                    clicked.append("d2")

                # ADD X AND Y
                clicked.append(f"{row}y")
                clicked.append(f"{col}x")

                for row in range(N_BLOCKS):
                    for col in range(N_BLOCKS):
                        if ai_grid[row, col] == ai_number:
                            ai_grid[row, col] = 10000

                for i in range(N_BLOCKS):
                    if all(ai_grid[i, :] == 10000):
                        ai_score += 1

                # Check columns
                for j in range(N_BLOCKS):
                    if all(ai_grid[:, j] == 10000):
                        ai_score += 1

                # Check diagonal 1
                if all(ai_grid.diagonal() == 10000):
                    ai_score += 1

                # Check diagonal 2
                if all(np.fliplr(ai_grid).diagonal() == 10000):
                    ai_score += 1

                # Check 3x2 or 2x3 grids
                for i in range(N_BLOCKS - 1):
                    for j in range(N_BLOCKS - 2):
                        if (ai_grid[i:i + 2, j:j + 3] == 10000).all():
                            ai_score += 6

                for i in range(N_BLOCKS - 2):
                    for j in range(N_BLOCKS - 1):
                        if (ai_grid[i:i + 3, j:j + 2] == 10000).all():
                            ai_score += 6

                # Show the AI grid in the console
                print("AI Grid After AI's Move:")
                print(ai_grid)
                print("AI Score:", ai_score)

                return grid2, ai_score, ai_number

    return None



def main(RANGE,difficulty):
    global PLAY_HOVER
    ai_number = None
    rrr = N_BLOCKS*N_BLOCKS
    # Separate grids for player and AI
    player_grid = random.sample(range(1, rrr + 1), N_BLOCKS * N_BLOCKS)
    player_grid = np.array(player_grid)
    player_grid = np.reshape(player_grid, (N_BLOCKS, N_BLOCKS))

    ai_grid = random.sample(range(1, rrr + 1), N_BLOCKS * N_BLOCKS)
    ai_grid = np.array(ai_grid)
    ai_grid = np.reshape(ai_grid, (N_BLOCKS, N_BLOCKS))

    grid2 = np.zeros((N_BLOCKS, N_BLOCKS), dtype=object)  # Use object dtype to store "*"
    grid3 = grid2.copy()

    # Show the AI grid in the console
    print("AI Grid:")
    print(ai_grid)

    run = True
    win = False
    m_menu = False
    clock = pygame.time.Clock()

    n_letters = 0
    clicked = []
    tkn_pos = []

    # DIAGONAL
    n1 = 0
    n2 = N_BLOCKS - 1
    diag_pos = []
    for _ in range(0, N_BLOCKS):
        diag_pos.append([n1, n2])
        n1 += 1
        n2 -= 1
    human_turn = 1  # 1 indicates human's turn, 0 indicates AI's turn
    ai_score=0
    # MAIN GAME LOOP
    while run:
        if win:
            #time.sleep(1)
            #while win:
            pygame.time.delay(1000)
            end_screen(AI,ai_grid)

        if m_menu:
            time.sleep(0.5)
            run = False

            while m_menu:
                main_menu(RANGE)

        WIN.blit(BG, (0, 0))

        # SHOWING NUMBERS
        show_numbers(player_grid, grid2,ai_number)

        # SHOWING BINGO LETTERS
        n = n_letters
        n_letters = len(tkn_pos)

        show_letters(n, n_letters)

        # SHOWING EXIT BUTTON
        #exit_btn()

        # WINNING
        #if n_letters == 5:
         #   win = True

        # CHECKING IF GOT LETTER
        for i in clicked:
            if clicked.count(i) >= N_BLOCKS and i not in tkn_pos:
                tkn_pos.append(i)

        for event in pygame.event.get():
            # QUIT
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # CLICK
            if event.type == pygame.MOUSEBUTTONDOWN and not win and human_turn == 1:

                pos = pygame.mouse.get_pos()
                column = pos[0] // (BLOCK_SIZE + MARGIN)
                row = pos[1] // (BLOCK_SIZE + MARGIN)

                if row < N_BLOCKS and column < N_BLOCKS:
                    # IF ALREADY CLICKED: UN-CLICK
                    if grid2[row, column] == 1:
                        x = player_grid[row,column]
 
                        
                        for r in range(N_BLOCKS):
                            for c in range(N_BLOCKS):
                                if ai_grid[r, c] == 10000:
                                    ai_grid[r, c] = x
                        # Show the AI grid in the console
                        print("AI Grid:")
                        print(ai_grid)
                        grid2[row, column] = 0

                        play_sound(REV_SCRATCH)

                        # REMOVE FROM D1
                        if row == column:
                            clicked.remove("d1")

                            if "d1" in tkn_pos:
                                tkn_pos.remove("d1")

                        # REMOVE FROM D2
                        if [row, column] in diag_pos:
                            clicked.remove("d2")

                            if "d2" in tkn_pos:
                                tkn_pos.remove("d2")

                        # REMOVE X AND Y
                        clicked.remove(f"{row}y")
                        clicked.remove(f"{column}x")

                        if f"{row}y" in tkn_pos:
                            tkn_pos.remove(f"{row}y")

                        if f"{column}x" in tkn_pos:
                            tkn_pos.remove(f"{column}x")

                    # IF NOT CLICKED: CLICK
                    else:
                        
                        x = player_grid[row,column]
                        grid2[row, column] = 1
                        
                        for r in range(N_BLOCKS):
                            for c in range(N_BLOCKS):
                                if ai_grid[r, c] == x:
                                    ai_grid[r, c] = 10000

                        # Show the AI grid in the console
                        print("AI Grid After Player's Move:")
                        print(ai_grid)
                        #print(grid2)
                        #mark_star(row,column);
                        #player_grid[row, column] = 1   #eimu

                        play_sound(SCRATCH)

                        # ADD TO D1
                        if row == column:
                            clicked.append("d1")

                        # ADD TO D2
                        if [row, column] in diag_pos:
                            clicked.append("d2")

                        # ADD X AND Y
                        clicked.append(f"{row}y")
                        clicked.append(f"{column}x")

                # EXIT BUTTON
                if (WIN_SIZE[0] - 60) <= pos[0] <= (WIN_SIZE[0] - 10) and 10 <= pos[1] <= 60:
                    m_menu = True
                if not win:
        
                    human_turn = 0  # Toggle the flag value between 0 and 1
        
        
        
        p_score = 0
        
        # ROWS
        for i in range(N_BLOCKS):
            if all(grid2[i, :] == 1):
                p_score += 1

        # COLUMNS
        for j in range(N_BLOCKS):
            if all(grid2[:, j] == 1):
                p_score += 1

        # DIAGONAL 1
        if all(grid2.diagonal() == 1):
            
            
            
            p_score += 1

        # DIAGONAL 2
        if all(np.fliplr(grid2).diagonal() == 1):
            p_score += 1
        '''
        # 3x2 or 2x3 GRIDS
        for i in range(N_BLOCKS - 1):
            for j in range(N_BLOCKS - 1):
                # Check for a 3x2 grid
                if (grid2[i:i+3, j:j+2] == 1).all() or (grid2[i:i+2, j:j+3] == 1).all():
                    p_score += 6

        '''
        for i in range(N_BLOCKS - 1):
            for j in range(N_BLOCKS - 2):
                # Check for a 2x3 grid
                if(grid2[i:i+2, j:j+3] == 1).all():
                    p_score += 5
        # 3x2 GRIDS
        for i in range(N_BLOCKS - 2):
            for j in range(N_BLOCKS - 1):
                # Check for a 3x2 grid
                if(grid2[i:i+3, j:j+2] == 1).all():
                    p_score += 5
        # WINNING
        if (p_score >= 5) :
            AI=0
            win = True
            
        
                    

        # AI MOVE
        if not win and human_turn == 0:
            print("AI's move now:")
            grid2,ai_score,ai_number = AI_move(player_grid, grid2, ai_grid,clicked,diag_pos,difficulty)
            
        # Update the human player's grid with the AI's move
            for row in range(N_BLOCKS):
                for col in range(N_BLOCKS):
                    if grid2[row, col] == 1:
                        #player_grid[row, col] = ai_grid[row, col]
                        eimu = 0
            human_turn = 1   # Toggle the flag value between 0 and 1
        # AI SCORE
        if ai_score >= 5 :
            AI=1
            win = True
        if ai_score>=5 and p_score>=5:
            AI=2
            win=True
        if win:
            pygame.time.delay(1000)
            end_screen(AI,ai_grid)
            
        

            
        

        # CHECKING IF GOT LETTER
        for i in clicked:
            if clicked.count(i) >= N_BLOCKS and i not in tkn_pos:
                tkn_pos.append(i)
                """
                if hover(exit_btn()):
                    #play_sound(EXIT)

                    m_menu = True
                else:
                    m_menu = False
                """

        



        pygame.display.flip()
        clock.tick(60)
    

main_menu(RANGE)