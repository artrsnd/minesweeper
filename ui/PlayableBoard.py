# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox as messagebox

from typing import Tuple, Optional, List

from time import time, sleep
from threading import Thread
from ui.utils import Threading
from ui.utils.Time import Time

from core.engine import MinesweeperBoard

IMG_PNG_ROOT_PATH = "ui/icons/png/"


class PlayableBoard(tk.Frame):
    board: MinesweeperBoard = None

    threads: List[Thread] = list()  # list of threads in the game
    images = dict()
    win = None

    exit = False

    fields = list()
    marked_fields: List[Tuple[int, int]] = list()
    opened_fields_counter = 0

    start_time = 0
    end_time = 0

    def __init__(self, board: MinesweeperBoard, master=None):
        super(PlayableBoard, self).__init__(master)
        self.master = master
        self.board = board
        self.grid()
        self.configure()
        self.build()

    def configure(self, **kwargs):
        self.master.resizable(False, False)
        self.load_images()
        self.master.title("Minesweeper [Campo Minado]")
        self.master.attributes()
        # app.master.iconbitmap(r'icons/ico/bomb_256.ico')  # Use this is raising a TclError "bitmap not defined"
        self.tk.call('wm', 'iconphoto', self.master._w,
                     self.images["bomb"])  # Define the menubar icon of the application

    def load_images(self):
        """
        Load all used images
        """
        self.images["bomb"] = tk.PhotoImage(file=IMG_PNG_ROOT_PATH + 'bomb_32.png')
        self.images["red_flag"] = tk.PhotoImage(file=IMG_PNG_ROOT_PATH + 'red_flag_32.png')
        self.images["white_flag"] = tk.PhotoImage(file=IMG_PNG_ROOT_PATH + 'white_flag_32.png')
        self.images["explosion"] = tk.PhotoImage(file=IMG_PNG_ROOT_PATH + 'explosion_32.png')
        self.images["field"] = tk.PhotoImage(file=IMG_PNG_ROOT_PATH + 'bg/field.png')
        self.images["field_open"] = tk.PhotoImage(file=IMG_PNG_ROOT_PATH + 'bg/field_open.png')

    @Threading.thread
    def show_time(self, parent: tk.Frame, interval):
        while True:
            sleep(interval)

            t = Time.calculate_time(self.start_time, time())

            if not self.exit:
                tk.Label(parent, text=Time.format_time(t)) \
                    .grid(row=0, column=2)
            else:
                return

    def build(self):
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

        self.create_table(game_frame)
        self.start_time = time()

    def create_table(self, parent: Optional[tk.Frame]):
        rows = self.board.dimensions[0]
        cols = self.board.dimensions[1]

        for row in range(rows):
            r = list()

            for col in range(cols):
                btn = tk.Button(parent,
                                image=self.images["field"],
                                width=32, height=32)

                # Bind mouse events to the button
                # https://stackoverflow.com/questions/3296893/how-to-pass-an-argument-to-event-handler-in-tkinter
                btn.bind("<Button-1>", lambda event, arg=(row, col): self.left_click(event, arg))
                btn.bind("<Button-3>", lambda event, arg=(row, col): self.right_click(event, arg))

                btn.grid(row=row, column=col)
                r.append(btn)

            self.fields.append(r)

    def right_click(self, event, coords: Tuple[int, int]):
        btn: tk.Button = self.fields[coords[0]][coords[1]]

        if event is None or btn["text"] == str():
            if btn["image"] == str(self.images["field"]):
                # Mark a position with a flag
                btn["image"] = self.images["white_flag"]
                self.marked_fields.append(coords)
            elif btn["image"] == str(self.images["white_flag"]):
                # Unmark that position
                btn["image"] = self.images["field"]
                self.marked_fields.remove(coords)

            self.is_win()

    def left_click(self, event, coords: Tuple[int, int]):
        btn: tk.Button = self.fields[coords[0]][coords[1]]
        value = self.board.board[coords[0]][coords[1]]

        if btn["image"] != str(self.images["white_flag"]):
            if value == '*':
                btn["image"] = self.images["explosion"]

                if event is not None:
                    self.show_bombs()

                    self.win = False
                    self.exit_app()
            elif value != 0:
                # Configure the button to show the number in a centralized position
                btn["compound"] = tk.CENTER
                btn["padx"] = 0
                btn["pady"] = 0
                btn["text"] = value
                self.opened_fields_counter += 1
            elif value == 0:
                # Open all adjacent empty fields
                self.open_empty_fields(coords)
            else:
                raise RuntimeError("An error has occurred")

            self.is_win()

    def show_bombs(self):
        """
        Show all the items on table

        :return: ---
        """
        for b in self.board.bombs:
            self.left_click(None, b)

    def open_empty_fields(self, coords: Tuple[int, int]):
        # TODO: SHOW THE FIRST VALUE OF THE FIELDS
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
                btn["image"] = self.images["field_open"]
                self.opened_fields_counter += 1

                if coords[0] > 0:
                    self.open_empty_fields((coords[0] - 1, coords[1]))

                if coords[1] < self.board.dimensions[1] - 1:
                    self.open_empty_fields((coords[0], coords[1] + 1))

                if coords[0] < self.board.dimensions[0] - 1:
                    self.open_empty_fields((coords[0] + 1, coords[1]))

                if coords[1] > 0:
                    self.open_empty_fields((coords[0], coords[1] - 1))
            else:
                self.left_click(None, (coords[0], coords[1]))

    def is_win(self):
        self.marked_fields.sort()

        if self.marked_fields == self.board.bombs:
            self.win = True
            self.exit_app()

    def exit_app(self):
        if self.win is None:
            if messagebox.askokcancel("Quit", "You want to quit now?"):
                self.exit = True
        elif self.win is True:
            self.end_time = time()

            messagebox.showinfo("End of game", "Congratulations! You won the game in {}!".format(
                Time.format_time(Time.calculate_time(self.start_time, self.end_time))))
            self.exit = True
        elif self.win is False:
            messagebox.showerror("End of game", "You lose the game!")
            self.exit = True

        if self.exit is True:
            for i in self.threads:
                i.join()

        self.quit()
