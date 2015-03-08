# /usr/bin/python3
# author: zhangys
# date  : 20140919
# ver   : 1.0
#         1.3 insert data into partition table
#
# session of ci

from Timestamp import *
from DbConnect import *
import mysql.connector
import time

__all__ = [ "Session" ,"parse_data" ]

__version__ = "1.0.2"

class Session:
    """
    """
    # conrresponding to run_record table run_id

    def __init__(self,ip,power_on_counter):
        self.add_log_data = []
        self.last_timestamp = Timestamp()
        self.session_id = 0
        self.should_be_exit = False
        self.b_expired = False
        self.series_state = 0
        self.cpu_state = 0
        self.power_on_counter = power_on_counter
        self.ip = ip

        add_session = ("INSERT INTO session (run_counter,start_tv_sec, start_tv_usec,ip) "
                      " VALUES (%(run_counter)s,"
                      "         %(start_tv_sec)s,"
                      "         %(start_tv_usec)s,"
                      "         %(ip)s)")

        cur_time = get_local_timestamp()
        # Insert session information
        data_session = {
          'run_counter': power_on_counter,
          'start_tv_sec': cur_time.sec,
          'start_tv_usec': cur_time.usec,
          'ip': ip,
        }

        try:
            cursor.execute(add_session,data_session)
        except mysql.connector.Error as err:
            print(cursor.statement)
            print("Something went wrong: {}".format(err))

        self.session_id = cursor.lastrowid
        return

    def log_cache_push(self):
        if len(self.add_log_data) == 0:
            return

        try:
            cur_time = time.localtime()
            cur_time_str = "{0:04}{1:02}{2:02}".format(cur_time.tm_year,cur_time.tm_mon,cur_time.tm_mday)
            #cur_time_str = "{0:04}{1:02}".format(cur_time.tm_year,cur_time.tm_mon)
            table_name = "log" + cur_time_str
            add_log_stmt = "INSERT INTO {0}(session_id, log_tv_sec, log_tv_usec,log_type,log_content) VALUES (%s,%s,%s,%s,%s)".format(table_name)

            cursor.executemany(add_log_stmt,self.add_log_data)
            # execute over.clear it
            self.add_log_data = []
        except mysql.connector.Error as err:
            print(cursor.statement)
            print("Something went wrong: {}".format(err))
        #print(cursor.statement)
        return

    def check_expired(self):
        """
        check session is expired
        """
        cur_timestamp = get_local_timestamp()

        if cur_timestamp.sec - self.last_timestamp.sec > 3:
            self.log_cache_push()
            self.system_exit()
            return True

        return self.b_expired

    def parse_one_log_str(self,log_str):
        """
        log_str ie. 1410226035.173226]cpu_cfg_recv_begin
        bracket of head has deleted
        """
        log_str = log_str.strip()
        # min length is 19,ie.[1409556974.011691]......
        if 19 > len(log_str):
            #print("len length 19 > %d" % len(log_str))
            return

        items = log_str.split("]")
        if len(items) < 2:
            print("data is wrong %s" % log_str)
            return

        #print(items)
        timestamp = get_timestamp(items[0])
        if timestamp == None:
            return False
        log_info = items[1]
        log_info_items = log_info.split(":")
        log_type = log_info_items[0]
        self.log_content = log_info_items[1:]

        log_type_id = get_log_type(log_type)

        content = log_info
        if 0 == log_type_id:
            #print(content)
            pass
        elif get_log_type("system_exit") == log_type_id:
            content = ":".join(self.log_content)
            print(content)
            self.system_exit()
        elif get_log_type("system_state") == log_type_id:
            self.parse_system_state(self.log_content)
            # system state message service for this program,not necessary record
            return;
        elif get_log_type("cpu_state") == log_type_id:
            # get cpu state
            self.update_cpu_state(get_cpu_state_id(self.log_content[0]))
        elif get_log_type("series_state") == log_type_id:
            # get series state
            self.update_series_state(get_series_state_id(self.log_content[0]))
        else:
            content = ":".join(self.log_content)

        data = [self.session_id,timestamp.sec,timestamp.usec,log_type_id,content]
        self.add_log_data.append(data)

        #print(data)
        if len(self.add_log_data) < 1000 and self.b_expired == False:
            return
        else:
            self.log_cache_push()

    def parse_system_state(self,state_str_list):
        """
        system state will change because switch
        """
        if len(state_str_list) < 2:
            #print("parse_system_state state_str_list < 2",state_str_list)
            return False

        series_state = int(state_str_list[0])
        cpu_state = int(state_str_list[0])

        if series_state != self.series_state and self.series_state != 0 and self.cpu_state != 0:
            # do switch job,
            # 1.push all current data,
            # 2.update session end timestamp
            # 3.INSERT new session data in order to get sessino_id
            # 4.change series and cpu state
            # 5.record new session parent session_id
            self.log_cache_push()
            self.system_exit()
            self.b_expired = False
            parent_id = self.session_id

            add_session = ("INSERT INTO session (run_counter,parent_id,start_tv_sec, start_tv_usec,series_state,cpu_state,ip) "
                          " VALUES (%(run_counter)s,  "
                          "         %(parent_id)s,    "
                          "         %(start_tv_sec)s, "
                          "         %(start_tv_usec)s,"
                          "         %(series_state)s, "
                          "         %(cpu_state)s,    "
                          "         %(ip)s)           ")

            cur_time = get_local_timestamp()
            # Insert session information
            data_session = {
              'run_counter': self.power_on_counter,
              'parent_id': parent_id,
              'start_tv_sec': cur_time.sec,
              'start_tv_usec': cur_time.usec,
              'series_state': series_state,
              'cpu_state': cpu_state,
              'ip': self.ip,
            }

            try:
                cursor.execute(add_session,data_session)
            except mysql.connector.Error as err:
                print(cursor.statement)
                print("Something went wrong: {}".format(err))

            self.session_id = cursor.lastrowid

            pass

        self.series_state = int(state_str_list[0])
        self.cpu_state = int(state_str_list[1])

        update_session = ("UPDATE session "
                          "SET `series_state` = %(series_state)s,`cpu_state` = %(cpu_state)s "
                          "WHERE `session_id` = %(session_id)s")

        # update session information
        data_session = {
          'series_state':self.series_state,
          'cpu_state':self.cpu_state,
          'session_id': self.session_id,
        }

        try:
            cursor.execute(update_session,data_session)
        except mysql.connector.Error as err:
            print(cursor.statement)
            print("Something went wrong: {}".format(err))
        return

    def parse_data(self,data):
        """
        parse log string
        """
        # check type
        if type(data) is not bytes:
            print("data type is not bytes %s" % type(data))
            return

        log_strs = data.decode('utf-8')
        #print(self.session_id,log_strs)
        log_str_list = log_strs.split('[')
        for log_str in log_str_list:
            self.parse_one_log_str(log_str)

        self.last_timestamp = get_local_timestamp()

    def update_cpu_state(self,cpu_state):
        self.cpu_state = cpu_state

        update_session = ("UPDATE session "
                          "SET `cpu_state` = %(cpu_state)s "
                          "WHERE `session_id` = %(session_id)s")

        # update session information
        data_session = {
          'cpu_state':self.cpu_state,
          'session_id': self.session_id,
        }

        try:
            cursor.execute(update_session,data_session)
        except mysql.connector.Error as err:
            print(cursor.statement)
            print("Something went wrong: {}".format(err))
        return

    def update_series_state(self,series_state):
        self.series_state = series_state

        update_session = ("UPDATE session "
                          "SET `series_state` = %(series_state)s "
                          "WHERE `session_id` = %(session_id)s")

        # update session information
        data_session = {
          'series_state':self.series_state,
          'session_id': self.session_id,
        }

        try:
            cursor.execute(update_session,data_session)
        except mysql.connector.Error as err:
            print(cursor.statement)
            print("Something went wrong: {}".format(err))
        return

    def system_exit(self):
        """
        ci is exit now
        """
        update_session = ("UPDATE session "
                        "SET `end_tv_sec` = %(end_tv_sec)s,`end_tv_usec` = %(end_tv_usec)s "
                        "WHERE `session_id` = %(session_id)s")

        # update session information
        timestamp = get_local_timestamp()
        data_session = {
          'end_tv_sec': timestamp.sec,
          'end_tv_usec': timestamp.usec,
          'session_id': self.session_id,
        }

        try:
            cursor.execute(update_session,data_session)
        except mysql.connector.Error as err:
            print(cursor.statement)
            print("Something went wrong: {}".format(err))

        self.b_expired = True

        return

if __name__ == "__main__":
    session = Session(2222)
