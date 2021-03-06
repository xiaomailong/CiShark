# /usr/bin/python3
# -*- coding: utf-8 -*-

"""
维护一个unix时间戳
"""
from time import time

class Timestamp:
    """
    maintain a structure like unix timestamp
    """

    def __init__(self,sec = 0,usec = 0):
        self.sec = sec
        self.usec = usec
        return

    def __repr__(self):
        return str(self.sec) + "." + str(self.usec)

    def __sub__(self,b):
        a_usec = self.sec * (10 ** 6) + self.usec
        b_usec = b.sec * (10 ** 6) + b.usec
        return a_usec - b_usec

    def empty(self):
        if self.sec == 0 and self.usec == 0:
            return False
        else:
            return True

    @staticmethod
    def from_str(timestamp_str):
        """
        timestamp_str is like this:
        1409556967.451036
        """
        timestamp_str_list = timestamp_str.split(".")
        if len(timestamp_str_list) != 2:
            #print("timestamp_str_list length not 2:",timestamp_str)
            return None
        if timestamp_str_list[0].isdigit() == False or timestamp_str_list[1].isdigit() == False:
            print("timestamp str not digit:",timestamp_str)
            return None

        sec = int(timestamp_str_list[0])
        usec = int(timestamp_str_list[1])
        timestamp = Timestamp(sec,usec)

        return timestamp

    @staticmethod
    def cur():
        """
        得到当前时间
        """
        cur_time = time()
        time_str = "{:.6f}".format(cur_time)
        return Timestamp.from_str(time_str)

if __name__ == "__main__":
    timestamp = Timestamp(2222,22222)
    print(timestamp)
