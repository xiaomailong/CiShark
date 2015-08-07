# CiShark

CiShark为联锁程序提供日志记录服务。由于CF卡大小限制，CI不能将产生的日志信息全部记录下来，我们对联锁程序使用如下日志模型：

    CIHmi_SendTips           向控显机发送的数据也会发送向远端日志服务器
       |
    CIRemoteLog              调用RemoteLog会间接调用CILog_Msg，RemoteLog即CIShark。
       |
    CILog_Msg--------------  调用CILog_Msg会向下面3层传递数据
       |          |       |
    CILocalLog CITailLog  stdout

CiShark保证了联锁日志的完整性，该程序运行是否正常决定了是否能够重现事故现场环境，对运维尤其重要。

# 主要功能

1. 存储多台联锁程序的日志信息。
2. 使用Mysql实现数据结构化管理。
3. 使用天表分割日志，能方便拷贝。
4. 提供简单接口能查询日志。

# DEPENDENCIES

1. Windows环境
2. Python3.4
3. Mysql
4. mysql-connector-python-2.0.0-py3.4

# HOW TO INSTALL

1. 下载代码至C盘。推荐使用C盘。
2. 创建数据库ci_log。
3. 依次在数据库当中执行DebugSql目录下的create\*.sql，get\*.sql，v\*.sql。
4. 在更改[cishark/db/MysqlConfig.py](cishark/db/MysqlConfig.py)确保数据库用户名和密码正确。
5. 双击[main.py](main.py)尝试运行。

详细文档请见内部手册。

# TODO

1. 以Windows服务程序运行CIShark。
2. 整理无用代码，使逻辑更加清晰。
3. 请解决有时Windows开机不能启动的bug。

