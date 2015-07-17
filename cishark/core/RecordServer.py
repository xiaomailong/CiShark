# -*- coding: utf-8 -*-
__author__ = 'Administrator'

import socketserver
import socket

from cishark.db import Session,DataDict,insert_logs
from cishark.util import Timestamp

class RecordRequestHandler(socketserver.BaseRequestHandler):
    """
    处理数据请求
    """
    sessions = {}
    caching_log_data = []

    def handle(self):
        """
        接收数据，并存储数据
        """
        data = self.request[0]
        address = self.client_address[0]
        if address not in RecordRequestHandler.sessions:
            # if not exist,create new session
            RecordRequestHandler.sessions[address] = Session(address)

        self.cur_session =  RecordRequestHandler.sessions[address]

        self.cache_data(data)

        self.cur_session.keep_alive()

        return

    @staticmethod
    def check_expired():
        """
        检查过期的session，并将其从session表中删除掉
        """
        # print("checking expired")
        sessions = RecordRequestHandler.sessions
        RecordRequestHandler.sessions = {addr:sessions[addr] for addr in sessions
                                         if sessions[addr].check_expired() == False}

        RecordRequestHandler.save_cache_data()

        return

    def _parse_one_log_str(self,log_str):
        """
        :param log_str:
        :return:timestamp,log_type_id,log_content
        """
        log_str = log_str.strip()
        # min length is 19,ie.[1409556974.011691]......
        if 19 > len(log_str):
            # print("len length 19 > %d" % len(log_str))
            return None,None,None

        try:
            timestamp,log_info = log_str.split(']')
        except ValueError as err:
            print("data is wrong {0}:{1}".format(log_str))
            return None,None,None

        timestamp = Timestamp.from_str(timestamp)

        items = log_info.split(":")
        if len(items) < 2:
            return timestamp,0,log_info
        else:
            log_type = items[0]
            log_content = items[1:]

        log_type_id = DataDict.get_log_type_id(log_type)

        if log_type_id == 0:
            content = log_info
        else:
            content = ":".join(log_content)

        return timestamp,log_type_id,content

    def _cache_one_log_str(self,log_str):
        """
        log_str ie. 1410226035.173226]cpu_cfg_recv_begin
        bracket of head has deleted
        """
        timestamp,log_type_id,content = self._parse_one_log_str(log_str)
        if timestamp == None and log_type_id == None and content == None:
            return

        # print(timestamp,log_type_id,content)

        data = [self.cur_session.session_id,timestamp.sec,timestamp.usec,log_type_id,content]

        if DataDict.get_log_type_id("system_state") == log_type_id:
            self.cur_session.series_state,self.cur_session.cpu_state = content.split(":")

        RecordRequestHandler.caching_log_data.append(data)

        return

    def cache_data(self,data):
        """
        分析数据
        """
        # check type
        if type(data) is not bytes:
            print("data type is not bytes %s" % type(data))
            return

        log_strs = data.decode('utf-8')
        #print(log_strs)
        log_str_list = log_strs.split('[')
        for log_str in log_str_list:
            self._cache_one_log_str(log_str)

        if len(RecordRequestHandler.caching_log_data) < 1000:
            return
        else:
            RecordRequestHandler.save_cache_data()

        return

    @staticmethod
    def save_cache_data():
        """
        将缓存当中的数据保存到数据库当中
        """
        insert_logs(RecordRequestHandler.caching_log_data)
        return

class RecordServer(socketserver.UDPServer):
    """
    日志记录服务程序
    """
    timeout = 1 # 1s

    def __init__(self,port):
        """
        重写init函数，我们不需要指定ip地址，只需要端口地址
        :param port: 端口地址
        :return:无
        """
        #addr = (socket.gethostname(),port)
        addr = ("192.168.1.109",port)
        super(RecordServer,self).__init__(addr,RecordRequestHandler)
        print("listen",addr)

    def service_actions(self):
        """
        该函数在serve_forever当中调用，每次超时后都会调用
        :return:
        """
        self.RequestHandlerClass.check_expired()
        return

