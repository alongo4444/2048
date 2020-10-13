import Board
from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QFileDialog
from win32api import GetSystemMetrics
import ctypes
import sys
import Settings



class Game(QMainWindow):
    def __init__(self, board_size, parent=None):
        super(Game, self).__init__(parent)
        self.setWindowTitle('2048')
        self.board_size = board_size
        self.board = Board.Board(self.board_size)
        self.tiles = [[0] * self.board_size for i in range(self.board_size)]
        self.setGeometry(GetSystemMetrics(0) / 2 - 60 * self.board_size / 2,
                         GetSystemMetrics(1) / 2 - 60 * self.board_size / 2, 60 * self.board_size, 60 * self.board_size + 21)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuGame = QtWidgets.QMenu(self.menubar)
        self.menuGame.setObjectName("menuGame")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.actionNew_Game = QtWidgets.QAction(self)
        self.actionNew_Game.setObjectName("actionNew_Game")
        self.actionSave_Game = QtWidgets.QAction(self)
        self.actionSave_Game.setObjectName("actionSave_Game")
        self.actionLoad_Game = QtWidgets.QAction(self)
        self.actionLoad_Game.setObjectName("actionLoad_Game")
        self.actionQuit = QtWidgets.QAction(self)
        self.actionQuit.setObjectName("actionQuit")
        self.menuGame.addAction(self.actionNew_Game)
        self.menuGame.addAction(self.actionSave_Game)
        self.menuGame.addAction(self.actionLoad_Game)
        self.menuGame.addSeparator()
        self.menuGame.addAction(self.actionQuit)
        self.menubar.addAction(self.menuGame.menuAction())
        self.actionNew_Game.triggered.connect(lambda: self.settings_game())
        self.actionSave_Game.triggered.connect(lambda: self.save_game())
        self.actionLoad_Game.triggered.connect(lambda: self.load_game())
        self.actionQuit.triggered.connect(lambda: self.close())
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)


        for i in range(self.board_size):
            for j in range(self.board_size):
                label = QtWidgets.QLabel(str(self.board.board_tiles[i][j].value), self)
                label.setStyleSheet(
                    "text-align: center; border :1px solid ; font-size: 15px; background-color: {}".format(
                        self.board.board_tiles[i][j].getColor()))
                label.setAlignment(QtCore.Qt.AlignCenter)
                label.setGeometry((j * 60), (i * 60) +21, 60, 60)
                self.tiles[i][j] = label
        # self.update_board()

    def settings_game(self):
        self.stngs = Settings.Settings(self)
        self.stngs.show()

    def new_game(self):
        self.board = Board.Board(self.board_size)
        self.board.update_tiles(self.board.board_arr)
        self.update_board()

    def save_game(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*)", options=options)
        try:
            file = open(fileName, 'w')
            arr = self.board.board_arr
            text = ""
            for i in range(len(arr)):
                for j in range(len(arr)):
                    text = text + str(arr[i][j]) + ","
                text = text + "\n"
            file.write(text)
            file.close()
        except:
            pass

    def load_game(self):
        self.close()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*)", options=options)
        lines = 0
        with open(fileName, 'r') as f:
            for line in f:
                lines = lines + 1
        self.board_size = lines
        arr_load = [[0] * lines for i in range(lines)]
        lines = 0
        with open(fileName, 'r') as f:
            for line in f:
                t = line.split(",")
                for n in range(len(t) -1):
                    arr_load[lines][n] = int(t[n])
                lines = lines + 1
        self.board.load_board(arr_load, len(arr_load))

        self.board.update_tiles(self.board.board_arr)
        self.tiles = [[0] * self.board_size for i in range(self.board_size)]
        self.setGeometry(GetSystemMetrics(0) / 2 - 60 * self.board_size / 2,
                         GetSystemMetrics(1) / 2 - 60 * self.board_size / 2, 60 * self.board_size, 60 * self.board_size + 21)
        for i in range(self.board_size):
            for j in range(self.board_size):
                label = QtWidgets.QLabel(str(self.board.board_tiles[i][j].value), self)
                label.setStyleSheet(
                    "text-align: center; border :1px solid ; font-size: 15px; background-color: {}".format(
                        self.board.board_tiles[i][j].getColor()))
                label.setAlignment(QtCore.Qt.AlignCenter)
                label.setGeometry((j * 60), (i * 60) +21, 60, 60)
                self.tiles[i][j] = label
        self.update_board()
        self.show()



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.menuGame.setTitle(_translate("MainWindow", "Game"))
        self.actionNew_Game.setText(_translate("MainWindow", "New Game"))
        self.actionSave_Game.setText(_translate("MainWindow", "Save Game"))
        self.actionLoad_Game.setText(_translate("MainWindow", "Load Game"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))


    def update_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.tiles[i][j].setText(str(self.board.board_tiles[i][j].value))
                self.tiles[i][j].setStyleSheet(
                    "text-align: center; border :1px solid ; font-size: 15px; background-color: {}".format(
                        self.board.board_tiles[i][j].getColor()))
                self.tiles[i][j].setAlignment(QtCore.Qt.AlignCenter)
                self.tiles[i][j].setGeometry((j * 60), (i * 60) + 21, 60, 60)
                self.tiles[i][j].updateGeometry()

    def show_game_over(self):
        ctypes.windll.user32.MessageBoxW(0, "No more available moves.", "Game Over", 0x40 | 0x0)

    def check_win(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board.board_tiles[i][j] == 2048:
                    ctypes.windll.user32.MessageBoxW(0, "You have reached to 2048!", "Congratulations!", 0x40 | 0x0)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            go = self.board.move_board_left()
            self.board.update_tiles(self.board.board_arr)
            self.update_board()
            if not go:
                self.show_game_over()
            self.check_win()
        if event.key() == Qt.Key_Up:
            go = self.board.move_board_up()
            self.board.update_tiles(self.board.board_arr)
            self.update_board()
            if not go:
                self.show_game_over()
            self.check_win()
        if event.key() == Qt.Key_Down:
            go = self.board.move_board_down()
            self.board.update_tiles(self.board.board_arr)
            self.update_board()
            if not go:
                self.show_game_over()
            self.check_win()
        if event.key() == Qt.Key_Right:
            go = self.board.move_board_right()
            self.board.update_tiles(self.board.board_arr)
            self.update_board()
            if not go:
                self.show_game_over()
            self.check_win()


def window():
    app = QApplication(sys.argv)
    win = Game(4)

    win.show()
    sys.exit(app.exec_())

window()
