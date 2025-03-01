#### Imports ####
import pygame
import math
from queue import PriorityQueue


####### COLORS #######
class Colors():
    def __init__(self):
        self.neutral = (255, 247, 243)
        self.explored = (33, 53, 85)
        self.exploring = (62, 88, 121)
        self.inactive = (42, 51, 53)
        self.path = (250, 208, 196)
####### COLORS #######


class Node():
    def __init__(self, row, col, size, total_rows):
        self.row = row
        self.col = col
        self.x = col * size
        self.y = row * size
        self.color = Colors().neutral
        self.size = size
        self.total_rows = total_rows
        
    

