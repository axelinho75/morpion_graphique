import pygame
import sys
import time


pygame.init()
font = pygame.font.Font(None, 36)

WINDOW_SIZE = (600, 600)

screen = pygame.display.set_mode(WINDOW_SIZE)

CELL_SIZE = 200

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

board = [[' ' for _ in range(3)] for _ in range(3)]

current_player = 'X'

def draw_board():
    for x in range(0, WINDOW_SIZE[0], CELL_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, WINDOW_SIZE[1]), 3)
    for y in range(0, WINDOW_SIZE[1], CELL_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WINDOW_SIZE[0], y), 3)

    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell == 'O': 
                position = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
                pygame.draw.circle(screen, WHITE if cell == 'X' else BLACK, position, CELL_SIZE // 3, 3)
            elif cell == 'X':
                pygame.draw.line(screen, WHITE, (x * CELL_SIZE + 50, y * CELL_SIZE + 50), (x * CELL_SIZE + CELL_SIZE - 50, y * CELL_SIZE + CELL_SIZE - 50), 3)
                pygame.draw.line(screen, WHITE, (x * CELL_SIZE + 50, y * CELL_SIZE + CELL_SIZE - 50), (x * CELL_SIZE + CELL_SIZE - 50, y * CELL_SIZE + 50), 3)
           
def choose_mode():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2
        screen.fill(RED)
        text = font.render("Appuyez sur 1 pour un joueur, 2 pour deux joueurs", True, WHITE)
        screen.blit(text, (WINDOW_SIZE[0] // 2 - text.get_width() // 2, WINDOW_SIZE[1] // 2 - text.get_height() // 2))
        pygame.display.update()


def handle_click(pos):
    global current_player
    x, y = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
    if board[y][x] == ' ':
        board[y][x] = current_player
        draw_board()
    if check_win():
        text = font.render("Le joueur " + current_player + " a gagné! Appuyez sur R pour relancer", True, WHITE)
        screen.blit(text, (WINDOW_SIZE[0] // 2 - text.get_width() // 2, WINDOW_SIZE[1] // 2 - text.get_height() // 2))
        pygame.display.update()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()
                return
    current_player = 'O' if current_player == 'X' else 'X'
    if mode == 1 and current_player == 'O':
        make_computer_move()


def make_computer_move():
    global current_player
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = current_player
                draw_board()
                if check_win():
                    text = font.render("L'ordinateur a gagné! Appuyez sur R pour relancer", True, WHITE)
                    screen.blit(text, (WINDOW_SIZE[0] // 2 - text.get_width() // 2, WINDOW_SIZE[1] // 2 - text.get_height() // 2))
                    pygame.display.update()
                    wait_for_restart()
                    reset_game()
                    return
                current_player = 'O' if current_player == 'X' else 'X'
                return

def check_win():
    for row in board:
        if row.count(row[0]) == len(row) and row[0] != ' ':
            return True
    for col in range(len(board[0])):
        check = []
        for row in board:
            check.append(row[col])
        if check.count(check[0]) == len(check) and check[0] != ' ':
            return True
    
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return True
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return True
    return False


def reset_game():
    global board, current_player
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'

def wait_for_restart():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return



def game():
    global mode
    mode = choose_mode()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_click(pygame.mouse.get_pos())
        screen.fill(RED)
        draw_board()
        if all(cell != ' ' for row in board for cell in row) and not check_win():
            text = font.render("Match nul! Appuyez sur R pour relancer", True, WHITE)
            screen.blit(text, (WINDOW_SIZE[0] // 2 - text.get_width() // 2, WINDOW_SIZE[1] // 2 - text.get_height() // 2))
            pygame.display.update()
            wait_for_restart()
            reset_game()
        pygame.display.update()

game()
