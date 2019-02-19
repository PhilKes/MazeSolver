# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\Programme\PythonProjects\MazeSolver\mazeUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QInputDialog, \
    QDesktopWidget

from MazeSolverA import AStar, Cell, Maze

tileSize=56

class Ui_MainWindow(QObject):
    updateUI=pyqtSignal(Cell,int)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.vLayout = QVBoxLayout(self.centralwidget)
        self.hLayout = QHBoxLayout()
        # self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        # self.gridLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 531, 411))
        # self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        MainWindow.setCentralWidget(self.centralwidget)

        # center the grid with stretch on both sides
        self.hLayout.addStretch(1)
        self.hLayout.addLayout(self.gridLayout)
        self.hLayout.addStretch(1)

        self.vLayout.addLayout(self.hLayout)
        # push grid to the top of the window
        self.vLayout.addStretch(1)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 528, 21))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.menuMenu.addAction("New...",self.showNewMazeDialog)
        
    def showNewMazeDialog(self):
        i, okPressed = QInputDialog.getInt(QInputDialog(), "Width of Maze", "Width: ", 10, 6, 60, 1)
        if okPressed:
            width=i
            i, okPressed = QInputDialog.getInt(QInputDialog(), "Height of Maze", "Height: ", 10, 0, 60, 1)
            if okPressed:
                height=i
                self.newMaze(width,height)
    pass

    def newMaze(self,width=10,height=10):
        walls = ((5, 1), (4, 1), (2, 2), (3, 3), (4, 3),
                 (4, 4), (4, 5), (0, 0), (0, 1), (0, 3), (1, 4))
        self.maze = Maze(width, height, (width-1, 0), (0, height-1))
        #self.maze=MazeGenerator.make_maze(10,10)
        self.solver = AStar(self.maze)
        c=(width/70)
        size=tileSize*(1-c)
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)

        for x in range(height):                      # INIT MAZE
            for y in range(width):
                cell=self.maze.get_cell(x,y)
                if not cell.reachable:
                    col=QColor(0, 0, 0)
                else:
                    col=QColor(255, 255, 255)
                text=QTextEdit()
                text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                text.setFixedSize(size,size)
                #text.setText(str(cell.x)+","+str(cell.y))
                text.setStyleSheet("background-color: rgb("+str(col.red())+","+str(col.green())+","+str(col.blue())+");")
                self.gridLayout.addWidget(text,*(x, y))

        self.setCell(self.maze.start,3)         #HIGHLIGHT START / END
        self.setCell(self.maze.end,4)
        self.setText(self.maze.start,"START\n"+str(self.maze.start.x)+","+str(self.maze.start.y))
        self.setText(self.maze.end, "END\n" + str(self.maze.end.x) + "," + str(self.maze.end.y))
        self.solver.updateCell.connect(self.setCell)
        MainWindow.setFixedSize(self.gridLayout.sizeHint())
        sg = QDesktopWidget().screenGeometry()
        MainWindow.move(sg.width()/2-(self.maze.width*size)/2,sg.height()/2-(self.maze.height*size)/1.8)
        self.solver.process()

    def setText(self,cell,txt):
        text = self.gridLayout.itemAt(cell.x * self.maze.height + cell.y).widget()
        text.setText(txt)

    @pyqtSlot(Cell,int)
    def setCell(self, cell, type):
        text = self.gridLayout.itemAt(cell.x * self.maze.height + cell.y).widget()
        if type == 1:                  #PROCESSED
            col = QColor(255, 0, 0)
        elif type ==2:                 #FINAL PATH
            col = QColor(0, 255, 0)
        elif type == 3:                #START
            col = QColor(255, 255, 0)
        else:                          #END
            col = QColor(255, 255, 0)
        text.setStyleSheet(
            "background-color: rgb("+str(col.red())+","+str(col.green())+","+str(col.blue())+");")
        #text.setText(str(cell.sum)+"\nC: "+str(cell.cost)+"\nD: "+str(cell.distance))


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

