# -*- coding: utf-8 -*-

from core.engine import MinesweeperBoard
from ui.PlayableBoard import PlayableBoard
from tkinter import Tk
from ui.PlayableBoard import Properties, Game
import subprocess
from re import sub


def load_config():
    # Load user info
    username: str = subprocess.Popen(["id", "-un"], stdout=subprocess.PIPE).communicate()[0]
    username = sub(r"[b\'\\n]", "", str(username))

    info = Game(username)
    properties = Properties()

    # TODO: load language from file
    # TODO: load minimum config

    return info, properties


def main():
    board = MinesweeperBoard(dimensions=(6, 6), bomb_percent=15)
    board.generate_board()
    print(str(board))
    print(board.format_board())

    info, properties = load_config()

    app = PlayableBoard(properties, info, board, Tk(className="Minesweeper"))
    app.master.protocol("WM_DELETE_WINDOW", app.__exit_app)
    app.mainloop()


if __name__ == "__main__":
    main()
