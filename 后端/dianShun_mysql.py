import pymysql
import taos
import time
from datetime import datetime, timedelta
import threading

def read_tdengine_and_write_mysql():
    # 连接TDengine数据库（远程主机）
    try:
        td_conn = taos.connect(host='10.10.10.130', user='root', password='taosdata', database='jinshen', port=6030)  # 远程主机IP
        td_cursor = td_conn.cursor()
        print("Successfully connected to TDengine")
    except Exception as e:
        print(f"TDengine connection error: {e}")
        return

    # 连接MySQL数据库（本机）
    try:
        mysql_conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='js',
                                     charset='utf8')  # 本机IP
        mysql_cursor = mysql_conn.cursor()
        print("Successfully connected to MySQL")
    except Exception as e:
        print(f"MySQL connection error: {e}")
        return

    # TDengine中的表名
    tables = [
        'CY_PLC3_012',
    ]

    # 无限循环以检查新数据
    while True:
        # 获取今天的日期
        today_date = datetime.now().date()

        # 从每个表读取当天的数据
        for table in tables:
            try:
                # 将时间加上 8 小时
                start_time = f"{today_date} 00:00:00"
                start_time_obj = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
                start_time = start_time_obj.strftime('%Y-%m-%d %H:%M:%S')

                end_time = f"{today_date} 23:59:59"
                end_time_obj = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
                end_time = end_time_obj.strftime('%Y-%m-%d %H:%M:%S')

                query = f"SELECT ts, fvalue FROM {table} WHERE ts >= '{start_time}' AND ts <= '{end_time}'"
                td_cursor.execute(query)
                data = td_cursor.fetchall()

                for row in data:
                    ts = row[0].strftime('%Y-%m-%d %H:%M:%S')
                    fvalue = row[1]

                    # 过滤每10分钟的数据  if ts_datetime.minute % 4 == 0 and ts_datetime.second == 0:
                    ts_datetime = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
                    if ts_datetime.second % 10 == 0:
                        ts_adjusted = (ts_datetime - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')

                        try:
                            # 获取最新 ratio
                            mysql_cursor.execute("SELECT ratio FROM dian_ratio ORDER BY id DESC LIMIT 1")
                            ratio_result = mysql_cursor.fetchone()
                            ratio = ratio_result[0] if ratio_result else 1
                            if ratio is None or ratio == 0:
                                ratio = 1

                            # 乘上 ratio
                            adjusted_fvalue = fvalue * ratio

                            # 检查数据是否已经存在
                            mysql_cursor.execute('SELECT COUNT(*) FROM cy_plc3_012 WHERE tS = %s', (ts_adjusted,))
                            exists = mysql_cursor.fetchone()[0]

                            if exists == 0:
                                mysql_cursor.execute(
                                    'INSERT INTO cy_plc3_012 (tS, aValue) VALUES (%s, %s)',
                                    (ts_adjusted, adjusted_fvalue)
                                )
                        except Exception as e:
                            print(f"Error writing data to MySQL: {e}")

            except Exception as e:
                print(f"Error reading data from table {table}: {e}")

        # 提交事务
        try:
            mysql_conn.commit()
            print("Transaction committed")
        except Exception as e:
            print(f"Error committing transaction: {e}")

        # 等待一段时间后再检查
        time.sleep(20)  # 每10分钟检查一次

def read_tdengine_and_write_mysql_1():
    # 连接TDengine数据库（远程主机）
    try:
        td_conn = taos.connect(host='10.10.10.130', user='root', password='taosdata', database='jinshen', port=6030)  # 远程主机IP
        td_cursor = td_conn.cursor()
        print("Successfully connected to TDengine")
    except Exception as e:
        print(f"TDengine connection error: {e}")
        return

    # 连接MySQL数据库（本机）
    try:
        mysql_conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='js',
                                     charset='utf8')  # 本机IP
        mysql_cursor = mysql_conn.cursor()
        print("Successfully connected to MySQL")
    except Exception as e:
        print(f"MySQL connection error: {e}")
        return

    # TDengine中的表名
    tables = [
        'CY_PLC3_012',
    ]

    # 无限循环以检查新数据
    while True:
        # 获取今天的日期
        today_date = datetime.now().date()

        # 从每个表读取当天的数据
        for table in tables:
            try:
                # 将时间加上 8 小时
                start_time = f"{today_date} 00:00:00"
                start_time_obj = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
                start_time = start_time_obj.strftime('%Y-%m-%d %H:%M:%S')

                end_time = f"{today_date} 23:59:59"
                end_time_obj = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
                end_time = end_time_obj.strftime('%Y-%m-%d %H:%M:%S')

                query = f"SELECT ts, fvalue FROM {table} WHERE ts >= '{start_time}' AND ts <= '{end_time}'"
                td_cursor.execute(query)
                data = td_cursor.fetchall()

                for row in data:
                    ts = row[0].strftime('%Y-%m-%d %H:%M:%S')
                    fvalue = row[1]

                    # 过滤每10分钟的数据  if ts_datetime.minute % 4 == 0 and ts_datetime.second == 0:
                    ts_datetime = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
                    if ts_datetime.second % 10 == 0:
                        ts_adjusted = (ts_datetime - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')

                        try:
                            # 获取最新 ratio
                            mysql_cursor.execute("SELECT ratio FROM dian_ratio ORDER BY id DESC LIMIT 1")
                            ratio_result = mysql_cursor.fetchone()
                            ratio = ratio_result[0] if ratio_result else 1
                            if ratio is None or ratio == 0:
                                ratio = 1

                            # 乘上 ratio
                            adjusted_fvalue = fvalue * ratio

                            # 检查数据是否已经存在
                            mysql_cursor.execute('SELECT COUNT(*) FROM dian_mysql WHERE tS = %s', (ts_adjusted,))
                            exists = mysql_cursor.fetchone()[0]

                            if exists == 0:
                                mysql_cursor.execute(
                                    'INSERT INTO dian_mysql (tS, aValue) VALUES (%s, %s)',
                                    (ts_adjusted, adjusted_fvalue)
                                )
                        except Exception as e:
                            print(f"Error writing data to MySQL: {e}")

            except Exception as e:
                print(f"Error reading data from table {table}: {e}")

        # 提交事务
        try:
            mysql_conn.commit()
            print("Transaction committed")
        except Exception as e:
            print(f"Error committing transaction: {e}")

        # 等待一段时间后再检查
        time.sleep(20)  # 每10分钟检查一次


def read_tdengine_and_write_mysql_002():
    # 连接TDengine数据库（远程主机）
    try:
        td_conn = taos.connect(host='10.10.10.130', user='root', password='taosdata', database='jinshen',
                               port=6030)  # 远程主机IP
        td_cursor = td_conn.cursor()
        print("Successfully connected to TDengine")
    except Exception as e:
        print(f"TDengine connection error: {e}")
        return

    # 连接MySQL数据库（本机）
    try:
        mysql_conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='js',
                                     charset='utf8')  # 本机IP
        mysql_cursor = mysql_conn.cursor()
        print("Successfully connected to MySQL")
    except Exception as e:
        print(f"MySQL connection error: {e}")
        return

    # TDengine中的表名
    tables = [
        'cy_plc3_002',
    ]

    # 无限循环以检查新数据
    while True:
        # 获取今天的日期
        today_date = datetime.now().date()

        # 从每个表读取当天的数据
        for table in tables:
            try:
                # 将时间加上 8 小时
                start_time = f"{today_date} 00:00:00"
                start_time_obj = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
                start_time = start_time_obj.strftime('%Y-%m-%d %H:%M:%S')

                end_time = f"{today_date} 23:59:59"
                end_time_obj = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
                end_time = end_time_obj.strftime('%Y-%m-%d %H:%M:%S')

                query = f"SELECT ts, fvalue FROM {table} WHERE ts >= '{start_time}' AND ts <= '{end_time}'"
                td_cursor.execute(query)
                data = td_cursor.fetchall()

                for row in data:
                    ts = row[0].strftime('%Y-%m-%d %H:%M:%S')
                    fvalue = row[1]

                    # 过滤每10分钟的数据  if ts_datetime.minute % 4 == 0 and ts_datetime.second == 0:
                    ts_datetime = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
                    if ts_datetime.second == 0:  # 每分钟的第一秒
                        ts_adjusted = (ts_datetime - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')

                        try:
                            # 获取最新 ratio
                            mysql_cursor.execute("SELECT ratio FROM dian_ratio ORDER BY id DESC LIMIT 1")
                            ratio_result = mysql_cursor.fetchone()
                            ratio = ratio_result[0] if ratio_result else 1
                            if ratio is None or ratio == 0:
                                ratio = 1

                            # 乘上 ratio
                            adjusted_fvalue = fvalue

                            # 检查数据是否已经存在
                            mysql_cursor.execute('SELECT COUNT(*) FROM cy_plc3_002 WHERE tS = %s', (ts_adjusted,))
                            exists = mysql_cursor.fetchone()[0]

                            if exists == 0:
                                mysql_cursor.execute(
                                    'INSERT INTO cy_plc3_002 (tS, aValue) VALUES (%s, %s)',
                                    (ts_adjusted, adjusted_fvalue)
                                )
                        except Exception as e:
                            print(f"Error writing data to MySQL: {e}")

            except Exception as e:
                print(f"Error reading data from table {table}: {e}")

        # 提交事务
        try:
            mysql_conn.commit()
            print("Transaction committed")
        except Exception as e:
            print(f"Error committing transaction: {e}")

        # 等待一段时间后再检查
        time.sleep(240)  # 每10分钟检查一次



def read_tdengine_and_write_mysql_005():
    # 连接TDengine数据库（远程主机）
    try:
        td_conn = taos.connect(host='10.10.10.130', user='root', password='taosdata', database='jinshen',
                               port=6030)  # 远程主机IP
        td_cursor = td_conn.cursor()
        print("Successfully connected to TDengine")
    except Exception as e:
        print(f"TDengine connection error: {e}")
        return

    # 连接MySQL数据库（本机）
    try:
        mysql_conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='js',
                                     charset='utf8')  # 本机IP
        mysql_cursor = mysql_conn.cursor()
        print("Successfully connected to MySQL")
    except Exception as e:
        print(f"MySQL connection error: {e}")
        return

    # TDengine中的表名
    tables = [
        'cy_plc3_005',
    ]

    # 无限循环以检查新数据
    while True:
        # 获取今天的日期
        today_date = datetime.now().date()

        # 从每个表读取当天的数据
        for table in tables:
            try:
                # 将时间加上 8 小时
                start_time = f"{today_date} 00:00:00"
                start_time_obj = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
                start_time = start_time_obj.strftime('%Y-%m-%d %H:%M:%S')

                end_time = f"{today_date} 23:59:59"
                end_time_obj = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
                end_time = end_time_obj.strftime('%Y-%m-%d %H:%M:%S')

                query = f"SELECT ts, fvalue FROM {table} WHERE ts >= '{start_time}' AND ts <= '{end_time}'"
                td_cursor.execute(query)
                data = td_cursor.fetchall()

                for row in data:
                    ts = row[0].strftime('%Y-%m-%d %H:%M:%S')
                    fvalue = row[1]

                    # 过滤每10分钟的数据  if ts_datetime.minute % 4 == 0 and ts_datetime.second == 0:
                    ts_datetime = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
                    if ts_datetime.second == 0:  # 每分钟的第一秒
                        ts_adjusted = (ts_datetime - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')

                        try:
                            # 获取最新 ratio
                            mysql_cursor.execute("SELECT ratio FROM dian_ratio ORDER BY id DESC LIMIT 1")
                            ratio_result = mysql_cursor.fetchone()
                            ratio = ratio_result[0] if ratio_result else 1
                            if ratio is None or ratio == 0:
                                ratio = 1

                            # 乘上 ratio
                            adjusted_fvalue = fvalue

                            # 检查数据是否已经存在
                            mysql_cursor.execute('SELECT COUNT(*) FROM cy_plc3_005 WHERE tS = %s', (ts_adjusted,))
                            exists = mysql_cursor.fetchone()[0]

                            if exists == 0:
                                mysql_cursor.execute(
                                    'INSERT INTO cy_plc3_005 (tS, aValue) VALUES (%s, %s)',
                                    (ts_adjusted, adjusted_fvalue)
                                )
                        except Exception as e:
                            print(f"Error writing data to MySQL: {e}")

            except Exception as e:
                print(f"Error reading data from table {table}: {e}")

        # 提交事务
        try:
            mysql_conn.commit()
            print("Transaction committed")
        except Exception as e:
            print(f"Error committing transaction: {e}")

        # 等待一段时间后再检查
        time.sleep(240)  # 每10分钟检查一次


def read_tdengine_and_write_mysql_010():
    # 连接TDengine数据库（远程主机）
    try:
        td_conn = taos.connect(host='10.10.10.130', user='root', password='taosdata', database='jinshen',
                               port=6030)  # 远程主机IP
        td_cursor = td_conn.cursor()
        print("Successfully connected to TDengine")
    except Exception as e:
        print(f"TDengine connection error: {e}")
        return

    # 连接MySQL数据库（本机）
    try:
        mysql_conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='js',
                                     charset='utf8')  # 本机IP
        mysql_cursor = mysql_conn.cursor()
        print("Successfully connected to MySQL")
    except Exception as e:
        print(f"MySQL connection error: {e}")
        return

    # TDengine中的表名
    tables = [
        'cy_plc3_010',
    ]

    # 无限循环以检查新数据
    while True:
        # 获取今天的日期
        today_date = datetime.now().date()

        # 从每个表读取当天的数据
        for table in tables:
            try:
                # 将时间加上 8 小时
                start_time = f"{today_date} 00:00:00"
                start_time_obj = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
                start_time = start_time_obj.strftime('%Y-%m-%d %H:%M:%S')

                end_time = f"{today_date} 23:59:59"
                end_time_obj = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
                end_time = end_time_obj.strftime('%Y-%m-%d %H:%M:%S')

                query = f"SELECT ts, fvalue FROM {table} WHERE ts >= '{start_time}' AND ts <= '{end_time}'"
                td_cursor.execute(query)
                data = td_cursor.fetchall()

                for row in data:
                    ts = row[0].strftime('%Y-%m-%d %H:%M:%S')
                    fvalue = row[1]

                    # 过滤每10分钟的数据  if ts_datetime.minute % 4 == 0 and ts_datetime.second == 0:
                    ts_datetime = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
                    if ts_datetime.second == 0:  # 每分钟的第一秒
                        ts_adjusted = (ts_datetime - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')

                        try:
                            # 获取最新 ratio
                            mysql_cursor.execute("SELECT ratio FROM dian_ratio ORDER BY id DESC LIMIT 1")
                            ratio_result = mysql_cursor.fetchone()
                            ratio = ratio_result[0] if ratio_result else 1
                            if ratio is None or ratio == 0:
                                ratio = 1

                            # 乘上 ratio
                            adjusted_fvalue = fvalue

                            # 检查数据是否已经存在
                            mysql_cursor.execute('SELECT COUNT(*) FROM cy_plc3_010 WHERE tS = %s', (ts_adjusted,))
                            exists = mysql_cursor.fetchone()[0]

                            if exists == 0:
                                mysql_cursor.execute(
                                    'INSERT INTO cy_plc3_010 (tS, aValue) VALUES (%s, %s)',
                                    (ts_adjusted, adjusted_fvalue)
                                )
                        except Exception as e:
                            print(f"Error writing data to MySQL: {e}")

            except Exception as e:
                print(f"Error reading data from table {table}: {e}")

        # 提交事务
        try:
            mysql_conn.commit()
            print("Transaction committed")
        except Exception as e:
            print(f"Error committing transaction: {e}")

        # 等待一段时间后再检查
        time.sleep(240)  # 每10分钟检查一次


# 创建并启动线程
threads = []

# 原始函数线程
#tdengine_thread = threading.Thread(target=read_tdengine_and_write_mysql)
#threads.append(tdengine_thread)

tdengine_thread1 = threading.Thread(target=read_tdengine_and_write_mysql_1)
threads.append(tdengine_thread1)

# 新增加的三个函数线程
tdengine_thread_002 = threading.Thread(target=read_tdengine_and_write_mysql_002)
threads.append(tdengine_thread_002)

tdengine_thread_005 = threading.Thread(target=read_tdengine_and_write_mysql_005)
threads.append(tdengine_thread_005)

tdengine_thread_010 = threading.Thread(target=read_tdengine_and_write_mysql_010)
threads.append(tdengine_thread_010)

# 启动所有线程
for thread in threads:
    thread.start()

# 等待所有线程完成（不会被执行，因为是无限循环）
for thread in threads:
    thread.join()

