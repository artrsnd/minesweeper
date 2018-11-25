#!/usr/bin/python3.7


"""

Minesweeper made in Python 3.7 by Pedro Augusto Resende (https://www.github.com/resxp)
All Rights Reserved (C) - 2018

"""

# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox as messagebox

from typing import Tuple, Optional, List

from random import randint

from time import time, sleep
from core import Threading
from threading import Thread
from utils.Time import Time

IMG_PNG_ROOT_PATH = "icons/png/"
IMG_ICO_ROOT_PATH = "icons/ico/"


class Minesweeper(tk.Frame):
    table_dimension: Tuple[int, int] = None
    images = dict()
    table = list()
    win = None
    threads: List[Thread] = list()
    exit = False

    bombs: List[Tuple[int, int]] = list()
    marked_fields: List[Tuple[int, int]] = list()
    opened_fields_counter = 0

    start_time = 0
    end_time = 0

    def __init__(self, master=None):
        super(Minesweeper, self).__init__(master)
        self.master = master
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

        self.create_table(game_frame, (9, 9))
        self.start_time = time()

    def create_table(self, parent: Optional[tk.Frame], dimension: Tuple[int, int]):
        # TODO: OPTIMIZE THE ALGORITHM AND FIX THE COUNTER OF THE FIELDS
        """
        Create the minesweeper table according the passed dimensions

        :param parent: the Tk Object that is parent
        :param dimension: a Tuple[int, int]
        """
        if dimension[1] < dimension[0]:
            raise ValueError("Table dimension is not valid")
        else:
            self.table_dimension = dimension

        parent = self if parent is None else parent

        # Create a table with zeroes
        for i in range(dimension[0]):
            self.table.append([0 for j in range(dimension[1])])

        for i in range(dimension[0]):
            for j in range(dimension[1]):
                btn = tk.Button(parent,
                                image=self.images["field"],
                                width=32, height=32)

                # Bind mouse events to the button
                # https://stackoverflow.com/questions/3296893/how-to-pass-an-argument-to-event-handler-in-tkinter
                btn.bind("<Button-1>", lambda event, arg=(i, j): self.left_click(event, arg))
                btn.bind("<Button-3>", lambda event, arg=(i, j): self.right_click(event, arg))

                btn.grid(row=i, column=j)

                # Every table cell have the button and the value
                pos = list()
                pos.append(btn)
                pos.append(0)
                self.table[i][j] = pos

        # Rand bombs
        for b in range(10):
            pos = None

            try:
                while True:
                    pos = (randint(0, 8), randint(0, 8))
                    self.bombs.index(pos, 0, 9)
            except ValueError:
                self.bombs.append(pos)

        self.bombs.sort()
        print(self.bombs)

        # Calculate the fields
        for bomb in self.bombs:
            pos = self.table[bomb[0]][bomb[1]]
            pos[1] = '*'

            # N
            if bomb[0] > 0:
                pos = self.table[bomb[0] - 1][bomb[1]]

                if type(pos[1]) != str:
                    pos[1] += 1

            # E
            if bomb[1] < len(self.table[0]) - 1:
                pos = self.table[bomb[0]][bomb[1] + 1]

                if type(pos[1]) != str:
                    pos[1] += 1

            # NE
            if (bomb[0] > 0) and (bomb[1] < len(self.table[0])) - 1:
                pos = self.table[bomb[0] - 1][bomb[1] + 1]

                if type(pos[1]) != str:
                    pos[1] += 1

            # S
            if bomb[0] < len(self.table) - 1:
                pos = self.table[bomb[0] + 1][bomb[1]]

                if type(pos[1]) != str:
                    pos[1] += 1

            # SE
            if (bomb[1] < len(self.table[0]) - 1) and (bomb[0] < len(self.table) - 1):
                pos = self.table[bomb[0] + 1][bomb[1] + 1]

                if type(pos[1]) != str:
                    pos[1] += 1

            # W
            if bomb[1] > 0:
                pos = self.table[bomb[0]][bomb[1] - 1]

                if type(pos[1]) != str:
                    pos[1] += 1

            # SW
            if (bomb[0] < len(self.table) - 1) and (bomb[1] > 0):
                pos = self.table[bomb[0] + 1][bomb[1] - 1]

                if type(pos[1]) != str:
                    pos[1] += 1

            # NW
            if (bomb[0] > 0) and (bomb[1] > 0):
                pos = self.table[bomb[0] - 1][bomb[1] - 1]

                if type(pos[1]) != str:
                    pos[1] += 1

    def right_click(self, event, coords: Tuple[int, int]):
        position = self.table[coords[0]][coords[1]]
        btn: tk.Button = position[0]

        if event is None or btn["text"] == str():
            if btn["image"] == str(self.images["field"]):
                # Mark a position with a flag
                btn["image"] = self.images["red_flag"]
                self.marked_fields.append(coords)
            elif btn["image"] == str(self.images["red_flag"]):
                # Unmark that position
                btn["image"] = self.images["field"]
                self.marked_fields.remove(coords)

            self.is_win()

    def left_click(self, event, coords: Tuple[int, int]):
        position = self.table[coords[0]][coords[1]]
        btn: tk.Button = position[0]
        value = position[1]

        if btn["image"] != str(self.images["red_flag"]):
            if value == '*':
                btn["image"] = self.images["explosion"]

                if event is not None:
                    self.show_all_table()

                    # End game here
                    # TODO: fix this bug
                    # Error here: when build the table, all the values is corrupted
                    # answer = messagebox.askyesno("End of game", "You lose the game. Try again?")
                    #
                    # if answer is True:
                    #     self.grid_remove()
                    #     self.grid()
                    #     self.build()
                    # else:
                    #     self.quit()
                    self.win = False
                    self.exit_app()
            elif value != 0:
                # Configure the button to show the number centrilized
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

    def show_all_table(self):
        """
        Show all the items on table

        :return: ---
        """
        for i in range(len(self.table)):
            for j in range(len(self.table[0])):
                self.left_click(None, (i, j))

    def open_empty_fields(self, coords: Tuple[int, int]):
        # TODO: SHOW THE FIRST VALUE OF THE FIELDS
        """
        Open all empty fields of the table using backtrack technique

        :param coords: Tuple[int, int]
        :return: ---
        """
        position = self.table[coords[0]][coords[1]]
        btn: tk.Button = position[0]
        value = position[1]

        if btn["state"] != tk.DISABLED:
            if value == 0:
                btn["state"] = tk.DISABLED
                btn["image"] = self.images["field_open"]
                self.opened_fields_counter += 1

                if coords[0] > 0:
                    self.open_empty_fields((coords[0] - 1, coords[1]))

                if coords[1] < len(self.table[0]) - 1:
                    self.open_empty_fields((coords[0], coords[1] + 1))

                if coords[0] < len(self.table) - 1:
                    self.open_empty_fields((coords[0] + 1, coords[1]))

                if coords[1] > 0:
                    self.open_empty_fields((coords[0], coords[1] - 1))
            else:
                self.left_click(None, (coords[0], coords[1]))

    def is_win(self):
        self.marked_fields.sort()

        if self.marked_fields == self.bombs:
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
            for i in app.threads:
                i.join()

            self.quit()


if __name__ == "__main__":
    app = Minesweeper(tk.Tk(className="Minesweeper"))
    app.master.protocol("WM_DELETE_WINDOW", app.exit_app)
    app.mainloop()
