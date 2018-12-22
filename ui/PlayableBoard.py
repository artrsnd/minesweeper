# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox as messagebox

from typing import Tuple, Optional, List

from time import time, sleep
from threading import Thread
from ui.utils import Threading
from ui.utils.Time import Time

from core.engine import MinesweeperBoard


class Properties(object):
    charset: dict = None
    paths: dict = None
    images: dict = None

    def __init__(self):
        # TODO: LOAD PROPERTIES FROM FILE
        self.paths = {"icons": "ui/icons/png/"}
        self.images = dict()

    def load_images(self):
        self.images["bomb"] = tk.PhotoImage(file=self.paths["icons"] + 'bomb_32.png')
        self.images["red_flag"] = tk.PhotoImage(file=self.paths["icons"] + 'red_flag_32.png')
        self.images["white_flag"] = tk.PhotoImage(file=self.paths["icons"] + 'white_flag_32.png')
        self.images["explosion"] = tk.PhotoImage(file=self.paths["icons"] + 'explosion_32.png')
        self.images["field"] = tk.PhotoImage(file=self.paths["icons"] + 'bg/field.png')
        self.images["field_open"] = tk.PhotoImage(file=self.paths["icons"] + 'bg/field_open.png')


class Game(object):
    """
    Class with all control variables and methods to control the game.
    """
    player: str = "none"
    win: bool = None
    exit: bool = False

    time: Time = Time()

    marked_fields: List[Tuple[int, int]] = list()  # List with the marked fields
    c_marked_fields: int = 0

    def __init__(self, player: str):
        self.player = player


class PlayableBoard(tk.Frame):
    """
    UI Implementation of the minesweeper game.
    """
    board: MinesweeperBoard = None
    properties: Properties = None
    game_info: Game = None

    __threads: List[Thread] = list()  # list of threads
    __fields = list()  # List of the fields and his associated buttons

    def __init__(self, properties: Properties, info: Game, board: MinesweeperBoard, master=None):
        super(PlayableBoard, self).__init__(master)
        self.master = master
        self.game_info = info
        self.properties = properties
        self.board = board
        self.grid()
        self.__configure()
        self.__build_window()

    def __configure(self):
        self.master.resizable(False, False)
        self.properties.load_images()
        self.master.title("Minesweeper")
        self.master.attributes()
        # app.master.iconbitmap(r'icons/ico/bomb_256.ico')  # Use this is raising a TclError "bitmap not defined"
        self.tk.call('wm', 'iconphoto', self.master._w,
                     self.properties.images["bomb"])  # Define the menubar icon of the application

    @Threading.thread
    def __show_time(self, parent: tk.Frame, interval):
        while True:
            sleep(interval)

            t = Time.calculate_time(self.game_info.time.start_time, time())

            if not self.game_info.exit and self.game_info.win is None:
                tk.Label(parent, text=Time.format_time(t)) \
                    .grid(row=0, column=1)
            else:
                return

    @Threading.thread
    def __update_game_info(self, parent: tk.Frame):
        qtd = self.game_info.c_marked_fields - 1

        while True:
            sleep(0.25)

            if not self.game_info.exit:
                if qtd != self.game_info.c_marked_fields or qtd == -1:
                    qtd = self.game_info.c_marked_fields

                    tk.Label(parent, text="Bombs: {}/{}".format(qtd, self.board.total_bombs)) \
                        .grid(row=0, column=2)
            else:
                return

    def __build_window(self):
        """
        Build the Tk Application
        :return:
        """
        # Frame that will contain the menu options
        menu_frame = tk.Frame(self.master)
        menu_frame.grid(row=0)

        # TODO: build menu interface

        # Frame that contain the specify values of the current game
        top_frame = tk.Frame(self.master)
        top_frame.grid(row=1)

        tk.Label(top_frame, text="Time: ").grid(row=0, column=0)
        self.__threads.append(self.__show_time(top_frame, 0.5))
        self.__threads.append(self.__update_game_info(top_frame))

        # Frame that contains the table of the game
        game_frame = tk.Frame(self.master)
        game_frame.grid(row=2)

        self.__create_tk_board(game_frame)
        self.game_info.time.start_time = time()

    def __create_tk_board(self, parent: Optional[tk.Frame]):
        rows = self.board.dimensions[0]
        cols = self.board.dimensions[1]

        for row in range(rows):
            r = list()

            for col in range(cols):
                btn = tk.Button(parent,
                                image=self.properties.images["field"],
                                width=32, height=32)

                # Bind mouse events to the button
                # https://stackoverflow.com/questions/3296893/how-to-pass-an-argument-to-event-handler-in-tkinter
                btn.bind("<Button-1>", lambda event, arg=(row, col): self.__left_click(event, arg))
                btn.bind("<Button-3>", lambda event, arg=(row, col): self.__right_click(event, arg))

                btn.grid(row=row, column=col)
                r.append(btn)

            self.__fields.append(r)

    def __right_click(self, event, coords: Tuple[int, int]):
        btn: tk.Button = self.__fields[coords[0]][coords[1]]

        if event is None or btn["text"] == str():
            if btn["image"] == str(self.properties.images["field"]):
                # Mark a position with a flag
                btn["image"] = self.properties.images["white_flag"]
                self.game_info.marked_fields.append(coords)
            elif btn["image"] == str(self.properties.images["white_flag"]):
                # Unmark that position
                btn["image"] = self.properties.images["field"]
                self.game_info.marked_fields.remove(coords)

            self.game_info.c_marked_fields += 1
            self.__is_win()

    def __left_click(self, event, coords: Tuple[int, int]):
        btn: tk.Button = self.__fields[coords[0]][coords[1]]
        value = self.board.board[coords[0]][coords[1]]

        if btn["image"] != str(self.properties.images["white_flag"]):
            if value == '*':
                btn["image"] = self.properties.images["explosion"]

                if event is not None:
                    self.__show_bombs()

                    self.game_info.win = False
                    self.__exit_app()
            elif value != 0:
                # Configure the button to show the number in a centralized position
                btn["compound"] = tk.CENTER
                btn["padx"] = 0
                btn["pady"] = 0
                btn["text"] = value
            elif value == 0:
                # Open all adjacent empty fields
                self.__open_empty_fields(coords)
            else:
                raise RuntimeError("An error has occurred")

            self.__is_win()

    def __show_bombs(self):
        """
        Show all the items on table

        :return: ---
        """
        for b in self.board.bombs:
            self.__left_click(None, b)

    def __open_empty_fields(self, coords: Tuple[int, int]):
        """
        Open all empty fields of the table using backtrack technique

        :param coords: Tuple[int, int]
        :return: ---
        """
        # TODO: OPEN CORNERS!!!!
        btn: tk.Button = self.__fields[coords[0]][coords[1]]
        value = self.board.board[coords[0]][coords[1]]

        if btn["state"] != tk.DISABLED:
            if value == 0:
                btn["state"] = tk.DISABLED
                btn["image"] = self.properties.images["field_open"]

                if coords[0] > 0:
                    self.__open_empty_fields((coords[0] - 1, coords[1]))

                if coords[1] < self.board.dimensions[1] - 1:
                    self.__open_empty_fields((coords[0], coords[1] + 1))

                if coords[0] < self.board.dimensions[0] - 1:
                    self.__open_empty_fields((coords[0] + 1, coords[1]))

                if coords[1] > 0:
                    self.__open_empty_fields((coords[0], coords[1] - 1))
            else:
                self.__left_click(None, (coords[0], coords[1]))

    def __is_win(self):
        """
        Verify if the the player win the game. If yes, the game is finished.
        To win the game, the player must mark all the fields bomb correctly;
        :return:
        """
        self.game_info.marked_fields.sort()  # sort the player marked fields

        if self.game_info.marked_fields == self.board.bombs:  # compare the marked fields with the solving set
            self.game_info.win = True
            self.__exit_app()

    def __exit_app(self):
        """
        Exit and close the game. This method can be called in various situations:
        - if the player wants close the game
        - if the player lost the game
        - if the player won the game

        :return: None
        """
        if self.game_info.win is None:
            if messagebox.askokcancel("Quit", "You want to quit now?"):
                self.game_info.exit = True
        elif self.game_info.win is True:
            self.game_info.time.end_time = time()
            self.game_info.time.all_time = Time.calculate_time(self.game_info.time.start_time, self.game_info.time.end_time)

            messagebox.showinfo("End of game", "Congratulations {}! You won the game in {}!".format(
                self.game_info.player,
                Time.format_time(self.game_info.time.all_time)))
            self.game_info.exit = True
        elif self.game_info.win is False:
            messagebox.showerror("End of game", "You lose the game!")
            self.game_info.exit = True

        if self.game_info.exit is True:  # terminate all threads correctly
            for thread in self.__threads:
                thread.join()

        self.quit()
