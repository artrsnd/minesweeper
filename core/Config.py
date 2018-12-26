# -*- coding: utf-8 -*-

from typing import Tuple, Dict
import configparser


DEFAULT_CONFIG_FILE = "config.properties"
SECTION_GENERAL = "GENERAL"
SECTION_BOARD = "BOARD"
SECTION_ENDGAME = "END_GAME"
SECTION_QUIT = "QUIT"
SECTION_ERROR = "ERROR"


class Language(object):
    lang: str

    end_game = {
        "TITLE": str,
        "WIN_MESSAGE": str,
        "LOSE_MESSAGE": str
    }
    error = {
        "RUNTIME_ERROR": str
    }
    general = {
        "TITLE": str,
        "BOMBS": str,
        "TIME": str
    }
    quit = {
        "TITLE": str,
        "MESSAGE": str
    }


class GameSettings(object):
    language = Language()
    minimum = {
        "board_size": Tuple[int, int],
        "bomb_percent": float
    }
    maximum = {
        "board_size": Tuple[int, int],
        "bomb_percent": float
    }

    def __init__(self, config_file: str = None):
        parser = configparser.RawConfigParser()
        parser.read(DEFAULT_CONFIG_FILE if config_file is None else config_file, "utf-8")

        # Load game config
        self.minimum["board_size"] = (parser.getint(SECTION_BOARD, 'min.width'),
                                      parser.getint(SECTION_BOARD, 'min.height'))
        self.minimum["bomb_percent"] = parser.getfloat(SECTION_BOARD, 'min.bomb_percent')

        self.maximum["board_size"] = (parser.getint(SECTION_BOARD, 'max.width'),
                                      parser.getint(SECTION_BOARD, 'max.height'))

        self.maximum["bomb_percent"] = parser.getfloat(SECTION_BOARD, 'max.bomb_percent')

        # Load game messages
        self.language.lang = parser.get(SECTION_GENERAL, 'lang')
        parser.read("core/lang/{}.lang".format(self.language.lang), "utf-8")

        # General
        self.language.general["TITLE"] = parser.get(SECTION_GENERAL, "TITLE")
        self.language.general["TIME"] = parser.get(SECTION_GENERAL, "TIME")
        self.language.general["BOMBS"] = parser.get(SECTION_GENERAL, "BOMBS")

        # Error
        self.language.error["RUNTIME_ERROR"] = parser.get(SECTION_ERROR, "RUNTIME_ERROR")

        # END_GAME
        self.language.end_game["TITLE"] = parser.get(SECTION_ENDGAME, "TITLE")
        self.language.end_game["WIN_MESSAGE"] = parser.get(SECTION_ENDGAME, "WIN_MESSAGE")
        self.language.end_game["LOSE_MESSAGE"] = parser.get(SECTION_ENDGAME, "LOSE_MESSAGE")

        # QUIT
        self.language.quit["TITLE"] = parser.get(SECTION_QUIT, "TITLE")
        self.language.quit["MESSAGE"] = parser.get(SECTION_QUIT, "MESSAGE")

    def __str__(self):
        return "[GAME SETTINGS]\n" \
               "Language: {}\n" \
               "Minimum Board Size: {}x{}\n" \
               "Minimum Bomb Percent: {}%\n" \
               "Maximum Board Size: {}x{}\n" \
               "Maximum Bomb Percent: {}%" \
            .format(self.language.lang,
                    self.minimum["board_size"][0],
                    self.minimum["board_size"][1],
                    self.minimum["bomb_percent"],
                    self.maximum["board_size"][0],
                    self.maximum["board_size"][1],
                    self.maximum["bomb_percent"])
