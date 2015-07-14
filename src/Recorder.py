# /usr/bin/python3
# author: zhangys
# date  : 20140904
# ver   : 1.2
#
# ci log file recorder

from Session import Session
from xxd import xxd_bin
import socketserver
from DbConnect import get_power_on_counter
from DbConnect import check_partition_table_day
from DbConnect import check_partition_table_month

__version__ = "1.0.2"

sessions = dict()
power_on_counter = 0

class UdpRecorderHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global sessions
        global power_on_counter
        data = self.request[0]
        address = self.client_address[0]
        #print("{0} wrote {1}".format(address,len(data)))
        #xxd_bin(data)

        # delete expired session
        sessions = {addr: sessions[addr] for addr in sessions if sessions[addr].check_expired() == False}

        # all session have expired,its meaning system is stop
        if len(sessions) == 0:
            power_on_counter += 1

        if address not in sessions:
            # if not exist,we create it
            sessions[address] = Session(address,power_on_counter)

        check_partition_table_day()
        # pass data in
        sessions[address].parse_data(data)

class NetUdpRecorder():
    """
    read all data from net
    """
    def __init__(self,port):
        """
        listen a port,and record every thing send to this port
        """
        self.port = port
        self.host = "192.168.1.106"
        #self.host = "localhost"
        return

    def do_record(self):
        """
        begin record data
        """
        #HOST, PORT = self.host, self.port
        HOST, PORT = self.host, self.port
        server = socketserver.UDPServer((HOST, PORT), UdpRecorderHandler)
        #print("listening..")
        server.serve_forever()
        return

if __name__ == "__main__":
    power_on_counter = get_power_on_counter()
    recorder = NetUdpRecorder(port = 3003)
    recorder.do_record()


