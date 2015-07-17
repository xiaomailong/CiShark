# -*- coding: utf-8 -*-
__author__ = 'Administrator'

import mysql.connector
from mysql.connector import errorcode
from . import MysqlConfig

class ModelBase:
    """
    数据模型基类
    """
    try:
        cnx = mysql.connector.connect(**MysqlConfig.config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exists")
        else:
            print(err)

    # print("init ModelBase cursor")
    cursor = cnx.cursor()

    def __init__(self):
        pass

    def execute(self,sql,data):
        """
        执行sql语句
        :return:
        """
        try:
            ModelBase.cursor.execute(sql,data)
        except mysql.connector.Error as err:
            print(ModelBase.cursor.statement)
            print("Something went wrong: {}".format(err))
        return

    def executemany(self,sql,data):
        """
        一次插入多条数据
        :return:
        """
        try:
            ModelBase.cursor.executemany(sql,data)
        except mysql.connector.Error as err:
            print(ModelBase.cursor.statement)
            print("Something went wrong: {}".format(err))
        #print(cursor.statement)
        return
