# IoTControlAndMonitoringWebSystem
Devices Control and Monitoring Django Web App to Handle MQTT Protocol in the IoT Cotext

只是一个简单的物联网,可视化demo

## 1.安装，启动django服务:

pip install requiremets.txt

安装后

"""可能出现mysqlclient错误error"""
  File "D:\物联网\IoTControl\enviot\lib\site-packages\MySQLdb\connections.py", line 179, in __init__
    super(Connection, self).__init__(*args, **kwargs2)
django.db.utils.OperationalError: (2059, <NULL>
怀疑mysqlclient问题，
改为安装使用pymsql，init下
import pymysql
pymysql.install_as_MySQLdb()
后续:  File "D:\物联网\IoTControl\enviot\lib\site-packages\django\db\backends\mysql\operations.py", line 146, in last_executed_query
    query = query.decode(errors='replace')
AttributeError: 'str' object has no attribute 'decode',改为encode
接着migrate
启动成功
享用

## 2.可视化:

使用mqttfx模拟推送数据(前置条件必须有mqtt服务,如何搭建见我另一个库iot)
比如选择DHT22/temperature
几个数据后发布,点开echarts刷新,会发现有temperatur的图表





