import pygame as pg
import time

WIDTH = 600
WINDOW = pg.display.set_mode((WIDTH, WIDTH))
pg.display.set_caption("Path Finding Agents_L.Akpanke")

# define colours that we will use throughout
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
PINK = (255, 192, 203)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)


class Node:
    def __init__(self, row, col, width, num_rows):
        self.row = row
        self.col = col
        # to keep track of the co-ordinate position on my screen
        self.x = row * width
        self.y = col * width
        self.colour = WHITE
        self.neighbours = []
        self.width = width
        self.num_rows = num_rows

    def current_position(self):
        return self.row, self.col

    # Once a node is explored it should then become grey.
    def explored(self):
        return self.colour == GREY

    def open_set(self):
        return self.colour == LIGHT_BLUE

    def obstacle(self):
        return self.colour == BLACK

    def start(self):
        return self.colour == PINK

    def exit(self):
        return self.colour == LIGHT_GREEN

    def clear(self):
        self.colour = WHITE

    def make_explored(self):
        self.colour = GREY

    def make_open_set(self):
        self.colour = LIGHT_BLUE

    def make_obstacle(self):
        self.colour = BLACK

    def make_start(self):
        self.colour = PINK

    def make_exit(self):
        self.colour = LIGHT_GREEN

    def make_path(self):
        self.colour = PINK

    def draw(self, WINDOW):
        pg.draw.rect(WINDOW, self.colour, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        # Check if neighbours are barriers or not
        self.neighbours = []
        if self.row < self.num_rows - 1 and not grid[self.row + 1][self.col].obstacle():  # Down
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].obstacle():  # Up
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.num_rows - 1 and not grid[self.row][self.col + 1].obstacle():  # Right
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].obstacle():  # Left
            self.neighbours.append(grid[self.row][self.col - 1])

    def __lt__(self, other):  # lt is less than used to compare two spots
        return False


def heuristic_func(pos1, pos2):  # coordinate values to discover the distance between point one and point two using Manhattan distance
    x1, y1 = pos1
    x2, y2 = pos2
    distance = abs(x1 - x2) + abs(y1 - y2)
    return distance


def reconstruct_path(prev, current, draw):
    while current in prev:
        current = prev[current]
        current.make_path()
        draw()


def dijkstra_Algo(draw, grid, start, end):
    open_set = [start]
    previous = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    while open_set:
        open_set.sort(key=lambda node: g_score[node])  # Custom sorting based on g_score
        current_node = open_set.pop(0)

        if current_node == end:
            reconstruct_path(previous, end, draw)
            end.make_exit()
            return True

        for neighbour in current_node.neighbours:
            temporary_g_score = g_score[current_node] + 1

            if temporary_g_score < g_score[neighbour]:
                previous[neighbour] = current_node
                g_score[neighbour] = temporary_g_score
                if neighbour not in open_set:
                    open_set.append(neighbour)
                    neighbour.make_open_set()
        draw()

        if current_node != start:
            current_node.make_explored()

    return False


def a_StarAlgo(draw, grid, start, end):
    open_set = [start]
    previous = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic_func(start.current_position(), end.current_position())

    while open_set:
        open_set.sort(key=lambda node: f_score[node])  # Custom sorting based on f_score
        current_node = open_set.pop(0)

        if current_node == end:
            reconstruct_path(previous, end, draw)
            end.make_exit()
            return True

        for neighbour in current_node.neighbours:
            temporary_g_score = g_score[current_node] + 1

            if temporary_g_score < g_score[neighbour]:
                previous[neighbour] = current_node
                g_score[neighbour] = temporary_g_score
                f_score[neighbour] = temporary_g_score + heuristic_func(neighbour.current_position(),
                                                                        end.current_position())
                if neighbour not in open_set:
                    open_set.append(neighbour)
                    neighbour.make_open_set()
        draw()

        if current_node != start:
            current_node.make_explored()

    return False


# create data structure to hold all nodes
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            new_node = Node(i, j, gap, rows)
            grid[i].append(new_node)
    return grid


# now we have to draw the grid
def draw_grid(WINDOW, rows, width):
    gap = width // rows
    # for every row we draw a horizontal line
    for i in range(rows):
        pg.draw.line(WINDOW, BLACK, (0, i * gap), (width, i * gap))
        # for every column we draw a vertical line
        for j in range(rows):
            pg.draw.line(WINDOW, BLACK, (j * gap, 0), (j * gap, width))


def draw_everything(WINDOW, grid, rows, width):
    WINDOW.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(WINDOW)

    draw_grid(WINDOW, rows, width)
    pg.display.update()


# lets get the mouse position to figure out what node we click on
def get_Mouseposition(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(WINDOW, width):
    ROWS = 20
    grid = make_grid(ROWS, width)

    start = None
    end = None
    started = False  # Initialize started variable

    run = True

    while run:
        draw_everything(WINDOW, grid, ROWS, width)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            # check what nodes in the grid have been clicked
            # if we clicked the left button
            if pg.mouse.get_pressed()[0]:
                pos = pg.mouse.get_pos()  # x,y coordinate of mouse when clicked
                row, col = get_Mouseposition(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_exit()
                elif node != end and node != start:
                    node.make_obstacle()
            # if we clicked the right button
            elif pg.mouse.get_pressed()[2]:
                pos = pg.mouse.get_pos()  # x,y coordinate of mouse when clicked
                row, col = get_Mouseposition(pos, ROWS, width)
                node = grid[row][col]
                node.clear()
                if node == start:
                    start = None
                elif node == end:
                    end = None
            # SPACE BAR TO RUN ALGORITHM
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not started and end:
                    started = True
                    starting_time=time.time()
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    # the lambda anonymous function helps us pass the function 'draw_everything' as a variable
                    a_StarAlgo(lambda: draw_everything(WINDOW, grid, ROWS, width), grid, start, end)
                    #dijkstra_Algo(lambda: draw_everything(WINDOW, grid, ROWS, width), grid, start, end) 0.5583
                    ending_time=time.time()
                    time_taken=ending_time-starting_time
                    print(f'The agent took {time_taken:.4} seconds')
                if event.key == pg.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pg.quit()


main(WINDOW, WIDTH)
