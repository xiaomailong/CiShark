# /usr/bin/python3

from DbConnect import cursor
import time
from Timestamp import Timestamp

log_file_name = "TimerInterval.txt"
f = open(log_file_name,"w+")
table_name = "log20140929"

last_timestamp = Timestamp()
last_sn = -1

def get_count(session_id):
    query = (" SELECT count(*)                                                      "
             " FROM `{0}`                                                           "
             " WHERE session_id = {1} AND log_type = get_log_type_id('timer_enter') "
             .format(table_name,session_id)
            )

    print("query data count(it will take a long time)...")
    cursor.execute(query)
    count = cursor.fetchone()
    print("count:",count)
    return int(count[0])

def get_timer_interval_limit(session_id,begin,end):
    """
    use page instead of select all data at once avoid data too large to
    crash
    """
    global last_timestamp
    global last_sn
    query = (" SELECT log_tv_sec,log_tv_usec,log_content        "
             " FROM `{0}`                               "
             " WHERE session_id = {1} AND log_type = get_log_type_id('timer_enter') "
             " LIMIT {2},{3}".format(table_name,session_id,begin,end)
            )
    print("query {0},{1}".format(begin,end))
    cursor.execute(query)
    rows = cursor.fetchall()

    for sec,usec,sn in rows:
        timestamp = Timestamp(int(sec),int(usec))
        sn = int(sn,16)
        if sn - last_sn == 1:
            interval = timestamp - last_timestamp
            # if it's great than 100ms,tell me
            if interval > 100000:
                print(interval / 1000.0,end="")
            s = "{0},".format(interval / 1000.0)
            f.write(s)
            pass

        last_sn = sn
        last_timestamp = timestamp
    return

def get_timer_interval(session_id):
    """
    get all timer information from db,and then calculate interval
    between of its,this is useful for analysis system performance.
    """

    count= get_count(session_id)
    i = 0
    # select 5000 data once
    page_size = 5000
    while i < count:
        get_timer_interval_limit(session_id,i,i + page_size)
        i += page_size

    f.write("\n")
    print()

    return

if __name__ == "__main__":
    #get_count(236)
    get_timer_interval(236)
    pass

