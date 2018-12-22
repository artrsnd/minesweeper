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
    win: bool = None
    exit: bool = False

    time: Time = Time()

    marked_fields: List[Tuple[int, int]] = list()  # List with the marked fields


class PlayableBoard(tk.Frame):
    """
    UI Implementation of the minesweeper game.
    """
    board: MinesweeperBoard = None
    properties: Properties = None
    info: Game = Game()

    threads: List[Thread] = list()  # list of threads
    fields = list()  # List of the fields and his associated buttons

    def __init__(self, properties: Properties, board: MinesweeperBoard, master=None):
        super(PlayableBoard, self).__init__(master)
        self.master = master
        self.properties = properties
        self.board = board
        self.grid()
        self.configure()
        self.__build_window()

    def configure(self, **kwargs):
        self.master.resizable(False, False)
        self.properties.load_images()
        self.master.title("Minesweeper")
        self.master.attributes()
        # app.master.iconbitmap(r'icons/ico/bomb_256.ico')  # Use this is raising a TclError "bitmap not defined"
        self.tk.call('wm', 'iconphoto', self.master._w,
                     self.properties.images["bomb"])  # Define the menubar icon of the application

    @Threading.thread
    def show_time(self, parent: tk.Frame, interval):
        while True:
            sleep(interval)

            t = Time.calculate_time(self.info.time.start_time, time())

            if not self.info.exit:
                tk.Label(parent, text=Time.format_time(t)) \
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
        self.threads.append(self.show_time(top_frame, 0.5))

        # Frame that contains the table of the game
        game_frame = tk.Frame(self.master)
        game_frame.grid(row=2)

        self.__create_tk_board(game_frame)
        self.info.time.start_time = time()

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

            self.fields.append(r)

    def __right_click(self, event, coords: Tuple[int, int]):
        btn: tk.Button = self.fields[coords[0]][coords[1]]

        if event is None or btn["text"] == str():
            if btn["image"] == str(self.properties.images["field"]):
                # Mark a position with a flag
                btn["image"] = self.properties.images["white_flag"]
                self.info.marked_fields.append(coords)
            elif btn["image"] == str(self.properties.images["white_flag"]):
                # Unmark that position
                btn["image"] = self.properties.images["field"]
                self.info.marked_fields.remove(coords)

            self.is_win()

    def __left_click(self, event, coords: Tuple[int, int]):
        btn: tk.Button = self.fields[coords[0]][coords[1]]
        value = self.board.board[coords[0]][coords[1]]

        if btn["image"] != str(self.properties.images["white_flag"]):
            if value == '*':
                btn["image"] = self.properties.images["explosion"]

                if event is not None:
                    self.__show_bombs()

                    self.info.win = False
                    self.exit_app()
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

            self.is_win()

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
        btn: tk.Button = self.fields[coords[0]][coords[1]]
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

    def is_win(self):
        """
        Verify if the the player win the game. If yes, the game is finished.
        To win the game, the player must mark all the fields bomb correctly;
        :return:
        """
        self.info.marked_fields.sort()  # sort the player marked fields

        if self.info.marked_fields == self.board.bombs:  # compare the marked fields with the solving set
            self.info.win = True
            self.exit_app()

    def exit_app(self):
        """
        Exit and close the game. This method can be called in various situations:
        - if the player wants close the game
        - if the player lost the game
        - if the player won the game

        :return: None
        """
        if self.info.win is None:
            if messagebox.askokcancel("Quit", "You want to quit now?"):
                self.info.exit = True
        elif self.info.win is True:
            self.info.time.end_time = time()

            messagebox.showinfo("End of game", "Congratulations! You won the game in {}!".format(
                Time.format_time(Time.calculate_time(self.info.time.start_time, self.info.time.end_time))))
            self.info.exit = True
        elif self.info.win is False:
            messagebox.showerror("End of game", "You lose the game!")
            self.info.exit = True

        if self.info.exit is True:  # terminate all threads correctly
            for thread in self.threads:
                thread.join()

        self.quit()
