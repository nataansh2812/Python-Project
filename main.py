import pygame
from queue import PriorityQueue

# Initialize pygame
pygame.init()

# Window size
WIDTH = 600
HEIGHT = 600

# Create window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding Simulation")

# Grid settings
ROWS = 20
COLS = 20
CELL_SIZE = WIDTH // COLS   # Size of each cell

# Colors (Pastel Theme)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PASTEL_GREEN = (119, 221, 119)   # Start node
PASTEL_RED = (255, 105, 97)      # End node
PASTEL_GRAY = (200, 200, 200)    # Obstacles
PASTEL_BLUE = (174, 198, 207)    # Final path
PASTEL_YELLOW = (255, 255, 186)  # Exploring nodes

# Create grid (2D list)
# 0 = empty, 1 = obstacle, 2 = path, 3 = exploring
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Start and End points
start = None
end = None


# 🔹 Function to draw everything on screen
def draw():
    win.fill(WHITE)  # Clear screen

    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            # Draw based on cell type
            if grid[row][col] == 1:
                pygame.draw.rect(win, PASTEL_GRAY, rect)  # Obstacle
            elif grid[row][col] == 2:
                pygame.draw.rect(win, PASTEL_BLUE, rect)  # Path
            elif grid[row][col] == 3:
                pygame.draw.rect(win, PASTEL_YELLOW, rect)  # Exploring
            elif (row, col) == start:
                pygame.draw.rect(win, PASTEL_GREEN, rect)  # Start
            elif (row, col) == end:
                pygame.draw.rect(win, PASTEL_RED, rect)  # End

            # Draw grid lines
            pygame.draw.rect(win, BLACK, rect, 1)

    pygame.display.update()  # Refresh screen


# 🔹 Heuristic function (Manhattan distance)
# Used in A* Algorithm to estimate distance to goal
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# 🔹 Get valid neighbors (up, down, left, right)
def get_neighbors(node):
    row, col = node
    neighbors = []

    for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        r, c = row + d[0], col + d[1]

        # Check boundaries and avoid obstacles
        if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c] != 1:
            neighbors.append((r, c))

    return neighbors


# 🔹 A* Pathfinding Algorithm
def a_star():
    open_set = PriorityQueue()
    open_set.put((0, start))  # Add start node

    came_from = {}  # To reconstruct path

    # Distance from start
    g_score = {(r, c): float("inf") for r in range(ROWS) for c in range(COLS)}
    g_score[start] = 0

    # Estimated total cost
    f_score = {(r, c): float("inf") for r in range(ROWS) for c in range(COLS)}
    f_score[start] = heuristic(start, end)

    # Main loop
    while not open_set.empty():

        # Allow window to close during execution
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[1]  # Get node with lowest f_score

        # Mark node as exploring (yellow)
        if current != start:
            grid[current[0]][current[1]] = 3

        draw()
        pygame.time.delay(30)

        # If reached destination
        if current == end:
            path = []

            # Backtrack to find path
            while current in came_from:
                path.append(current)
                current = came_from[current]

            path.reverse()

            # Draw final path (blue)
            for node in path:
                if node != start and node != end:
                    grid[node[0]][node[1]] = 2
                    draw()
                    pygame.time.delay(50)

            # Simulate car movement
            for node in path:
                draw()
                pygame.draw.circle(
                    win,
                    (0, 0, 0),
                    (node[1] * CELL_SIZE + CELL_SIZE // 2,
                     node[0] * CELL_SIZE + CELL_SIZE // 2),
                    CELL_SIZE // 3
                )
                pygame.display.update()
                pygame.time.delay(100)

            return

        # Check neighbors
        for neighbor in get_neighbors(current):
            temp_g = g_score[current] + 1

            # If better path found
            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + heuristic(neighbor, end)
                open_set.put((f_score[neighbor], neighbor))

    # If no path found
    print("No Path Found")
    pygame.display.set_caption("No Path Found!")
    pygame.time.delay(2000)


# 🔹 Convert mouse click position to grid coordinates
def get_clicked_pos(pos):
    x, y = pos
    return y // CELL_SIZE, x // CELL_SIZE


# 🔁 Main loop
running = True
while running:
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Left click → set start, end, obstacles
        if pygame.mouse.get_pressed()[0]:
            row, col = get_clicked_pos(pygame.mouse.get_pos())

            if not start:
                start = (row, col)
            elif not end:
                end = (row, col)
            else:
                grid[row][col] = 1  # obstacle

        # Right click → remove/reset
        elif pygame.mouse.get_pressed()[2]:
            row, col = get_clicked_pos(pygame.mouse.get_pos())
            grid[row][col] = 0

            if (row, col) == start:
                start = None
            elif (row, col) == end:
                end = None

        # Press SPACE to run A*
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start and end:
                a_star()

pygame.quit()