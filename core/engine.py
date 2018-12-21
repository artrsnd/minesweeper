# -*- coding: utf-8 -*-

from typing import Tuple, List, NewType
from random import randint

Board = NewType("Field", List[List[int]])


class MinesweeperBoard(object):
    """
    Class to generate and manage the minesweeper board.

    Author: Pedro Augusto (resxp) - pedro.resende99@gmail.com
    """
    minimum_percentage = 5  # the minimum percentage of the bombs in the board

    __dimensions: Tuple[int, int] = None
    __board: Board = None

    __bomb_percent: float
    __bombs: List[Tuple[int, int]]

    __total_fields: int
    __total_bombs: int

    def __init__(self, dimensions: Tuple[int, int], bomb_percent: float):
        """
        Create the Minesweeper Object. The constructor only test the dimensions of the board and the set the bomb
        percent.

        :param dimensions: the dimensions of the board.
        :param bomb_percent: the bomb percent in the table. Can not be less than 5% of the board size.
        """
        if dimensions[1] < dimensions[0]:  # TODO: add a minimum height x width for the board
            raise ValueError("Table dimension is not valid")
        else:
            self.__dimensions = dimensions
            self.__total_fields = dimensions[0] * dimensions[1]

        minimum_bomb_percent = int(self.__total_fields * (MinesweeperBoard.minimum_percentage / 100))

        if minimum_bomb_percent > bomb_percent:
            raise ValueError("Quantity of bombs can not be less than {}% of the total fields.\n"
                             "- Quantity of fields: {}\n"
                             "- Minimum percentage of bombs: {}%"
                             .format(MinesweeperBoard.minimum_percentage,
                                     self.__total_fields,
                                     minimum_bomb_percent))

        elif bomb_percent > 100:
            raise ValueError("Percentage of bombs can not be greater than 100%!")
        else:
            self.__bomb_percent = bomb_percent
            total_bombs = self.__total_fields * bomb_percent / 100
            # round the number
            self.__total_bombs = int(total_bombs) if total_bombs - int(total_bombs) < 0.5 else int(total_bombs) + 1

    def generate_board(self) -> None:
        """
        Generate the board with the bombs and all near fields filled

        :return: None
        """
        # Create the board with zeroes
        self.__board = list()
        for i in range(self.__dimensions[0]):
            self.__board.append([0 for b in range(self.__dimensions[1])])

        self.__place_bombs()

    def __place_bombs(self) -> None:
        """
        Rand all the bombs in the grid and place in the list of bombs and sum 1 to the fields nearby.

        :return: None
        """
        if self.__bombs is None:
            self.__bombs = list()
        else:
            self.__bombs.clear()

        # Rand bombs
        for b in range(self.__total_bombs):
            bomb = None

            try:
                while True:
                    # generate a (x, y) point
                    bomb = (randint(0, self.__dimensions[0] - 1), randint(0, self.__dimensions[1] - 1))
                    self.__bombs.index(bomb)  # verify if this point is included in solution set
            except ValueError:
                # if not, insert it into the list
                self.__bombs.append(bomb)
                self.__board[bomb[0]][bomb[1]] = '*'
                # Adds 1 to all fields nearby the bomb
                self.__count_fields(bomb)

        self.__bombs.sort()

    def __count_fields(self, bomb: Tuple[int, int]) -> None:
        """
        Sum 1 to all fields nearby of the bomb

        :param bomb: The bomb position on the board
        :return: None
        """
        row = bomb[0]
        col = bomb[1]
        row_limit = self.__dimensions[0]
        col_limit = self.__dimensions[1]

        # This algorithm run in all 3x3 fields, including the bomb position. This can be improved!

        for r in range(row - 1, row + 2):  # Run in interval [row - 1, row + 1] (start from the row above)
            if -1 < r < row_limit:  # Test if the row is valid
                # For each row, test all columns
                for c in range(col - 1, col + 2):  # Run in interval [col - 1, col + 1] (start from the left column)
                    # If the column is valid and the column is not a bomb, sum 1 to the field
                    if (-1 < c < col_limit) and (self.__board[r][c] != '*'):
                        self.__board[r][c] += 1

    def __str__(self):
        return "=== [MINESWEEPER BOARD] ===\n" \
               "- Dimensions: {}x{}\n" \
               "- Quantity of fields: {}\n" \
               "- Quantity of bombs: {}\n" \
               "- Percentage of bombs: {}\n" \
               "- Board Answer: {}\n" \
               .format(self.__dimensions[0], self.__dimensions[1],
                       self.__total_fields,
                       self.__total_bombs,
                       self.__bomb_percent,
                       self.__bombs)

    def format_board(self) -> str:
        """
        Format the board in a string to print in terminal without colors.

        :return: String containing the actual state of the board
        """
        line = str()

        def print_value_line(row: List[int]):
            """
            Print the valid row of the board.

            :param row: The row to be printable
            :return: None
            """
            str_line = "║"

            for j in row:
                str_line += " {} ║".format(j)

            return str_line + "\n"

        columns = self.__dimensions[0]
        lines = self.__dimensions[1]

        for i in range(lines + 1):
            if i == 0:  # Change the charset to print the line before the first row
                charset = {
                    "start_line": "╔",
                    "end_line": "╗",
                    "connector": "╦"
                }
            elif i == lines:  # Change the charset to print the line after the last row
                charset = {
                    "start_line": "╚",
                    "end_line": "╝",
                    "connector": "╩"
                }
            else:  # Change the charset to print the line between the rows
                charset = {
                    "start_line": "╠",
                    "end_line": "╣",
                    "connector": "╬"
                }

            # Print the line plus the row
            line += charset["start_line"]
            for c in range(columns):
                line += "═══{}".format(charset["end_line"] if c == columns - 1 else charset["connector"])

            line += "\n"

            if i < lines:
                line += print_value_line(self.__board[i])

        return line
