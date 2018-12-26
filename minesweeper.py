#!/usr/bin/python3

# -*- coding: utf-8 -*-

from core.Engine import MinesweeperBoard
from ui.PlayableBoard import PlayableBoard
from tkinter import Tk
from ui.PlayableBoard import UIProperties, Game
import subprocess
from re import sub
from core.Config import GameSettings


def load_config():
    # Load user info
    username: str = subprocess.Popen(["id", "-un"], stdout=subprocess.PIPE).communicate()[0]
    username = sub(r"[b\'\\n]", "", str(username))

    properties = UIProperties()
    settings = GameSettings()
    info = Game(username, settings)
    print(settings)

    return info, properties


def main():
    board = MinesweeperBoard(dimensions=(10, 10), bomb_percent=25)
    board.generate_board()
    print(str(board))
    print(board.format_board())

    info, properties = load_config()

    app = PlayableBoard(properties, info, board, Tk(className="Minesweeper"))
    app.master.protocol("WM_DELETE_WINDOW", app.exit_app)
    app.mainloop()


if __name__ == "__main__":
    main()
