import heapq
import random
import sys
import time
from random import randrange, shuffle

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QEventLoop, QTimer

FindDelay= 120

BOTTOMWALL = 0
RIGHTWALL = 1
VISITED = 2

NORTH = 0
SOUTH = 1
WEST = 2
EAST = 3
class Cell(object):

    def __init__(self, x, y, reachable):
        """
        Initialize new cell

        @param x cell x coordinate
        @param y cell y coordinate
        @param reachable is cell reachable? not a wall?
        """
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.cost = 0
        self.distance = 0
        self.sum = 0

    def __lt__(self,other):
        return self.sum < other.sum


class Maze(object):

    def __init__(self,width,height,start,end):
        self.width=width
        self.height=height
        self.start=start
        self.end=end
        self.cells=[[Cell(x,y,False) for x in range(width)] for y in range(height)]
        #self.init_grid()
        self.stack=[]
        self.generateMaze()

    def generateMaze(self):
        self.stack.insert(0,Cell(0,0,True))
        while len(self.stack):
            next=self.stack.pop(0)
            if self.validNextNode(next):
                self.cells[next.y][next.x].reachable=True
                neighb=self.findNeighbors(next)
                self.randomlyAddNodesToStack(neighb)
        self.start = self.get_cell(self.width-1, 0)
        self.start.reachable=True
        self.end = self.get_cell(0, self.height-1)
        self.end.reachable=True
    pass

    def init_grid(self):
        for x in range(self.width):
            for y in range(self.height):
                # if (x, y) in self.walls:
                #     reachable = False
                # else:
                #     reachable = True
                self.cells.append(Cell(x, y, False))
        self.start = self.get_cell(5, 0)
        self.end = self.get_cell(0, 5)

    def get_cell(self, x, y):
        return self.cells[y][x]

    def get_adjacent_cells(self, cell):
        cells = []
        if cell.x < self.width - 1:
            cells.append(self.get_cell(cell.x + 1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y - 1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x - 1, cell.y))
        if cell.y < self.height - 1:
            cells.append(self.get_cell(cell.x, cell.y + 1))
        return cells

    def validNextNode(self, node):
        numNeighbours=0
        for y in range(node.y-1,node.y+2):
            for x in range(node.x-1,node.x+2):
                if self.pointOnGrid(x,y) \
                        and self.pointNotNode(node,x,y) \
                        and self.cells[y][x].reachable == False:
                    numNeighbours=numNeighbours+1
        return (numNeighbours>=3) and self.cells[node.y][node.x].reachable is not True

    def pointOnGrid(self, x, y):
        return x>=0 and y>= 0 and x< self.width and y< self.height

    def pointNotNode(self,node,x,y):
        return not (x==node.x and y==node.y)

    def findNeighbors(self, node):
        neighb=[]
        for y in range(node.y-1,node.y+2):
            for x in range(node.x-1,node.x+2):
                if self.pointOnGrid(x,y) and self.pointNotCorner(node,x,y) and self.pointNotNode(node,x,y):
                    neighb.append(Cell(x,y,True))
        return neighb

    def pointNotCorner(self, node, x, y):
        return x==node.x or y==node.y

    def randomlyAddNodesToStack(self, neighb):
        idx=0
        while len(neighb):
            idx= random.randint(0, len(neighb)-1)
            self.stack.insert(0,neighb.pop(idx))
        pass


class AStar(QtCore.QThread):
    updateCell = pyqtSignal(Cell, int)

    def __init__(self, maze, parent=None):
        super(AStar, self).__init__(parent)
        self.opened = []
        self.closed = set()
        heapq.heapify(self.opened)
        self.maze = maze
        self.FindDelay = FindDelay / (self.maze.width-5)

    def get_heuristic(self, cell):
        return 10 * (abs(cell.x - self.maze.end.x) + abs(cell.y - self.maze.end.y))

    def display_path(self):
        cell = self.maze.end
        while cell.parent is not self.maze.start:
            cell = cell.parent
            print('path: cell: %d,%d' % (cell.x, cell.y))
            self.updateCell.emit(cell, 2)
            loop = QEventLoop()
            QTimer.singleShot(self.FindDelay, loop.quit)
            loop.exec_()

    def update_cell(self, adj, cell):
        adj.cost = cell.cost + 10
        adj.distance = self.get_heuristic(adj)
        adj.parent = cell
        adj.sum = adj.distance + adj.cost
        if cell is not self.maze.start:
            self.updateCell.emit(cell,1)

    def process(self):
        heapq.heappush(self.opened, (self.maze.start.sum, self.maze.start))
        while len(self.opened):
            # pop cell from heap queue
            f, cell = heapq.heappop(self.opened)
            self.closed.add(cell)
            # if ending cell, finished
            if cell is self.maze.end:
                self.display_path()
                break
            adj_cells = self.maze.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.sum, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found for this adj
                        # cell.
                        if adj_cell.cost > cell.cost + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.sum, adj_cell))
            loop = QEventLoop()
            QTimer.singleShot(self.FindDelay, loop.quit)
            loop.exec_()


if __name__ == "__main__":
    star= AStar()
    star.process()
