import pygame
import sys
import time
from tic_tac_env import EphemeralTicTacToeEnv

WIDTH, HEIGHT = 600, 720
GRID_SIZE = 3
CELL_SIZE = WIDTH // GRID_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
PLAYER1_COLOR = (100, 149, 237)
PLAYER2_COLOR = (255, 99, 71)

IMGFILEPATH = {
    'X': '/Users/someshb/Downloads/eTTT/X.png',
    'O': '/Users/someshb/Downloads/eTTT/O.png',
    'background': '/Users/someshb/Downloads/eTTT/board.png'
}

try:
    X_IMG = pygame.image.load(IMGFILEPATH['X']) if IMGFILEPATH['X'] else None
    O_IMG = pygame.image.load(IMGFILEPATH['O']) if IMGFILEPATH['O'] else None
    BG_IMG = pygame.image.load(IMGFILEPATH['background']) if IMGFILEPATH['background'] else None
except pygame.error:
    X_IMG, O_IMG, BG_IMG = None, None, None

if X_IMG: X_IMG = pygame.transform.scale(X_IMG, (CELL_SIZE // 2, CELL_SIZE // 2))
if O_IMG: O_IMG = pygame.transform.scale(O_IMG, (CELL_SIZE // 2, CELL_SIZE // 2))
if BG_IMG: BG_IMG = pygame.transform.scale(BG_IMG, (WIDTH, WIDTH))

game_ended = False
action_results = [None, None, None]
fps = 60
sleeptime = 1.0
clock = None
screen = None

game = EphemeralTicTacToeEnv()

def setup(GUI=True):
    global screen, clock
    if GUI:
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Ephemeral Tic-Tac-Toe Visualization")
        clock = pygame.time.Clock()

def position_to_grid(position):
    row, col = position
    return col * CELL_SIZE, row * CELL_SIZE

def draw_grid():
    screen.fill(BLACK)
    if BG_IMG:
        screen.blit(BG_IMG, (0, 0))
    else:
        pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, WIDTH))
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, WIDTH, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)
    pygame.draw.rect(screen, GRAY, (0, WIDTH, WIDTH, HEIGHT - WIDTH))

def draw_symbols():
    board, ages, _, owners = game.game.get_state()
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x, y = position_to_grid((row, col))
            center_x, center_y = x + CELL_SIZE // 2, y + CELL_SIZE // 2
            if board[row][col] == 'X':
                if X_IMG:
                    screen.blit(X_IMG, (center_x - CELL_SIZE // 4, center_y - CELL_SIZE // 4))
                else:
                    pygame.draw.line(screen, PLAYER1_COLOR, (x + 40, y + 40), (x + CELL_SIZE - 40, y + CELL_SIZE - 40), 10)
                    pygame.draw.line(screen, PLAYER1_COLOR, (x + CELL_SIZE - 40, y + 40), (x + 40, y + CELL_SIZE - 40), 10)
            elif board[row][col] == 'O':
                if O_IMG:
                    screen.blit(O_IMG, (center_x - CELL_SIZE // 4, center_y - CELL_SIZE // 4))
                else:
                    pygame.draw.circle(screen, PLAYER2_COLOR, (center_x, center_y), CELL_SIZE // 3, 10)
            
            if board[row][col] is not None:
                lifespan = game.game.lifespan_x if owners[row][col] == 'X' else game.game.lifespan_o
                remaining_life = lifespan - ages[row][col]
                for i in range(lifespan):
                    circle_pos = (x + 10 + i * 15, y + 20)
                    color = WHITE if i < remaining_life else DARK_GRAY
                    pygame.draw.circle(screen, color, circle_pos, 6, 0 if i < remaining_life else 2)

def display_end_message(message):
    font = pygame.font.Font(None, 100)
    text_surface = font.render(message, True, DARK_GRAY)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, WIDTH // 2))
    screen.blit(text_surface, text_rect)

def refresh(obs, reward, done, info, delay=1.0):
    global game_ended, action_results
    action = info.get('action', f"({divmod(info['action'], GRID_SIZE)})")
    prev_player = 'O' if game.game.current_player == 'X' else 'X'
    result = f"Player {prev_player} moved to {action}, Reward: {reward}"
    if None in action_results:
        action_results[action_results.index(None)] = result
    else:
        action_results.pop(0)
        action_results.append(result)

    draw_grid()
    draw_symbols()
    if done:
        game_ended = True
        end_message = "X Wins!" if reward == 1 and prev_player == 'X' else "O Wins!" if reward == 1 else "Draw!"
        display_end_message(end_message)

    font = pygame.font.Font(None, 30)
    console_surface = font.render("Actions", True, BLACK)
    screen.blit(console_surface, (10, WIDTH + 10))
    font = pygame.font.Font(None, 24)
    y_offset = WIDTH + 40
    for result in action_results:
        if result:
            result_surface = font.render(result, True, BLACK)
            screen.blit(result_surface, (10, y_offset))
            y_offset += 30

    pygame.display.flip()
    clock.tick(fps)
    time.sleep(delay)

def main():
    global game_ended, action_results
    running = True
    state = game.reset()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_ended:
                x, y = event.pos
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                    action = row * GRID_SIZE + col
                    if action in game.get_legal_actions():
                        prev_player = game.game.current_player
                        state, reward, done, info = game.step(action)
                        action_results.append(f"Player {prev_player} moved to ({row}, {col}), Reward: {reward}")
                        if done:
                            game_ended = True
                            end_message = "X Wins!" if reward == 1 and prev_player == 'X' else "O Wins!" if reward == 1 else "Draw!"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                state = game.reset()
                game_ended = False
                action_results = [None, None, None]

        draw_grid()
        draw_symbols()
        if game_ended:
            display_end_message(end_message)

        font = pygame.font.Font(None, 30)
        console_surface = font.render("Actions", True, BLACK)
        screen.blit(console_surface, (10, WIDTH + 10))
        font = pygame.font.Font(None, 24)
        y_offset = WIDTH + 40
        for result in action_results[-3:]:
            if result:
                result_surface = font.render(result, True, BLACK)
                screen.blit(result_surface, (10, y_offset))
                y_offset += 30

        pygame.display.flip()
        clock.tick(fps)
        time.sleep(sleeptime)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    setup()
    main()