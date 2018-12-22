# -*- coding: utf-8 -*-

from core.engine import MinesweeperBoard
from ui.PlayableBoard import PlayableBoard
from tkinter import Tk
from ui.PlayableBoard import Properties


def main():
    board = MinesweeperBoard(dimensions=(8, 8), bomb_percent=15)
    board.generate_board()
    print(str(board))
    print(board.format_board())

    properties = Properties()
    app = PlayableBoard(properties, board, Tk(className="Minesweeper"))
    app.master.protocol("WM_DELETE_WINDOW", app.exit_app)
    app.mainloop()


if __name__ == "__main__":
    main()
