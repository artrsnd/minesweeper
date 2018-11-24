#!/usr/bin/python3.7


"""

Minesweeper made in Python 3.7 by Pedro Augusto Resende (https://www.github.com/resxp)
All Rights Reserved (C) - 2018

"""

# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox as messagebox

from typing import Tuple, Optional


IMG_PNG_ROOT_PATH = "icons/png/"
IMG_ICO_ROOT_PATH = "icons/ico/"


class Minesweeper(tk.Frame):
    table_dimension: Tuple[int, int] = None
    images = dict()
    table = [
        [1, 1, 1, 0, 0, 0, 1, '*', 1],
        [1, '*', 2, 1, 1, 1, 2, 2, 1],
        [2, 2, 3, '*', 1, 1, '*', 1, 0],
        [1, '*', 2, 1, 1, 1, 2, 2, 1],
        [1, 1, 1, 1, 1, 0, 1, '*', 1],
        [0, 0, 1, '*', 2, 1, 1, 1, 1],
        [1, 1, 2, 2, '*', 1, 0, 0, 0],
        [1, '*', 1, 0, 1, 1, 1, 0, 0],
        [1, 1, 1, 0, 1, '*', 1, 0, 0]
    ]

    bombs = [(0, 7), (1, 1), (2, 3), (2, 6), (3, 1), (4, 7), (5, 3), (6, 4), (7, 1), (8, 5)]
    marked_fields = list()
    opened_fields_counter = 0

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.resizable(False, False)
        self.grid()
        self.configure()
        self.build()

    def configure(self, **kwargs):
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

    def build(self):
        # Frame that will contain the menu options
        menu_frame = tk.Frame(self.master)
        menu_frame.grid(row=0)

        # TODO: build menu interface

        # Frame that contain the specify values of the current game
        top_frame = tk.Frame(self.master)
        top_frame.grid(row=1)

        # TODO: build interface and make functional
        # tk.Label(top_frame, text="Time: ").grid(row=0, column=0, )
        # tk.Label(top_frame, text="00:00").grid(row=0, column=1)

        # Frame that contains the table of the game
        game_frame = tk.Frame(self.master)
        game_frame.grid(row=2)

        self.create_table(game_frame, (9, 9))

    def create_table(self, parent: Optional[tk.Frame], dimension: Tuple[int, int]):
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

        # TODO: CREATE RANDOM TABLES

        for i in range(dimension[0]):
            for j in range(dimension[1]):
                btn = tk.Button(parent,
                                image=self.images["field"],
                                width=32, height=32)

                # Bind mouse events to the button
                # https://stackoverflow.com/questions/3296893/how-to-pass-an-argument-to-event-handler-in-tkinter
                btn.bind("<Button-1>", lambda event, arg=(i, j): self.left_click(event, arg))
                btn.bind("<Button-3>", lambda event, arg=(i, j): self.right_click(event, arg))

                # Every table cell have the button and the value
                self.table[i][j] = (btn, self.table[i][j])

                btn.grid(row=i, column=j)

    def right_click(self, event, coords: Tuple[int, int]):
        position = self.table[coords[0]][coords[1]]
        btn: tk.Button = position[0]
        value = position[1]

        if btn["text"] == str():
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

                    messagebox.showerror("End of game", "You lose the game!")
                    self.quit()
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
        """
        Open all empty fields of the table using backtrack technique

        :param coords: Tuple[int, int]
        :return: ---
        """
        position = self.table[coords[0]][coords[1]]
        btn: tk.Button = position[0]
        value = position[1]

        if btn["state"] != tk.DISABLED and value == 0:
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

    def is_win(self):
        self.marked_fields.sort()

        if (self.opened_fields_counter == (9 * 9) - 9) and (self.marked_fields == self.bombs):
            # if self.marked_fields == self.bombs:
            messagebox.showinfo("End of game", "Congratulations! You won the game!")
            self.quit()


if __name__ == "__main__":
    Minesweeper(tk.Tk(className="Minesweeper")).mainloop()
