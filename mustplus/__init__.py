"""
Hey, PyLint? SHUT UP
"""
import pymysql

pymysql.install_as_MySQLdb()

# import time
# import threading
#
#
# def thread_heartbeat():
#     while True:
#         time.sleep(5)
#         print("Heartbeat", time.time())
#
#
# x = threading.Thread(target=thread_heartbeat)
# x.start()
