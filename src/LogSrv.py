#-*- coding:utf-8 -*-
import win32serviceutil
import win32service
import win32event

class LogSrv(win32serviceutil.ServiceFramework):

    _svc_name_ = "LogSrv"
    _svc_display_name_ = "Ci log service"
    _svc_description_ = "This service used to record all log infomation send by CI machine"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = self._getLogger()
        self.isAlive = True

    def _getLogger(self):
        import logging
        import os
        import inspect

        logger = logging.getLogger('[LogSrv]')

        this_file = inspect.getfile(inspect.currentframe())
        dirpath = os.path.abspath(os.path.dirname(this_file))
        handler = logging.FileHandler(os.path.join(dirpath, "log_srv.log"))

        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger

    def SvcDoRun(self):
        from Recorder import NetUdpRecorder
        from DbConnect import get_power_on_counter
        from subprocess import Popen, PIPE

        power_on_counter = get_power_on_counter()
        recorder = NetUdpRecorder(port = 3005)
        recorder.do_record()

        run_proc = Popen(["python", "Recorder.py"],
                        stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False,
                         cwd="D:\\HJ\\ci\\tools\\CIShark\\server0.02")

        #why this can't stop?
        #res, err = run_proc.communicate()
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
        run_proc.kill() # kill sub process

    def SvcStop(self):
        self.logger.error("svc do stop....")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

if __name__=='__main__':
    win32serviceutil.HandleCommandLine(LogSrv)
