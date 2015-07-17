# -*- coding: utf-8 -*-

from cishark import RecordServer

if __name__ == "__main__":
    recorder = RecordServer(port = 3003)
    recorder.serve_forever()
