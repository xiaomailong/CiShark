Dim WinScriptHost
Set WinScriptHost = CreateObject("WScript.Shell")
WinScriptHost.Run "C:\Python34\python.exe C:\CIShark\server0.02\Recorder.py" & Chr(34),0
Set WinScriptHost = NoThing