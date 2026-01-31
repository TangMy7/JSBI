import pymysql
import taos
import time
from datetime import datetime, timedelta
import threading


def read_tdengine_and_write_mysql():
    # 连接TDengine数据库（远程主机）
    try:
        td_conn = taos.connect(host='10.10.10.130', user='root', password='taosdata', database='jinshen')  # 远程主机IP
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

    tables = ['YLY_DCS_FIQ2505', 'YLY_DCS_FIQ2201', 'YLY_DCS_FQ2241', 'YLY_DCS_FQ2248', 'YLY_DCS_FQ_MY',
              'YLY_DCS_FQ2239', 'YLY_DCS_FIQ1101', 'yly_dcs_ft_2200_sm']

    # 目标时间
    target_times = ["07:50:00", "15:50:00", "23:50:00"]

    column_names = ['aValue', 'bValue', 'cValue', 'eValue', 'fValue', 'gValue', 'hValue', 'newValue']

    while True:
        data_dict = {}

        today_date = datetime.now().date()

        # 从每个表读取当天特定时间的数据
        for table in tables:
            try:
                for target_time in target_times:
                    # 生成目标时间段
                    start_time = f"{today_date} {target_time}"
                    start_time_obj = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
                    start_time = start_time_obj.strftime('%Y-%m-%d %H:%M:%S')

                    # 结束时间+1秒
                    end_seconds = int(target_time.split(':')[-1]) + 1
                    end_time = f"{today_date} {target_time[:-2]}{end_seconds:02d}"
                    end_time_obj = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
                    end_time = end_time_obj.strftime('%Y-%m-%d %H:%M:%S')

                    query = f"SELECT * FROM {table} WHERE ts >= '{start_time}' AND ts < '{end_time}'"
                    print(f"Executing query: {query}")
                    td_cursor.execute(query)
                    data = td_cursor.fetchall()

                    for row in data:
                        ts = row[0].strftime('%Y-%m-%d %H:%M:%S')
                        fvalue = row[2]

                        if ts not in data_dict:
                            data_dict[ts] = [None] * 8
                        column_index = tables.index(table)
                        data_dict[ts][column_index] = fvalue
            except Exception as e:
                print(f"Error reading data from table {table}: {e}")

        # 写入或更新到MySQL
        for ts in sorted(data_dict.keys()):
            values = data_dict[ts]
            try:
                # 时间减8小时
                ts_datetime = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
                ts_adjusted = (ts_datetime - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')

                mysql_cursor.execute('SELECT COUNT(*) FROM cql WHERE tS = %s', (ts_adjusted,))
                exists = mysql_cursor.fetchone()[0]

                if exists == 0:
                    # 没有，插入
                    mysql_cursor.execute(
                        'INSERT INTO cql (tS, aValue, bValue, cValue, eValue, fValue, gValue, hValue, newValue) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (ts_adjusted, values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7])
                    )
                else:
                    # 已存在，只更新有值的字段
                    update_fields = []
                    update_values = []
                    for idx, v in enumerate(values):
                        if v is not None:
                            update_fields.append(f"{column_names[idx]} = %s")
                            update_values.append(v)
                    if update_fields:
                        sql = f"UPDATE cql SET {', '.join(update_fields)} WHERE tS = %s"
                        mysql_cursor.execute(sql, update_values + [ts_adjusted])
            except Exception as e:
                print(f"Error writing data to MySQL: {e}")

        # 提交事务
        try:
            mysql_conn.commit()
        except Exception as e:
            print(f"Error committing transaction: {e}")

        time.sleep(10)

    # 关闭连接
    # td_cursor.close()
    # td_conn.close()
    # mysql_cursor.close()
    # mysql_conn.close()


def read_tdengine_and_write_mysql_1():
    # 连接TDengine数据库（远程主机）
    try:
        td_conn = taos.connect(host='10.10.10.130', user='root', password='taosdata', database='jinshen')  # 远程主机IP
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

    # 只保留 YLY_DCS_FIQ2505
    tables = ['YLY_DCS_FIQ2505']

    # 目标时间      target_times = ["08:10:00", "16:10:00", "0:10:00"]
    target_times = ["08:07:00", "16:07:00", "0:07:00"]

    # 只对应一个字段
    column_names = ['aValue']

    while True:
        data_dict = {}

        today_date = datetime.now().date()

        # 从每个表读取当天特定时间的数据
        for table in tables:
            try:
                for target_time in target_times:
                    # 生成目标时间段
                    start_time = f"{today_date} {target_time}"
                    start_time_obj = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
                    start_time = start_time_obj.strftime('%Y-%m-%d %H:%M:%S')

                    # 结束时间+1秒
                    end_seconds = int(target_time.split(':')[-1]) + 1
                    end_time = f"{today_date} {target_time[:-2]}{end_seconds:02d}"
                    end_time_obj = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
                    end_time = end_time_obj.strftime('%Y-%m-%d %H:%M:%S')

                    query = f"SELECT * FROM {table} WHERE ts >= '{start_time}' AND ts < '{end_time}'"
                    print(f"Executing query: {query}")
                    td_cursor.execute(query)
                    data = td_cursor.fetchall()

                    for row in data:
                        ts = row[0].strftime('%Y-%m-%d %H:%M:%S')
                        fvalue = row[2]

                        if ts not in data_dict:
                            data_dict[ts] = [None]
                        # 只剩一个表，索引始终是0
                        data_dict[ts][0] = fvalue
            except Exception as e:
                print(f"Error reading data from table {table}: {e}")

        # 写入或更新到MySQL
        for ts in sorted(data_dict.keys()):
            values = data_dict[ts]
            try:
                # 时间减8小时
                ts_datetime = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
                ts_adjusted = (ts_datetime - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')

                mysql_cursor.execute('SELECT COUNT(*) FROM cql WHERE tS = %s', (ts_adjusted,))
                exists = mysql_cursor.fetchone()[0]

                if exists == 0:
                    # 没有，插入
                    mysql_cursor.execute(
                        'INSERT INTO cql (tS, aValue) VALUES (%s, %s)',
                        (ts_adjusted, values[0])
                    )
                else:
                    # 已存在，只更新有值的字段
                    update_fields = []
                    update_values = []
                    for idx, v in enumerate(values):
                        if v is not None:
                            update_fields.append(f"{column_names[idx]} = %s")
                            update_values.append(v)
                    if update_fields:
                        sql = f"UPDATE cql SET {', '.join(update_fields)} WHERE tS = %s"
                        mysql_cursor.execute(sql, update_values + [ts_adjusted])
            except Exception as e:
                print(f"Error writing data to MySQL: {e}")

        # 提交事务
        try:
            mysql_conn.commit()
        except Exception as e:
            print(f"Error committing transaction: {e}")

        time.sleep(10)



# 定义函数用于从MySQL读取数据并写入output表
def read_mysql_and_write_output():
    # 连接MySQL数据库
    try:
        mysql_conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='123456',
            db='js',
            charset='utf8'
        )
        mysql_cursor = mysql_conn.cursor()
    except pymysql.MySQLError as e:
        print(f"连接MySQL时出错: {e}")
        return

    # 只选择的时间段
    target_times = {"07:30:00", "15:30:00", "23:30:00"}

    # 用于存储前一行的各字段的值（用字典来明确管理字段）
    previous_values = {
        "bban": None,
        "aban": None,
        "bqi": None,
        "aqi": None,
        "bhao": None,
        "ahao": None,
        "bmu": None,
        "amu": None,
        "bhui": None,
        "ahui": None,
        "bcold": None,
        "acold": None,
        "bWater": None,
        "aWater": None,
        "btao": None,
        "atao": None
    }

    while True:
        try:
            mysql_conn.commit()

            # 获取今天的日期
            today_date = datetime.now().date()
            yesterday_date = today_date - timedelta(days=1)

            # 只查询目标时间段的数据
            query = '''
                SELECT SQL_NO_CACHE tS, aValue, bValue, cValue, eValue, fValue, gValue, hValue, newValue
                FROM cql 
                WHERE DATE(tS) IN (%s, %s) AND TIME(tS) IN %s
                ORDER BY tS
            '''
            mysql_cursor.execute(query, (today_date, yesterday_date, tuple(target_times)))
            data = mysql_cursor.fetchall()

            for row in data:
                dataTime = row[0]
                time_str = dataTime.strftime('%H:%M:%S')

                # 检查时间是否在目标时间段内
                if time_str in target_times:
                    aValue = row[1]
                    bValue = row[2]
                    cValue = row[3]
                    eValue = row[4]
                    fValue = row[5]
                    gValue = row[6]
                    hValue = row[7]
                    newValue = row[8]

                    # 确定timePoint值
                    if time_str == "07:30:00":
                        timePoint = "0-8点"
                    elif time_str == "15:30:00":
                        timePoint = "8-16点"
                    elif time_str == "23:30:00":
                        timePoint = "16-24点"

                    # 检查是否已存在于output表中
                    mysql_cursor.execute('SELECT COUNT(*) FROM output WHERE dataTime = %s', (dataTime,))
                    exists = mysql_cursor.fetchone()[0]

                    # 获取output表中最新的各字段值，用于previous_values
                    mysql_cursor.execute('''
                        SELECT bban, aban, bqi, aqi, bhao, ahao, bmu, amu, bhui, ahui, bcold, acold, bWater, aWater, btao, atao
                        FROM output
                        ORDER BY dataTime DESC LIMIT 1
                    ''')
                    last_values = mysql_cursor.fetchone()
                    if last_values:
                        previous_values.update({
                            "bban": last_values[0],
                            "aban": last_values[1],
                            "bqi": last_values[2],
                            "aqi": last_values[3],
                            "bhao": last_values[4],
                            "ahao": last_values[5],
                            "bmu": last_values[6],
                            "amu": last_values[7],
                            "bhui": last_values[8],
                            "ahui": last_values[9],
                            "bcold": last_values[10],
                            "acold": last_values[11],
                            "bWater": last_values[12],
                            "aWater": last_values[13],
                            "btao": last_values[14],
                            "atao": last_values[15]
                        })

                    if exists == 0:
                        # 不存在则插入
                        try:
                            mysql_cursor.execute(
                                '''INSERT INTO output 
                                (dataTime, timePoint, bban, aban, bqi, aqi, bhao, ahao, bmu, amu, bhui, ahui, bcold, acold, bWater, aWater, btao, atao) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                                (dataTime, timePoint, aValue, previous_values["bban"], bValue, previous_values["bqi"], cValue, previous_values["bhao"],
                                 eValue, previous_values["bmu"], fValue, previous_values["bhui"], gValue, previous_values["bcold"], hValue, previous_values["bWater"],
                                 newValue, previous_values["btao"])
                            )
                            mysql_conn.commit()
                            print(f"插入到output: dataTime={dataTime}, timePoint={timePoint}, bban={aValue}, aban={previous_values['bban']}, "
                                  f"bqi={bValue}, aqi={previous_values['bqi']}, bhao={cValue}, ahao={previous_values['bhao']}, "
                                  f"bmu={eValue}, amu={previous_values['bmu']}, bhui={fValue}, ahui={previous_values['bhui']}, "
                                  f"bcold={gValue}, acold={previous_values['bcold']}, bWater={hValue}, aWater={previous_values['bWater']}, "
                                  f"btao={newValue}, atao={previous_values['btao']}")
                        except pymysql.MySQLError as e:
                            print(f"插入数据时出错: {e}")
                    else:
                        # 已存在则更新
                        try:
                            # 只更新本次有新数据的字段，其他字段保持原样
                            update_fields = []
                            update_values = []

                            # 字段映射关系
                            field_map = [
                                ('bban', aValue),
                                ('bqi', bValue),
                                ('bhao', cValue),
                                ('bmu', eValue),
                                ('bhui', fValue),
                                ('bcold', gValue),
                                ('bWater', hValue),
                                ('btao', newValue)
                            ]
                            for field, value in field_map:
                                if value is not None:
                                    update_fields.append(f"{field} = %s")
                                    update_values.append(value)
                            # timePoint 也可以更新（如果有变化）
                            update_fields.append("timePoint = %s")
                            update_values.append(timePoint)
                            # 拼接SQL
                            if update_fields:
                                update_sql = f"UPDATE output SET {', '.join(update_fields)} WHERE dataTime = %s"
                                update_values.append(dataTime)
                                mysql_cursor.execute(update_sql, tuple(update_values))
                                mysql_conn.commit()
                                print(f"更新output: dataTime={dataTime}, 更新字段: {update_fields}")

                        except pymysql.MySQLError as e:
                            print(f"更新数据时出错: {e}")

                    # 更新前一行的值
                    previous_values["bban"] = aValue
                    previous_values["bqi"] = bValue
                    previous_values["bhao"] = cValue
                    previous_values["bmu"] = eValue
                    previous_values["bhui"] = fValue
                    previous_values["bcold"] = gValue
                    previous_values["bWater"] = hValue
                    previous_values["btao"] = newValue

            time.sleep(10)
        except pymysql.MySQLError as e:
            print(f"执行查询时出错: {e}")
            time.sleep(10)

# 关闭连接部分保持不变

def fix_cql_timepoints_for_last_7_days():
    """
    每10秒检查最近7天的cql表，将 tS 字段为 07:59、15:59、23:59 的时间点修正为 07:30、15:30、23:30
    """
    fix_time_map = {
        '07:50:00': '07:30:00',
        '15:50:00': '15:30:00',
        '23:50:00': '23:30:00'
    }
    while True:
        try:
            mysql_conn = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                passwd='123456',
                db='js',
                charset='utf8'
            )
            mysql_cursor = mysql_conn.cursor()
        except Exception as e:
            print(f"MySQL connection error: {e}")
            time.sleep(10)
            continue

        today = datetime.now().date()
        last_7_days = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

        try:
            for day in last_7_days:
                for wrong_time, right_time in fix_time_map.items():
                    wrong_ts = f"{day} {wrong_time}"
                    right_ts = f"{day} {right_time}"

                    try:
                        mysql_cursor.execute(
                            "UPDATE cql SET tS = %s WHERE tS = %s",
                            (right_ts, wrong_ts)
                        )
                        if mysql_cursor.rowcount > 0:
                            print(f"Updated tS from {wrong_ts} to {right_ts}")
                    except pymysql.err.IntegrityError as e:
                        # 唯一约束冲突，不处理
                        print(f"Skip updating {wrong_ts} to {right_ts}: {e}")

            mysql_conn.commit()
        except Exception as e:
            print(f"Error during fixing timepoints: {e}")
        finally:
            mysql_cursor.close()
            mysql_conn.close()
        time.sleep(10)


def fix_cql_timepoints_for_last_7_days_1():
    """
    每10秒检查最近7天的cql表，将 tS 字段为 07:59、15:59、23:59 的时间点修正为 07:30、15:30、23:30
    这个函数没用了，现在都没有59分的了
    """
    fix_time_map = {
        '07:59:00': '07:30:00',
        '15:59:00': '15:30:00',
        '23:59:00': '23:30:00'
    }
    while True:
        try:
            mysql_conn = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                passwd='123456',
                db='js',
                charset='utf8'
            )
            mysql_cursor = mysql_conn.cursor()
        except Exception as e:
            print(f"MySQL connection error: {e}")
            time.sleep(10)
            continue

        today = datetime.now().date()
        last_7_days = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

        try:
            for day in last_7_days:
                for wrong_time, right_time in fix_time_map.items():
                    wrong_ts = f"{day} {wrong_time}"
                    right_ts = f"{day} {right_time}"

                    try:
                        mysql_cursor.execute(
                            "UPDATE cql SET tS = %s WHERE tS = %s",
                            (right_ts, wrong_ts)
                        )
                        if mysql_cursor.rowcount > 0:
                            print(f"Updated tS from {wrong_ts} to {right_ts}")
                    except pymysql.err.IntegrityError as e:
                        # 唯一约束冲突，不处理
                        print(f"Skip updating {wrong_ts} to {right_ts}: {e}")

            mysql_conn.commit()
        except Exception as e:
            print(f"Error during fixing timepoints: {e}")
        finally:
            mysql_cursor.close()
            mysql_conn.close()
        time.sleep(10)


def sync_cql_time_pairs_1():

    # 需要同步的时间对 (源时间, 目标时间)    ("08:10:00", "07:30:00"),   ("16:10:00", "15:30:00"),
    time_pairs = [
        ("08:07:00", "07:30:00"),
        ("16:07:00", "15:30:00"),
    ]

    # 要同步的字段（去除tS主键字段）
    columns = [
        "aValue"
    ]

    while True:
        try:
            mysql_conn = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                passwd='123456',
                db='js',
                charset='utf8'
            )
            mysql_cursor = mysql_conn.cursor()
        except Exception as e:
            print(f"MySQL connection error in sync_cql_time_pairs: {e}")
            time.sleep(10)
            continue

        today = datetime.now().date()
        last_7_days = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

        try:
            for day in last_7_days:
                for src_time, dst_time in time_pairs:
                    src_ts = f"{day} {src_time}"
                    dst_ts = f"{day} {dst_time}"

                    # 查询源行
                    mysql_cursor.execute(
                        f"SELECT {', '.join(columns)} FROM cql WHERE tS = %s", (src_ts,)
                    )
                    src_row = mysql_cursor.fetchone()
                    if src_row is None:
                        continue  # 如果源行没有，跳过

                    # 检查目标行是否存在
                    mysql_cursor.execute("SELECT COUNT(*) FROM cql WHERE tS = %s", (dst_ts,))
                    dst_exists = mysql_cursor.fetchone()[0]

                    if dst_exists:
                        # 更新目标行
                        set_clause = ', '.join([f"{col} = %s" for col in columns])
                        update_sql = f"UPDATE cql SET {set_clause} WHERE tS = %s"
                        mysql_cursor.execute(update_sql, (*src_row, dst_ts))
                        print(f"sync_cql_time_pairs: 覆盖 {dst_ts} <- {src_ts}")
                    else:
                        # 如果目标行不存在，可以选择插入，或跳过，这里选择跳过
                        print(f"sync_cql_time_pairs: 目标行 {dst_ts} 不存在，跳过覆盖。")

            mysql_conn.commit()
        except Exception as e:
            print(f"Error in sync_cql_time_pairs: {e}")
        finally:
            mysql_cursor.close()
            mysql_conn.close()
        time.sleep(15)


def sync_cql_time_pairs():
    """
    每15秒将每天07:50, 15:50, 23:50的数据同步到07:30, 15:30, 23:30行（字段全覆盖，主键tS除外）。
    """

    # 需要同步的时间对 (源时间, 目标时间)
    time_pairs = [
        ("07:50:00", "07:30:00"),
        ("15:50:00", "15:30:00"),
        ("23:50:00", "23:30:00")
    ]

    # 要同步的字段（去除tS主键字段）
    columns = [
         "bValue", "cValue", "eValue", "fValue", "gValue", "hValue", "newValue"
    ]

    while True:
        try:
            mysql_conn = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                passwd='123456',
                db='js',
                charset='utf8'
            )
            mysql_cursor = mysql_conn.cursor()
        except Exception as e:
            print(f"MySQL connection error in sync_cql_time_pairs: {e}")
            time.sleep(10)
            continue

        today = datetime.now().date()
        last_7_days = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

        try:
            for day in last_7_days:
                for src_time, dst_time in time_pairs:
                    src_ts = f"{day} {src_time}"
                    dst_ts = f"{day} {dst_time}"

                    # 查询源行
                    mysql_cursor.execute(
                        f"SELECT {', '.join(columns)} FROM cql WHERE tS = %s", (src_ts,)
                    )
                    src_row = mysql_cursor.fetchone()
                    if src_row is None:
                        continue  # 如果源行没有，跳过

                    # 检查目标行是否存在
                    mysql_cursor.execute("SELECT COUNT(*) FROM cql WHERE tS = %s", (dst_ts,))
                    dst_exists = mysql_cursor.fetchone()[0]

                    if dst_exists:
                        # 更新目标行
                        set_clause = ', '.join([f"{col} = %s" for col in columns])
                        update_sql = f"UPDATE cql SET {set_clause} WHERE tS = %s"
                        mysql_cursor.execute(update_sql, (*src_row, dst_ts))
                        print(f"sync_cql_time_pairs: 覆盖 {dst_ts} <- {src_ts}")
                    else:
                        # 如果目标行不存在，可以选择插入，或跳过，这里选择跳过
                        print(f"sync_cql_time_pairs: 目标行 {dst_ts} 不存在，跳过覆盖。")

            mysql_conn.commit()
        except Exception as e:
            print(f"Error in sync_cql_time_pairs: {e}")
        finally:
            mysql_cursor.close()
            mysql_conn.close()
        time.sleep(15)

def sync_cql_time_pairs_2():

    # 需要同步的时间对 (源时间, 目标时间)
    # 源时间为当天00:10:00，目标时间为前一天23:30:00          ("00:10:00", "23:30:00")
    time_pairs = [
        ("00:07:00", "23:30:00")
    ]

    # 要同步的字段（去除tS主键字段）
    columns = [
        "aValue"
    ]

    while True:
        try:
            mysql_conn = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                passwd='123456',
                db='js',
                charset='utf8'
            )
            mysql_cursor = mysql_conn.cursor()
        except Exception as e:
            print(f"MySQL connection error in sync_cql_time_pairs: {e}")
            time.sleep(10)
            continue

        today = datetime.now().date()
        last_7_days = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

        try:
            for day in last_7_days:
                for src_time, dst_time in time_pairs:
                    # 源时间是当天00:10:00
                    src_ts = f"{day} {src_time}"
                    # 目标时间是前一天的23:30:00
                    prev_day = (datetime.strptime(day, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
                    dst_ts = f"{prev_day} {dst_time}"

                    # 查询源行
                    mysql_cursor.execute(
                        f"SELECT {', '.join(columns)} FROM cql WHERE tS = %s", (src_ts,)
                    )
                    src_row = mysql_cursor.fetchone()
                    if src_row is None:
                        continue  # 如果源行没有，跳过

                    # 检查目标行是否存在
                    mysql_cursor.execute("SELECT COUNT(*) FROM cql WHERE tS = %s", (dst_ts,))
                    dst_exists = mysql_cursor.fetchone()[0]

                    if dst_exists:
                        # 更新目标行
                        set_clause = ', '.join([f"{col} = %s" for col in columns])
                        update_sql = f"UPDATE cql SET {set_clause} WHERE tS = %s"
                        mysql_cursor.execute(update_sql, (*src_row, dst_ts))
                        print(f"sync_cql_time_pairs: 覆盖 {dst_ts} <- {src_ts}")
                    else:
                        # 如果目标行不存在，可以选择插入，或跳过，这里选择跳过
                        print(f"sync_cql_time_pairs: 目标行 {dst_ts} 不存在，跳过覆盖。")

            mysql_conn.commit()
        except Exception as e:
            print(f"Error in sync_cql_time_pairs: {e}")
        finally:
            mysql_cursor.close()
            mysql_conn.close()
        time.sleep(15)


# 创建并启动线程
tdengine_thread = threading.Thread(target=read_tdengine_and_write_mysql)
output_thread = threading.Thread(target=read_mysql_and_write_output)
fix_timepoints_thread = threading.Thread(target=fix_cql_timepoints_for_last_7_days)
fix_timepoints_thread1 = threading.Thread(target=sync_cql_time_pairs)
fix_timepoints_thread2 = threading.Thread(target=fix_cql_timepoints_for_last_7_days_1)
fix_timepoints_thread3 = threading.Thread(target=sync_cql_time_pairs_1)
tdengine_thread4 = threading.Thread(target=read_tdengine_and_write_mysql_1)
tdengine_thread5 = threading.Thread(target=sync_cql_time_pairs_2)

tdengine_thread.start()
output_thread.start()
fix_timepoints_thread.start()
fix_timepoints_thread1.start()
fix_timepoints_thread2.start()
fix_timepoints_thread3.start()
tdengine_thread4.start()
tdengine_thread5.start()

tdengine_thread.join()
output_thread.join()
fix_timepoints_thread.join()
fix_timepoints_thread1.join()
fix_timepoints_thread2.join()
fix_timepoints_thread3.join()
tdengine_thread4.join()
tdengine_thread5.join()