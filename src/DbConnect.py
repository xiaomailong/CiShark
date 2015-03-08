# /usr/bin/python3
# author: zhangys
# date  : 20140904
# ver   : 1.0
#
# session of ci

import mysql.connector
import MysqlConfig
import time

__all__ = [ "get_power_on_counter" ,
            "get_session_id" ,
            "get_log_type" ,
            "get_cpu_state_id" ,
            "get_series_state_id" ,
            "get_switch_type_id" ,
            "cursor",
            ]

__version__ = "1.0.2"

# check cursor exist or not
if 'cursor' not in locals():
    try:
        cnx = mysql.connector.connect(**MysqlConfig.config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exists")
        else:
            print(err)

    cursor = cnx.cursor()

def get_power_on_counter():
    """
    read maximum run counter from session table
    """
    query = ("SELECT MAX(run_counter) as max_run_counter FROM SESSION")
    cursor.execute(query)
    max_run_counter = cursor.fetchone()[0]
    if max_run_counter == None:
        return 0
    else:
        return int(max_run_counter)

    return

def get_session_id():
    """
    read maximum session id from session table
    """
    query = ("SELECT MAX(session_id) as max_session_id FROM SESSION")
    cursor.execute(query)
    max_session_id = cursor.fetchone()[0]
    if max_session_id == None:
        return 0
    else:
        return int(max_session_id)
    pass

def check_partition_table_day():
    """
    in order to avoid log db file too large,storage data every day
    this also simplified method of delete db file which we considered unuse.
    create if partition table not exist
    """
    cur_time = time.localtime()
    cur_time_str = "{0:04}{1:02}{2:02}".format(cur_time.tm_year,cur_time.tm_mon,cur_time.tm_mday)
    table_name = "log" + cur_time_str
    query = ("SHOW TABLES LIKE '%s'" % table_name)
    cursor.execute(query)
    item = cursor.fetchone()
    if item == None:
        # it's say that table not created,so we need create it
        query = ("CREATE TABLE {0} as (SELECT * FROM log)".format(table_name))
        cursor.execute(query)
        pass
    return

def check_partition_table_month():
    """
    in order to avoid log db file too large,storage data every month.
    this also simplified method of delete db file which we considered unuse.
    create if partition table not exist
    """
    cur_time = time.localtime()
    cur_time_str = "{0:04}{1:02}".format(cur_time.tm_year,cur_time.tm_mon)
    table_name = "log" + cur_time_str
    query = ("SHOW TABLES LIKE '%s'" % table_name)
    cursor.execute(query)
    item = cursor.fetchone()
    if item == None:
        # it's say that table not created,so we need create it
        query = ("CREATE TABLE {0} as (SELECT * FROM log)".format(table_name))
        cursor.execute(query)
        pass
    return

log_type_dict = {}
series_type_dict = {}
cpu_type_dict = {}
switch_type_dict = {}

def init_log_type_dict():
    """
    """
    global log_type_dict
    query = (" SELECT enum_name,fd_value"
             " FROM data_dict"
             " WHERE tb_name = 'log' AND fd_name = 'log_type'")
    cursor.execute(query)
    values = cursor.fetchall()
    log_type_dict = dict(values)
    #print(log_type_dict['cpu_cfg_send_fail_a'])
    return

def init_series_type_dict():
    global series_type_dict
    query = (" SELECT enum_name,fd_value"
             " FROM data_dict"
             " WHERE tb_name = 'session' AND fd_name = 'series_state'")
    cursor.execute(query)
    values = cursor.fetchall()
    series_type_dict = dict(values)
    #print(series_type_dict)
    #print(series_type_dict['series_master'])

def init_cpu_type_dict():
    """
    """
    global cpu_type_dict
    query = (" SELECT enum_name,fd_value"
             " FROM data_dict"
             " WHERE tb_name = 'session' AND fd_name = 'cpu_state'")
    cursor.execute(query)
    values = cursor.fetchall()
    cpu_type_dict = dict(values)
    #print(cpu_type_dict)
    #print(cpu_type_dict['cpu_master'])

def init_switch_type_dict():
    """
    """
    global switch_type_dict
    query = (" SELECT enum_name,fd_value"
             " FROM data_dict"
             " WHERE tb_name = 'session' AND fd_name = 'switch_type'")
    cursor.execute(query)
    values = cursor.fetchall()
    switch_type_dict = dict(values)
    #print(switch_type_dict)
    #print(switch_type_dict['master_to_check'])

def get_log_type(enum_name):
    if len(log_type_dict) <= 0:
        init_log_type_dict()
    return log_type_dict.get(enum_name,0)

def get_series_state_id(state_str):
    """
    read series_state value from db
    """
    if len(series_type_dict) <= 0:
        init_series_type_dict()
    return series_type_dict.get(state_str,0)

def get_cpu_state_id(state_str):
    """
    read cpu_state value from db
    """
    if len(cpu_type_dict) <= 0:
        init_cpu_type_dict()
    #print(cpu_type_dict)
    return cpu_type_dict.get(state_str,0)

def get_switch_type_id(type_str):
    """
    read switch type value from db
    """
    if len(switch_type_dict) <= 0:
        init_series_type_dict()
    return switch_type_dict.get(type_str,0)

if __name__ == "__main__":
    #init_log_type_dict()
    #init_series_type_dict()
    #get_cpu_state_id("cpu_master")
    #init_switch_type_dict()
    check_partition_table_day()
    check_partition_table_month()
