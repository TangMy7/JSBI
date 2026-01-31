import pymysql
import taos
import time
from datetime import datetime, timedelta
import pytz
import threading


def read_tdengine_and_write_mysql():
    # 连接TDengine数据库（远程主机）
    try:
        td_conn = taos.connect(host='10.10.10.130', user='root', password='taosdata', port=6030,
                               database='jinshen')  # 远程主机IP 172.20.37.210
        td_cursor = td_conn.cursor()
        print("Successfully connected to TDengine")
    except Exception as e:
        print(f"TDengine connection error: {e}")
        return

    # 连接MySQL数据库（本机）
    try:
        mysql_conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='js',
                                     charset='utf8')
        mysql_cursor = mysql_conn.cursor()
        print("Successfully connected to MySQL")
    except Exception as e:
        print(f"MySQL connection error: {e}")
        return

    # TDengine中的表名
    tables_to_add = ['YLY_DL_YM25617', 'YLY_DL_YM25625']  # 加法操作
    tables_to_subtract = ['YLY_DL_YM25653', 'YLY_DL_YM25661', 'YLY_DL_YM25669']  # 减法操作
    tables_direct = ['YLY_DCS_FIQ2201', 'YLY_DCS_FQ2241']  # 直接存储到MySQL 这两个，气 卤 跟之前那个是一样的

    # 定义目标时间为列表
    target_times = ["07:30:00", "15:30:00", "23:30:00"]

    # 获取本地时区对象（东八区，用于MySQL时间处理）
    local_tz = pytz.timezone('Asia/Shanghai')

    # 无限循环以检查新数据
    while True:
        # 临时字典存储数据
        data_dict = {}

        # 从每个表读取当天特定时间的数据
        for target_time in target_times:
            try:
                # 处理时间格式转换，将类似2024-12-27T15:30:00.000Z的格式转为datetime对象，并转为本地时间（东八区时间），再减去8小时
                target_time_utc = datetime.strptime(target_time, '%H:%M:%S').time()
                target_date = datetime.now(local_tz).date()
                combined_utc = datetime.combine(target_date, target_time_utc).replace(tzinfo=pytz.utc)
                local_time = combined_utc.astimezone(local_tz)
                local_time_minus_8 = local_time - timedelta(hours=8)  # 减去8小时
                start_time = local_time_minus_8.strftime('%Y-%m-%d %H:%M:%S')

                # 计算结束时间，思路同开始时间，先处理为东八区时间再减去8小时，这里秒数加1
                end_seconds = int(target_time.split(':')[-1]) + 1
                end_time_utc = (datetime.combine(target_date, target_time_utc) + timedelta(seconds=1)).replace(
                    tzinfo=pytz.utc)
                end_time_local = end_time_utc.astimezone(local_tz)
                end_time_local_minus_8 = end_time_local - timedelta(hours=8)
                end_time = end_time_local_minus_8.strftime('%Y-%m-%d %H:%M:%S')

                # 处理加法操作
                total_add_value = 0
                for table in tables_to_add:
                    query = f"SELECT * FROM {table} WHERE ts >= '{combined_utc.isoformat()}' AND ts < '{end_time_utc.isoformat()}'"
                    #print(f"Executing query for addition: {query}")
                    td_cursor.execute(query)
                    data = td_cursor.fetchall()
                    if data:  # 只在有数据时才进行加法操作
                        for row in data:
                            total_add_value += row[2]  # 第三列是需要加的值

                # 处理减法操作
                total_subtract_value = 0
                for table in tables_to_subtract:
                    query = f"SELECT * FROM {table} WHERE ts >= '{combined_utc.isoformat()}' AND ts < '{end_time_utc.isoformat()}'"
                    #print(f"Executing query for subtraction: {query}")
                    td_cursor.execute(query)
                    data = td_cursor.fetchall()
                    if data:  # 只在有数据时才进行减法操作
                        for row in data:
                            total_subtract_value += row[2]  # 第三列是需要减的值

                # 获取直接存储的数据
                direct_data = {}
                for table in tables_direct:
                    query = f"SELECT * FROM {table} WHERE ts >= '{combined_utc.isoformat()}' AND ts < '{end_time_utc.isoformat()}'"
                    #print(f"Executing query for direct storage: {query}")
                    td_cursor.execute(query)
                    data = td_cursor.fetchall()
                    if data:  # 只在有数据时才存储
                        for row in data:
                            if table == 'YLY_DCS_FIQ2201':
                                direct_data['qiHao'] = row[2]  # 第三列是需要的值
                            if table == 'YLY_DCS_FQ2241':
                                direct_data['luHao'] = row[2]  # 第三列是需要的值

                # 最终的合成值
                final_value = total_add_value - total_subtract_value

                # 根据目标时间设置sub列的值
                sub_value = None
                if target_time == "07:30:00":
                    sub_value = "0-8"  # 07:30:00时sub插入0-8
                elif target_time == "15:30:00":
                    sub_value = "8-16"  # 15:30:00时sub插入8-16
                elif target_time == "23:30:00":
                    sub_value = "16-24"  # 23:30:00时sub插入16-24

                # 只有在有有效数据时才插入
                if (total_add_value or total_subtract_value or direct_data):  # 检查是否有有效数据
                    # 检查数据是否已经存在
                    mysql_cursor.execute('SELECT COUNT(*) FROM threehand WHERE inputTime = %s', (start_time,))
                    exists = mysql_cursor.fetchone()[0]

                    if exists == 0:  # 如果不存在，则插入数据
                        # 插入数据到MySQL，sub列插入相应值
                        mysql_cursor.execute(
                            'INSERT INTO threehand (inputTime, dianHao, qiHao, luHao, sub) VALUES (%s, %s, %s, %s, %s)',
                            (start_time, final_value, direct_data.get('qiHao'), direct_data.get('luHao'), sub_value)
                        )
                        print(
                            f"Inserted new data: {start_time}, {final_value}, {direct_data.get('qiHao')}, {direct_data.get('luHao')}, sub={sub_value}")
                else:
                    print(f"No data for {target_time}, skipping insertion.")

            except Exception as e:
                print(f"Error processing data for target time {target_time}: {e}")

        # 提交事务
        try:
            mysql_conn.commit()
        except Exception as e:
            print(f"Error committing transaction: {e}")

        # 等待一段时间后再检查
        time.sleep(10)

    # 关闭连接（这里原代码注释掉了关闭连接部分，实际使用中可根据需要决定是否正确关闭，比如线程结束时关闭等）
    # td_cursor.close()
    # td_conn.close()
    # mysql_cursor.close()
    # mysql_conn.close()


# 创建并启动线程
tdengine_thread = threading.Thread(target=read_tdengine_and_write_mysql)
tdengine_thread.start()

# 等待线程完成（不会被执行，因为是无限循环）
tdengine_thread.join()
