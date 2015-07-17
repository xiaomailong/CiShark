# -*- coding: utf-8 -*-
__author__ = 'Administrator'

from .ModelBase import ModelBase
import time

class Log(ModelBase):
    """

    """
    def __init__(self, table_name):
        """

        """
        super().__init__()
        self.table_name = table_name
        self.add_log_stmt = "INSERT INTO {0}(session_id, log_tv_sec, log_tv_usec,log_type,log_content) " \
                            "VALUES (%s,%s,%s,%s,%s)".format(table_name)
        # 确保天表已经被建立
        self.check_partition_day_table()
        return

    def check_partition_day_table(self):
        """
        in order to avoid log db file too large,storage data every day
        this also simplified method of delete db file which we considered unuse.
        create if partition table not exist
        """
        query = ("SHOW TABLES LIKE '%s'" % self.table_name)
        ModelBase.cursor.execute(query)
        item = ModelBase.cursor.fetchone()
        if item == None:
            # it's say that table not created,so we need create it
            query = ("CREATE TABLE {0} as (SELECT * FROM log)".format(self.table_name))
            ModelBase.cursor.execute(query)
            pass
        return

def insert_logs(data):
    """
    """
    cur_time = time.localtime()
    cur_time_str = "{0:04}{1:02}{2:02}".format(cur_time.tm_year,cur_time.tm_mon,cur_time.tm_mday)
    #cur_time_str = "{0:04}{1:02}".format(cur_time.tm_year,cur_time.tm_mon)
    table_name = "log" + cur_time_str

    model = Log(table_name)
    model.executemany(model.add_log_stmt,data)

    return

