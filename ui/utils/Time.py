
from typing import Tuple


class Time:
    @staticmethod
    def calculate_time(start_time: float, end_time: float) -> Tuple[int, int]:
        t = end_time - start_time
        minutes = int(t / 60)
        seconds = int(t % 60)

        return minutes, seconds

    @staticmethod
    def format_time(time: Tuple[int, int]) -> str:
        """
        Return a time in MM:SS
        :param time: a Tuple[int, int]
        :return: a string in format MM:SS
        """
        return "{}:{}".format('0{}'.format(time[0]) if time[0] < 10 else time[0],
                              '0{}'.format(time[1]) if time[1] < 10 else time[1])
