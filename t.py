import pygame
import sys
import numpy as np
import matplotlib.pyplot as plt

# Constants
SIZE = 10  # Grid size for the rooks problem
WIDTH, HEIGHT = 800, 800
CELL_SIZE = WIDTH // SIZE
WHITE, BLACK, RED, GREEN, BLUE, GRAY = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (100, 100, 100)

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Load background music and sound effects
pygame.mixer.music.load('sounds/275673__foolboymedia__c64-melody.wav')  # Looping background music
pygame.mixer.music.play(-1)  # Start playing background music in a loop

# Sound effects
place_sound = pygame.mixer.Sound('sounds/459611__bolkmar__fx-slime-click.wav')
win_sound = pygame.mixer.Sound('sounds/342218__littlerainyseasons__good_end.mp3')
threat_sound = pygame.mixer.Sound('sounds/633248__aesterial-arts__arcade-die.wav')

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive N-rooks Game")

# Load and scale the rook image
img_happy_path = 'images/queen_happy.png'  # Update this to the path of your rook image
img_happy = pygame.image.load(img_happy_path)
img_happy = pygame.transform.scale(img_happy, (CELL_SIZE, CELL_SIZE))
img_sad_path = 'images/queen_sad.png'  # Update this to the path of your rook image
img_sad = pygame.image.load(img_sad_path)
img_sad = pygame.transform.scale(img_sad, (CELL_SIZE, CELL_SIZE))

# Board data: 0 = empty,  1 = blocked, 2 = rook
board = np.array([[0] * SIZE for _ in range(SIZE)])


# Generate N distinct colors
def generate_colors(num_colors):
    cmap = plt.get_cmap('tab20')  # Use 'tab20' or another suitable colormap
    colors = [cmap(i) for i in np.linspace(0, 1, num_colors)]
    return [(int(r*255), int(g*255), int(b*255)) for r, g, b, _ in colors]

colors = generate_colors(SIZE)
color_map = {}

def get_cell(pos):
    x, y = pos
    return x // CELL_SIZE, y // CELL_SIZE

def toggle(row, col):
    board[row][col] = (board[row][col] + 1) % 3  # Place a rook if the cell is empty

def is_threatened(row, col):
    # Check row and column
    for i in range(SIZE):
        if i != col and board[row][i] == 2:
            return True
        if i != row and board[i][col] == 2:
            return True
    return False

def sample_board():
    board.fill(0)
    row, col = np.arange(SIZE), np.random.permutation(SIZE)
    for i in range(SIZE):
        board[row[i]][col[i]] = 2

def is_solved():
    return ((board == 2).sum(axis=0) == 1).sum() == SIZE and ((board == 2).sum(axis=1) == 1).sum() == SIZE

def draw_board():
    threatened = False
    for row in range(SIZE):
        for col in range(SIZE):
            if (row, col) in color_map:
                color = color_map[(row, col)][0]
            else:
                color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if board[row][col] == 2:
                if is_threatened(row, col):
                    threatened = True
                    #pygame.draw.circle(screen, BLUE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
                    screen.blit(img_sad, (col * CELL_SIZE, row * CELL_SIZE))
                else:
                    screen.blit(img_happy, (col * CELL_SIZE, row * CELL_SIZE))
            elif board[row][col] == 1:
                pygame.draw.circle(screen, GRAY, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 8)
    # Draw borders for color clusters
    border_color = BLACK  # Color for the borders
    border_thickness = 2  # Thickness of the borders
    for row in range(SIZE):
        for col in range(SIZE):
            current_color = color_map.get((row, col), None)
            if col < SIZE - 1:  # Check right
                right_color = color_map.get((row, col + 1), None)
                if right_color != current_color:
                    pygame.draw.line(screen, border_color, (col * CELL_SIZE + CELL_SIZE, row * CELL_SIZE),
                                     (col * CELL_SIZE + CELL_SIZE, row * CELL_SIZE + CELL_SIZE), border_thickness)
            if row < SIZE - 1:  # Check down
                down_color = color_map.get((row + 1, col), None)
                if down_color != current_color:
                    pygame.draw.line(screen, border_color, (col * CELL_SIZE, row * CELL_SIZE + CELL_SIZE),
                                     (col * CELL_SIZE + CELL_SIZE, row * CELL_SIZE + CELL_SIZE), border_thickness)
    return threatened
def sample_board():
    board.fill(0)
    positions = [(i, j) for i, j in zip(np.random.permutation(SIZE), np.random.permutation(SIZE))]
    for idx, (r, c) in enumerate(positions):
        board[r][c] = 2
        # Assign colors based on nearest rook for Voronoi-like effect
        for x in range(SIZE):
            for y in range(SIZE):
                if (x, y) in color_map:
                    existing_rook = positions[color_map[(x, y)][1]]
                    if abs(x - r) + abs(y - c) < abs(x - existing_rook[0]) + abs(y - existing_rook[1]):
                        color_map[(x, y)] = (colors[idx % len(colors)], idx)
                else:
                    color_map[(x, y)] = (colors[idx % len(colors)], idx)

running = True
sample_board()  # Sample initial configuration
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            col, row = get_cell(pygame.mouse.get_pos())
            if event.button == 1:  # Left-click to place or remove a rook
                place_sound.play()
                toggle(row, col)
            if is_solved():
                win_sound.play()
                print("Congratulations! You've solved the puzzle")

    screen.fill((50, 50, 50))
    threatened = draw_board()
    if threatened:
        threat_sound.play()
    pygame.display.flip()

pygame.quit()
sys.exit()
