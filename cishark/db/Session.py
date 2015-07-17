# -*- coding: utf-8 -*-
__author__ = 'Administrator'

from .ModelBase import ModelBase
from cishark.util import Timestamp
import mysql.connector

class Session(ModelBase):
    """
    维护Session信息，直接在数据库当中存取
    """

    def __init__(self, ip):
        super().__init__()
        self.last_timestamp = Timestamp.cur()
        self.ip = ip
        self._series_state = 0
        self._cpu_state = 0
        self.b_switch = False

        print("create new session",self.ip)

        cur_time = Timestamp.cur()
        add_session_sql = (
        "INSERT INTO session (start_tv_sec, start_tv_usec,ip) "
        " VALUES (%(start_tv_sec)s,"
        "         %(start_tv_usec)s,"
        "         %(ip)s)")

        data_session = {
            'start_tv_sec': cur_time.sec,
            'start_tv_usec': cur_time.usec,
            'ip': ip,
        }

        self.execute(add_session_sql, data_session)
        self.session_id = ModelBase.cursor.lastrowid

        return

    def __del__(self):
        """
        回收session时，向session当中写入session结束的时间
        :return:
        """
        update_session = ("UPDATE session "
                          "SET `end_tv_sec` = %(end_tv_sec)s,`end_tv_usec` = %(end_tv_usec)s "
                          "WHERE `session_id` = %(session_id)s")

        # update session information
        timestamp = Timestamp.cur()
        data_session = {
            'end_tv_sec': timestamp.sec,
            'end_tv_usec': timestamp.usec,
            'session_id': self.session_id,
        }

        print("delete session,update end time",self.ip)

        self.execute(update_session,data_session)

        pass

    @property
    def series_state(self):
        """
        获取双系状态值
        :return:双系状态
        """
        return self._series_state

    @series_state.setter
    def series_state(self,state):
        """
        设置双系状态值，这里会跟踪双系状态是否发生变化，若发生变化应该特殊处理
        :param value:
        :return:
        """
        if self._series_state == state:
            return
        elif self._series_state != state and self._series_state != 0:
            self.b_switch = True
            # 发生切换，等待检查是否过期并回收本session
            return

        self._series_state = state

        update_session = ("UPDATE session "
                          "SET `series_state` = %(series_state)s "
                          "WHERE `session_id` = %(session_id)s")

        # update session information
        data_session = {
            'series_state':self._series_state,
            'session_id': self.session_id,
        }
        self.execute(update_session,data_session)

        return

    @property
    def cpu_state(self):
        return self._cpu_state

    @cpu_state.setter
    def cpu_state(self,state):
        if self._cpu_state == state:
            return

        self._cpu_state = state

        update_session = ("UPDATE session "
                          "SET `cpu_state` = %(cpu_state)s "
                          "WHERE `session_id` = %(session_id)s")

        # update session information
        data_session = {
            'cpu_state':self._cpu_state,
            'session_id': self.session_id,
        }

        self.execute(update_session,data_session)

        return

    def keep_alive(self):
        """
        调用该函数存储session的访问时间，使其在检查session是否过期的时候正确检查
        """
        self.last_timestamp = Timestamp.cur()
        return

    def check_expired(self):
        """
        检查Session是否过期
        :return:
        """
        cur_timestamp = Timestamp.cur()

        if cur_timestamp.sec - self.last_timestamp.sec > 10:
            return True

        return self.b_switch
