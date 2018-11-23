#!/usr/bin/python3.7


"""

Minesweeper made in Python 3.7 by Pedro Augusto Resende (https://www.github.com/resxp)
All Rights Reserved (C) - 2018

"""

# -*- coding: utf-8 -*-

import tkinter as tk

from typing import Tuple, Optional


IMG_PNG_ROOT_PATH = "icons/png/"
IMG_ICO_ROOT_PATH = "icons/ico/"


class Minesweeper(tk.Frame):
    table_dimension: Tuple[int, int] = None
    images = dict()

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.configure()
        self.build()

    def configure(self):
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
        self.images["field"] = tk.PhotoImage(file=IMG_PNG_ROOT_PATH + 'bg/field.png')
        self.images["field_open"] = tk.PhotoImage(file=IMG_PNG_ROOT_PATH + 'bg/field_open.png')

    def build(self):
        # Frame that will contain the menu options
        menu_frame = tk.Frame(self.master)
        menu_frame.grid(row=0)

        # TODO: build menu interface
        # tk.Label(menubar_frame, text="oi").grid()

        # Frame that contain the specify values of the current game
        top_frame = tk.Frame(self.master)
        top_frame.grid(row=1)

        # TODO: build interface and make functional
        tk.Label(top_frame, text="Time: ").grid(row=0, column=0, )
        tk.Label(top_frame, text="00:00").grid(row=0, column=1)

        # Frame that contains the table of the game
        # TODO: make the game functional
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

        # Create graphic representation
        # TODO: Add func to buttons
        for i in range(dimension[0]):
            for j in range(dimension[1]):
                tk.Button(parent, image=self.images["field_open"], width=32, height=32, command=None)\
                    .grid(row=i, column=j)

        # TODO: Create logical representation


if __name__ == "__main__":
    Minesweeper(tk.Tk(className="Minesweeper")).mainloop()