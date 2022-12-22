import pygame
import sys
import time
from pygame.locals import *

WIDTH = 400
HEIGHT = 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
RED_DARKER = (230, 0, 0)
GREEN_DARKER = (0, 153, 51)
BLUE_DARKER = (0, 115, 230)
FPS = 60
CLOCK = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + 100), 0, 32)
pygame.display.set_caption("My TicTacToe game 2.0: AI opponent")

x_img = pygame.image.load("img_X.png")
o_img = pygame.image.load("img_O.png")

x_img = pygame.transform.scale(x_img, (80, 80))
o_img = pygame.transform.scale(o_img, (80, 80))

# board view
# [['_', '_', '_'],
#  ['_', '_', '_'],
#  ['_', '_', '_']]
board = [['_']*3 for _ in range(3)]

step = 0  # turn step
evaluation = 0  # save score evaluation
winner = None  # check for winner
draw = None  # check for draw


def game_init():
    screen.fill(WHITE)

    pygame.draw.line(screen, BLACK, (WIDTH / 3, 0), (WIDTH / 3, HEIGHT), 7)
    pygame.draw.line(screen, BLACK, (WIDTH / 3 * 2, 0), (WIDTH / 3 * 2, HEIGHT), 7)

    pygame.draw.line(screen, BLACK, (0, HEIGHT / 3), (WIDTH, HEIGHT / 3), 7)
    pygame.draw.line(screen, BLACK, (0, HEIGHT / 3 * 2), (WIDTH, HEIGHT / 3 * 2), 7)

    game_status()


def game_status():
    global draw, step, winner

    if winner is None:
        turn_status = "AI's turn !" if step % 2 == 1 else "Yours turn !"
    else:
        turn_status = "AI is winner !" if winner == 'X' else "You're winner !"
    if draw:
        turn_status = "Game Draw !"

    font = pygame.font.Font(None, 33)
    text = font.render(turn_status, True, WHITE)

    match turn_status:
        case "You're winner !":
            text_color = GREEN_DARKER
        case "AI is winner !":
            text_color = RED_DARKER
        case "Game Draw !":
            text_color = BLUE_DARKER
        case _:
            text_color = BLACK

    screen.fill(text_color, (0, 400, 500, 100))
    text_area = text.get_rect(center=(WIDTH / 2, 500 - 50))
    screen.blit(text, text_area)

    pygame.display.update()


def check_win(depth, status):  # if status Evaluate, hence this is evaluation function for minmax algorithm
    global board, winner, draw

    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and (board[row][0] != '_'):
            if status == "Evaluate":
                return 10 - depth if board[row][0] == 'X' else depth - 10
            else:
                winner = board[row][0]
                pygame.draw.line(screen, RED, (0, (row + 1) * HEIGHT / 3 - HEIGHT / 6),  # draw red line if three in raw
                                 (WIDTH, (row + 1) * HEIGHT / 3 - HEIGHT / 6), 4)
            break

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and (board[0][col] != '_'):
            if status == "Evaluate":
                return 10 - depth if board[0][col] == 'X' else depth - 10
            else:
                winner = board[0][col]
                pygame.draw.line(screen, RED, ((col + 1) * WIDTH / 3 - WIDTH / 6, 0),
                                 ((col + 1) * WIDTH / 3 - WIDTH / 6, HEIGHT), 4)
            break

    if board[0][0] == board[1][1] == board[2][2] and (board[0][0] != '_'):
        if status == "Evaluate":
            return 10 - depth if board[0][0] == 'X' else depth - 10
        else:
            winner = board[0][0]
        pygame.draw.line(screen, RED, (50, 50), (350, 350), 4)

    if board[0][2] == board[1][1] == board[2][0] and (board[0][2] != '_'):
        if status == "Evaluate":
            return 10 - depth if board[0][2] == 'X' else depth - 10
        else:
            winner = board[0][2]
        pygame.draw.line(screen, RED, (350, 50), (50, 350), 4)

    if winner is None and step == 9:
        draw = True

    if status == "Evaluate":
        return 0

    game_status()


def insert_img(row, col):
    global board, step

    # find specific row in board to insert image
    if row == 1:
        pos_x = 30
    elif row == 2:
        pos_x = WIDTH / 3 + 30
    elif row == 3:
        pos_x = WIDTH / 3 * 2 + 30

    # find specific col in board to insert image
    if col == 1:
        pos_y = 25
    elif col == 2:
        pos_y = HEIGHT / 3 + 25
    elif col == 3:
        pos_y = HEIGHT / 3 * 2 + 25

    board[row - 1][col - 1] = 'X' if step % 2 == 1 else 'O'

    if step % 2 == 1:
        screen.blit(x_img, (pos_y, pos_x))  # pasting image of 'X' over the board cell
    else:
        screen.blit(o_img, (pos_y, pos_x))  # pasting image of 'O' over the board cell

    step += 1
    pygame.display.update()


def check_mouse_click():
    x, y = pygame.mouse.get_pos()  # get coordinates of mouse click

    # get cols from mouse click
    if x < WIDTH / 3:
        col = 1
    elif x < WIDTH / 3 * 2:
        col = 2
    elif x < WIDTH:
        col = 3
    else:
        col = None

    # get rows from mouse click
    if y < HEIGHT / 3:
        row = 1
    elif y < HEIGHT / 3 * 2:
        row = 2
    elif y < HEIGHT:
        row = 3
    else:
        row = None

    if (row is not None) and (col is not None) and board[row - 1][col - 1] == '_':
        insert_img(row, col)  # insert the image in board[row][col]
        check_win(0, "Check")


def check_endgame():  # check if game is end for minimax algorithm
    global board
    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                return True
    return False


def minimax(depth, is_max, score):  # minimax algorithm with my changes for smarter AI's behavior
    global board
    new_score = check_win(depth, "Evaluate")

    if is_max and new_score > score:
        return new_score

    if not is_max and new_score < score:
        return new_score

    if not check_endgame():
        return 0

    if is_max:
        best = -1000

        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = 'X'
                    best = max(best, minimax(depth + 1, not is_max, new_score))
                    board[i][j] = '_'
        return best

    else:
        best = 1000

        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = 'O'
                    best = min(best, minimax(depth + 1, not is_max, new_score))
                    board[i][j] = '_'
        return best


def find_best_move():  # means AI best move
    global board
    best_value = -1000
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                board[i][j] = 'X'
                score = check_win(0, "Evaluate")
                move_value = minimax(0, False, score)
                board[i][j] = '_'
                if move_value > best_value:
                    best_move = (i, j)
                    best_value = move_value
    time.sleep(0.5)  # special delay of AI's moves because of very quick minimax algorithm response
    return best_move


def reset_game():
    global board, winner, step, evaluation, draw
    time.sleep(3)
    step = 0
    evaluation = 0
    draw = False
    winner = None
    board = [['_'] * 3 for _ in range(3)]
    game_init()


game_init()
while True:
    if step % 2 == 0:  # Player's turn
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                check_mouse_click()

                if winner or draw:
                    reset_game()

    else:  # AI's turn
        best_ai_move = find_best_move()
        insert_img(best_ai_move[0]+1, best_ai_move[1]+1)  # insert the image in board[row][col]
        check_win(0, "Check")

        if winner or draw:
            reset_game()

    pygame.display.update()
    CLOCK.tick(FPS)
