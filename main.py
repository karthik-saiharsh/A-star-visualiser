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
    def __init__(self, row, col, size, total_rows, enable_diagonal_paths=False):
        self.row = row
        self.col = col
        self.x = col * size
        self.y = row * size
        self.color = Colors().neutral
        self.size = size
        self.total_rows = total_rows
        self.neighbours = []
        self.enable_diagonal_paths = enable_diagonal_paths

    # Returns position of node
    def get_pos(self):
        return self.row, self.col
    

    #Methods to get state of node
    def is_explored(self):
        return self.color == Colors().explored
    
    def is_inactive(self):
        return self.color == Colors().inactive
    
    def is_being_explored(self):
        return self.color == Colors().exploring
    
    def is_start(self):
        return self.color == Colors().start
    
    def is_end(self):
        return self.color == Colors().end
    
    # Methods to set state of Node
    def set_explored(self):
        self.color = Colors().explored
    
    def set_inactive(self):
        self.color = Colors().inactive
    
    def set_being_explored(self):
        self.color = Colors().exploring
    
    def set_start(self):
        self.color = Colors().start
    
    def set_end(self):
        self.color = Colors().end

    def reset(self):
        self.color = Colors().neutral

    
    # Additional methods
    def draw(self, win):
        # draw node on screen
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

    def determine_neighbours(self, grid):
        if self.col > 0 and not grid[self.row][self.col-1].is_inactive():
            self.neighbours.append(grid[self.row][self.col-1])

        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_inactive():
            self.neighbours.append(grid[self.row][self.col+1])

        if self.row > 0 and not grid[self.row-1][self.col].is_inactive():
            self.neighbours.append(grid[self.row-1][self.col])

        if self.row < self.total_rows-1 and not grid[self.col+1][self.col].is_inactive():
            self.neighbours.append(grid[self.col+1][self.col])

        if self.enable_diagonal_paths:
            if self.row > 0 and self.col > 0 and not grid[self.row-1][self.col-1].is_inactive():
                self.neighbours.append(grid[self.row-1][self.col-1])

            if self.row > 0 and self.col < self.total_rows and not grid[self.row-1][self.col+1].is_inactive():
                self.neighbours.append(grid[self.row-1][self.col+1])

            if self.row < self.total_rows and self.col > 0 and not grid[self.row+1][self.col-1].is_inactive():
                self.neighbours.append(grid[self.row+1][self.col-1])

            if self.row < self.total_rows and self.col < self.total_rows and not grid[self.row+1][self.col+1].is_inactive():
                self.neighbours.append(grid[self.row+1][self.col+1])



####### Visualisor class #######
class Visualizer():
    def __init__(self, size, rows, enable_diagonal_paths=False):

        # Verify that the dimentions of the window are in proper ration
        if int(str(size/rows)[str(size/rows).find(".")+1:]) != 0:
            print("The window size must be divisible by the number of rows")
            exit(1)

        self.enable_diagonal_paths = enable_diagonal_paths
        self.size = size
        self.rows = rows
        self.win = pygame.display.set_mode((size, size))

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
        pygame.quit()


    def heuristic_function(self, pos1, pos2, alternate=None):
        # Heuristic function for A*
        # Default heuristic is just the eucledian distance between 2 points
        if alternate is not None:
            return alternate(pos1, pos2)
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
                node = Node(i, j, gap, self.rows, self.enable_diagonal_paths)
                grid[i].append(node)

        return grid
    

if __name__ == "__main__":
    vis = Visualizer(1300, 20)