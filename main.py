#### Imports ####
import pygame
from math import sqrt
from queue import PriorityQueue
from sys import exit
####### COLORS #######
class Colors():
    def __init__(self):
        self.neutral = (255, 247, 243)
        self.explored = (33, 53, 85)
        self.exploring = (62, 88, 121)
        self.inactive = (42, 51, 53)
        self.path = (250, 208, 196)
        self.end = (239, 182, 200)
        self.start = (239, 182, 200)
####### COLORS #######


####### NODE CLASS #######
class Node():
    def __init__(self, row, col, size, total_rows, Colors, enable_diagonal_paths=False):
        self.colors = Colors
        self.row = row
        self.col = col
        self.x = col * size
        self.y = row * size
        self.color = self.colors.neutral
        self.size = size
        self.total_rows = total_rows
        self.neighbours = []
        self.enable_diagonal_paths = enable_diagonal_paths

    # Returns position of node
    def get_pos(self):
        return self.row, self.col
    

    #Methods to get state of node
    def is_explored(self):
        return self.color == self.colors.explored
    
    def is_inactive(self):
        return self.color == self.colors.inactive
    
    def is_being_explored(self):
        return self.color == self.colors.exploring
    
    def is_start(self):
        return self.color == self.colors.start
    
    def is_end(self):
        return self.color == self.colors.end
    
    # Methods to set state of Node
    def set_explored(self):
        self.color = self.colors.explored
    
    def set_inactive(self):
        self.color = self.colors.inactive
    
    def set_being_explored(self):
        self.color = self.colors.exploring
    
    def set_start(self):
        self.color = self.colors.start
    
    def set_end(self):
        self.color = self.colors.end

    def set_path(self):
        self.color = self.colors.path

    def reset(self):
        self.color = self.colors.neutral

    
    # Additional methods
    def draw(self, win):
        # draw node on screen
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

    def determine_neighbours(self, grid):
        # Left Neighbour
        if self.col > 0 and not grid[self.row][self.col-1].is_inactive():
            self.neighbours.append(grid[self.row][self.col-1])

        # Right neighbour
        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_inactive():
            self.neighbours.append(grid[self.row][self.col+1])

        # Top neighbour
        if self.row > 0 and not grid[self.row-1][self.col].is_inactive():
            self.neighbours.append(grid[self.row-1][self.col])

        # Bottom Neighbour
        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_inactive():
            self.neighbours.append(grid[self.row+1][self.col])

        if self.enable_diagonal_paths:
            if self.row > 0 and self.col > 0 and not grid[self.row-1][self.col-1].is_inactive():
                self.neighbours.append(grid[self.row-1][self.col-1])

            if self.row > 0 and self.col < self.total_rows-1 and not grid[self.row-1][self.col+1].is_inactive():
                self.neighbours.append(grid[self.row-1][self.col+1])

            if self.row < self.total_rows-1 and self.col > 0 and not grid[self.row+1][self.col-1].is_inactive():
                self.neighbours.append(grid[self.row+1][self.col-1])

            if self.row < self.total_rows-1 and self.col < self.total_rows-1 and not grid[self.row+1][self.col+1].is_inactive():
                self.neighbours.append(grid[self.row+1][self.col+1])



####### Visualisor class #######
class Visualizer():
    def __init__(self, size, rows, Colors, enable_diagonal_paths=False):
        self.colors = Colors
        # Verify that the dimentions of the window are in proper ration
        assert size % rows == 0, "The window size must be divisible by the number of rows"

        self.enable_diagonal_paths = enable_diagonal_paths
        self.size = size
        self.rows = rows
        self.win = pygame.display.set_mode((size, size))

        # A custom heurisic function can be passed here
        self.heuristic = None

        pygame.display.set_caption("PathFinding algorithm vizualiser")


        start_node = None
        end_node = None
        is_running = True
        started_algorithm = False

        grid = self.make_grid()

        # Make the border edges as inactive
        for row in grid:
            for node in row:
                row, col = node.get_pos()
                if row in [0, self.rows-1] or col in [0, self.rows-1]:
                    node.set_inactive()

        while is_running:
            self.draw(grid)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                if started_algorithm: continue

                if pygame.mouse.get_pressed()[0]:
                    click_pos = pygame.mouse.get_pos()
                    row, col = self.get_click_pos(click_pos)
                    node = grid[row][col]

                    if start_node == None:
                        start_node = node
                        start_node.set_start()

                    elif end_node == None and node != start_node:
                        end_node = node
                        end_node.set_end()

                    elif node != start_node and node != end_node:
                        node.set_inactive()

                elif pygame.mouse.get_pressed()[2]:
                    click_pos = pygame.mouse.get_pos()
                    row, col = self.get_click_pos(click_pos)
                    node = grid[row][col]
                    node.reset()

                    if node == start_node:
                        start_node = None
                    if node == end_node:
                        end_node = None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not started_algorithm:
                        for row in grid:
                            for node in row:
                                node.determine_neighbours(grid)
                        self.run_algorithm(grid, start_node, end_node)
        pygame.quit()


    def heuristic_function(self, pos1, pos2):
        # Heuristic function for A*
        # Default heuristic is just the eucledian distance between 2 points
        if self.heuristic != None:
            return self.heuristic(pos1, pos2)
        x1, y1 = pos1
        x2, y2 = pos2
        return sqrt((x2-x1)**2 + (y2-y1)**2)
    

    def draw_grid(self, grid):
        # Draw grid lines between nodes
        space_per_row = self.size // self.rows

        for i in range(self.rows):
            pygame.draw.line(self.win, (0, 0, 0), (0, i*space_per_row), (self.size, i*space_per_row))
            for j in range(self.rows):
                pygame.draw.line(self.win, (0, 0, 0), (j*space_per_row, 0), (j*space_per_row, self.size))


    # Draw nodes
    def draw(self, grid):
        self.win.fill((255,255,255));

        for row in grid:
            for node in row:
                node.draw(self.win)

        self.draw_grid(grid)
        pygame.display.update()

    # get the position(row, col) where mouse click happens
    def get_click_pos(self, pos):
        gap = self.size // self.rows
        x, y = pos
        row = y // gap
        col = x // gap

        return row, col
    
    def make_grid(self):
        grid = []
        gap = self.size // self.rows

        for i in range(self.rows):
            grid.append([])
            for j in range(self.rows):
                node = Node(i, j, gap, self.rows, self.colors, self.enable_diagonal_paths)
                grid[i].append(node)

        return grid

    # A* Algorithm
    def run_algorithm(self, grid, start, end):
        count = 0

        processing_vertices = PriorityQueue()
        processing_vertices.put((0, count, start))

        processing = {start}

        parent = {}

        # Keep track of distances to each node
        g_dist = {node: float('inf') for row in grid for node in row}
        f_dist = {node: float('inf') for row in grid for node in row}

        g_dist[start] = 0
        f_dist[start] = self.heuristic_function(start.get_pos(), end.get_pos())

        while not processing_vertices.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = processing_vertices.get()[2]
            processing.remove(current)

            if current == end:
                self.draw_path(parent, end, start, end, grid)
                return True

            for neighbour in current.neighbours:
                temp_g_value = g_dist[current] + 1

                if temp_g_value + self.heuristic_function(current.get_pos(), end.get_pos()) < f_dist[neighbour]:
                    parent[neighbour] = current
                    g_dist[neighbour] = temp_g_value
                    f_dist[neighbour] = temp_g_value + self.heuristic_function(neighbour.get_pos(), end.get_pos())

                    if neighbour not in processing:
                        count += 1
                        processing_vertices.put((f_dist[neighbour], count, neighbour))
                        processing.add(neighbour)
                        neighbour.set_being_explored()
            
            self.draw(grid)

            if current != start:
                current.set_explored()
        return False

    def draw_path(self, parents, current, start, end, grid):
        while current in parents and current != start:
            current = parents[current]
            current.set_path()
            self.draw(grid)
        start.set_start()
        end.set_end()
        self.draw(grid)
    

if __name__ == "__main__":
    col = Colors()
    vis = Visualizer(1500, 30, col, False)
