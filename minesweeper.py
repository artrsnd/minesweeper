# -*- coding: utf-8 -*-

from core.engine import MinesweeperBoard


def main():
    board = MinesweeperBoard(dimensions=(8, 8), bomb_percent=15)
    board.generate_board()
    print(str(board))
    print(board.format_board())


if __name__ == "__main__":
    main()
