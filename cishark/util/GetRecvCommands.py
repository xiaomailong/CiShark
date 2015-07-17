# /usr/bin/python3

from DbConnect import cursor

log_file_name = "GetRecvCommandsResult.txt"
table_name = "log20140929"
f = open(log_file_name,"w+")

def get_recv_commands(session_id):
    query = (" SELECT log_content"
            " FROM {0}"
            " WHERE session_id = {1} AND log_type = get_log_type_id('eeu_recv_commands')"
            " ORDER BY log_tv_sec,log_tv_usec".format(table_name,session_id))

    cursor.execute(query)
    rows = cursor.fetchall()
    print(cursor.statement)
    commands_dict = {}
    for row in rows:
        #tuple first item
        row = row[0].rstrip(",")
        commands_list = row.split(",")
        for command_item in commands_list:
            commands_info = command_item.split(":")
            addr = commands_info[0]
            ga = int(addr.split("-")[0])
            ea = int(addr.split("-")[1])
            commands = commands_info[1]
            commands_dict[(ga,ea)] = commands
            s = "[{0}-{1}:{2}]\t".format(ga,ea,commands)
            print(s)
            f.write(s)
        f.write("\t{0}\t".format(len(commands_dict)))
        for item in sorted(commands_dict):
            s = "{0}-{1}:{2}\t".format(item[0],item[1],commands_dict[item])
            print(s,end = "")
            f.write(s)
        f.write("\n")
        print()
    return

if __name__ == "__main__":
    get_recv_commands(7)
