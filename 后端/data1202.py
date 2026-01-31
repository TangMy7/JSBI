from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
from datetime import datetime, timedelta, time as dt_time
import taos
import logging
import threading
import time
import pymysql
from dbutils.pooled_db import PooledDB
from functools import lru_cache
from threading import Thread
import time as time_module
import math
import json

# 在文件开头添加全局变量
is_first_run = True
last_update_time = None  # 添加这个变量来记录上次更新时间

# 创建数据库连接池
pool = PooledDB(
    creator=pymysql,
    maxconnections=50,  # 同时允许最多30个连接（视服务器资源而定）
    mincached=50,  # 初始化时创建5个连接
    maxcached=50,  # 最多缓存20个连接
    maxshared=50,  # 最多共享10个连接（对线程无效，建议比 maxcached 小）
    blocking=True,  # 如果连接满了就等待（而不是报错）
    maxusage=None,  # 单连接最大使用次数，None 表示无限
    setsession=[],
    ping=1,  # 检查连接是否可用
    host='127.0.0.1',
    port=3306,
    user='root',
    password='123456',
    database='js',
    charset='utf8'
)

app = Flask(__name__)
# 禁用 Werkzeug 的 INFO 日志
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
CORS(app, resources={r"/*": {"origins": "*"}})  # 启用跨域请求

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 配置 MySQL 数据库连接
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_HOST'] = 'localhost'  # 数据库主机
app.config['MYSQL_USER'] = 'root'  # 数据库用户名
app.config['MYSQL_PASSWORD'] = '123456'  # 数据库密码
app.config['MYSQL_DB'] = 'js'  # 数据库名称
app.config['MYSQL_CHARSET'] = 'utf8'  # 添加这一行

mysql = MySQL(app)


# 新增函数：获取数据库连接
def get_db_connection():
    """获取数据库连接"""
    try:
        return pool.connection()
    except Exception as e:
        print(f"数据库连接失败：{str(e)}")
        return None


# TDengine 连接配置
tdengine_conn = None

# MySQL 数据库连接配置
mysql_conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='js',
                             charset='utf8')
cursor = mysql_conn.cursor()

# 在文件开头添加全局变量
alarm_type_stats = {
    'device': 0,  # 设备类报警累计数
    'craft': 0  # 工艺类报警累计数
}


def init_tdengine_connection() -> None:
    """初始化 TDengine 数据库连接"""
    global tdengine_conn
    try:
        tdengine_conn = taos.connect(
            host="10.10.10.130",
            user="root",
            password="taosdata",
            database="jinshen",
            port=6030
        )
        logger.info("TDengine connection established")
    except Exception as e:
        logger.error(f"Error connecting to TDengine: {e}")


# 添加更新状态的函数
def update_alarm_status(point_id: str, status: str):
    """更新点位的报警状态

    Args:
        point_id: 点位ID（PointId）
        status: 状态，如 'warning', 'ignore', 'resolved'
    """
    try:
        cursor = mysql.connection.cursor()
        
        # 先通过PointId查找数据库id
        cursor.execute("""
            SELECT id FROM js.alarm WHERE PointId = %s
        """, (point_id,))
        
        point_exists = cursor.fetchone()
        if not point_exists:
            cursor.close()
            print(f"Point '{point_id}' not found in database")
            return False
            
        # 获取数据库id
        db_id = point_exists[0]

        # 更新alarm表中的handling字段，使用id字段
        cursor.execute("""
            UPDATE js.alarm 
            SET handling = %s 
            WHERE id = %s
        """, (status, db_id))

        mysql.connection.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"更新报警状态失败: {str(e)}")
        return False


# 修改现有的报警处理函数，加入状态更新
def increment_alarm_count(point_id: str):
    """在 MySQL 中增加报警计数"""
    yearmonth = datetime.now().strftime('%Y-%m')

    try:
        cursor = mysql.connection.cursor()

        # 查询是否已有当月记录
        cursor.execute("SELECT count FROM alarmmonth WHERE yearmonth = %s", (yearmonth,))
        result = cursor.fetchone()

        if result is None:
            # 没有记录，插入新行
            cursor.execute("INSERT INTO alarmmonth (yearmonth, count) VALUES (%s, 1) ", (yearmonth,))
        else:
            # 已有记录，count + 1
            cursor.execute("UPDATE alarmmonth SET count = count + 1 WHERE yearmonth = %s", (yearmonth,))

        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        mysql.connection.rollback()
        import traceback
        logger.error(traceback.format_exc())
        raise


def get_latest_value(table_name: str) -> float:
    """获取指定的最新 fvalue 值（使用 TDengine）"""
    try:
        if tdengine_conn:
            cursor = tdengine_conn.cursor()

            # 首先检查表是否存在
            try:
                cursor.execute(f"DESCRIBE jinshen.{table_name}")
                cursor.fetchall()  # 清空结果
            except Exception as e:
                # logger.warning(f"Table {table_name} does not exist in TDengine: {e}")
                cursor.close()
                return None

            # 如果表存在，则查询最新值
            query = f"SELECT fvalue FROM jinshen.{table_name} ORDER BY ts DESC LIMIT 1;"
            cursor.execute(query)
            query_res = cursor.fetchall()
            result = query_res[0][0] if query_res else None
            cursor.close()

            return round(float(result), 1) if result is not None else None
        else:
            logger.warning("No TDengine connection available")
            return None

    except Exception as e:
        # logger.error(f"Error getting latest value for {table_name}: {e}")
        return None

# 检查连接是否有效，若无效则重连
def check_and_reconnect():
    global conn, cursor
    if conn is None or not conn.open:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='js',
                               charset='utf8')
    if cursor is None:
        cursor = conn.cursor()


# 查询数据库的通用函数
def fetch_data_from_db(table_name):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        curtime = datetime.now()
        # 将小时、分钟和秒设置为0
        curtime_zeroed = curtime.replace(hour=0, minute=0, second=0, microsecond=0)
        # 格式化为字符串
        ten_days_ago = curtime_zeroed - timedelta(days=10)
        ten_days_ago = ten_days_ago.strftime('%Y-%m-%d %H:%M:%S')

        # 执行数据库查询
        cursor.execute(f"SELECT * FROM {table_name};")

        if not cursor.description:
            raise Exception(f"表 {table_name} 不存在或为空")

        columns = [column[0] for column in cursor.description]  # 获取列名
        results = cursor.fetchall()

        # 将列名和数据组合成字典列表
        data = [{columns[i]: row[i] for i in range(len(columns))} for row in results]
        return data
    except Exception as e:
        print(f"Error in fetch_data_from_db: {str(e)}")
        raise Exception(f"数据库查询失败: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_today_chanliang(table_name, return_from_last=False):
    """
    获取今日产量并存储到last表
    :param table_name: 表名
    :param return_from_last: 是否从last表返回数据
    :return: 今日产量值
    """
    current_time = datetime.now()

    # 定义固定的时间点
    time_points = [
        {"time": current_time.replace(hour=7, minute=30, second=0, microsecond=0), "label": "07:30"},
        {"time": current_time.replace(hour=15, minute=30, second=0, microsecond=0), "label": "15:30"},
        {"time": current_time.replace(hour=23, minute=30, second=0, microsecond=0), "label": "23:30"},
    ]

    # 根据当前时间确定应该使用的时间点
    if current_time.hour < 7 or (current_time.hour == 7 and current_time.minute < 50):
        # 7:30之前使用昨天23:30的数据
        target_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
    elif current_time.hour < 15 or (current_time.hour == 15 and current_time.minute < 50):
        # 15:30之前使用7:30的数据
        target_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
    elif current_time.hour < 23 or (current_time.hour == 23 and current_time.minute < 50):
        # 23:30之前使用15:30的数据
        target_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
    else:
        # 23:30之后使用23:30的数据
        target_time = current_time.replace(hour=23, minute=30, second=0, microsecond=0)
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()
        # 获取目标时间点的产量值
        sql = f"SELECT bban FROM {table_name} where dataTime = '{target_time}'"
        cursor.execute(sql)
        cur_res = cursor.fetchall()
        if len(cur_res) > 0 and cur_res[0][0] is not None:  # 添加 None 检查
            today_chanliang = cur_res[0][0]
        else:
            return 0  # 如果没有有效数据，返回0
        # 获取昨天23.30时，产量值
        pre_time = (current_time.replace(hour=23, minute=30, second=0, microsecond=0) -
                    timedelta(days=1))
        sql = f"SELECT bban FROM {table_name} where dataTime = '{pre_time}'"
        cursor.execute(sql)
        pre_res = cursor.fetchall()
        if len(pre_res) > 0:
            today_chanliang = today_chanliang - pre_res[0][0]

        cursor.close()
        conn.close()

        today_chanliang = round(0.99*today_chanliang, 0)

        return today_chanliang
    except Exception as e:
        print("baocuo1")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def get_month_chanliang(table_name, return_from_last=False):
    """
    获取月产量并存储到last表
    :param table_name: 表名
    :param return_from_last: 是否从last表返回数据
    :return: 月产量值
    """
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        if not conn:
            print("无法获取数据库连接")
            return 0.0

        cursor = conn.cursor()
        current_time = datetime.now()
        # print(f"当前时间：{current_time}")

        # 根据当前时间确定应该使用的时间点
        if current_time.hour < 7 or (current_time.hour == 7 and current_time.minute < 50):
            # 7:30之前使用昨天23:30的数据
            target_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
        elif current_time.hour < 15 or (current_time.hour == 15 and current_time.minute < 50):
            # 15:30之前使用7:30的数据
            target_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
        elif current_time.hour < 23 or (current_time.hour == 23 and current_time.minute < 50):
            # 23:30之前使用15:30的数据
            target_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
        else:
            # 23:30之后使用23:30的数据
            target_time = current_time.replace(hour=23, minute=30, second=0, microsecond=0)

        # print(f"目标时间点：{target_time}")

        if return_from_last:
            # 从last表查询对应时间点的产量
            sql = "SELECT monthchanliang FROM last WHERE tS = %s"
            cursor.execute(sql, (target_time,))
            result = cursor.fetchone()

            if result and result[0] is not None:
                return float(result[0])
            return 0.0


        sql = f"""
            SELECT bban 
            FROM {table_name} 
            WHERE dataTime = %s
        """
        cursor.execute(sql, (target_time,))
        cur_res = cursor.fetchone()

        if not cur_res:
            print(f"未找到目标时间点 {target_time} 的产量数据")
            return 0.0

        current_value = float(cur_res[0])
        current_data_time = target_time

        if current_time.day <=25:
            # 如果当前日期在25日之前，使用上月25日23:30作为基准
            if current_time.month == 1:
                base_date = current_time.replace(year=current_time.year - 1, month=12, day=25,hour=23, minute=30, second=0, microsecond=0)
            else:
                base_date = current_time.replace(month=current_time.month - 1, day=25,hour=23, minute=30, second=0, microsecond=0)
        else:
            # 如果当前日期在25日之后，使用当月25日23:30作为基准
            base_date = current_time.replace(day=25)

        base_time = base_date.replace(hour=23, minute=30, second=0, microsecond=0)
        # print(f"基准时间：{base_time}")

        # 获取基准时间的产量值
        sql = f"""
            SELECT bban 
            FROM {table_name} 
            WHERE dataTime = '{base_time}'
        """
        cursor.execute(sql)
        base_res = cursor.fetchone()

        if not base_res:
            print(f"未找到基准时间 {base_time} 的产量数据")
            return 0.0

        base_value = base_res[0]
        # print(f"基准时间产量值：{base_value}")

        # 计算月产量
        month_chanliang = 0.99*(current_value - base_value)
        month_chanliang = round(month_chanliang, 0)
        # print(f"计算得到的月产量：{month_chanliang}")

        # 将计算结果存储到last表中，使用目标时间点
        try:
            # 先检查是否存在该时间点的记录
            check_sql = "SELECT id FROM last WHERE tS = %s"
            cursor.execute(check_sql, (target_time,))
            result = cursor.fetchone()

            if result:
                # 如果记录存在，则更新
                update_sql = """
                    UPDATE last 
                    SET monthchanliang = %s 
                    WHERE tS = %s
                """
                cursor.execute(update_sql, (month_chanliang, target_time))
            else:
                # 如果记录不存在，则插入新记录
                insert_sql = """
                    INSERT INTO last (tS, monthchanliang)
                    VALUES (%s, %s)
                """
                cursor.execute(insert_sql, (target_time, month_chanliang))

            conn.commit()
            print(f"成功更新/插入 {target_time} 的月产量数据：{month_chanliang}")
        except Exception as e:
            print("baocuo3")
            conn.rollback()
            print(f"更新数据库时出错：{str(e)}")

        return month_chanliang
    except Exception as e:
        print(f"执行过程中出错：{str(e)}")
        print("baocuo3")
        if conn:
            conn.rollback()
        return 0.0
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_year_chanliang(table_name, return_from_last=False):
    """
    获取年产量并存储到last表
    :param table_name: 表名
    :param return_from_last: 是否从last表返回数据
    :return: 年产量值
    """
    try:
        current_time = datetime.now()
        conn = pool.connection()
        cursor = conn.cursor()
        # 定义固定的时间点
        time_points = [
            {"time": current_time.replace(hour=7, minute=30, second=0, microsecond=0), "label": "07:30"},
            {"time": current_time.replace(hour=15, minute=30, second=0, microsecond=0), "label": "15:30"},
            {"time": current_time.replace(hour=23, minute=30, second=0, microsecond=0), "label": "23:30"},
        ]

        # 根据当前时间确定应该使用的时间点
        if current_time.hour < 7 or (current_time.hour == 7 and current_time.minute < 50):
            # 7:30之前使用昨天23:30的数据
            target_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
        elif current_time.hour < 15 or (current_time.hour == 15 and current_time.minute < 50):
            # 15:30之前使用7:30的数据
            target_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
        elif current_time.hour < 23 or (current_time.hour == 23 and current_time.minute < 50):
            # 23:30之前使用15:30的数据
            target_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
        else:
            # 23:30之后使用23:30的数据
            target_time = current_time.replace(hour=23, minute=30, second=0, microsecond=0)

        if return_from_last:
            # 从last表查询对应时间点的产量
            sql = "SELECT yearchanliang FROM last WHERE tS = %s"
            cursor.execute(sql, (target_time,))
            result = cursor.fetchone()

            if result and result[0] is not None:
                return float(result[0])
            return 0.0

        # 原有的从cql表获取数据并存储到last表的逻辑
        year_chanliang = 0

        # 获取目标时间点的产量值
        sql = f"SELECT bban FROM {table_name} where dataTime = '{target_time}'"
        cursor.execute(sql)
        cur_res = cursor.fetchall()
        if len(cur_res) > 0:
            year_chanliang = cur_res[0][0]

        # 获取去年12月25日23:30的基准值
        if (current_time.year == 2024):
            last_year = current_time.year
        else:
            last_year = current_time.year - 1
        base_time = datetime(last_year, 12, 25, 23, 30, 0)

        # 获取去年12月25日23:30时的产量
        sql = f"SELECT bban FROM {table_name} WHERE dataTime = '{base_time}'"
        cursor.execute(sql)
        pre_res = cursor.fetchall()
        if len(pre_res) > 0:
            year_chanliang = 0.99*(year_chanliang - pre_res[0][0])

        year_chanliang = round(year_chanliang, 1)

        if not return_from_last:
            # 将计算结果存储到last表中
            try:
                # 先检查是否存在该时间点的记录
                check_sql = "SELECT id FROM last WHERE tS = %s"
                cursor.execute(check_sql, (target_time,))
                result = cursor.fetchone()

                if result:
                    # 如果记录存在，则更新
                    update_sql = """
                        UPDATE last 
                        SET yearchanliang = %s 
                        WHERE tS = %s
                    """
                    cursor.execute(update_sql, (year_chanliang, target_time))
                else:
                    # 如果记录不存在，则插入新记录
                    insert_sql = """
                        INSERT INTO last (tS, yearchanliang)
                        VALUES (%s, %s)
                    """
                    cursor.execute(insert_sql, (target_time, year_chanliang))

                cursor.connection.commit()
                print(f"成功更新/插入 {target_time} 的年产量数据：{year_chanliang}")
            except Exception as e:
                cursor.connection.rollback()
                print(f"更新数据库时出错：{str(e)}")

        return year_chanliang
    except Exception as e:
        print("baocuo2")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_last_month_end_date():
    # 获取当前日期
    current_date = datetime.now()

    # 获取上个月的最后一天
    # 计算上个月的第一天：先将当前日期的月份减1，再设置日期为1号
    first_day_of_current_month = current_date.replace(day=1)
    last_day_of_last_month = first_day_of_current_month - timedelta(days=1)

    # 返回上个月最后一天的日期
    return last_day_of_last_month.date()


def get_last_year_end_date():
    """
    获取去年的最后一天日期
    """
    # 获取当前日期
    current_date = datetime.now()

    # 获取去年的第一天
    first_day_of_current_year = current_date.replace(month=1, day=1)
    last_day_of_last_year = first_day_of_current_year - timedelta(days=1)

    # 返回去年的最后一天的日期
    return last_day_of_last_year.date()


from datetime import datetime, timedelta


def get_today_dianhao(table_name, return_from_last=False):
    """
    获取今日电耗并存储到last表
    :param table_name: 表名
    :param return_from_last: 是否从last表返回数据
    :return: 今日电耗值
    """
    current_time = datetime.now()

    # 定义固定的时间点
    time_points = [
        {"time": current_time.replace(hour=7, minute=30, second=0, microsecond=0), "label": "07:30"},
        {"time": current_time.replace(hour=15, minute=30, second=0, microsecond=0), "label": "15:30"},
        {"time": current_time.replace(hour=23, minute=30, second=0, microsecond=0), "label": "23:30"},
    ]

    # 根据当前时间确定应该使用的时间点
    if current_time.hour < 7 or (current_time.hour == 7 and current_time.minute < 30):
        # 7:30之前使用昨天23:30的数据
        target_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
    elif current_time.hour < 15 or (current_time.hour == 15 and current_time.minute < 30):
        # 15:30之前使用7:30的数据
        target_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
    elif current_time.hour < 23 or (current_time.hour == 23 and current_time.minute < 30):
        # 23:30之前使用15:30的数据
        target_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
    else:
        # 23:30之后使用23:30的数据
        target_time = current_time.replace(hour=23, minute=30, second=0, microsecond=0)

    # 原有的从threehand表获取数据并存储到last表的逻辑
    today_dianhao = 0.0
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()
        # 获取目标时间点的电耗值
        sql = f"SELECT dianHao FROM {table_name} WHERE inputTime = '{target_time}'"
        cursor.execute(sql)
        cur_res = cursor.fetchall()
        if len(cur_res) > 0:
            today_dianhao = float(cur_res[0][0])

        # 获取昨天23:30时的电耗值
        pre_time = (current_time.replace(hour=23, minute=30, second=0, microsecond=0) -
                    timedelta(days=1))
        sql = f"SELECT dianHao FROM {table_name} WHERE inputTime = '{pre_time}'"

        cursor.execute(sql)
        pre_res = cursor.fetchall()

        if len(pre_res) > 0:
            today_dianhao -= float(pre_res[0][0])

        today_dianhao = round(today_dianhao, 1)

        return today_dianhao
    except Exception as e:
        logger.error(f"发生错误: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# def get_month_dianhao(table_name, return_from_last=False):
#     """
#     获取月电耗并存储到last表
#     :param table_name: 表名
#     :param return_from_last: 是否从last表返回数据
#     :return: 月电耗值
#     """
#     current_time = datetime.now()
#
#     # 定义固定的时间点
#     time_points = [
#         {"time": current_time.replace(hour=7, minute=30, second=0, microsecond=0), "label": "07:30"},
#         {"time": current_time.replace(hour=15, minute=30, second=0, microsecond=0), "label": "15:30"},
#         {"time": current_time.replace(hour=23, minute=30, second=0, microsecond=0), "label": "23:30"},
#     ]
#
#     # 根据当前时间确定应该使用的时间点
#     if current_time.hour < 7 or (current_time.hour == 7 and current_time.minute < 30):
#         # 7:30之前使用昨天23:30的数据
#         target_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
#     elif current_time.hour < 15 or (current_time.hour == 15 and current_time.minute < 30):
#         # 15:30之前使用7:30的数据
#         target_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
#     elif current_time.hour < 23 or (current_time.hour == 23 and current_time.minute < 30):
#         # 23:30之前使用15:30的数据
#         target_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
#     else:
#         # 23:30之后使用23:30的数据
#         target_time = current_time.replace(hour=23, minute=30, second=0, microsecond=0)
#
#     # 原有的从threehand表获取数据并存储到last表的逻辑
#     month_dianhao = 0.0
#     conn = None
#     cursor = None
#     try:
#         conn = pool.connection()
#         cursor = conn.cursor()
#
#         # 获取目标时间点的电耗值
#         sql = f"SELECT dianHao FROM {table_name} WHERE inputTime = '{target_time}'"
#         cursor.execute(sql)
#         cur_res = cursor.fetchall()
#         if len(cur_res) > 0:
#             month_dianhao = float(cur_res[0][0])
#
#         # 获取上月25日23:00的基准值
#         if current_time.day < 25:
#             if current_time.month == 1:
#                 base_date = current_time.replace(year=current_time.year - 1, month=12, day=25)
#             else:
#                 base_date = current_time.replace(month=current_time.month - 1, day=25)
#         else:
#             base_date = current_time.replace(day=25)
#
#         base_time = base_date.replace(hour=23, minute=30, second=0, microsecond=0)
#
#         sql = f"SELECT dianHao FROM {table_name} WHERE inputTime = '{base_time}'"
#         cursor.execute(sql)
#         pre_res = cursor.fetchall()
#         if len(pre_res) > 0:
#             month_dianhao -= float(pre_res[0][0])
#
#         month_dianhao = round(month_dianhao, 1)
#
#         return month_dianhao
#     except Exception as e:
#         logger.error(f"获取月电耗时发生错误: {e}")
#     finally:
#         if cursor: cursor.close()
#         if conn: conn.close()
def get_month_dianhao(table_name, return_from_last=False):
    """
    获取月电耗并存储到last表
    :param table_name: 表名
    :param return_from_last: 是否从last表返回数据
    :return: 月电耗值
    """
    current_time = datetime.now()

    # 定义固定的时间点
    time_points = [
        {"time": current_time.replace(hour=7, minute=30, second=0, microsecond=0), "label": "07:30"},
        {"time": current_time.replace(hour=15, minute=30, second=0, microsecond=0), "label": "15:30"},
        {"time": current_time.replace(hour=23, minute=30, second=0, microsecond=0), "label": "23:30"},
    ]

    # 根据当前时间确定应该使用的时间点
    if current_time.hour < 7 or (current_time.hour == 7 and current_time.minute < 30):
        # 7:30之前使用昨天23:30的数据
        target_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
    elif current_time.hour < 15 or (current_time.hour == 15 and current_time.minute < 30):
        # 15:30之前使用7:30的数据
        target_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
    elif current_time.hour < 23 or (current_time.hour == 23 and current_time.minute < 30):
        # 23:30之前使用15:30的数据
        target_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
    else:
        # 23:30之后使用23:30的数据
        target_time = current_time.replace(hour=23, minute=30, second=0, microsecond=0)

    # 原有的从threehand表获取数据并存储到last表的逻辑
    month_dianhao = 0.0
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()

        # 获取目标时间点的电耗值
        sql = f"SELECT dianHao FROM {table_name} WHERE inputTime = '{target_time}'"
        cursor.execute(sql)
        cur_res = cursor.fetchall()
        if len(cur_res) > 0:
            month_dianhao = float(cur_res[0][0])

        # 获取上月25日23:00的基准值
        if current_time.day < 26:#改
            if current_time.month == 1:
                base_date = current_time.replace(year=current_time.year - 1, month=12, day=25)
            else:
                base_date = current_time.replace(month=current_time.month - 1, day=25)
        else:
            base_date = current_time.replace(day=25)

        base_time = base_date.replace(hour=23, minute=30, second=0, microsecond=0)

        sql = f"SELECT dianHao FROM {table_name} WHERE inputTime = '{base_time}'"
        cursor.execute(sql)
        pre_res = cursor.fetchall()
        if len(pre_res) > 0:
            month_dianhao -= float(pre_res[0][0])

        month_dianhao = round(month_dianhao, 1)

        return month_dianhao
    except Exception as e:
        logger.error(f"获取月电耗时发生错误: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# def get_year_dianhao(table_name, return_from_last=False):
#     """
#     获取年电耗并存储到last表
#     :param table_name: 表名
#     :param return_from_last: 是否从last表返回数据
#     :return: 年电耗值
#     """
#     current_time = datetime.now()
#
#     # 定义固定的时间点
#     time_points = [
#         {"time": current_time.replace(hour=7, minute=30, second=0, microsecond=0), "label": "07:30"},
#         {"time": current_time.replace(hour=15, minute=30, second=0, microsecond=0), "label": "15:30"},
#         {"time": current_time.replace(hour=23, minute=30, second=0, microsecond=0), "label": "23:30"},
#     ]
#
#     # 根据当前时间确定应该使用的时间点
#     if current_time.hour < 7 or (current_time.hour == 7 and current_time.minute < 30):
#         # 7:30之前使用昨天23:30的数据
#         target_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
#     elif current_time.hour < 15 or (current_time.hour == 15 and current_time.minute < 30):
#         # 15:30之前使用7:30的数据
#         target_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
#     elif current_time.hour < 23 or (current_time.hour == 23 and current_time.minute < 30):
#         # 23:30之前使用15:30的数据
#         target_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
#     else:
#         # 23:30之后使用23:30的数据
#         target_time = current_time.replace(hour=23, minute=30, second=0, microsecond=0)
#
#     # 原有的从threehand表获取数据并存储到last表的逻辑
#     year_dianhao = 0.0
#     conn = None
#     cursor = None
#     try:
#         conn = pool.connection()
#         cursor = conn.cursor()
#         # 获取目标时间点的电耗值
#         sql = f"SELECT dianHao FROM {table_name} WHERE inputTime = '{target_time}'"
#         cursor.execute(sql)
#         cur_res = cursor.fetchall()
#         if len(cur_res) > 0:
#             year_dianhao = float(cur_res[0][0])
#
#         # 获取去年12月25日23:30的基准值
#         if (current_time.year == 2024):
#             last_year = current_time.year
#         else:
#             last_year = current_time.year - 1
#         base_time = datetime(last_year, 12, 25, 23, 30, 0)
#
#         # 获取去年12月25日23:30时的电耗值
#         sql = f"SELECT dianHao FROM {table_name} WHERE inputTime = '{base_time}'"
#         cursor.execute(sql)
#         pre_res = cursor.fetchall()
#         if len(pre_res) > 0:
#             year_dianhao -= float(pre_res[0][0])
#
#         year_dianhao = round(year_dianhao, 1)
#
#         return year_dianhao
#     except Exception as e:
#         logger.error(f"获取月电耗时发生错误: {e}")
#     finally:
#         if cursor: cursor.close()
#         if conn: conn.close()


# 获取汽耗的函数
def get_year_dianhao(table_name, return_from_last=False):
    """
    获取年电耗并存储到last表
    :param table_name: 表名
    :param return_from_last: 是否从last表返回数据
    :return: 年电耗值
    """
    current_time = datetime.now()

    # 定义固定的时间点
    time_points = [
        {"time": current_time.replace(hour=7, minute=30, second=0, microsecond=0), "label": "07:30"},
        {"time": current_time.replace(hour=15, minute=30, second=0, microsecond=0), "label": "15:30"},
        {"time": current_time.replace(hour=23, minute=30, second=0, microsecond=0), "label": "23:30"},
    ]

    # 根据当前时间确定应该使用的时间点
    if current_time.hour < 7 or (current_time.hour == 7 and current_time.minute < 30):
        # 7:30之前使用昨天23:30的数据
        target_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
    elif current_time.hour < 15 or (current_time.hour == 15 and current_time.minute < 30):
        # 15:30之前使用7:30的数据
        target_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
    elif current_time.hour < 23 or (current_time.hour == 23 and current_time.minute < 30):
        # 23:30之前使用15:30的数据
        target_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
    else:
        # 23:30之后使用23:30的数据
        target_time = current_time.replace(hour=23, minute=30, second=0, microsecond=0)

    # 原有的从threehand表获取数据并存储到last表的逻辑
    year_dianhao = 0.0
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()
        # 获取目标时间点的电耗值
        sql = f"SELECT dianHao FROM {table_name} WHERE inputTime = '{target_time}'"
        cursor.execute(sql)
        cur_res = cursor.fetchall()
        if len(cur_res) > 0:
            year_dianhao = float(cur_res[0][0])

        # 获取去年12月25日23:30的基准值
        if (current_time.year == 2024):
            last_year = current_time.year
        else:
            last_year = current_time.year - 1
        base_time = datetime(last_year, 12, 26, 23, 30, 0)#改

        # 获取去年12月25日23:30时的电耗值
        sql = f"SELECT dianHao FROM {table_name} WHERE inputTime = '{base_time}'"
        cursor.execute(sql)
        pre_res = cursor.fetchall()
        if len(pre_res) > 0:
            year_dianhao -= float(pre_res[0][0])

        year_dianhao = round(year_dianhao, 1)

        return year_dianhao
    except Exception as e:
        logger.error(f"获取月电耗时发生错误: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_today_qihao(table_name, return_from_last=False):
    """
    获取今日汽耗并存储到last表
    :param table_name: 表名
    :param return_from_last: 是否从last表返回数据
    :return: 今日汽耗值
    """
    current_time = datetime.now()

    # 定义固定的时间点
    time_points = [
        {"time": current_time.replace(hour=7, minute=30, second=0, microsecond=0), "label": "07:30"},
        {"time": current_time.replace(hour=15, minute=30, second=0, microsecond=0), "label": "15:30"},
        {"time": current_time.replace(hour=23, minute=30, second=0, microsecond=0), "label": "23:30"},
    ]

    # 根据当前时间确定应该使用的时间点
    if current_time.hour < 7 or (current_time.hour == 7 and current_time.minute < 30):
        target_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
    elif current_time.hour < 15 or (current_time.hour == 15 and current_time.minute < 30):
        target_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
    elif current_time.hour < 23 or (current_time.hour == 23 and current_time.minute < 30):
        target_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
    else:
        target_time = current_time.replace(hour=23, minute=30, second=0, microsecond=0)

    # 原有的从threehand表获取数据并存储到last表的逻辑
    today_qihao = 0.0
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()
        # 获取目标时间点的汽耗值
        sql = f"SELECT bqi FROM {table_name} WHERE dataTime = '{target_time}'"
        cursor.execute(sql)
        cur_res = cursor.fetchall()
        if len(cur_res) > 0:
            today_qihao = float(cur_res[0][0])

        # 获取昨天23:30时的汽耗值
        pre_time = (current_time.replace(hour=23, minute=30, second=0, microsecond=0) -
                    timedelta(days=1))
        sql = f"SELECT bqi FROM {table_name} WHERE dataTime = '{pre_time}'"
        cursor.execute(sql)
        pre_res = cursor.fetchall()
        if len(pre_res) > 0:
            today_qihao -= float(pre_res[0][0])

        today_qihao = round(today_qihao, 1)

        return today_qihao
    except Exception as e:
        logger.error(f"获取月电耗时发生错误: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# def get_month_qihao(table_name, return_from_last=False):
#     """
#     获取月汽耗并存储到last表
#     :param table_name: 表名
#     :param return_from_last: 是否从last表返回数据
#     :return: 月汽耗值
#     """
#     current_time = datetime.now()
#
#     # 定义固定的时间点
#     time_points = [
#         {"time": current_time.replace(hour=7, minute=30, second=0, microsecond=0), "label": "07:30"},
#         {"time": current_time.replace(hour=15, minute=30, second=0, microsecond=0), "label": "15:30"},
#         {"time": current_time.replace(hour=23, minute=30, second=0, microsecond=0), "label": "23:30"},
#     ]
#
#     # 根据当前时间确定应该使用的时间点
#     if current_time.hour < 7 or (current_time.hour == 7 and current_time.minute < 30):
#         target_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
#     elif current_time.hour < 15 or (current_time.hour == 15 and current_time.minute < 30):
#         target_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
#     elif current_time.hour < 23 or (current_time.hour == 23 and current_time.minute < 30):
#         target_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
#     else:
#         target_time = current_time.replace(hour=23, minute=30, second=0, microsecond=0)
#
#     # 原有的从threehand表获取数据并存储到last表的逻辑
#     month_qihao = 0.0
#     conn = None
#     cursor = None
#     try:
#         conn = pool.connection()
#         cursor = conn.cursor()
#         # 获取目标时间点的汽耗值
#         sql = f"SELECT bqi FROM {table_name} WHERE dataTime = '{target_time}'"
#         cursor.execute(sql)
#         cur_res = cursor.fetchall()
#         if len(cur_res) > 0:
#             month_qihao = float(cur_res[0][0])
#
#         # 获取上月25日23:00的基准值
#         if current_time.day < 25:
#             if current_time.month == 1:
#                 base_date = current_time.replace(year=current_time.year - 1, month=12, day=25)
#             else:
#                 base_date = current_time.replace(month=current_time.month - 1, day=25)
#         else:
#             base_date = current_time.replace(day=25)
#
#         base_time = base_date.replace(hour=23, minute=30, second=0, microsecond=0)
#
#         sql = f"SELECT bqi FROM {table_name} WHERE dataTime = '{base_time}'"
#         cursor.execute(sql)
#         pre_res = cursor.fetchall()
#         if len(pre_res) > 0:
#             month_qihao -= float(pre_res[0][0])
#
#         month_qihao = round(month_qihao, 1)
#
#         return month_qihao
#     except Exception as e:
#         logger.error(f"获取月qi耗时发生错误: {e}")
#     finally:
#         if cursor: cursor.close()
#         if conn: conn.close()
def get_month_qihao(table_name, return_from_last=False):
    """
    获取月汽耗并存储到last表
    :param table_name: 表名
    :param return_from_last: 是否从last表返回数据
    :return: 月汽耗值
    """
    current_time = datetime.now()

    # 定义固定的时间点
    time_points = [
        {"time": current_time.replace(hour=7, minute=30, second=0, microsecond=0), "label": "07:30"},
        {"time": current_time.replace(hour=15, minute=30, second=0, microsecond=0), "label": "15:30"},
        {"time": current_time.replace(hour=23, minute=30, second=0, microsecond=0), "label": "23:30"},
    ]

    # 根据当前时间确定应该使用的时间点
    if current_time.hour < 7 or (current_time.hour == 7 and current_time.minute < 30):
        target_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
    elif current_time.hour < 15 or (current_time.hour == 15 and current_time.minute < 30):
        target_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
    elif current_time.hour < 23 or (current_time.hour == 23 and current_time.minute < 30):
        target_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
    else:
        target_time = current_time.replace(hour=23, minute=30, second=0, microsecond=0)

    # 原有的从threehand表获取数据并存储到last表的逻辑
    month_qihao = 0.0
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()
        # 获取目标时间点的汽耗值
        sql = f"SELECT bqi FROM {table_name} WHERE dataTime = '{target_time}'"
        cursor.execute(sql)
        cur_res = cursor.fetchall()
        if len(cur_res) > 0:
            month_qihao = float(cur_res[0][0])

        # 获取上月25日23:00的基准值
        if current_time.day < 26:#改
            if current_time.month == 1:
                base_date = current_time.replace(year=current_time.year - 1, month=12, day=25)
            else:
                base_date = current_time.replace(month=current_time.month - 1, day=25)
        else:
            base_date = current_time.replace(day=25)

        base_time = base_date.replace(hour=23, minute=30, second=0, microsecond=0)

        sql = f"SELECT bqi FROM {table_name} WHERE dataTime = '{base_time}'"
        cursor.execute(sql)
        pre_res = cursor.fetchall()
        if len(pre_res) > 0:
            month_qihao -= float(pre_res[0][0])

        month_qihao = round(month_qihao, 1)

        return month_qihao
    except Exception as e:
        logger.error(f"获取月qi耗时发生错误: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def get_year_qihao(table_name, return_from_last=False):
    """
    获取年汽耗并存储到last表
    :param table_name: 表名
    :param return_from_last: 是否从last表返回数据
    :return: 年汽耗值
    """
    current_time = datetime.now()

    # 定义固定的时间点
    time_points = [
        {"time": current_time.replace(hour=7, minute=30, second=0, microsecond=0), "label": "07:30"},
        {"time": current_time.replace(hour=15, minute=30, second=0, microsecond=0), "label": "15:30"},
        {"time": current_time.replace(hour=23, minute=30, second=0, microsecond=0), "label": "23:30"},
    ]

    # 根据当前时间确定应该使用的时间点
    if current_time.hour < 7 or (current_time.hour == 7 and current_time.minute < 30):
        target_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
    elif current_time.hour < 15 or (current_time.hour == 15 and current_time.minute < 30):
        target_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
    elif current_time.hour < 23 or (current_time.hour == 23 and current_time.minute < 30):
        target_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
    else:
        target_time = current_time.replace(hour=23, minute=30, second=0, microsecond=0)

    # 原有的从threehand表获取数据并存储到last表的逻辑
    year_qihao = 0.0
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()
        # 获取目标时间点的汽耗值
        sql = f"SELECT bqi FROM {table_name} WHERE dataTime = '{target_time}'"
        cursor.execute(sql)
        cur_res = cursor.fetchall()
        if len(cur_res) > 0:
            year_qihao = float(cur_res[0][0])

        # 获取去年12月25日23:00的基准值
        if (current_time.year == 2024):
            last_year = current_time.year
        else:
            last_year = current_time.year - 1
        base_time = datetime(last_year, 12, 25, 23, 30, 0)

        # 获取去年12月25日23:30时的汽耗值
        sql = f"SELECT bqi FROM {table_name} WHERE dataTime = '{base_time}'"
        cursor.execute(sql)
        pre_res = cursor.fetchall()
        if len(pre_res) > 0:
            year_qihao -= float(pre_res[0][0])

        year_qihao = round(year_qihao, 1)

        return year_qihao
    except Exception as e:
        logger.error(f"获取yearqi耗时发生错误: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def get_today_luhao(table_name, return_from_last=False):
    """
    获取今日卤耗并存储到last表
    :param table_name: 表名
    :param return_from_last: 是否从last表返回数据
    :return: 今日卤耗值
    """
    current_time = datetime.now()

    # 定义固定的时间点
    time_points = [
        {"time": current_time.replace(hour=7, minute=30, second=0, microsecond=0), "label": "07:30"},
        {"time": current_time.replace(hour=15, minute=30, second=0, microsecond=0), "label": "15:30"},
        {"time": current_time.replace(hour=23, minute=30, second=0, microsecond=0), "label": "23:30"},
    ]

    # 根据当前时间确定应该使用的时间点
    if current_time.hour < 7 or (current_time.hour == 7 and current_time.minute < 30):
        target_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
    elif current_time.hour < 15 or (current_time.hour == 15 and current_time.minute < 30):
        target_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
    elif current_time.hour < 23 or (current_time.hour == 23 and current_time.minute < 30):
        target_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
    else:
        target_time = current_time.replace(hour=23, minute=30, second=0, microsecond=0)

    # 原有的从threehand表获取数据并存储到last表的逻辑
    today_luhao = 0.0
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()
        # 获取目标时间点的卤耗值
        sql = f"SELECT bhao FROM {table_name} WHERE dataTime = '{target_time}'"
        cursor.execute(sql)
        cur_res = cursor.fetchall()
        if len(cur_res) > 0:
            today_luhao = float(cur_res[0][0])

        # 获取昨天23:30时的卤耗值
        pre_time = (current_time.replace(hour=23, minute=30, second=0, microsecond=0) -
                    timedelta(days=1))
        sql = f"SELECT bhao FROM {table_name} WHERE dataTime = '{pre_time}'"
        cursor.execute(sql)
        pre_res = cursor.fetchall()
        if len(pre_res) > 0:
            today_luhao -= float(pre_res[0][0])

        today_luhao = round(today_luhao, 1)

        return today_luhao
    except Exception as e:
        logger.error(f"获取todaydian耗时发生错误: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# def get_month_luhao(table_name, return_from_last=False):
#     """
#     获取月卤耗并存储到last表
#     :param table_name: 表名
#     :param return_from_last: 是否从last表返回数据
#     :return: 月卤耗值
#     """
#     current_time = datetime.now()
#
#     # 定义固定的时间点
#     time_points = [
#         {"time": current_time.replace(hour=7, minute=30, second=0, microsecond=0), "label": "07:30"},
#         {"time": current_time.replace(hour=15, minute=30, second=0, microsecond=0), "label": "15:30"},
#         {"time": current_time.replace(hour=23, minute=30, second=0, microsecond=0), "label": "23:30"},
#     ]
#
#     # 根据当前时间确定应该使用的时间点
#     if current_time.hour < 7 or (current_time.hour == 7 and current_time.minute < 30):
#         target_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
#     elif current_time.hour < 15 or (current_time.hour == 15 and current_time.minute < 30):
#         target_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
#     elif current_time.hour < 23 or (current_time.hour == 23 and current_time.minute < 30):
#         target_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
#     else:
#         target_time = current_time.replace(hour=23, minute=30, second=0, microsecond=0)
#
#     # 原有的从threehand表获取数据并存储到last表的逻辑
#     month_luhao = 0.0
#     conn = None
#     cursor = None
#     try:
#         conn = pool.connection()
#         cursor = conn.cursor()
#         # 获取目标时间点的卤耗值
#         sql = f"SELECT bhao FROM {table_name} WHERE dataTime = '{target_time}'"
#         cursor.execute(sql)
#         cur_res = cursor.fetchall()
#         if len(cur_res) > 0:
#             month_luhao = float(cur_res[0][0])
#
#         # 获取上月25日23:00的基准值
#         if current_time.day < 25:
#             if current_time.month == 1:
#                 base_date = current_time.replace(year=current_time.year - 1, month=12, day=25)
#             else:
#                 base_date = current_time.replace(month=current_time.month - 1, day=25)
#         else:
#             base_date = current_time.replace(day=25)
#
#         base_time = base_date.replace(hour=23, minute=30, second=0, microsecond=0)
#
#         sql = f"SELECT bhao FROM {table_name} WHERE dataTime = '{base_time}'"
#         cursor.execute(sql)
#         pre_res = cursor.fetchall()
#         if len(pre_res) > 0:
#             month_luhao -= float(pre_res[0][0])
#
#         month_luhao = round(month_luhao, 1)
#
#         return month_luhao
#     except Exception as e:
#         logger.error(f"获取monthlu耗时发生错误: {e}")
#     finally:
#         if cursor: cursor.close()
#         if conn: conn.close()
def get_month_luhao(table_name, return_from_last=False):
    """
    获取月卤耗并存储到last表
    :param table_name: 表名
    :param return_from_last: 是否从last表返回数据
    :return: 月卤耗值
    """
    current_time = datetime.now()

    # 定义固定的时间点
    time_points = [
        {"time": current_time.replace(hour=7, minute=30, second=0, microsecond=0), "label": "07:30"},
        {"time": current_time.replace(hour=15, minute=30, second=0, microsecond=0), "label": "15:30"},
        {"time": current_time.replace(hour=23, minute=30, second=0, microsecond=0), "label": "23:30"},
    ]

    # 根据当前时间确定应该使用的时间点
    if current_time.hour < 7 or (current_time.hour == 7 and current_time.minute < 30):
        target_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
    elif current_time.hour < 15 or (current_time.hour == 15 and current_time.minute < 30):
        target_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
    elif current_time.hour < 23 or (current_time.hour == 23 and current_time.minute < 30):
        target_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
    else:
        target_time = current_time.replace(hour=23, minute=30, second=0, microsecond=0)

    # 原有的从threehand表获取数据并存储到last表的逻辑
    month_luhao = 0.0
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()
        # 获取目标时间点的卤耗值
        sql = f"SELECT bhao FROM {table_name} WHERE dataTime = '{target_time}'"
        cursor.execute(sql)
        cur_res = cursor.fetchall()
        if len(cur_res) > 0:
            month_luhao = float(cur_res[0][0])

        # 获取上月25日23:00的基准值
        if current_time.day < 26:
            if current_time.month == 1:
                base_date = current_time.replace(year=current_time.year - 1, month=12, day=25)
            else:
                base_date = current_time.replace(month=current_time.month - 1, day=25)
        else:
            base_date = current_time.replace(day=25)

        base_time = base_date.replace(hour=23, minute=30, second=0, microsecond=0)

        sql = f"SELECT bhao FROM {table_name} WHERE dataTime = '{base_time}'"
        cursor.execute(sql)
        pre_res = cursor.fetchall()
        if len(pre_res) > 0:
            month_luhao -= float(pre_res[0][0])

        month_luhao = round(month_luhao, 1)

        return month_luhao
    except Exception as e:
        logger.error(f"获取monthlu耗时发生错误: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_month_qihao(table_name, return_from_last=False):
    """
    获取月汽耗并存储到last表
    :param table_name: 表名
    :param return_from_last: 是否从last表返回数据
    :return: 月汽耗值
    """
    current_time = datetime.now()

    # 定义固定的时间点
    time_points = [
        {"time": current_time.replace(hour=7, minute=30, second=0, microsecond=0), "label": "07:30"},
        {"time": current_time.replace(hour=15, minute=30, second=0, microsecond=0), "label": "15:30"},
        {"time": current_time.replace(hour=23, minute=30, second=0, microsecond=0), "label": "23:30"},
    ]

    # 根据当前时间确定应该使用的时间点
    if current_time.hour < 7 or (current_time.hour == 7 and current_time.minute < 30):
        target_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
    elif current_time.hour < 15 or (current_time.hour == 15 and current_time.minute < 30):
        target_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
    elif current_time.hour < 23 or (current_time.hour == 23 and current_time.minute < 30):
        target_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
    else:
        target_time = current_time.replace(hour=23, minute=30, second=0, microsecond=0)

    # 原有的从threehand表获取数据并存储到last表的逻辑
    month_qihao = 0.0
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()
        # 获取目标时间点的汽耗值
        sql = f"SELECT bqi FROM {table_name} WHERE dataTime = '{target_time}'"
        cursor.execute(sql)
        cur_res = cursor.fetchall()
        if len(cur_res) > 0:
            month_qihao = float(cur_res[0][0])

        # 获取上月25日23:00的基准值
        if current_time.day < 26:#改
            if current_time.month == 1:
                base_date = current_time.replace(year=current_time.year - 1, month=12, day=25)
            else:
                base_date = current_time.replace(month=current_time.month - 1, day=25)
        else:
            base_date = current_time.replace(day=25)

        base_time = base_date.replace(hour=23, minute=30, second=0, microsecond=0)

        sql = f"SELECT bqi FROM {table_name} WHERE dataTime = '{base_time}'"
        cursor.execute(sql)
        pre_res = cursor.fetchall()
        if len(pre_res) > 0:
            month_qihao -= float(pre_res[0][0])

        month_qihao = round(month_qihao, 1)

        return month_qihao
    except Exception as e:
        logger.error(f"获取月qi耗时发生错误: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def get_year_luhao(table_name, return_from_last=False):
    """
    获取年卤耗并存储到last表
    :param table_name: 表名
    :param return_from_last: 是否从last表返回数据
    :return: 年卤耗值
    """
    current_time = datetime.now()

    # 定义固定的时间点
    time_points = [
        {"time": current_time.replace(hour=7, minute=30, second=0, microsecond=0), "label": "07:30"},
        {"time": current_time.replace(hour=15, minute=30, second=0, microsecond=0), "label": "15:30"},
        {"time": current_time.replace(hour=23, minute=30, second=0, microsecond=0), "label": "23:30"},
    ]

    # 根据当前时间确定应该使用的时间点
    if current_time.hour < 7 or (current_time.hour == 7 and current_time.minute < 30):
        target_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
    elif current_time.hour < 15 or (current_time.hour == 15 and current_time.minute < 30):
        target_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
    elif current_time.hour < 23 or (current_time.hour == 23 and current_time.minute < 30):
        target_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
    else:
        target_time = current_time.replace(hour=23, minute=30, second=0, microsecond=0)

    # 原有的从threehand表获取数据并存储到last表的逻辑
    year_luhao = 0.0
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()
        # 获取目标时间点的卤耗值
        sql = f"SELECT bhao FROM {table_name} WHERE dataTime = '{target_time}'"
        cursor.execute(sql)
        cur_res = cursor.fetchall()
        if len(cur_res) > 0:
            year_luhao = float(cur_res[0][0])

        # 获取去年12月25日23:00的基准值
        if (current_time.year == 2024):
            last_year = current_time.year
        else:
            last_year = current_time.year - 1
        base_time = datetime(last_year, 12, 25, 23, 30, 0)

        # 获取去年12月25日23:30时的卤耗值
        sql = f"SELECT bhao FROM {table_name} WHERE dataTime = '{base_time}'"
        cursor.execute(sql)
        pre_res = cursor.fetchall()
        if len(pre_res) > 0:
            year_luhao -= float(pre_res[0][0])

        year_luhao = round(year_luhao, 1)

        return year_luhao
    except Exception as e:
        logger.error(f"获取yearlu耗时发生错误: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def should_update_data():
    """
    检查是否需要更新数据
    每5分钟更新一次
    """
    global last_update_time
    current_time = datetime.now()

    # 如果是首次运行，或者距离上次更新已经过了5分钟，就需要更新
    if last_update_time is None or (current_time - last_update_time).total_seconds() >= 600:  # 300秒 = 5分钟
        last_update_time = current_time
        return True

    return False


def get_abanchanliang(table_name):
    """获取A班产量，使用aban字段"""
    conn = None
    cursor = None
    try:

        current_time = datetime.now()
        conn = pool.connection()
        cursor = conn.cursor()

        # 计算起始时间（上个月25日）
        if current_time.day >= 26:
            # 如果今天是25号及以后，比如5月25日，就用本月25日
            start_day = current_time.replace(day=26, hour=7, minute=30, second=0, microsecond=0)
        else:
            # 如果今天是25号之前，比如4月15日，就用上个月25日
            if current_time.month == 1:
                # 特别处理1月，回到上一年12月
                start_day = current_time.replace(year=current_time.year - 1, month=12, day=26, hour=7, minute=30,
                                                 second=0, microsecond=0)
            else:
                start_day = current_time.replace(month=current_time.month - 1, day=26, hour=7, minute=30, second=0,
                                                 microsecond=0)

        # 结束时间是当前时间
        end_day = current_time

        # 修改SQL查询，使用aban字段，排除NULL值和空值
        sql = f"""
            SELECT dataTime, bban 
            FROM {table_name} 
            WHERE banci = '一班' 
            AND dataTime >= '{start_day}' 
            AND dataTime < '{end_day}'
            AND bban IS NOT NULL
            AND bban != ''
            ORDER BY dataTime
        """

        cursor.execute(sql)
        results = cursor.fetchall()

        aban_chanliang = 0.0
        for row in results:
            current_time = row[0]
            try:
                current_value = float(row[1])
            except (TypeError, ValueError):
                continue  # 跳过无法转换为float的值

            # 计算前一个时间点
            if current_time.hour == 7 and current_time.minute == 30:
                previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
            elif current_time.hour == 15 and current_time.minute == 30:
                previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
            elif current_time.hour == 23 and current_time.minute == 30:
                previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
            else:
                continue

            # 查询前一个时间点的值，同样使用aban字段
            sql = f"""
                SELECT bban 
                FROM {table_name} 
                WHERE dataTime = '{previous_time}'
                AND bban IS NOT NULL
                AND bban != ''
            """
            cursor.execute(sql)
            previous_result = cursor.fetchone()

            if previous_result:
                try:
                    previous_value = float(previous_result[0])
                    difference = current_value - previous_value
                    if difference > 0:  # 只累加正值
                        aban_chanliang += difference
                except (TypeError, ValueError):
                    continue  # 跳过无法转换为float的值
        aban_chanliang=0.99*aban_chanliang
        return round(aban_chanliang, 1)
    except Exception as e:
        logger.error(f"获取A班产量时发生错误: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def get_abanqihao(table_name):
    aban_qihao = 0.0
    current_time = datetime.now()

    # 【修改1】获取起始时间（上个月25日）
    if current_time.day >= 26:
        # 如果今天是25号或之后，比如5月25日，用本月25日
        start_day = current_time.replace(day=26, hour=7, minute=30, second=0, microsecond=0)
    else:
        # 今天小于25号，比如4月15日，用上个月25日
        if current_time.month == 1:
            start_day = current_time.replace(year=current_time.year - 1, month=12, day=26, hour=7, minute=30, second=0,
                                             microsecond=0)
        else:
            start_day = current_time.replace(month=current_time.month - 1, day=26, hour=7, minute=30, second=0,
                                             microsecond=0)

    # 【修改2】结束时间是当前时刻
    end_day = current_time
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()

        # SQL查询获取当月"一班"的所有记录，按时间排序
        sql = f"""
            SELECT inputTime, qiHao 
        FROM {table_name} 
        WHERE classes = '一班' 
        AND inputTime >= '{start_day}' 
        AND inputTime < '{end_day}'
        ORDER BY inputTime
    """

        cursor.execute(sql)
        results = cursor.fetchall()

        # 处理每条记录
        for row in results:
            current_time = row[0]  # 当前记录的时间
            current_value = float(row[1])  # 当前记录的qiHao值

            # 计算前一个时间点
            if current_time.hour == 7 and current_time.minute == 30:
                # 如果当前是7:30，则前一个时间点是前一天的23:30
                previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
            elif current_time.hour == 15 and current_time.minute == 30:
                # 如果当前是15:30，则前一个时间点是当天的7:30
                previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
            elif current_time.hour == 23 and current_time.minute == 30:
                # 如果当前是23:30，则前一个时间点是当天的15:30
                previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
            else:
                # 跳过其他时间点
                continue

            # 查询前一个时间点的值
            sql = f"""
                SELECT qiHao 
                FROM {table_name} 
                WHERE inputTime = '{previous_time}'
            """
            cursor.execute(sql)
            previous_result = cursor.fetchone()

            if previous_result:
                previous_value = float(previous_result[0])
                difference = current_value - previous_value
                if difference > 0:  # 只累加正值
                    aban_qihao += difference

        return round(aban_qihao, 1)
    except Exception as e:
        logger.error(f"获取一班qihao时发生错误: {e}")

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def get_abanluhao(table_name):
    aban_luhao = 0.0
    current_time = datetime.now()

    # 【修改1】获取起始时间（上个月25日）
    if current_time.day >= 26:
        # 如果今天是25号或之后，比如5月25日，用本月25日
        start_day = current_time.replace(day=26, hour=7, minute=30, second=0, microsecond=0)
    else:
        # 今天小于25号，比如4月15日，用上个月25日
        if current_time.month == 1:
            start_day = current_time.replace(year=current_time.year - 1, month=12, day=26, hour=7, minute=30, second=0,
                                             microsecond=0)
        else:
            start_day = current_time.replace(month=current_time.month - 1, day=26, hour=7, minute=30, second=0,
                                             microsecond=0)

    # 【修改2】结束时间是当前时刻
    end_day = current_time
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()

        # SQL查询获取当月"一班"的所有记录，按时间排序
        sql = f"""
            SELECT dataTime, bhao 
        FROM {table_name} 
        WHERE banci = '一班' 
        AND dataTime >= '{start_day}' 
        AND dataTime < '{end_day}'
        ORDER BY dataTime
    """

        cursor.execute(sql)
        results = cursor.fetchall()

        # 处理每条记录
        for row in results:
            current_time = row[0]  # 当前记录的时间
            current_value = float(row[1])  # 当前记录的ahao值

            # 计算前一个时间点
            if current_time.hour == 7 and current_time.minute == 30:
                # 如果当前是7:30，则前一个时间点是前一天的23:30
                previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
            elif current_time.hour == 15 and current_time.minute == 30:
                # 如果当前是15:30，则前一个时间点是当天的7:30
                previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
            elif current_time.hour == 23 and current_time.minute == 30:
                # 如果当前是23:30，则前一个时间点是当天的15:30
                previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
            else:
                # 跳过其他时间点
                continue

            # 查询前一个时间点的值
            sql = f"""
                SELECT bhao 
                FROM {table_name} 
                WHERE dataTime = '{previous_time}'
            """
            cursor.execute(sql)
            previous_result = cursor.fetchone()

            if previous_result:
                previous_value = float(previous_result[0])
                difference = current_value - previous_value
                if difference > 0:  # 只累加正值
                    aban_luhao += difference

        return round(aban_luhao, 1)
    except Exception as e:
        logger.error(f"获取一班炉号时发生错误: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# 二班
def get_bbanchanliang(table_name):
    """获取B班产量，使用aban字段"""
    conn = None
    cursor = None
    try:
        current_time = datetime.now()
        conn = pool.connection()
        cursor = conn.cursor()

        # 计算起始时间（上个月25日）
        if current_time.day >= 26:
            # 如果今天是25号及以后，比如5月25日，就用本月25日
            start_day = current_time.replace(day=26, hour=7, minute=30, second=0, microsecond=0)
        else:
            # 如果今天是25号之前，比如4月15日，就用上个月25日
            if current_time.month == 1:
                # 特别处理1月，回到上一年12月
                start_day = current_time.replace(year=current_time.year - 1, month=12, day=26, hour=7, minute=30,
                                                 second=0, microsecond=0)
            else:
                start_day = current_time.replace(month=current_time.month - 1, day=26, hour=7, minute=30, second=0,
                                                 microsecond=0)

        # 结束时间是当前时间
        end_day = current_time

        # 修改SQL查询，使用aban字段
        sql = f"""
            SELECT dataTime, bban 
            FROM {table_name} 
            WHERE banci = '二班' 
            AND dataTime >= '{start_day}' 
            AND dataTime < '{end_day}'
            AND bban IS NOT NULL
            AND bban != ''
            ORDER BY dataTime
        """

        cursor.execute(sql)
        results = cursor.fetchall()

        bban_chanliang = 0.0
        for row in results:
            current_time = row[0]
            try:
                current_value = float(row[1])
            except (TypeError, ValueError):
                continue  # 跳过无法转换为float的值

            # 计算前一个时间点
            if current_time.hour == 7 and current_time.minute == 30:
                previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
            elif current_time.hour == 15 and current_time.minute == 30:
                previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
            elif current_time.hour == 23 and current_time.minute == 30:
                previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
            else:
                continue

            # 查询前一个时间点的值，同样使用aban字段
            sql = f"""
                SELECT bban 
                FROM {table_name} 
                WHERE dataTime = '{previous_time}'
                AND bban IS NOT NULL
                AND bban != ''
            """
            cursor.execute(sql)
            previous_result = cursor.fetchone()

            if previous_result:
                try:
                    previous_value = float(previous_result[0])
                    difference = current_value - previous_value
                    if difference > 0:  # 只累加正值
                        bban_chanliang += difference
                except (TypeError, ValueError):
                    continue  # 跳过无法转换为float的值

        cursor.close()
        conn.close()
        bban_chanliang=0.99*bban_chanliang
        return round(bban_chanliang, 1)
    except Exception as e:
        logger.error(f"获取B班产量时发生错误: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def get_bbanqihao(table_name):
    bban_qihao = 0.0
    current_time = datetime.now()

    # 【修改1】获取起始时间（上个月25日）
    if current_time.day >= 26:
        # 如果今天是25号或之后，比如5月25日，用本月25日
        start_day = current_time.replace(day=26, hour=7, minute=30, second=0, microsecond=0)
    else:
        # 今天小于25号，比如4月15日，用上个月25日
        if current_time.month == 1:
            start_day = current_time.replace(year=current_time.year - 1, month=12, day=26, hour=7, minute=30, second=0,
                                             microsecond=0)
        else:
            start_day = current_time.replace(month=current_time.month - 1, day=26, hour=7, minute=30, second=0,
                                             microsecond=0)

    # 【修改2】结束时间是当前时刻
    end_day = current_time
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()

        # SQL查询获取当月"二班"的所有记录，按时间排序
        sql = f"""
            SELECT inputTime, qiHao 
        FROM {table_name} 
        WHERE classes = '二班' 
        AND inputTime >= '{start_day}' 
        AND inputTime < '{end_day}'
        ORDER BY inputTime
    """

        cursor.execute(sql)
        results = cursor.fetchall()

        # 处理每条记录
        for row in results:
            current_time = row[0]  # 当前记录的时间
            current_value = float(row[1])  # 当前记录的qiHao值

            # 计算前一个时间点
            if current_time.hour == 7 and current_time.minute == 30:
                # 如果当前是7:30，则前一个时间点是前一天的23:30
                previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
            elif current_time.hour == 15 and current_time.minute == 30:
                # 如果当前是15:30，则前一个时间点是当天的7:30
                previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
            elif current_time.hour == 23 and current_time.minute == 30:
                # 如果当前是23:30，则前一个时间点是当天的15:30
                previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
            else:
                # 跳过其他时间点
                continue

            # 查询前一个时间点的值
            sql = f"""
                SELECT qiHao 
                FROM {table_name} 
                WHERE inputTime = '{previous_time}'
            """
            cursor.execute(sql)
            previous_result = cursor.fetchone()

            if previous_result:
                previous_value = float(previous_result[0])
                difference = current_value - previous_value
                if difference > 0:  # 只累加正值
                    bban_qihao += difference
        cursor.close()
        conn.close()
        return round(bban_qihao, 1)
    except Exception as e:
        logger.error(f"获取二班期号时发生错误: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def get_bbanluhao(table_name):
    bban_luhao = 0.0
    current_time = datetime.now()

    # 【修改1】获取起始时间（上个月25日）
    if current_time.day >= 26:
        # 如果今天是25号或之后，比如5月25日，用本月25日
        start_day = current_time.replace(day=26, hour=7, minute=30, second=0, microsecond=0)
    else:
        # 今天小于25号，比如4月15日，用上个月25日
        if current_time.month == 1:
            start_day = current_time.replace(year=current_time.year - 1, month=12, day=26, hour=23, minute=30, second=0,
                                             microsecond=0)
        else:
            start_day = current_time.replace(month=current_time.month - 1, day=26, hour=7, minute=30, second=0,
                                             microsecond=0)

    # 【修改2】结束时间是当前时刻
    end_day = current_time
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()

        # SQL查询获取当月"一班"的所有记录，按时间排序
        sql = f"""
            SELECT dataTime, bhao 
        FROM {table_name} 
        WHERE banci = '二班' 
        AND dataTime >= '{start_day}' 
        AND dataTime < '{end_day}'
        ORDER BY dataTime
    """

        cursor.execute(sql)
        results = cursor.fetchall()

        # 处理每条记录
        for row in results:
            current_time = row[0]  # 当前记录的时间
            current_value = float(row[1])  # 当前记录的ahao值

            # 计算前一个时间点
            if current_time.hour == 7 and current_time.minute == 30:
                # 如果当前是7:30，则前一个时间点是前一天的23:30
                previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
            elif current_time.hour == 15 and current_time.minute == 30:
                # 如果当前是15:30，则前一个时间点是当天的7:30
                previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
            elif current_time.hour == 23 and current_time.minute == 30:
                # 如果当前是23:30，则前一个时间点是当天的15:30
                previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
            else:
                # 跳过其他时间点
                continue

            # 查询前一个时间点的值
            sql = f"""
                SELECT bhao 
                FROM {table_name} 
                WHERE dataTime = '{previous_time}'
            """
            cursor.execute(sql)
            previous_result = cursor.fetchone()

            if previous_result:
                previous_value = float(previous_result[0])
                difference = current_value - previous_value
                if difference > 0:  # 只累加正值
                    bban_luhao += difference
        cursor.close()
        conn.close()
        return round(bban_luhao, 1)
    except Exception as e:
        logger.error(f"获取二班炉号时发生错误: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# 三班
def get_cbanchanliang(table_name):
    """获取C班产量，使用aban字段"""
    conn = None
    cursor = None
    try:
        current_time = datetime.now()
        conn = pool.connection()
        cursor = conn.cursor()

        # 计算起始时间（上个月25日）
        if current_time.day >= 26:
            # 如果今天是25号及以后，比如5月25日，就用本月25日
            start_day = current_time.replace(day=26, hour=7, minute=30, second=0, microsecond=0)
        else:
            # 如果今天是25号之前，比如4月15日，就用上个月25日
            if current_time.month == 1:
                # 特别处理1月，回到上一年12月
                start_day = current_time.replace(year=current_time.year - 1, month=12, day=26, hour=7, minute=30,
                                                 second=0, microsecond=0)
            else:
                start_day = current_time.replace(month=current_time.month - 1, day=26, hour=7, minute=30, second=0,
                                                 microsecond=0)

        # 结束时间是当前时间
        end_day = current_time

        # 修改SQL查询，使用aban字段
        sql = f"""
            SELECT dataTime, bban 
            FROM {table_name} 
            WHERE banci = '三班' 
            AND dataTime >= '{start_day}' 
            AND dataTime < '{end_day}'
            AND bban IS NOT NULL
            AND bban != ''
            ORDER BY dataTime
        """

        cursor.execute(sql)
        results = cursor.fetchall()

        cban_chanliang = 0.0
        for row in results:
            current_time = row[0]
            try:
                current_value = float(row[1])
            except (TypeError, ValueError):
                continue  # 跳过无法转换为float的值

            # 计算前一个时间点
            if current_time.hour == 7 and current_time.minute == 30:
                previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
            elif current_time.hour == 15 and current_time.minute == 30:
                previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
            elif current_time.hour == 23 and current_time.minute == 30:
                previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
            else:
                continue

            # 查询前一个时间点的值，同样使用aban字段
            sql = f"""
                SELECT bban 
                FROM {table_name} 
                WHERE dataTime = '{previous_time}'
                AND bban IS NOT NULL
                AND bban != ''
            """
            cursor.execute(sql)
            previous_result = cursor.fetchone()

            if previous_result:
                try:
                    previous_value = float(previous_result[0])
                    difference = current_value - previous_value
                    if difference > 0:  # 只累加正值
                        cban_chanliang += difference
                except (TypeError, ValueError):
                    continue  # 跳过无法转换为float的值

        cursor.close()
        conn.close()
        cban_chanliang=0.99*cban_chanliang
        return round(cban_chanliang, 1)
    except Exception as e:
        logger.error(f"获取C班产量时发生错误: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def get_cbanqihao(table_name):
    cban_qihao = 0.0
    current_time = datetime.now()

    # 【修改1】获取起始时间（上个月25日）
    if current_time.day >= 26:
        # 如果今天是25号或之后，比如5月25日，用本月25日
        start_day = current_time.replace(day=26, hour=7, minute=30, second=0, microsecond=0)
    else:
        # 今天小于25号，比如4月15日，用上个月25日
        if current_time.month == 1:
            start_day = current_time.replace(year=current_time.year - 1, month=12, day=26, hour=7, minute=30, second=0,
                                             microsecond=0)
        else:
            start_day = current_time.replace(month=current_time.month - 1, day=26, hour=7, minute=30, second=0,
                                             microsecond=0)

    # 【修改2】结束时间是当前时刻
    end_day = current_time
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()

        # SQL查询获取当月"三班"的所有记录，按时间排序
        sql = f"""
            SELECT inputTime, qiHao 
        FROM {table_name} 
        WHERE classes = '三班' 
        AND inputTime >= '{start_day}' 
        AND inputTime < '{end_day}'
        ORDER BY inputTime
    """

        cursor.execute(sql)
        results = cursor.fetchall()

        # 处理每条记录
        for row in results:
            current_time = row[0]  # 当前记录的时间
            current_value = float(row[1])  # 当前记录的qiHao值

            # 计算前一个时间点
            if current_time.hour == 7 and current_time.minute == 30:
                # 如果当前是7:30，则前一个时间点是前一天的23:30
                previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
            elif current_time.hour == 15 and current_time.minute == 30:
                # 如果当前是15:30，则前一个时间点是当天的7:30
                previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
            elif current_time.hour == 23 and current_time.minute == 30:
                # 如果当前是23:30，则前一个时间点是当天的15:30
                previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
            else:
                # 跳过其他时间点
                continue

            # 查询前一个时间点的值
            sql = f"""
                SELECT qiHao 
                FROM {table_name} 
                WHERE inputTime = '{previous_time}'
            """
            cursor.execute(sql)
            previous_result = cursor.fetchone()

            if previous_result:
                previous_value = float(previous_result[0])
                difference = current_value - previous_value
                if difference > 0:  # 只累加正值
                    cban_qihao += difference
        cursor.close()
        conn.close()
        return round(cban_qihao, 1)
    except Exception as e:
        logger.error(f"获取三班期号时发生错误: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def get_cbanluhao(table_name):
    cban_luhao = 0.0
    current_time = datetime.now()

    # 【修改1】获取起始时间（上个月25日）
    if current_time.day >= 26:
        # 如果今天是25号或之后，比如5月25日，用本月25日
        start_day = current_time.replace(day=26, hour=7, minute=30, second=0, microsecond=0)
    else:
        # 今天小于25号，比如4月15日，用上个月25日
        if current_time.month == 1:
            start_day = current_time.replace(year=current_time.year - 1, month=12, day=26, hour=7, minute=30, second=0,
                                             microsecond=0)
        else:
            start_day = current_time.replace(month=current_time.month - 1, day=26, hour=7, minute=30, second=0,
                                             microsecond=0)

    # 【修改2】结束时间是当前时刻
    end_day = current_time
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()

        # SQL查询获取当月"一班"的所有记录，按时间排序
        sql = f"""
            SELECT dataTime, bhao 
        FROM {table_name} 
        WHERE banci = '三班' 
        AND dataTime >= '{start_day}' 
        AND dataTime < '{end_day}'
        ORDER BY dataTime
    """

        cursor.execute(sql)
        results = cursor.fetchall()

        # 处理每条记录
        for row in results:
            current_time = row[0]  # 当前记录的时间
            current_value = float(row[1])  # 当前记录的ahao值

            # 计算前一个时间点
            if current_time.hour == 7 and current_time.minute == 30:
                # 如果当前是7:30，则前一个时间点是前一天的23:30
                previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
            elif current_time.hour == 15 and current_time.minute == 30:
                # 如果当前是15:30，则前一个时间点是当天的7:30
                previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
            elif current_time.hour == 23 and current_time.minute == 30:
                # 如果当前是23:30，则前一个时间点是当天的15:30
                previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
            else:
                # 跳过其他时间点
                continue

            # 查询前一个时间点的值
            sql = f"""
                SELECT bhao 
                FROM {table_name} 
                WHERE dataTime = '{previous_time}'
            """
            cursor.execute(sql)
            previous_result = cursor.fetchone()

            if previous_result:
                previous_value = float(previous_result[0])
                difference = current_value - previous_value
                if difference > 0:  # 只累加正值
                    cban_luhao += difference
        cursor.close()
        conn.close()
        return round(cban_luhao, 1)
    except Exception as e:
        logger.error(f"获取三班炉号时发生错误: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# 四班
def get_dbanchanliang(table_name):
    """获取D班产量，使用aban字段"""
    conn = None
    cursor = None
    try:
        current_time = datetime.now()
        conn = pool.connection()
        cursor = conn.cursor()

        # 计算起始时间（上个月25日）
        if current_time.day >= 26:
            # 如果今天是25号及以后，比如5月25日，就用本月25日
            start_day = current_time.replace(day=26, hour=7, minute=30, second=0, microsecond=0)
        else:
            # 如果今天是25号之前，比如4月15日，就用上个月25日
            if current_time.month == 1:
                # 特别处理1月，回到上一年12月
                start_day = current_time.replace(year=current_time.year - 1, month=12, day=26, hour=7, minute=30,
                                                 second=0, microsecond=0)
            else:
                start_day = current_time.replace(month=current_time.month - 1, day=26, hour=7, minute=30, second=0,
                                                 microsecond=0)

        # 结束时间是当前时间
        end_day = current_time

        # 修改SQL查询，使用aban字段
        sql = f"""
            SELECT dataTime, bban 
            FROM {table_name} 
            WHERE banci = '四班' 
            AND dataTime >= '{start_day}' 
            AND dataTime < '{end_day}'
            AND bban IS NOT NULL
            AND bban != ''
            ORDER BY dataTime
        """

        cursor.execute(sql)
        results = cursor.fetchall()

        dban_chanliang = 0.0
        for row in results:
            current_time = row[0]
            try:
                current_value = float(row[1])
            except (TypeError, ValueError):
                continue  # 跳过无法转换为float的值

            # 计算前一个时间点
            if current_time.hour == 7 and current_time.minute == 30:
                previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
            elif current_time.hour == 15 and current_time.minute == 30:
                previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
            elif current_time.hour == 23 and current_time.minute == 30:
                previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
            else:
                continue

            # 查询前一个时间点的值，同样使用aban字段
            sql = f"""
                SELECT bban 
                FROM {table_name} 
                WHERE dataTime = '{previous_time}'
                AND bban IS NOT NULL
                AND bban != ''
            """
            cursor.execute(sql)
            previous_result = cursor.fetchone()

            if previous_result:
                try:
                    previous_value = float(previous_result[0])
                    difference = current_value - previous_value
                    if difference > 0:  # 只累加正值
                        dban_chanliang += difference
                except (TypeError, ValueError):
                    continue  # 跳过无法转换为float的值

        cursor.close()
        conn.close()
        dban_chanliang=0.99*dban_chanliang
        return round(dban_chanliang, 1)
    except Exception as e:
        logger.error(f"获取D班产量时发生错误: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def get_dbanqihao(table_name):
    dban_qihao = 0.0
    current_time = datetime.now()

    # 【修改1】获取起始时间（上个月25日）
    if current_time.day >= 26:
        # 如果今天是25号或之后，比如5月25日，用本月25日
        start_day = current_time.replace(day=26, hour=7, minute=30, second=0, microsecond=0)
    else:
        # 今天小于25号，比如4月15日，用上个月25日
        if current_time.month == 1:
            start_day = current_time.replace(year=current_time.year - 1, month=12, day=26, hour=7, minute=30, second=0,
                                             microsecond=0)
        else:
            start_day = current_time.replace(month=current_time.month - 1, day=26, hour=7, minute=30, second=0,
                                             microsecond=0)

    # 【修改2】结束时间是当前时刻
    end_day = current_time
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()

        # SQL查询获取当月"四班"的所有记录，按时间排序
        sql = f"""
            SELECT inputTime, qiHao 
        FROM {table_name} 
        WHERE classes = '四班' 
        AND inputTime >= '{start_day}' 
        AND inputTime < '{end_day}'
        ORDER BY inputTime
    """

        cursor.execute(sql)
        results = cursor.fetchall()

        # 处理每条记录
        for row in results:
            current_time = row[0]  # 当前记录的时间
            current_value = float(row[1])  # 当前记录的qiHao值

            # 计算前一个时间点
            if current_time.hour == 7 and current_time.minute == 30:
                # 如果当前是7:30，则前一个时间点是前一天的23:30
                previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
            elif current_time.hour == 15 and current_time.minute == 30:
                # 如果当前是15:30，则前一个时间点是当天的7:30
                previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
            elif current_time.hour == 23 and current_time.minute == 30:
                # 如果当前是23:30，则前一个时间点是当天的15:30
                previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
            else:
                # 跳过其他时间点
                continue

            # 查询前一个时间点的值
            sql = f"""
                SELECT qiHao 
                FROM {table_name} 
                WHERE inputTime = '{previous_time}'
            """
            cursor.execute(sql)
            previous_result = cursor.fetchone()

            if previous_result:
                previous_value = float(previous_result[0])
                difference = current_value - previous_value
                if difference > 0:  # 只累加正值
                    dban_qihao += difference

        cursor.close()
        conn.close()
        return round(dban_qihao, 1)
    except Exception as e:
        logger.error(f"获取四班期号时发生错误: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def get_dbanluhao(table_name):
    dban_luhao = 0.0
    current_time = datetime.now()

    # 【修改1】获取起始时间（上个月25日）
    if current_time.day >= 26:
        # 如果今天是25号或之后，比如5月25日，用本月25日
        start_day = current_time.replace(day=26, hour=7, minute=30, second=0, microsecond=0)
    else:
        # 今天小于25号，比如4月15日，用上个月25日
        if current_time.month == 1:
            start_day = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=23, minute=30, second=0,
                                             microsecond=0)
        else:
            start_day = current_time.replace(month=current_time.month - 1, day=25, hour=23, minute=30, second=0,
                                             microsecond=0)

    # 【修改2】结束时间是当前时刻
    end_day = current_time
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()

        # SQL查询获取当月"一班"的所有记录，按时间排序
        sql = f"""
            SELECT dataTime, bhao 
        FROM {table_name} 
        WHERE banci = '四班' 
        AND dataTime >= '{start_day}' 
        AND dataTime < '{end_day}'
        ORDER BY dataTime
    """

        cursor.execute(sql)
        results = cursor.fetchall()

        # 处理每条记录
        for row in results:
            current_time = row[0]  # 当前记录的时间
            current_value = float(row[1])  # 当前记录的ahao值

            # 计算前一个时间点
            if current_time.hour == 7 and current_time.minute == 30:
                # 如果当前是7:30，则前一个时间点是前一天的23:30
                previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
            elif current_time.hour == 15 and current_time.minute == 30:
                # 如果当前是15:30，则前一个时间点是当天的7:30
                previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
            elif current_time.hour == 23 and current_time.minute == 30:
                # 如果当前是23:30，则前一个时间点是当天的15:30
                previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
            else:
                # 跳过其他时间点
                continue

            # 查询前一个时间点的值
            sql = f"""
                SELECT bhao 
                FROM {table_name} 
                WHERE dataTime = '{previous_time}'
            """
            cursor.execute(sql)
            previous_result = cursor.fetchone()

            if previous_result:
                previous_value = float(previous_result[0])
                difference = current_value - previous_value
                if difference > 0:  # 只累加正值
                    dban_luhao += difference
        cursor.close()
        conn.close()
        return round(dban_luhao, 1)
    except Exception as e:
        logger.error(f"获取四班炉号时发生错误: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# 2025.3.27
def get_abandianhao(table_name):
    aban_dianhao = 0.0
    current_time = datetime.now()

    # 【修改1】获取起始时间（上个月25日）
    if current_time.day >= 26:
        # 如果今天是25号或之后，比如5月25日，用本月25日
        start_day = current_time.replace(day=25, hour=23, minute=30, second=0, microsecond=0)
    else:
        # 今天小于25号，比如4月15日，用上个月25日
        if current_time.month == 1:
            start_day = current_time.replace(year=current_time.year - 1, month=12, day=26, hour=7, minute=30, second=0,
                                             microsecond=0)
        else:
            start_day = current_time.replace(month=current_time.month - 1, day=26, hour=7, minute=30, second=0,
                                             microsecond=0)

    # 【修改2】结束时间是当前时刻
    end_day = current_time

    # SQL查询获取当月"一班"的所有记录，按时间排序
    sql = f"""
        SELECT inputTime, dianHao 
        FROM {table_name} 
        WHERE classes = '一班' 
        AND inputTime >= '{start_day}' 
        AND inputTime < '{end_day}'
        ORDER BY inputTime
    """

    conn = None
    cursor = None

    try:
        conn = pool.connection()  # 从连接池获取连接
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()

        # 处理每条记录
        for row in results:
            current_time = row[0]  # 当前记录的时间
            current_value = float(row[1])  # 当前记录的qiHao值

            # 计算前一个时间点
            if current_time.hour == 7 and current_time.minute == 30:
                # 如果当前是7:30，则前一个时间点是前一天的23:30
                previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
            elif current_time.hour == 15 and current_time.minute == 30:
                # 如果当前是15:30，则前一个时间点是当天的7:30
                previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
            elif current_time.hour == 23 and current_time.minute == 30:
                # 如果当前是23:30，则前一个时间点是当天的15:30
                previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
            else:
                continue

            # 查找前一个非零电耗值
            found_previous_value = False
            skip_count = 0  # 记录跳过的有效时间点数量
            while not found_previous_value and previous_time >= start_day:
                sql = f"""
                    SELECT dianHao 
                    FROM {table_name} 
                    WHERE inputTime = '{previous_time}'
                """
                cursor.execute(sql)
                previous_result = cursor.fetchone()

                if previous_result:
                    previous_value = float(previous_result[0])
                    if previous_value > 0:  # 找到非零值
                        found_previous_value = True
                        difference = current_value - previous_value
                        if difference > 0:  # 只累加正值
                            # 根据跳过的有效时间点数量调整差值
                            if skip_count > 0:
                                adjusted_difference = difference / (skip_count + 1)
                                aban_dianhao += adjusted_difference
                            else:
                                aban_dianhao += difference
                    else:
                        skip_count += 1
                        # 计算更早的时间点
                        if previous_time.hour == 7 and previous_time.minute == 30:
                            previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                        microsecond=0)
                        elif previous_time.hour == 15 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                        elif previous_time.hour == 23 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    # 计算更早的时间点
                    if previous_time.hour == 7 and previous_time.minute == 30:
                        previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                    microsecond=0)
                    elif previous_time.hour == 15 and previous_time.minute == 30:
                        previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                    elif previous_time.hour == 23 and previous_time.minute == 30:
                        previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
    except Exception as e:
        print(f"查询一班电耗数据时出错：{e}")
    finally:
        # 确保关闭游标和连接，防止连接池泄漏
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return round(aban_dianhao, 1)


def get_bbandianhao(table_name):
    bban_dianhao = 0.0
    current_time = datetime.now()

    # 【修改1】获取起始时间（上个月25日）
    if current_time.day >= 26:
        # 如果今天是25号或之后，比如5月25日，用本月25日
        start_day = current_time.replace(day=25, hour=23, minute=30, second=0, microsecond=0)
    else:
        # 今天小于25号，比如4月15日，用上个月25日
        if current_time.month == 1:
            start_day = current_time.replace(year=current_time.year - 1, month=12, day=26, hour=7, minute=30, second=0,
                                             microsecond=0)
        else:
            start_day = current_time.replace(month=current_time.month - 1, day=26, hour=7, minute=30, second=0,
                                             microsecond=0)

    # 【修改2】结束时间是当前时刻
    end_day = current_time

    # SQL查询获取当月"二班"的所有记录，按时间排序
    sql = f"""
        SELECT inputTime, dianHao
        FROM {table_name}
        WHERE classes = '二班'
        AND inputTime >= '{start_day}'
        AND inputTime < '{end_day}'
        ORDER BY inputTime
    """

    conn = None
    cursor = None

    try:
        conn = pool.connection()  # 从连接池获取连接
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()

        # 处理每条记录
        for row in results:
            current_time = row[0]  # 当前记录的时间
            current_value = float(row[1])  # 当前记录的qiHao值

            # 计算前一个时间点
            if current_time.hour == 7 and current_time.minute == 30:
                # 如果当前是7:30，则前一个时间点是前一天的23:30
                previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
            elif current_time.hour == 15 and current_time.minute == 30:
                # 如果当前是15:30，则前一个时间点是当天的7:30
                previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
            elif current_time.hour == 23 and current_time.minute == 30:
                # 如果当前是23:30，则前一个时间点是当天的15:30
                previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
            else:
                continue

            # 查找前一个非零电耗值
            found_previous_value = False
            skip_count = 0  # 记录跳过的有效时间点数量
            while not found_previous_value and previous_time >= start_day:
                sql = f"""
                    SELECT dianHao
                    FROM {table_name}
                    WHERE inputTime = '{previous_time}'
                """
                cursor.execute(sql)
                previous_result = cursor.fetchone()

                if previous_result:
                    previous_value = float(previous_result[0])
                    if previous_value > 0:  # 找到非零值
                        found_previous_value = True
                        difference = current_value - previous_value
                        if difference > 0:  # 只累加正值
                            # 根据跳过的有效时间点数量调整差值
                            if skip_count > 0:
                                adjusted_difference = difference / (skip_count + 1)
                                bban_dianhao += adjusted_difference
                            else:
                                bban_dianhao += difference
                    else:
                        skip_count += 1
                        # 计算更早的时间点
                        if previous_time.hour == 7 and previous_time.minute == 30:
                            previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                        microsecond=0)
                        elif previous_time.hour == 15 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                        elif previous_time.hour == 23 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    # 计算更早的时间点
                    if previous_time.hour == 7 and previous_time.minute == 30:
                        previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                    microsecond=0)
                    elif previous_time.hour == 15 and previous_time.minute == 30:
                        previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                    elif previous_time.hour == 23 and previous_time.minute == 30:
                        previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
    except Exception as e:
        logging.error(f"查询一班电耗数据时出错：{e}")
    finally:
        # 确保关闭游标和连接，防止连接池泄漏
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return round(bban_dianhao, 1)


# def get_cbandianhao(table_name):
#     # print("\n=== 开始计算三班电耗 ===")
#     cban_dianhao = 0.0
#     current_time = datetime.now()
#     # print(f"当前时间: {current_time}")
#
#     # 【修改1】获取起始时间（上个月25日）
#     if current_time.day >= 26:
#         # 如果今天是25号或之后，比如5月25日，用本月25日
#         start_day = current_time.replace(day=25, hour=23, minute=30, second=0, microsecond=0)
#     else:
#         # 今天小于25号，比如4月15日，用上个月25日
#         if current_time.month == 1:
#             start_day = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=23, minute=30, second=0,
#                                              microsecond=0)
#         else:
#             start_day = current_time.replace(month=current_time.month - 1, day=25, hour=23, minute=30, second=0,
#                                              microsecond=0)
#
#     # 【修改2】结束时间是当前时刻
#     end_day = current_time
#
#     # SQL查询获取当月"三班"的所有记录，按时间排序
#     sql = f"""
#         SELECT inputTime, dianHao
#         FROM {table_name}
#         WHERE classes = '三班'
#         AND inputTime >= '{start_day}'
#         AND inputTime < '{end_day}'
#         ORDER BY inputTime
#     """
#
#     conn = None
#     cursor = None
#
#     try:
#         conn = pool.connection()  # 从连接池获取连接
#         cursor = conn.cursor()
#         cursor.execute(sql)
#         results = cursor.fetchall()
#
#         # 处理每条记录
#         for row in results:
#             current_time = row[0]  # 当前记录的时间
#             current_value = float(row[1])  # 当前记录的dianHao值
#             # print(f"\n处理时间点: {current_time}, 当前电耗值: {current_value}")
#
#             # 计算前一个时间点
#             if current_time.hour == 7 and current_time.minute == 30:
#                 # 如果当前是7:30，则前一个时间点是前一天的23:30
#                 previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
#                 # print(f"7:30班次，前一个时间点: {previous_time}")
#             elif current_time.hour == 15 and current_time.minute == 30:
#                 # 如果当前是15:30，则前一个时间点是当天的7:30
#                 previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
#                 # print(f"15:30班次，前一个时间点: {previous_time}")
#             elif current_time.hour == 23 and current_time.minute == 30:
#                 # 如果当前是23:30，则前一个时间点是当天的15:30
#                 previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
#                 # print(f"23:30班次，前一个时间点: {previous_time}")
#             else:
#                 # print(f"跳过其他时间点: {current_time}")
#                 continue
#
#             # 查找前一个非零电耗值
#             found_previous_value = False
#             skip_count = 0  # 记录跳过的有效时间点数量
#             while not found_previous_value and previous_time >= start_day:
#                 sql = f"""
#                     SELECT dianHao
#                     FROM {table_name}
#                     WHERE inputTime = '{previous_time}'
#                 """
#                 # print(f"查询前一个时间点的SQL: {sql}")
#                 cursor.execute(sql)
#                 previous_result = cursor.fetchone()
#
#                 if previous_result:
#                     previous_value = float(previous_result[0])
#                     # print(f"前一个时间点电耗值: {previous_value}")
#                     if previous_value > 0:  # 找到非零值
#                         found_previous_value = True
#                         difference = current_value - previous_value
#                         # print(f"电耗差值: {difference}")
#                         if difference > 0:  # 只累加正值
#                             # 根据跳过的有效时间点数量调整差值
#                             if skip_count > 0:
#                                 adjusted_difference = difference / (skip_count + 1)
#                                 # print(f"跳过了 {skip_count} 个时间点，调整后的差值: {adjusted_difference}")
#                                 cban_dianhao += adjusted_difference
#                                 # print(f"当前累计电耗: {cban_dianhao}")
#                             else:
#                                 cban_dianhao += difference
#                                 # print(f"当前累计电耗: {cban_dianhao}")
#                         else:
#                             print(f"电耗差值为负，不累加")
#                     else:
#                         print(f"前一个时间点电耗值为0，继续往前查找")
#                         skip_count += 1
#                         # 计算更早的时间点
#                         if previous_time.hour == 7 and previous_time.minute == 30:
#                             previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
#                                                                                         microsecond=0)
#                         elif previous_time.hour == 15 and previous_time.minute == 30:
#                             previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
#                         elif previous_time.hour == 23 and previous_time.minute == 30:
#                             previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
#                 else:
#                     print(f"未找到前一个时间点的数据，继续往前查找")
#                     # 计算更早的时间点
#                     if previous_time.hour == 7 and previous_time.minute == 30:
#                         previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
#                                                                                     microsecond=0)
#                     elif previous_time.hour == 15 and previous_time.minute == 30:
#                         previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
#                     elif previous_time.hour == 23 and previous_time.minute == 30:
#                         previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
#
#             if not found_previous_value:
#                 print(f"未找到有效的非零前值，跳过此时间点")
#
#         print(f"\n=== 三班电耗计算完成 ===")
#         print(f"最终电耗值: {round(cban_dianhao, 1)}")
#     except Exception as e:
#         logging.error(f"查询一班电耗数据时出错：{e}")
#     finally:
#         # 确保关闭游标和连接，防止连接池泄漏
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()
#     return round(cban_dianhao, 1)
def get_cbandianhao(table_name):
    # print("\n=== 开始计算三班电耗 ===")
    cban_dianhao = 0.0
    current_time = datetime.now()
    # print(f"当前时间: {current_time}")

    # 【修改1】获取起始时间（上个月25日）
    if current_time.day >= 26:#改
        # 如果今天是25号或之后，比如5月25日，用本月25日
        start_day = current_time.replace(day=25, hour=23, minute=30, second=0, microsecond=0)#改
    else:
        # 今天小于25号，比如4月15日，用上个月25日
        if current_time.month == 1:
            start_day = current_time.replace(year=current_time.year - 1, month=12, day=26, hour=7, minute=30, second=0,
                                             microsecond=0)
        else:
            start_day = current_time.replace(month=current_time.month - 1, day=26, hour=7, minute=30, second=0,
                                             microsecond=0)

    # 【修改2】结束时间是当前时刻
    end_day = current_time

    # SQL查询获取当月"三班"的所有记录，按时间排序
    sql = f"""
        SELECT inputTime, dianHao 
        FROM {table_name} 
        WHERE classes = '三班' 
        AND inputTime >= '{start_day}' 
        AND inputTime < '{end_day}'
        ORDER BY inputTime
    """

    conn = None
    cursor = None

    try:
        conn = pool.connection()  # 从连接池获取连接
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()

        # 处理每条记录
        for row in results:
            current_time = row[0]  # 当前记录的时间
            current_value = float(row[1])  # 当前记录的dianHao值
            # print(f"\n处理时间点: {current_time}, 当前电耗值: {current_value}")

            # 计算前一个时间点
            if current_time.hour == 7 and current_time.minute == 30:
                # 如果当前是7:30，则前一个时间点是前一天的23:30
                previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
                # print(f"7:30班次，前一个时间点: {previous_time}")
            elif current_time.hour == 15 and current_time.minute == 30:
                # 如果当前是15:30，则前一个时间点是当天的7:30
                previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
                # print(f"15:30班次，前一个时间点: {previous_time}")
            elif current_time.hour == 23 and current_time.minute == 30:
                # 如果当前是23:30，则前一个时间点是当天的15:30
                previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
                # print(f"23:30班次，前一个时间点: {previous_time}")
            else:
                # print(f"跳过其他时间点: {current_time}")
                continue

            # 查找前一个非零电耗值
            found_previous_value = False
            skip_count = 0  # 记录跳过的有效时间点数量
            while not found_previous_value and previous_time >= start_day:
                sql = f"""
                    SELECT dianHao 
                    FROM {table_name} 
                    WHERE inputTime = '{previous_time}'
                """
                # print(f"查询前一个时间点的SQL: {sql}")
                cursor.execute(sql)
                previous_result = cursor.fetchone()

                if previous_result:
                    previous_value = float(previous_result[0])
                    # print(f"前一个时间点电耗值: {previous_value}")
                    if previous_value > 0:  # 找到非零值
                        found_previous_value = True
                        difference = current_value - previous_value
                        # print(f"电耗差值: {difference}")
                        if difference > 0:  # 只累加正值
                            # 根据跳过的有效时间点数量调整差值
                            if skip_count > 0:
                                adjusted_difference = difference / (skip_count + 1)
                                # print(f"跳过了 {skip_count} 个时间点，调整后的差值: {adjusted_difference}")
                                cban_dianhao += adjusted_difference
                                # print(f"当前累计电耗: {cban_dianhao}")
                            else:
                                cban_dianhao += difference
                                # print(f"当前累计电耗: {cban_dianhao}")
                        else:
                            print(f"电耗差值为负，不累加")
                    else:
                        print(f"前一个时间点电耗值为0，继续往前查找")
                        skip_count += 1
                        # 计算更早的时间点
                        if previous_time.hour == 7 and previous_time.minute == 30:
                            previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                        microsecond=0)
                        elif previous_time.hour == 15 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                        elif previous_time.hour == 23 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    print(f"未找到前一个时间点的数据，继续往前查找")
                    # 计算更早的时间点
                    if previous_time.hour == 7 and previous_time.minute == 30:
                        previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                    microsecond=0)
                    elif previous_time.hour == 15 and previous_time.minute == 30:
                        previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                    elif previous_time.hour == 23 and previous_time.minute == 30:
                        previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)

            if not found_previous_value:
                print(f"未找到有效的非零前值，跳过此时间点")

        print(f"\n=== 三班电耗计算完成 ===")
        print(f"最终电耗值: {round(cban_dianhao, 1)}")
    except Exception as e:
        logging.error(f"查询一班电耗数据时出错：{e}")
    finally:
        # 确保关闭游标和连接，防止连接池泄漏
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return round(cban_dianhao, 1)


# def get_dbandianhao(table_name):
#     dban_dianhao = 0.0
#     current_time = datetime.now()
#
#     # 【修改1】获取起始时间（上个月25日）
#     if current_time.day >= 26:
#         # 如果今天是25号或之后，比如5月25日，用本月25日
#         start_day = current_time.replace(day=25, hour=23, minute=30, second=0, microsecond=0)
#     else:
#         # 今天小于25号，比如4月15日，用上个月25日
#         if current_time.month == 1:
#             start_day = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=23, minute=30, second=0,
#                                              microsecond=0)
#         else:
#             start_day = current_time.replace(month=current_time.month - 1, day=25, hour=23, minute=30, second=0,
#                                              microsecond=0)
#
#     # 【修改2】结束时间是当前时刻
#     end_day = current_time
#
#     # SQL查询获取当月"四班"的所有记录，按时间排序
#     sql = f"""
#         SELECT inputTime, dianHao
#         FROM {table_name}
#         WHERE classes = '四班'
#         AND inputTime >= '{start_day}'
#         AND inputTime < '{end_day}'
#         ORDER BY inputTime
#     """
#
#     conn = None
#     cursor = None
#
#     try:
#         conn = pool.connection()  # 从连接池获取连接
#         cursor = conn.cursor()
#         cursor.execute(sql)
#         results = cursor.fetchall()
#
#         # 处理每条记录
#         for row in results:
#             current_time = row[0]  # 当前记录的时间
#             current_value = float(row[1])  # 当前记录的qiHao值
#
#             # 计算前一个时间点
#             if current_time.hour == 7 and current_time.minute == 30:
#                 # 如果当前是7:30，则前一个时间点是前一天的23:30
#                 previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
#             elif current_time.hour == 15 and current_time.minute == 30:
#                 # 如果当前是15:30，则前一个时间点是当天的7:30
#                 previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
#             elif current_time.hour == 23 and current_time.minute == 30:
#                 # 如果当前是23:30，则前一个时间点是当天的15:30
#                 previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
#             else:
#                 # 跳过其他时间点
#                 continue
#
#             # 查找前一个非零电耗值
#             found_previous_value = False
#             skip_count = 0  # 记录跳过的有效时间点数量
#             while not found_previous_value and previous_time >= start_day:
#                 sql = f"""
#                     SELECT dianHao
#                     FROM {table_name}
#                     WHERE inputTime = '{previous_time}'
#                 """
#                 cursor.execute(sql)
#                 previous_result = cursor.fetchone()
#
#                 if previous_result:
#                     previous_value = float(previous_result[0])
#                     if previous_value > 0:  # 找到非零值
#                         found_previous_value = True
#                         difference = current_value - previous_value
#                         if difference > 0:  # 只累加正值
#                             # 根据跳过的有效时间点数量调整差值
#                             if skip_count > 0:
#                                 adjusted_difference = difference / (skip_count + 1)
#                                 dban_dianhao += adjusted_difference
#                             else:
#                                 dban_dianhao += difference
#                     else:
#                         skip_count += 1
#                         # 计算更早的时间点
#                         if previous_time.hour == 7 and previous_time.minute == 30:
#                             previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
#                                                                                         microsecond=0)
#                         elif previous_time.hour == 15 and previous_time.minute == 30:
#                             previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
#                         elif previous_time.hour == 23 and previous_time.minute == 30:
#                             previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
#                 else:
#                     # 计算更早的时间点
#                     if previous_time.hour == 7 and previous_time.minute == 30:
#                         previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
#                                                                                     microsecond=0)
#                     elif previous_time.hour == 15 and previous_time.minute == 30:
#                         previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
#                     elif previous_time.hour == 23 and previous_time.minute == 30:
#                         previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
#     except Exception as e:
#         logging.error(f"查询一班电耗数据时出错：{e}")
#     finally:
#         # 确保关闭游标和连接，防止连接池泄漏
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()
#     return round(dban_dianhao, 1)
def get_dbandianhao(table_name):
    dban_dianhao = 0.0
    current_time = datetime.now()

    # 【修改1】获取起始时间（上个月25日）
    if current_time.day >= 26:#改
        # 如果今天是25号或之后，比如5月25日，用本月25日
        start_day = current_time.replace(day=25, hour=23, minute=30, second=0, microsecond=0)#改
    else:
        # 今天小于25号，比如4月15日，用上个月25日
        if current_time.month == 1:
            start_day = current_time.replace(year=current_time.year - 1, month=12, day=26, hour=7, minute=30, second=0,
                                             microsecond=0)
        else:
            start_day = current_time.replace(month=current_time.month - 1, day=26, hour=7, minute=30, second=0,
                                             microsecond=0)

    # 【修改2】结束时间是当前时刻
    end_day = current_time

    # SQL查询获取当月"四班"的所有记录，按时间排序
    sql = f"""
        SELECT inputTime, dianHao 
        FROM {table_name} 
        WHERE classes = '四班' 
        AND inputTime >= '{start_day}' 
        AND inputTime < '{end_day}'
        ORDER BY inputTime
    """

    conn = None
    cursor = None

    try:
        conn = pool.connection()  # 从连接池获取连接
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()

        # 处理每条记录
        for row in results:
            current_time = row[0]  # 当前记录的时间
            current_value = float(row[1])  # 当前记录的qiHao值
            print("dianhao1")
            print(current_value)

            # 计算前一个时间点
            if current_time.hour == 7 and current_time.minute == 30:
                # 如果当前是7:30，则前一个时间点是前一天的23:30
                previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
            elif current_time.hour == 15 and current_time.minute == 30:
                # 如果当前是15:30，则前一个时间点是当天的7:30
                previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
            elif current_time.hour == 23 and current_time.minute == 30:
                # 如果当前是23:30，则前一个时间点是当天的15:30
                previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
            else:
                # 跳过其他时间点
                continue

            # 查找前一个非零电耗值
            found_previous_value = False
            skip_count = 0  # 记录跳过的有效时间点数量
            while not found_previous_value and previous_time >= start_day:
                sql = f"""
                    SELECT dianHao 
                    FROM {table_name} 
                    WHERE inputTime = '{previous_time}'
                """
                cursor.execute(sql)
                previous_result = cursor.fetchone()

                if previous_result:
                    previous_value = float(previous_result[0])
                    if previous_value > 0:  # 找到非零值
                        found_previous_value = True
                        difference = current_value - previous_value
                        print(difference)
                        if difference > 0:  # 只累加正值
                            # 根据跳过的有效时间点数量调整差值
                            if skip_count > 0:
                                adjusted_difference = difference / (skip_count + 1)
                                dban_dianhao += adjusted_difference
                            else:
                                dban_dianhao += difference
                    else:
                        skip_count += 1
                        # 计算更早的时间点
                        if previous_time.hour == 7 and previous_time.minute == 30:
                            previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                        microsecond=0)
                        elif previous_time.hour == 15 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                        elif previous_time.hour == 23 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    # 计算更早的时间点
                    if previous_time.hour == 7 and previous_time.minute == 30:
                        previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                    microsecond=0)
                    elif previous_time.hour == 15 and previous_time.minute == 30:
                        previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                    elif previous_time.hour == 23 and previous_time.minute == 30:
                        previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
    except Exception as e:
        logging.error(f"查询一班电耗数据时出错：{e}")
    finally:
        # 确保关闭游标和连接，防止连接池泄漏
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return round(dban_dianhao, 1)


def get_today_ganyan(table_name):
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()
        today_ganyan = 0

        # 获取当前时间
        current_time = datetime.now()

        # 定义当天的三个时间点
        time_points = [
            current_time.replace(hour=7, minute=30, second=0, microsecond=0),
            current_time.replace(hour=15, minute=30, second=0, microsecond=0),
            current_time.replace(hour=23, minute=30, second=0, microsecond=0)
        ]

        # 遍历所有时间点，累加 aban1 和 bban1 的值
        for point in time_points:
            if point <= current_time:  # 只处理当前时间之前的时间点
                sql = f"""
                    SELECT aban1, bban1 
                    FROM {table_name} 
                    WHERE dataTime = '{point}'
                """
                cursor.execute(sql)
                result = cursor.fetchall()
                if len(result) > 0 and result[0][0] is not None:  # 确保数据不为 None:
                    aban1 = float(result[0][0] or 0)
                    bban1 = float(result[0][1] or 0)
                    today_ganyan += (aban1 + bban1)

        return round(today_ganyan, 1)
    except Exception as e:
        print(f"执行过程中出错：{str(e)}")
        return 0.0
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# def get_month_ganyan(table_name):
#     conn = None
#     cursor = None
#     try:
#         conn = pool.connection()
#         if not conn:
#             print("无法获取数据库连接")
#             return 0.0
#
#         cursor = conn.cursor()
#         month_ganyan = 0
#
#         # 获取当前时间
#         current_time = datetime.now()
#
#         # 计算时间范围
#         if current_time.day >= 25:
#             # 如果当前日期已过本月25日，开始日期是本月25日
#             start_date = current_time.replace(day=25, hour=23, minute=30, second=0, microsecond=0)
#             # 结束日期是当前时间
#             end_date = current_time
#         else:
#             # 如果当前日期在本月25日之前，开始日期是上月25日
#             if current_time.month == 1:
#                 start_date = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=23, minute=30,
#                                                   second=0, microsecond=0)
#             else:
#                 start_date = current_time.replace(month=current_time.month - 1, day=25, hour=23, minute=30, second=0,
#                                                   microsecond=0)
#             # 结束日期是当前时间
#             end_date = current_time
#
#         print(f"月干盐产量计算 - 时间范围: {start_date} 至 {end_date}")
#
#         # 定义每天的三个时间点
#         daily_times = [
#             (7, 30),
#             (15, 30),
#             (23, 30)
#         ]
#
#         # 遍历日期范围内的每一天
#         current_date = start_date
#         while current_date.date() <= end_date.date():
#             # 遍历每天的三个时间点
#             for hour, minute in daily_times:
#                 check_time = current_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
#
#                 # 如果 check_time 小于 start_date，也跳过
#                 if check_time < start_date:
#                     continue
#
#                 # 如果是当前日期，只处理到当前小时的数据
#                 if current_date.date() == end_date.date() and hour > end_date.hour:
#                     continue
#
#                 # 如果是最后一天且不是当前日期，跳过当前时间之后的数据
#                 if current_date.date() == end_date.date() and check_time > end_date:
#                     continue
#
#                 sql = f"""
#                     SELECT aban1, bban1
#                     FROM {table_name}
#                     WHERE dataTime = '{check_time}'
#                 """
#                 cursor.execute(sql)
#                 result = cursor.fetchall()
#                 if len(result) > 0:
#                     aban1 = float(result[0][0] or 0)
#                     bban1 = float(result[0][1] or 0)
#                     month_ganyan += (aban1 + bban1)
#                     print(f"时间点 {check_time} 的干盐产量: 一班={aban1}, 二班={bban1}, 合计={aban1 + bban1}")
#
#             # 移到下一天
#             current_date += timedelta(days=1)
#
#         print(f"月干盐产量总计: {round(month_ganyan, 1)}")
#         return round(month_ganyan, 1)
#     except Exception as e:
#         print(f"执行过程中出错：{str(e)}")
#         if conn:
#             conn.rollback()
#         return 0.0
#     finally:
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()
def get_month_ganyan(table_name):
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        if not conn:
            print("无法获取数据库连接")
            return 0.0

        cursor = conn.cursor()
        month_ganyan = 0

        # 获取当前时间
        current_time = datetime.now()

        # 计算时间范围
        if current_time.day >= 26:
            # 如果当前日期已过本月25日，开始日期是本月25日
            start_date = current_time.replace(day=26, hour=7, minute=30, second=0, microsecond=0)
            # 结束日期是当前时间
            end_date = current_time
        else:
            # 如果当前日期在本月25日之前，开始日期是上月25日
            if current_time.month == 1:
                start_date = current_time.replace(year=current_time.year - 1, month=12, day=26, hour=7, minute=30,
                                                  second=0, microsecond=0)
            else:
                start_date = current_time.replace(month=current_time.month - 1, day=26, hour=7, minute=30, second=0,
                                                  microsecond=0)
            # 结束日期是当前时间
            end_date = current_time

        print(f"月干盐产量计算 - 时间范围: {start_date} 至 {end_date}")

        # 定义每天的三个时间点
        daily_times = [
            (7, 30),
            (15, 30),
            (23, 30)
        ]

        # 遍历日期范围内的每一天
        current_date = start_date
        while current_date.date() <= end_date.date():
            # 遍历每天的三个时间点
            for hour, minute in daily_times:
                check_time = current_date.replace(hour=hour, minute=minute, second=0, microsecond=0)

                # 如果 check_time 小于 start_date，也跳过
                if check_time < start_date:
                    continue

                # 如果是当前日期，只处理到当前小时的数据
                if current_date.date() == end_date.date() and hour > end_date.hour:
                    continue

                # 如果是最后一天且不是当前日期，跳过当前时间之后的数据
                if current_date.date() == end_date.date() and check_time > end_date:
                    continue

                sql = f"""
                    SELECT aban1, bban1
                    FROM {table_name}
                    WHERE dataTime = '{check_time}'
                """
                cursor.execute(sql)
                result = cursor.fetchall()
                if len(result) > 0:
                    aban1 = float(result[0][0] or 0)
                    bban1 = float(result[0][1] or 0)
                    month_ganyan += (aban1 + bban1)
                    print(f"时间点 {check_time} 的干盐产量: 一班={aban1}, 二班={bban1}, 合计={aban1 + bban1}")

            # 移到下一天
            current_date += timedelta(days=1)

        print(f"月干盐产量总计: {round(month_ganyan, 1)}")
        return round(month_ganyan, 1)
    except Exception as e:
        print(f"执行过程中出错：{str(e)}")
        if conn:
            conn.rollback()
        return 0.0
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_year_ganyan(table_name):
    conn = None
    cursor = None
    try:
        year_ganyan = 0
        conn = pool.connection()
        cursor = conn.cursor()
        # 获取当前时间
        current_time = datetime.now()

        # 计算今年12月25日
        current_year_end = current_time.replace(month=12, day=26)

        # 计算去年12月25日
        if current_time.month == 12 and current_time.day >= 26:
            # 如果当前日期已过今年12月25日，开始日期是今年12月25日
            start_date = current_time.replace(month=12, day=26)
            # 结束日期是明年12月25日
            end_date = start_date.replace(year=start_date.year + 1)
        else:
            # 如果当前日期在12月25日之前，开始日期是去年12月25日
            start_date = current_time.replace(year=current_time.year - 1, month=12, day=26)
            # 结束日期是今年12月25日
            end_date = current_year_end

        # 定义每天的三个时间点
        daily_times = [
            (7, 30),
            (15, 30),
            (23, 30)
        ]

        # 遍历日期范围内的每一天
        current_date = start_date
        while current_date <= min(end_date, current_time):
            # 遍历每天的三个时间点
            for hour, minute in daily_times:
                check_time = current_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                if check_time <= current_time:  # 只处理当前时间之前的时间点
                    sql = f"""
                        SELECT aban1, bban1 
                        FROM {table_name} 
                        WHERE dataTime = '{check_time}'
                    """
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if len(result) > 0:  # 确保数据不为 None:
                        aban1 = float(result[0][0] or 0)
                        bban1 = float(result[0][1] or 0)
                        year_ganyan += (aban1 + bban1)

            # 移到下一天
            current_date += timedelta(days=1)

        return round(year_ganyan, 1)
    except Exception as e:
        print(f"执行过程中出错：{str(e)}")
        if conn:
            conn.rollback()
        return 0.0
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def get_today_taoxi(table_name):
    current_time = datetime.now()

    # 定义固定时间点
    if current_time.hour < 7 or (current_time.hour == 7 and current_time.minute < 30):
        # 7:30 之前，用昨天的 23:30
        target_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
    elif current_time.hour < 15 or (current_time.hour == 15 and current_time.minute < 30):
        # 15:30 之前，用今天的 7:30
        target_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
    elif current_time.hour < 23 or (current_time.hour == 23 and current_time.minute < 30):
        # 23:30 之前，用今天的 15:30
        target_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
    else:
        # 23:30 之后，用今天的 23:30
        target_time = current_time.replace(hour=23, minute=30, second=0, microsecond=0)

    today_taoxi = 0.0
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()

        # 当前目标时间点的淘洗值
        sql = f"SELECT btao FROM {table_name} WHERE dataTime = '{target_time}'"
        cursor.execute(sql)
        cur_res = cursor.fetchall()
        if len(cur_res) > 0 and cur_res[0][0] is not None:
            today_taoxi = float(cur_res[0][0])

        # 昨天 23:30 的淘洗值（用作差值起点）
        pre_time = (current_time.replace(hour=23, minute=30, second=0, microsecond=0)
                    - timedelta(days=1))
        sql = f"SELECT btao FROM {table_name} WHERE dataTime = '{pre_time}'"
        cursor.execute(sql)
        pre_res = cursor.fetchall()
        if len(pre_res) > 0 and pre_res[0][0] is not None:
            today_taoxi -= float(pre_res[0][0])

        return round(today_taoxi, 1)
    except Exception as e:
        logger.error(f"发生错误: {e}")
        return 0.0
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# def get_month_taoxi(table_name, return_from_last=False):
#     """
#     获取月淘洗量
#     :param table_name: 表名
#     :param return_from_last: 是否从last表返回数据（当前未使用）
#     :return: 月淘洗值
#     """
#     current_time = datetime.now()
#
#     # 确定目标时间点
#     if current_time.hour < 7 or (current_time.hour == 7 and current_time.minute < 30):
#         target_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
#     elif current_time.hour < 15 or (current_time.hour == 15 and current_time.minute < 30):
#         target_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
#     elif current_time.hour < 23 or (current_time.hour == 23 and current_time.minute < 30):
#         target_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
#     else:
#         target_time = current_time.replace(hour=23, minute=30, second=0, microsecond=0)
#
#     month_taoxi = 0.0
#     conn = None
#     cursor = None
#     try:
#         conn = pool.connection()
#         cursor = conn.cursor()
#
#         # 获取当前目标时间点的淘洗值
#         sql = f"SELECT btao FROM {table_name} WHERE dataTime = '{target_time}'"
#         cursor.execute(sql)
#         cur_res = cursor.fetchall()
#         if len(cur_res) > 0 and cur_res[0][0] is not None:
#             month_taoxi = float(cur_res[0][0])
#
#         # 获取上月25日 23:30 的淘洗基准值
#         if current_time.day < 25:
#             if current_time.month == 1:
#                 base_date = current_time.replace(year=current_time.year - 1, month=12, day=25)
#             else:
#                 base_date = current_time.replace(month=current_time.month - 1, day=25)
#         else:
#             base_date = current_time.replace(day=25)
#
#         base_time = base_date.replace(hour=23, minute=30, second=0, microsecond=0)
#
#         sql = f"SELECT btao FROM {table_name} WHERE dataTime = '{base_time}'"
#         cursor.execute(sql)
#         pre_res = cursor.fetchall()
#         if len(pre_res) > 0 and pre_res[0][0] is not None:
#             month_taoxi -= float(pre_res[0][0])
#
#         return round(month_taoxi, 1)
#     except Exception as e:
#         logger.error(f"获取月淘洗量时发生错误: {e}")
#         return 0.0
#     finally:
#         if cursor: cursor.close()
#         if conn: conn.close()
def get_month_taoxi(table_name, return_from_last=False):
    """
    获取月淘洗量
    :param table_name: 表名
    :param return_from_last: 是否从last表返回数据（当前未使用）
    :return: 月淘洗值
    """
    current_time = datetime.now()

    # 确定目标时间点
    if current_time.hour < 7 or (current_time.hour == 7 and current_time.minute < 30):
        target_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
    elif current_time.hour < 15 or (current_time.hour == 15 and current_time.minute < 30):
        target_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
    elif current_time.hour < 23 or (current_time.hour == 23 and current_time.minute < 30):
        target_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
    else:
        target_time = current_time.replace(hour=23, minute=30, second=0, microsecond=0)

    month_taoxi = 0.0
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()

        # 获取当前目标时间点的淘洗值
        sql = f"SELECT btao FROM {table_name} WHERE dataTime = '{target_time}'"
        cursor.execute(sql)
        cur_res = cursor.fetchall()
        if len(cur_res) > 0 and cur_res[0][0] is not None:
            month_taoxi = float(cur_res[0][0])

        # 获取上月25日 23:30 的淘洗基准值
        if current_time.day < 26:#改
            if current_time.month == 1:
                base_date = current_time.replace(year=current_time.year - 1, month=12, day=25)
            else:
                base_date = current_time.replace(month=current_time.month - 1, day=25)
        else:
            base_date = current_time.replace(day=25)

        base_time = base_date.replace(hour=23, minute=30, second=0, microsecond=0)

        sql = f"SELECT btao FROM {table_name} WHERE dataTime = '{base_time}'"
        cursor.execute(sql)
        pre_res = cursor.fetchall()
        if len(pre_res) > 0 and pre_res[0][0] is not None:
            month_taoxi -= float(pre_res[0][0])

        return round(month_taoxi, 1)
    except Exception as e:
        logger.error(f"获取月淘洗量时发生错误: {e}")
        return 0.0
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_year_taoxi(table_name):
    """
    获取年淘洗量（以去年12月25日23:30为基准）
    :param table_name: 数据表名
    :return: 年淘洗量
    """
    current_time = datetime.now()

    # 根据当前时间确定目标时间点
    if current_time.hour < 7 or (current_time.hour == 7 and current_time.minute < 30):
        target_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
    elif current_time.hour < 15 or (current_time.hour == 15 and current_time.minute < 30):
        target_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
    elif current_time.hour < 23 or (current_time.hour == 23 and current_time.minute < 30):
        target_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
    else:
        target_time = current_time.replace(hour=23, minute=30, second=0, microsecond=0)

    year_taoxi = 0.0
    conn = None
    cursor = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()

        # 获取当前目标时间点的淘洗值
        sql = f"SELECT btao FROM {table_name} WHERE dataTime = '{target_time}'"
        cursor.execute(sql)
        cur_res = cursor.fetchall()
        if len(cur_res) > 0 and cur_res[0][0] is not None:
            year_taoxi = float(cur_res[0][0])

        # 获取去年12月25日23:30的淘洗基准值
        base_time = datetime(current_time.year - 1, 12, 25, 23, 30, 0)

        sql = f"SELECT btao FROM {table_name} WHERE dataTime = '{base_time}'"
        cursor.execute(sql)
        pre_res = cursor.fetchall()
        if len(pre_res) > 0 and pre_res[0][0] is not None:
            year_taoxi -= float(pre_res[0][0])

        return round(year_taoxi, 1)
    except Exception as e:
        logger.error(f"获取年淘洗量时发生错误: {e}")
        return 0.0
    finally:
        if cursor: cursor.close()
        if conn: conn.close()



def get_abanganyan(table_name):
    """
    统计一班月干盐产量
    计算时间范围：
    - 如果当前日期在本月25日之前，从上月25日到当前日期
    - 如果当前日期在本月25日之后，从本月25日到当前日期
    """
    abanganyan = 0.0
    current_time = datetime.now()
    print(f"当前时间：{current_time}")

    # 计算时间范围
    if current_time.day >= 26:
        # 如果当前日期已过本月25日，开始日期是本月25日
        start_date = current_time.replace(day=26, hour=7, minute=30, second=0, microsecond=0)
    else:
        # 如果当前日期在本月25日之前，开始日期是上月25日
        if current_time.month == 1:
            start_date = current_time.replace(year=current_time.year - 1, month=12, day=26, hour=7, minute=30, second=0,
                                              microsecond=0)
        else:
            start_date = current_time.replace(month=current_time.month - 1, day=26, hour=7, minute=30, second=0,
                                              microsecond=0)

    # 结束日期是当前日期
    end_date = current_time

    print(f"一班月干盐产量计算时间范围：{start_date} 到 {end_date}")

    # 查询一班在指定时间范围内的干盐产量
    # 使用COALESCE函数处理NULL值，将其转换为0
    sql = f"""
        SELECT SUM(COALESCE(aban1, 0)) 
        FROM {table_name} 
        WHERE banci = '一班' 
        AND dataTime >= '{start_date}' 
        AND dataTime <= '{end_date}'
    """
    conn = None
    cursor = None

    try:
        conn = pool.connection()  # 🔥 每次从连接池取连接
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()

        if result and result[0] is not None:
            abanganyan = float(result[0])
            print(f"一班月干盐产量：{abanganyan}")
        else:
            print("未找到一班月干盐产量数据")
    except Exception as e:
        print(f"查询一班月干盐产量时出错：{e}")
    finally:
        # 🔥 注意一定要关掉，不然连接池连接会泄漏
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return round(abanganyan, 1)


def get_bbanganyan(table_name):
    """
    统计二班月干盐产量
    计算时间范围：
    - 如果当前日期在本月25日之前，从上月25日到当前日期
    - 如果当前日期在本月25日之后，从本月25日到当前日期
    """
    bbanganyan = 0.0
    current_time = datetime.now()
    print(f"当前时间：{current_time}")

    # 计算时间范围
    if current_time.day >= 26:
        # 如果当前日期已过本月25日，开始日期是本月25日
        start_date = current_time.replace(day=26, hour=7, minute=30, second=0, microsecond=0)
    else:
        # 如果当前日期在本月25日之前，开始日期是上月25日
        if current_time.month == 1:
            start_date = current_time.replace(year=current_time.year - 1, month=12, day=26, hour=7, minute=30, second=0,
                                              microsecond=0)
        else:
            start_date = current_time.replace(month=current_time.month - 1, day=26, hour=7, minute=30, second=0,
                                              microsecond=0)

    # 结束日期是当前日期
    end_date = current_time

    print(f"二班月干盐产量计算时间范围：{start_date} 到 {end_date}")

    # 查询二班在指定时间范围内的干盐产量
    # 使用COALESCE函数处理NULL值，将其转换为0
    sql = f"""
        SELECT SUM(COALESCE(aban1, 0)) 
        FROM {table_name} 
        WHERE banci = '二班' 
        AND dataTime >= '{start_date}' 
        AND dataTime <= '{end_date}'
    """
    conn = None
    cursor = None

    try:
        conn = pool.connection()  # 🔥 每次从连接池取连接
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()

        if result and result[0] is not None:
            bbanganyan = float(result[0])
            print(f"二班月干盐产量：{bbanganyan}")
        else:
            print("未找到二班月干盐产量数据")
    except Exception as e:
        print(f"查询二班月干盐产量时出错：{e}")
    finally:
        # 🔥 注意一定要关掉，不然连接池连接会泄漏
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return round(bbanganyan, 1)


def get_cbanganyan(table_name):
    cbanganyan = 0.0
    current_time = datetime.now()
    print(f"当前时间：{current_time}")

    # 计算时间范围
    if current_time.day >= 26:
        # 如果当前日期已过本月25日，开始日期是本月25日
        start_date = current_time.replace(day=26, hour=7, minute=30, second=0, microsecond=0)
    else:
        # 如果当前日期在本月25日之前，开始日期是上月25日
        if current_time.month == 1:
            start_date = current_time.replace(year=current_time.year - 1, month=12, day=26, hour=7, minute=30, second=0,
                                              microsecond=0)
        else:
            start_date = current_time.replace(month=current_time.month - 1, day=26, hour=7, minute=30, second=0,
                                              microsecond=0)

    # 结束日期是当前日期
    end_date = current_time

    print(f"三班月干盐产量计算时间范围：{start_date} 到 {end_date}")

    # 查询三班在指定时间范围内的干盐产量
    # 使用COALESCE函数处理NULL值，将其转换为0
    sql = f"""
        SELECT SUM(COALESCE(aban1, 0)) 
        FROM {table_name} 
        WHERE banci = '三班' 
        AND dataTime >= '{start_date}' 
        AND dataTime <= '{end_date}'
    """
    conn = None
    cursor = None

    try:
        conn = pool.connection()  # 🔥 每次从连接池取连接
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()

        if result and result[0] is not None:
            cbanganyan = float(result[0])
            print(f"三班月干盐产量：{cbanganyan}")
        else:
            print("未找到三班月干盐产量数据")
    except Exception as e:
        print(f"查询三班月干盐产量时出错：{e}")
    finally:
        # 🔥 注意一定要关掉，不然连接池连接会泄漏
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return round(cbanganyan, 1)


def get_dbanganyan(table_name):
    dbanganyan = 0.0
    current_time = datetime.now()
    print(f"当前时间：{current_time}")

    # 计算时间范围
    if current_time.day >= 26:
        # 如果当前日期已过本月25日，开始日期是本月25日
        start_date = current_time.replace(day=26, hour=7, minute=30, second=0, microsecond=0)
    else:
        # 如果当前日期在本月25日之前，开始日期是上月25日
        if current_time.month == 1:
            start_date = current_time.replace(year=current_time.year - 1, month=12, day=26, hour=7, minute=30, second=0,
                                              microsecond=0)
        else:
            start_date = current_time.replace(month=current_time.month - 1, day=26, hour=7, minute=30, second=0,
                                              microsecond=0)

    # 结束日期是当前日期
    end_date = current_time

    print(f"四班月干盐产量计算时间范围：{start_date} 到 {end_date}")

    # 查询四班在指定时间范围内的干盐产量
    # 使用COALESCE函数处理NULL值，将其转换为0
    sql = f"""
        SELECT SUM(COALESCE(aban1, 0)) 
        FROM {table_name} 
        WHERE banci = '四班' 
        AND dataTime >= '{start_date}' 
        AND dataTime <= '{end_date}'
    """
    conn = None
    cursor = None

    try:
        conn = pool.connection()  # 🔥 每次从连接池取连接
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()

        if result and result[0] is not None:
            dbanganyan = float(result[0])
            print(f"四班月干盐产量：{dbanganyan}")
        else:
            print("未找到四班月干盐产量数据")
    except Exception as e:
        print(f"查询四班月干盐产量时出错：{e}")
    finally:
        # 🔥 注意一定要关掉，不然连接池连接会泄漏
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return round(dbanganyan, 1)



def get_abantaoxi(table_name):
    aban_taoxi = 0.0
    current_time = datetime.now()

    # 【修改1】获取起始时间（上个月25日）
    if current_time.day >= 26:
        # 如果今天是25号或之后，比如5月25日，用本月25日
        start_day = current_time.replace(day=25, hour=23, minute=30, second=0, microsecond=0)
    else:
        # 今天小于25号，比如4月15日，用上个月25日
        if current_time.month == 1:
            start_day = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=23, minute=30, second=0,
                                             microsecond=0)
        else:
            start_day = current_time.replace(month=current_time.month - 1, day=25, hour=23, minute=30, second=0,
                                             microsecond=0)

    # 【修改2】结束时间是当前时刻
    end_day = current_time

    # SQL查询获取当月"一班"的所有记录，按时间排序
    sql = f"""
        SELECT dataTime, atao 
        FROM {table_name} 
        WHERE banci = '一班' 
        AND dataTime >= '{start_day}' 
        AND dataTime < '{end_day}'
        ORDER BY dataTime
    """

    conn = None
    cursor = None

    try:
        conn = pool.connection()  # 从连接池获取连接
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()

        # 处理每条记录
        for row in results:
            current_time = row[0]  # 当前记录的时间
            current_value = float(row[1])  # 当前记录的qiHao值

            # 计算前一个时间点
            if current_time.hour == 7 and current_time.minute == 30:
                # 如果当前是7:30，则前一个时间点是前一天的23:30
                previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
            elif current_time.hour == 15 and current_time.minute == 30:
                # 如果当前是15:30，则前一个时间点是当天的7:30
                previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
            elif current_time.hour == 23 and current_time.minute == 30:
                # 如果当前是23:30，则前一个时间点是当天的15:30
                previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
            else:
                continue

            # 查找前一个非零电耗值
            found_previous_value = False
            skip_count = 0  # 记录跳过的有效时间点数量
            while not found_previous_value and previous_time >= start_day:
                sql = f"""
                    SELECT atao 
                    FROM {table_name} 
                    WHERE dataTime = '{previous_time}'
                """
                cursor.execute(sql)
                previous_result = cursor.fetchone()

                if previous_result:
                    previous_value = float(previous_result[0])
                    if previous_value > 0:  # 找到非零值
                        found_previous_value = True
                        difference = current_value - previous_value
                        if difference > 0:  # 只累加正值
                            # 根据跳过的有效时间点数量调整差值
                            if skip_count > 0:
                                adjusted_difference = difference / (skip_count + 1)
                                aban_taoxi += adjusted_difference
                            else:
                                aban_taoxi += difference
                    else:
                        skip_count += 1
                        # 计算更早的时间点
                        if previous_time.hour == 7 and previous_time.minute == 30:
                            previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                        microsecond=0)
                        elif previous_time.hour == 15 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                        elif previous_time.hour == 23 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    # 计算更早的时间点
                    if previous_time.hour == 7 and previous_time.minute == 30:
                        previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                    microsecond=0)
                    elif previous_time.hour == 15 and previous_time.minute == 30:
                        previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                    elif previous_time.hour == 23 and previous_time.minute == 30:
                        previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
    except Exception as e:
        print(f"查询一班电耗数据时出错：{e}")
    finally:
        # 确保关闭游标和连接，防止连接池泄漏
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return round(aban_taoxi, 1)

def get_bbantaoxi(table_name):
    bban_taoxi = 0.0
    current_time = datetime.now()

    # 【修改1】获取起始时间（上个月25日）
    if current_time.day >= 26:
        # 如果今天是25号或之后，比如5月25日，用本月25日
        start_day = current_time.replace(day=25, hour=23, minute=30, second=0, microsecond=0)
    else:
        # 今天小于25号，比如4月15日，用上个月25日
        if current_time.month == 1:
            start_day = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=23, minute=30, second=0,
                                             microsecond=0)
        else:
            start_day = current_time.replace(month=current_time.month - 1, day=25, hour=23, minute=30, second=0,
                                             microsecond=0)

    # 【修改2】结束时间是当前时刻
    end_day = current_time

    # SQL查询获取当月"一班"的所有记录，按时间排序
    sql = f"""
        SELECT dataTime, atao 
        FROM {table_name} 
        WHERE banci = '二班' 
        AND dataTime >= '{start_day}' 
        AND dataTime < '{end_day}'
        ORDER BY dataTime
    """

    conn = None
    cursor = None

    try:
        conn = pool.connection()  # 从连接池获取连接
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()

        # 处理每条记录
        for row in results:
            current_time = row[0]  # 当前记录的时间
            current_value = float(row[1])  # 当前记录的qiHao值

            # 计算前一个时间点
            if current_time.hour == 7 and current_time.minute == 30:
                # 如果当前是7:30，则前一个时间点是前一天的23:30
                previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
            elif current_time.hour == 15 and current_time.minute == 30:
                # 如果当前是15:30，则前一个时间点是当天的7:30
                previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
            elif current_time.hour == 23 and current_time.minute == 30:
                # 如果当前是23:30，则前一个时间点是当天的15:30
                previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
            else:
                continue

            # 查找前一个非零电耗值
            found_previous_value = False
            skip_count = 0  # 记录跳过的有效时间点数量
            while not found_previous_value and previous_time >= start_day:
                sql = f"""
                    SELECT atao 
                    FROM {table_name} 
                    WHERE dataTime = '{previous_time}'
                """
                cursor.execute(sql)
                previous_result = cursor.fetchone()

                if previous_result:
                    previous_value = float(previous_result[0])
                    if previous_value > 0:  # 找到非零值
                        found_previous_value = True
                        difference = current_value - previous_value
                        if difference > 0:  # 只累加正值
                            # 根据跳过的有效时间点数量调整差值
                            if skip_count > 0:
                                adjusted_difference = difference / (skip_count + 1)
                                bban_taoxi += adjusted_difference
                            else:
                                bban_taoxi += difference
                    else:
                        skip_count += 1
                        # 计算更早的时间点
                        if previous_time.hour == 7 and previous_time.minute == 30:
                            previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                        microsecond=0)
                        elif previous_time.hour == 15 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                        elif previous_time.hour == 23 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    # 计算更早的时间点
                    if previous_time.hour == 7 and previous_time.minute == 30:
                        previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                    microsecond=0)
                    elif previous_time.hour == 15 and previous_time.minute == 30:
                        previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                    elif previous_time.hour == 23 and previous_time.minute == 30:
                        previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
    except Exception as e:
        print(f"查询2班taoxi数据时出错：{e}")
    finally:
        # 确保关闭游标和连接，防止连接池泄漏
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return round(bban_taoxi, 1)

def get_cbantaoxi(table_name):
    cban_taoxi = 0.0
    current_time = datetime.now()

    # 【修改1】获取起始时间（上个月25日）
    if current_time.day >= 26:
        # 如果今天是25号或之后，比如5月25日，用本月25日
        start_day = current_time.replace(day=25, hour=23, minute=30, second=0, microsecond=0)
    else:
        # 今天小于25号，比如4月15日，用上个月25日
        if current_time.month == 1:
            start_day = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=23, minute=30, second=0,
                                             microsecond=0)
        else:
            start_day = current_time.replace(month=current_time.month - 1, day=25, hour=23, minute=30, second=0,
                                             microsecond=0)

    # 【修改2】结束时间是当前时刻
    end_day = current_time

    # SQL查询获取当月"一班"的所有记录，按时间排序
    sql = f"""
        SELECT dataTime, atao 
        FROM {table_name} 
        WHERE banci = '三班' 
        AND dataTime >= '{start_day}' 
        AND dataTime < '{end_day}'
        ORDER BY dataTime
    """

    conn = None
    cursor = None

    try:
        conn = pool.connection()  # 从连接池获取连接
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()

        # 处理每条记录
        for row in results:
            current_time = row[0]  # 当前记录的时间
            current_value = float(row[1])  # 当前记录的qiHao值

            # 计算前一个时间点
            if current_time.hour == 7 and current_time.minute == 30:
                # 如果当前是7:30，则前一个时间点是前一天的23:30
                previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
            elif current_time.hour == 15 and current_time.minute == 30:
                # 如果当前是15:30，则前一个时间点是当天的7:30
                previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
            elif current_time.hour == 23 and current_time.minute == 30:
                # 如果当前是23:30，则前一个时间点是当天的15:30
                previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
            else:
                continue

            # 查找前一个非零电耗值
            found_previous_value = False
            skip_count = 0  # 记录跳过的有效时间点数量
            while not found_previous_value and previous_time >= start_day:
                sql = f"""
                    SELECT atao 
                    FROM {table_name} 
                    WHERE dataTime = '{previous_time}'
                """
                cursor.execute(sql)
                previous_result = cursor.fetchone()

                if previous_result:
                    previous_value = float(previous_result[0])
                    if previous_value > 0:  # 找到非零值
                        found_previous_value = True
                        difference = current_value - previous_value
                        if difference > 0:  # 只累加正值
                            # 根据跳过的有效时间点数量调整差值
                            if skip_count > 0:
                                adjusted_difference = difference / (skip_count + 1)
                                cban_taoxi += adjusted_difference
                            else:
                                cban_taoxi += difference
                    else:
                        skip_count += 1
                        # 计算更早的时间点
                        if previous_time.hour == 7 and previous_time.minute == 30:
                            previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                        microsecond=0)
                        elif previous_time.hour == 15 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                        elif previous_time.hour == 23 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    # 计算更早的时间点
                    if previous_time.hour == 7 and previous_time.minute == 30:
                        previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                    microsecond=0)
                    elif previous_time.hour == 15 and previous_time.minute == 30:
                        previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                    elif previous_time.hour == 23 and previous_time.minute == 30:
                        previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
    except Exception as e:
        print(f"查询3班taoxi数据时出错：{e}")
    finally:
        # 确保关闭游标和连接，防止连接池泄漏
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return round(cban_taoxi, 1)

def get_dbantaoxi(table_name):
    dban_taoxi = 0.0
    current_time = datetime.now()

    # 【修改1】获取起始时间（上个月25日）
    if current_time.day >= 26:
        # 如果今天是25号或之后，比如5月25日，用本月25日
        start_day = current_time.replace(day=25, hour=23, minute=30, second=0, microsecond=0)
    else:
        # 今天小于25号，比如4月15日，用上个月25日
        if current_time.month == 1:
            start_day = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=23, minute=30, second=0,
                                             microsecond=0)
        else:
            start_day = current_time.replace(month=current_time.month - 1, day=25, hour=23, minute=30, second=0,
                                             microsecond=0)

    # 【修改2】结束时间是当前时刻
    end_day = current_time

    # SQL查询获取当月"一班"的所有记录，按时间排序
    sql = f"""
        SELECT dataTime, atao 
        FROM {table_name} 
        WHERE banci = '四班' 
        AND dataTime >= '{start_day}' 
        AND dataTime < '{end_day}'
        ORDER BY dataTime
    """

    conn = None
    cursor = None

    try:
        conn = pool.connection()  # 从连接池获取连接
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()

        # 处理每条记录
        for row in results:
            current_time = row[0]  # 当前记录的时间
            current_value = float(row[1])  # 当前记录的qiHao值

            # 计算前一个时间点
            if current_time.hour == 7 and current_time.minute == 30:
                # 如果当前是7:30，则前一个时间点是前一天的23:30
                previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
            elif current_time.hour == 15 and current_time.minute == 30:
                # 如果当前是15:30，则前一个时间点是当天的7:30
                previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
            elif current_time.hour == 23 and current_time.minute == 30:
                # 如果当前是23:30，则前一个时间点是当天的15:30
                previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
            else:
                continue

            # 查找前一个非零电耗值
            found_previous_value = False
            skip_count = 0  # 记录跳过的有效时间点数量
            while not found_previous_value and previous_time >= start_day:
                sql = f"""
                    SELECT atao 
                    FROM {table_name} 
                    WHERE dataTime = '{previous_time}'
                """
                cursor.execute(sql)
                previous_result = cursor.fetchone()

                if previous_result:
                    previous_value = float(previous_result[0])
                    if previous_value > 0:  # 找到非零值
                        found_previous_value = True
                        difference = current_value - previous_value
                        if difference > 0:  # 只累加正值
                            # 根据跳过的有效时间点数量调整差值
                            if skip_count > 0:
                                adjusted_difference = difference / (skip_count + 1)
                                dban_taoxi += adjusted_difference
                            else:
                                dban_taoxi += difference
                    else:
                        skip_count += 1
                        # 计算更早的时间点
                        if previous_time.hour == 7 and previous_time.minute == 30:
                            previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                        microsecond=0)
                        elif previous_time.hour == 15 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                        elif previous_time.hour == 23 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    # 计算更早的时间点
                    if previous_time.hour == 7 and previous_time.minute == 30:
                        previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                    microsecond=0)
                    elif previous_time.hour == 15 and previous_time.minute == 30:
                        previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                    elif previous_time.hour == 23 and previous_time.minute == 30:
                        previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
    except Exception as e:
        print(f"查询4班taoxi数据时出错：{e}")
    finally:
        # 确保关闭游标和连接，防止连接池泄漏
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return round(dban_taoxi, 1)






@app.route('/api/data/', methods=['GET']) 
def get_data():
    """API endpoint to get data"""
    try:
        with app.app_context():
            cursor = mysql.connection.cursor()

            # 获取最近10天的日期范围
            cursor.execute("SELECT DISTINCT DATE(inputtime) FROM threehand ORDER BY DATE(inputtime) DESC LIMIT 10")
            date_results = cursor.fetchall()
            if not date_results:
                return jsonify([])

            earliest_date = date_results[-1][0]

            # 查询基准数据
            cursor.execute("""
                SELECT * FROM threehand 
                WHERE DATE(inputtime) < %s 
                ORDER BY inputtime DESC 
                LIMIT 1
            """, (earliest_date,))
            base_data = cursor.fetchall()

            # 查询10天数据
            cursor.execute("SELECT * FROM threehand WHERE DATE(inputtime) >= %s ORDER BY inputtime DESC",
                           (earliest_date,))
            threehand_data = cursor.fetchall()

            if base_data:
                threehand_data = list(threehand_data) + list(base_data)

            threehand_columns = [column[0] for column in cursor.description]

            cursor.execute("""
                SELECT timepoint, datatime, banci, aban, bban, aban1, atao
                FROM output 
                WHERE DATE(datatime) >= %s
                ORDER BY datatime DESC
            """, (earliest_date,))
            output_data = cursor.fetchall()

            production_by_date_shift = {}
            atao_by_date_shift = {}  # 存储每个班次的atao消耗量
            previous_atao = None  # 存储上一个班次的atao值
            previous_date_shift = None  # 存储上一个班次的日期和班次

            for row in output_data:
                timepoint, datatime, banci, aban, bban, aban1, atao = row
                date_key = datatime.strftime('%Y-%m-%d')
                current_date_shift = (date_key, banci)
                
                if banci and bban is not None and aban is not None:
                    if aban1 is None:
                        production = float(bban) - float(aban)
                    else:
                        production = float(bban) - float(aban) + float(aban1)
                    production_by_date_shift[current_date_shift] = production

                # 计算atao的消耗量
                if atao is not None:
                    if previous_atao is not None and previous_date_shift is not None:
                        atao_consumption = previous_atao - float(atao)  # 倒过来计算
                        atao_by_date_shift[previous_date_shift] = atao_consumption
                    previous_atao = float(atao)
                    previous_date_shift = current_date_shift

            result_data = []
            previous_values = {'dianHao': None, 'qiHao': None, 'luHao': None}
            threehand_data = list(reversed(threehand_data))
            has_base_record = bool(base_data)

            for index, row in enumerate(threehand_data):
                record = dict(zip(threehand_columns, row))
                date = record['inputTime'].strftime('%Y-%m-%d')
                banci = record['classes']
                current_date_shift = (date, banci)

                for field in ['dianHao', 'qiHao', 'luHao']:
                    current_value = float(record[field]) if record[field] else 0
                    if previous_values[field] is not None:
                        consumption = current_value - previous_values[field]
                        
                        # 如果是luHao，需要加上atao的消耗量
                        if field == 'luHao':
                            atao_consumption = atao_by_date_shift.get(current_date_shift, 0)
                            consumption += atao_consumption
                            
                        if consumption > 0:
                            production = production_by_date_shift.get(current_date_shift, 0)
                            if production > 0:
                                record[f'{field}_unit'] = round(consumption / production, 2)
                            else:
                                record[f'{field}_unit'] = 0.0
                        else:
                            record[f'{field}_unit'] = 0.0
                    else:
                        record[f'{field}_unit'] = 0.0

                    previous_values[field] = current_value

                if index > 0 or not has_base_record:
                    result_data.append(record)

            # ---------------- 统计四个班次的均值 ----------------
            from collections import defaultdict

            stats = defaultdict(lambda: {
                'dianHao_unit_sum': 0.0,
                'qiHao_unit_sum': 0.0,
                'luHao_unit_sum': 0.0,
                'count': 0
            })

            for item in result_data:
                shift = item.get('classes')
                if shift:
                    stats[shift]['dianHao_unit_sum'] += item.get('dianHao_unit', 0)
                    stats[shift]['qiHao_unit_sum'] += item.get('qiHao_unit', 0)
                    stats[shift]['luHao_unit_sum'] += item.get('luHao_unit', 0)
                    stats[shift]['count'] += 1

            shift_avg_list = []
            for shift, values in stats.items():
                count = values['count']
                if count > 0:
                    shift_avg_list.append({
                        'classes': shift,
                        'avg_dianHao_unit': round(values['dianHao_unit_sum'] / count, 2),
                        'avg_qiHao_unit': round(values['qiHao_unit_sum'] / count, 2),
                        'avg_luHao_unit': round(values['luHao_unit_sum'] / count, 2),
                        'count': count
                    })

            # 添加统计结果到返回数据中
            result = {
                'records': result_data,
                'class_stats': shift_avg_list
            }

            return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})


@app.route("/get_value/<element_id>", methods=["GET"])
def get_value(element_id: str) -> jsonify:
    """API 路由: 获取指定元素 ID 的最新值"""
    value = get_latest_value(element_id)
    return jsonify({"id": element_id, "value": value})



@app.route("/get_monthly_alarms", methods=["GET"])
def get_monthly_alarms():
    """获取月度报警统计数据"""
    try:
        cursor = mysql.connection.cursor()

        # 从js.alarmmonth表中获取最近12个月的数据
        cursor.execute("""
            SELECT yearmonth, count 
            FROM js.alarmmonth 
            ORDER BY yearmonth DESC 
            LIMIT 12
        """)

        results = cursor.fetchall()

        # 格式化数据
        monthly_data = [
            {
                'month': row[0],  # yearmonth
                'count': row[1]  # count
            }
            for row in results
        ]

        cursor.close()

        return jsonify(monthly_data)

    except Exception as e:
        logger.error(f"Error fetching monthly alarms: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def get_cursor():
    """获取数据库游标，如果连接失效会重新连接"""
    mysql_conn = pool.connection()
    try:
        mysql_conn.ping(reconnect=True)  # 检查连接是否有效，如果断开则重连
        return mysql_conn.cursor()
    except:
        mysql_conn = get_db_connection()  # 重新建立连接
        if mysql_conn:
            return mysql_conn.cursor()
        return None



@app.route('/api/data7/', methods=['GET'])
def get_data7():
    try:
        global is_first_run
        cursor = get_cursor()  # 获取有效的游标

        if cursor is None:
            return jsonify({"error": "数据库连接失败"}), 500

        if is_first_run or should_update_data():
            # 在首次启动或达到更新时间点时更新数据
            get_today_dianhao('threehand', return_from_last=False)
            get_month_dianhao('threehand', return_from_last=False)
            get_year_dianhao('threehand', return_from_last=False)
            get_today_qihao('output', return_from_last=False)
            get_month_qihao('output', return_from_last=False)
            get_year_qihao('output', return_from_last=False)
            get_today_luhao('output', return_from_last=False)
            get_month_luhao('output', return_from_last=False)
            get_year_luhao('output', return_from_last=False)
            get_year_taoxi('output')
            get_month_taoxi('output')
            is_first_run = False

        # 直接从last表获取数据返回
        today_dianhao = get_today_dianhao('threehand', return_from_last=True)
        month_dianhao = get_month_dianhao('threehand', return_from_last=True)
        year_dianhao = get_year_dianhao('threehand', return_from_last=True)
        today_qihao = get_today_qihao('output', return_from_last=True)
        month_qihao = get_month_qihao('output', return_from_last=True)
        year_qihao = get_year_qihao('output', return_from_last=True)
        today_luhao = get_today_luhao('output', return_from_last=True) + get_today_taoxi('output')
        month_luhao = get_month_luhao('output', return_from_last=True) + get_month_taoxi('output')
        year_luhao = get_year_luhao('output', return_from_last=True) + get_year_taoxi('output')
        taoxi=get_today_taoxi('output')
        year_taoxi=get_year_taoxi('output')
        month_taoxi=get_month_taoxi('output')

        respons_data = {

            "today_dianhao": today_dianhao,
            "month_dianhao": month_dianhao,
            "year_dianhao": year_dianhao,
            "today_qihao": today_qihao,
            "month_qihao": month_qihao,
            "year_qihao": year_qihao,
            "today_luhao": today_luhao,
            "month_luhao": month_luhao,
            "year_luhao": year_luhao,
            "taoxi":taoxi,
            "year_taoxi":year_taoxi,
            "month_taoxi":month_taoxi,
        }
        return jsonify(respons_data)

    except Exception as e:
        print(f"Error in get_chanliangame: {str(e)}")
        return jsonify({
            "error": "数据获取失败",
            "message": str(e)
        }), 500

#综合能耗
@app.route('/api/data8/', methods=['GET'])
def get_data8():
    try:
        global is_first_run
        cursor = get_cursor()  # 获取有效的游标

        if cursor is None:
            return jsonify({"error": "数据库连接失败"}), 500

        month_chanliang = get_month_chanliang('output', return_from_last=True)
        month_dianhao = get_month_dianhao('threehand', return_from_last=True)
        month_qihao = get_month_qihao('output', return_from_last=True)
        month_luhao = get_month_luhao('output', return_from_last=True) + get_month_taoxi('output')
        month_ganyan = get_month_ganyan('output')



        dandianhao = round(month_dianhao / (month_chanliang + month_ganyan), 2) if (month_chanliang + month_ganyan) != 0 else 0
        danluhao = round((month_luhao) / (month_chanliang + month_ganyan), 2) if (month_chanliang + month_ganyan) != 0 else 0
        danqihao = round(month_qihao / (month_chanliang + month_ganyan), 2) if (month_chanliang + month_ganyan) != 0 else 0
        zonghenenghao = round((danqihao * 128.6 + dandianhao * 0.1229), 2)

        respons_data = {
            "dandianhao": dandianhao,
            "danluhao": danluhao,
            "danqihao": danqihao,
            "zonghenenghao": zonghenenghao,

        }

        return jsonify(respons_data)

    except Exception as e:
        print(f"Error in get_chanliangame: {str(e)}")
        return jsonify({
            "error": "数据获取失败",
            "message": str(e)
        }), 500



@app.route('/api/data9/', methods=['GET'])
def get_data9():
    try:
        global is_first_run
        cursor = get_cursor()  # 获取有效的游标

        if cursor is None:
            return jsonify({"error": "数据库连接失败"}), 500


        aban_taoxi = get_abantaoxi('output')
        bban_taoxi = get_bbantaoxi('output')
        cban_taoxi = get_cbantaoxi('output')
        dban_taoxi = get_dbantaoxi('output')

        abanchanliang = get_abanchanliang('output')
        bbanchanliang = get_bbanchanliang('output')
        cbanchanliang = get_cbanchanliang('output')
        dbanchanliang = get_dbanchanliang('output')

        abanluhao = get_abanluhao('output')
        bbanluhao = get_bbanluhao('output')
        cbanluhao = get_cbanluhao('output')
        dbanluhao = get_dbanluhao('output')

        abanqihao = get_abanqihao('threehand')
        bbanqihao = get_bbanqihao('threehand')
        cbanqihao = get_cbanqihao('threehand')
        dbanqihao = get_dbanqihao('threehand')

        abandianhao = get_abandianhao('threehand')
        bbandianhao = get_bbandianhao('threehand')
        cbandianhao = get_cbandianhao('threehand')
        dbandianhao = get_dbandianhao('threehand')


        abanganyan = get_abanganyan('output')
        bbanganyan = get_bbanganyan('output')
        cbanganyan = get_cbanganyan('output')
        dbanganyan = get_dbanganyan('output')

        # 添加除零保护
        adunluhao = round((abanluhao+aban_taoxi) / (abanchanliang + abanganyan), 2) if (abanchanliang + abanganyan) != 0 else 0
        bdunluhao = round((bbanluhao+bban_taoxi) / (bbanchanliang + bbanganyan), 2) if (bbanchanliang + bbanganyan) != 0 else 0
        cdunluhao = round((cbanluhao+cban_taoxi) / (cbanchanliang + cbanganyan), 2) if (cbanchanliang + cbanganyan) != 0 else 0
        ddunluhao = round((dbanluhao+dban_taoxi) / (dbanchanliang + dbanganyan), 2) if (dbanchanliang + dbanganyan) != 0 else 0

        adunqihao = round(abanqihao / (abanchanliang + abanganyan), 2) if (abanchanliang + abanganyan) != 0 else 0
        bdunqihao = round(bbanqihao / (bbanchanliang + bbanganyan), 2) if (bbanchanliang + bbanganyan) != 0 else 0
        cdunqihao = round(cbanqihao / (cbanchanliang + cbanganyan), 2) if (cbanchanliang + cbanganyan) != 0 else 0
        ddunqihao = round(dbanqihao / (dbanchanliang + dbanganyan), 2) if (dbanchanliang + dbanganyan) != 0 else 0

        adundianhao = round(abandianhao / (abanchanliang + abanganyan), 2) if (abanchanliang + abanganyan) != 0 else 0
        bdundianhao = round(bbandianhao / (bbanchanliang + bbanganyan), 2) if (bbanchanliang + bbanganyan) != 0 else 0
        cdundianhao = round(cbandianhao / (cbanchanliang + cbanganyan), 2) if (cbanchanliang + cbanganyan) != 0 else 0
        ddundianhao = round(dbandianhao / (dbanchanliang + dbanganyan), 2) if (dbanchanliang + dbanganyan) != 0 else 0



        respons_data = {

            "abanchanliang": abanchanliang,
            "bbanchanliang": bbanchanliang,
            "cbanchanliang": cbanchanliang,
            "dbanchanliang": dbanchanliang,
            "abanluhao": abanluhao,
            "bbanluhao": bbanluhao,
            "cbanluhao": cbanluhao,
            "dbanluhao": dbanluhao,
            "abanqihao": abanqihao,
            "bbanqihao": bbanqihao,
            "cbanqihao": cbanqihao,
            "dbanqihao": dbanqihao,
            "adunluhao": adunluhao,
            "bdunluhao": bdunluhao,
            "cdunluhao": cdunluhao,
            "ddunluhao": ddunluhao,
            "adunqihao": adunqihao,
            "bdunqihao": bdunqihao,
            "cdunqihao": cdunqihao,
            "ddunqihao": ddunqihao,
            "adundianhao": adundianhao,
            "bdundianhao": bdundianhao,
            "cdundianhao": cdundianhao,
            "ddundianhao": ddundianhao,
            "abanganyan": abanganyan,
            "bbanganyan": bbanganyan,
            "cbanganyan": cbanganyan,
            "dbanganyan": dbanganyan,
            "ataoxi":aban_taoxi,
            "b":bban_taoxi,
            "c":cban_taoxi,
            "d":dban_taoxi,
            'abandianhao' :abandianhao,
            'bbandianhao' :bbandianhao,
            'cbandianhao' :cbandianhao,
            'dbandianhao' :dbandianhao,
        }

        return jsonify(respons_data)

    except Exception as e:
        print(f"Error in get_chanliangame: {str(e)}")
        return jsonify({
            "error": "数据获取失败",
            "message": str(e)
        }), 500

#日月年产量
@app.route('/api/data2/', methods=['GET'])
def get_chanliangame():
    try:
        global is_first_run
        cursor = get_cursor()  # 获取有效的游标

        if cursor is None:
            return jsonify({"error": "数据库连接失败"}), 500

        if is_first_run or should_update_data():
            # 在首次启动或达到更新时间点时更新数据
            get_today_chanliang('output', return_from_last=False)
            get_month_chanliang('output', return_from_last=False)
            get_year_chanliang('output', return_from_last=False)
            get_today_dianhao('threehand', return_from_last=False)
            get_month_dianhao('threehand', return_from_last=False)
            get_year_dianhao('threehand', return_from_last=False)
            get_today_qihao('output', return_from_last=False)
            get_month_qihao('output', return_from_last=False)
            get_year_qihao('output', return_from_last=False)
            get_today_luhao('output', return_from_last=False)
            get_month_luhao('output', return_from_last=False)
            get_year_luhao('output', return_from_last=False)
            is_first_run = False

        # 直接从last表获取数据返回
        today_chanliang = get_today_chanliang('output')
        month_chanliang = get_month_chanliang('output')
        year_chanliang = get_year_chanliang('output')
        today_ganyan = get_today_ganyan('output')
        month_ganyan = get_month_ganyan('output')
        year_ganyan = get_year_ganyan('output')


        respons_data = {
            "today_chanliang": today_chanliang,
            "month_chanliang": month_chanliang,
            "year_chanliang": year_chanliang,
            "today_ganyan": today_ganyan,
            "month_ganyan": month_ganyan,
            "year_ganyan": year_ganyan,

        }

        return jsonify(respons_data)

    except Exception as e:
        print(f"Error in get_chanliangame: {str(e)}")
        return jsonify({
            "error": "数据获取失败",
            "message": str(e)
        }), 500


@app.route('/api/data3/', methods=['GET'])
def get_data2():
    try:
        data = fetch_data_from_db('output')
        return jsonify(data)
    except Exception as e:
        print(f"Error in get_data2: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/data4/', methods=['GET'])
def get_data4():
    try:
        # # 确保数据库连接正常
        # check_and_reconnect()

        # 获取数据
        data = fetch_data_from_db('threehand')

        if not data:
            return jsonify({
                "error": "未找到数据",
                "message": "threehand表中没有数据"
            }), 404

        return jsonify(data)
    except Exception as e:
        error_msg = str(e)
        print(f"Error in get_data4: {error_msg}")
        return jsonify({
            "error": "数据获取失败",
            "message": error_msg,
            "details": "请检查数据库连接和threehand表是否存在"
        }), 500


def check_mysql_connection():
    """检查 MySQL 连接是否有效"""
    try:
        with app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return True
    except Exception as e:
        logger.error(f"MySQL connection error: {e}")
        return False


def mysql_heartbeat():
    """MySQL 心跳函数"""
    while True:
        if not check_mysql_connection():
            logger.info("Reconnecting to MySQL...")
            try:
                with app.app_context():
                    mysql.connection.ping(reconnect=True)
                    logger.info("MySQL reconnection successful")
            except Exception as e:
                logger.error(f"MySQL reconnection failed: {e}")
        time.sleep(180)  # 每3分钟检查一次


# 启动心跳线程
def start_heartbeat():
    """启动心跳线程"""
    heartbeat_thread = threading.Thread(target=mysql_heartbeat, daemon=True)
    heartbeat_thread.start()
    logger.info("MySQL heartbeat thread started")


def check_refresh():
    """检查是否需要刷新数据"""
    global last_refresh_time

    if last_refresh_time is None:
        return True

    now = datetime.now()
    # 如果是新的一天(过了凌晨)，则需要刷新
    return now.date() > last_refresh_time.date()


# 添加定时刷新函数
def daily_refresh():
    """每日刷新数据的线程函数"""
    while True:
        now = datetime.now()
        # 计算下一个凌晨0点的时间
        next_day = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        # 计算需要睡眠的秒数
        sleep_seconds = (next_day - now).total_seconds()

        time.sleep(sleep_seconds)

# 排名

def aban_month_chanliang(table_name):
    """获取一班一年12个月每月的产量（潮盐+干盐）"""
    try:
        current_time = datetime.now()
        conn = pool.connection()
        cursor = conn.cursor()

        # 初始化12个月的数据数组
        monthly_data = [0.0] * 12

        # 遍历每个月
        for month in range(1, 13):
            # 计算每月的起始和结束时间
            if month == current_time.month:
                # 当前月，结束时间为当前时间
                end_time = current_time
            else:
                # 其他月份，结束时间为当月最后一天
                if month == 12:
                    end_time = current_time.replace(year=current_time.year, month=12, day=31, hour=23, minute=59,
                                                    second=59)
                else:
                    next_month = current_time.replace(month=month + 1, day=1)
                    end_time = (next_month - timedelta(days=1)).replace(hour=23, minute=59, second=59)

            # 计算开始时间（上月25日）
            if month == 1:
                start_time = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=7, minute=30,
                                                  second=0)
            else:
                start_time = current_time.replace(month=month, day=25, hour=7, minute=30, second=0)

            # 修改SQL查询，同时获取aban和aban1字段
            sql = f"""
                SELECT dataTime, bban, aban1 
                FROM {table_name} 
                WHERE banci = '一班' 
                AND dataTime >= '{start_time}' 
                AND dataTime <= '{end_time}'
                AND bban IS NOT NULL
                AND bban != ''

                ORDER BY dataTime
            """

            cursor.execute(sql)
            results = cursor.fetchall()

            month_chanliang = 0.0
            month_ganyan = 0.0  # 用于累计干盐产量

            for row in results:
                current_time = row[0]
                try:
                    current_value = float(row[1]) if row[1] else 0.0
                    current_ganyan = float(row[2]) if row[2] else 0.0
                except (TypeError, ValueError):
                    continue  # 跳过无法转换为float的值

                # 累加干盐产量
                month_ganyan += current_ganyan

                # 计算前一个时间点
                if current_time.hour == 7 and current_time.minute == 30:
                    previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                               microsecond=0)
                elif current_time.hour == 15 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
                elif current_time.hour == 23 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    continue

                # 查询前一个时间点的值
                sql = f"""
                    SELECT bban 
                    FROM {table_name} 
                    WHERE dataTime = '{previous_time}'
                    AND bban IS NOT NULL
                    AND bban != ''
                """
                cursor.execute(sql)
                previous_result = cursor.fetchone()

                if previous_result:
                    try:
                        previous_value = float(previous_result[0])
                        difference = current_value - previous_value
                        if difference > 0:  # 只累加正值
                            month_chanliang += difference
                    except (TypeError, ValueError):
                        continue  # 跳过无法转换为float的值

            # 将当月总产量（潮盐+干盐）存入数组
            monthly_data[month - 1] = round(month_chanliang + month_ganyan, 1)

        cursor.close()
        conn.close()
        return monthly_data
    except Exception as e:
        logger.error(f"获取一班月度产量时发生错误: {e}")
        return [0.0] * 12  # 发生错误时返回12个0


def bban_month_chanliang(table_name):
    """获取一班一年12个月每月的产量（潮盐+干盐）"""
    try:
        current_time = datetime.now()
        conn = pool.connection()
        cursor = conn.cursor()

        # 初始化12个月的数据数组
        monthly_data = [0.0] * 12

        # 遍历每个月
        for month in range(1, 13):
            # 计算每月的起始和结束时间
            if month == current_time.month:
                # 当前月，结束时间为当前时间
                end_time = current_time
            else:
                # 其他月份，结束时间为当月最后一天
                if month == 12:
                    end_time = current_time.replace(year=current_time.year, month=12, day=31, hour=23, minute=59,
                                                    second=59)
                else:
                    next_month = current_time.replace(month=month + 1, day=1)
                    end_time = (next_month - timedelta(days=1)).replace(hour=23, minute=59, second=59)

            # 计算开始时间（上月25日）
            if month == 1:
                start_time = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=7, minute=30,
                                                  second=0)
            else:
                start_time = current_time.replace(month=month, day=25, hour=7, minute=30, second=0)

            # 修改SQL查询，同时获取aban和aban1字段
            sql = f"""
                SELECT dataTime, bban, aban1 
                FROM {table_name} 
                WHERE banci = '二班' 
                AND dataTime >= '{start_time}' 
                AND dataTime <= '{end_time}'
                AND bban IS NOT NULL
                AND bban != ''

                ORDER BY dataTime
            """

            cursor.execute(sql)
            results = cursor.fetchall()

            month_chanliang = 0.0
            month_ganyan = 0.0  # 用于累计干盐产量

            for row in results:
                current_time = row[0]
                try:
                    current_value = float(row[1]) if row[1] else 0.0
                    current_ganyan = float(row[2]) if row[2] else 0.0
                except (TypeError, ValueError):
                    continue  # 跳过无法转换为float的值

                # 累加干盐产量
                month_ganyan += current_ganyan

                # 计算前一个时间点
                if current_time.hour == 7 and current_time.minute == 30:
                    previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                               microsecond=0)
                elif current_time.hour == 15 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
                elif current_time.hour == 23 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    continue

                # 查询前一个时间点的值
                sql = f"""
                    SELECT bban 
                    FROM {table_name} 
                    WHERE dataTime = '{previous_time}'
                    AND bban IS NOT NULL
                    AND bban != ''
                """
                cursor.execute(sql)
                previous_result = cursor.fetchone()

                if previous_result:
                    try:
                        previous_value = float(previous_result[0])
                        difference = current_value - previous_value
                        if difference > 0:  # 只累加正值
                            month_chanliang += difference
                    except (TypeError, ValueError):
                        continue  # 跳过无法转换为float的值

            # 将当月总产量（潮盐+干盐）存入数组
            monthly_data[month - 1] = round(month_chanliang + month_ganyan, 1)

        cursor.close()
        conn.close()
        return monthly_data
    except Exception as e:
        logger.error(f"获取一班月度产量时发生错误: {e}")
        return [0.0] * 12  # 发生错误时返回12个0


def cban_month_chanliang(table_name):
    """获取一班一年12个月每月的产量（潮盐+干盐）"""
    try:
        current_time = datetime.now()
        conn = pool.connection()
        cursor = conn.cursor()

        # 初始化12个月的数据数组
        monthly_data = [0.0] * 12

        # 遍历每个月
        for month in range(1, 13):
            # 计算每月的起始和结束时间
            if month == current_time.month:
                # 当前月，结束时间为当前时间
                end_time = current_time
            else:
                # 其他月份，结束时间为当月最后一天
                if month == 12:
                    end_time = current_time.replace(year=current_time.year, month=12, day=31, hour=23, minute=59,
                                                    second=59)
                else:
                    next_month = current_time.replace(month=month + 1, day=1)
                    end_time = (next_month - timedelta(days=1)).replace(hour=23, minute=59, second=59)

            # 计算开始时间（上月25日）
            if month == 1:
                start_time = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=7, minute=30,
                                                  second=0)
            else:
                start_time = current_time.replace(month=month, day=25, hour=7, minute=30, second=0)

            # 修改SQL查询，同时获取aban和aban1字段
            sql = f"""
                SELECT dataTime, bban, aban1 
                FROM {table_name} 
                WHERE banci = '三班' 
                AND dataTime >= '{start_time}' 
                AND dataTime <= '{end_time}'
                AND bban IS NOT NULL
                AND bban != ''

                ORDER BY dataTime
            """

            cursor.execute(sql)
            results = cursor.fetchall()

            month_chanliang = 0.0
            month_ganyan = 0.0  # 用于累计干盐产量

            for row in results:
                current_time = row[0]
                try:
                    current_value = float(row[1]) if row[1] else 0.0
                    current_ganyan = float(row[2]) if row[2] else 0.0
                except (TypeError, ValueError):
                    continue  # 跳过无法转换为float的值

                # 累加干盐产量
                month_ganyan += current_ganyan

                # 计算前一个时间点
                if current_time.hour == 7 and current_time.minute == 30:
                    previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                               microsecond=0)
                elif current_time.hour == 15 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
                elif current_time.hour == 23 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    continue

                # 查询前一个时间点的值
                sql = f"""
                    SELECT bban 
                    FROM {table_name} 
                    WHERE dataTime = '{previous_time}'
                    AND bban IS NOT NULL
                    AND bban != ''
                """
                cursor.execute(sql)
                previous_result = cursor.fetchone()

                if previous_result:
                    try:
                        previous_value = float(previous_result[0])
                        difference = current_value - previous_value
                        if difference > 0:  # 只累加正值
                            month_chanliang += difference
                    except (TypeError, ValueError):
                        continue  # 跳过无法转换为float的值

            # 将当月总产量（潮盐+干盐）存入数组
            monthly_data[month - 1] = round(month_chanliang + month_ganyan, 1)

        cursor.close()
        conn.close()
        return monthly_data
    except Exception as e:
        logger.error(f"获取一班月度产量时发生错误: {e}")
        return [0.0] * 12  # 发生错误时返回12个0


def dban_month_chanliang(table_name):
    """获取一班一年12个月每月的产量（潮盐+干盐）"""
    try:
        current_time = datetime.now()
        conn = pool.connection()
        cursor = conn.cursor()

        # 初始化12个月的数据数组
        monthly_data = [0.0] * 12

        # 遍历每个月
        for month in range(1, 13):
            # 计算每月的起始和结束时间
            if month == current_time.month:
                # 当前月，结束时间为当前时间
                end_time = current_time
            else:
                # 其他月份，结束时间为当月最后一天
                if month == 12:
                    end_time = current_time.replace(year=current_time.year, month=12, day=31, hour=23, minute=59,
                                                    second=59)
                else:
                    next_month = current_time.replace(month=month + 1, day=1)
                    end_time = (next_month - timedelta(days=1)).replace(hour=23, minute=59, second=59)

            # 计算开始时间（上月25日）
            if month == 1:
                start_time = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=7, minute=30,
                                                  second=0)
            else:
                start_time = current_time.replace(month=month, day=25, hour=7, minute=30, second=0)

            # 修改SQL查询，同时获取aban和aban1字段
            sql = f"""
                SELECT dataTime, bban, aban1 
                FROM {table_name} 
                WHERE banci = '四班' 
                AND dataTime >= '{start_time}' 
                AND dataTime <= '{end_time}'
                AND bban IS NOT NULL
                AND bban != ''

                ORDER BY dataTime
            """

            cursor.execute(sql)
            results = cursor.fetchall()

            month_chanliang = 0.0
            month_ganyan = 0.0  # 用于累计干盐产量

            for row in results:
                current_time = row[0]
                try:
                    current_value = float(row[1]) if row[1] else 0.0
                    current_ganyan = float(row[2]) if row[2] else 0.0
                except (TypeError, ValueError):
                    continue  # 跳过无法转换为float的值

                # 累加干盐产量
                month_ganyan += current_ganyan

                # 计算前一个时间点
                if current_time.hour == 7 and current_time.minute == 30:
                    previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                               microsecond=0)
                elif current_time.hour == 15 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
                elif current_time.hour == 23 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    continue

                # 查询前一个时间点的值
                sql = f"""
                    SELECT bban 
                    FROM {table_name} 
                    WHERE dataTime = '{previous_time}'
                    AND bban IS NOT NULL
                    AND bban != ''
                """
                cursor.execute(sql)
                previous_result = cursor.fetchone()

                if previous_result:
                    try:
                        previous_value = float(previous_result[0])
                        difference = current_value - previous_value
                        if difference > 0:  # 只累加正值
                            month_chanliang += difference
                    except (TypeError, ValueError):
                        continue  # 跳过无法转换为float的值

            # 将当月总产量（潮盐+干盐）存入数组
            monthly_data[month - 1] = round(month_chanliang + month_ganyan, 1)

        cursor.close()
        conn.close()
        return monthly_data
    except Exception as e:
        logger.error(f"获取一班月度产量时发生错误: {e}")
        return [0.0] * 12  # 发生错误时返回12个0


def aban_month_dianhao(table_name):
    """获取一班一年12个月每月的电耗"""
    try:
        current_time = datetime.now()
        conn = pool.connection()
        cursor = conn.cursor()

        # 初始化12个月的数据数组
        monthly_data = [0.0] * 12

        # 遍历每个月
        for month in range(1, 13):
            # 计算每月的起始和结束时间
            if month == current_time.month:
                # 当前月，结束时间为当前时间
                end_time = current_time
            else:
                # 其他月份，结束时间为当月最后一天
                if month == 12:
                    end_time = current_time.replace(year=current_time.year, month=12, day=31, hour=23, minute=59,
                                                    second=59)
                else:
                    next_month = current_time.replace(month=month + 1, day=1)
                    end_time = (next_month - timedelta(days=1)).replace(hour=23, minute=59, second=59)

            # 计算开始时间（上月25日）
            if month == 1:
                start_time = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=7, minute=30,
                                                  second=0)
            else:
                start_time = current_time.replace(month=month, day=25, hour=7, minute=30, second=0)

            # SQL查询获取当月"一班"的所有记录，按时间排序
            sql = f"""
                SELECT inputTime, dianHao 
                FROM {table_name} 
                WHERE classes = '一班' 
                AND inputTime >= '{start_time}' 
                AND inputTime <= '{end_time}'
                ORDER BY inputTime
            """

            cursor.execute(sql)
            results = cursor.fetchall()

            month_dianhao = 0.0

            # 处理每条记录
            for row in results:
                current_time = row[0]  # 当前记录的时间
                current_value = float(row[1])  # 当前记录的电耗值

                # 计算前一个时间点
                if current_time.hour == 7 and current_time.minute == 30:
                    previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                               microsecond=0)
                elif current_time.hour == 15 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
                elif current_time.hour == 23 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    continue

                # 查找前一个非零电耗值
                found_previous_value = False
                skip_count = 0  # 记录跳过的有效时间点数量
                while not found_previous_value and previous_time >= start_time:
                    sql = f"""
                        SELECT dianHao 
                        FROM {table_name} 
                        WHERE inputTime = '{previous_time}'
                    """
                    cursor.execute(sql)
                    previous_result = cursor.fetchone()

                    if previous_result:
                        previous_value = float(previous_result[0])
                        if previous_value > 0:  # 找到非零值
                            found_previous_value = True
                            difference = current_value - previous_value
                            if difference > 0:  # 只累加正值
                                # 根据跳过的有效时间点数量调整差值
                                if skip_count > 0:
                                    adjusted_difference = difference / (skip_count + 1)
                                    month_dianhao += adjusted_difference
                                else:
                                    month_dianhao += difference
                        else:
                            skip_count += 1
                            # 计算更早的时间点
                            if previous_time.hour == 7 and previous_time.minute == 30:
                                previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30,
                                                                                            second=0, microsecond=0)
                            elif previous_time.hour == 15 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                            elif previous_time.hour == 23 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
                    else:
                        # 计算更早的时间点
                        if previous_time.hour == 7 and previous_time.minute == 30:
                            previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                        microsecond=0)
                        elif previous_time.hour == 15 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                        elif previous_time.hour == 23 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)

            # 将当月电耗存入数组
            monthly_data[month - 1] = round(month_dianhao, 1)

        cursor.close()
        conn.close()
        return monthly_data
    except Exception as e:
        logger.error(f"获取一班月度电耗时发生错误: {e}")
        return [0.0] * 12  # 发生错误时返回12个0


def bban_month_dianhao(table_name):
    """获取一班一年12个月每月的电耗"""
    try:
        current_time = datetime.now()
        conn = pool.connection()
        cursor = conn.cursor()

        # 初始化12个月的数据数组
        monthly_data = [0.0] * 12

        # 遍历每个月
        for month in range(1, 13):
            # 计算每月的起始和结束时间
            if month == current_time.month:
                # 当前月，结束时间为当前时间
                end_time = current_time
            else:
                # 其他月份，结束时间为当月最后一天
                if month == 12:
                    end_time = current_time.replace(year=current_time.year, month=12, day=31, hour=23, minute=59,
                                                    second=59)
                else:
                    next_month = current_time.replace(month=month + 1, day=1)
                    end_time = (next_month - timedelta(days=1)).replace(hour=23, minute=59, second=59)

            # 计算开始时间（上月25日）
            if month == 1:
                start_time = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=7, minute=30,
                                                  second=0)
            else:
                start_time = current_time.replace(month=month, day=25, hour=7, minute=30, second=0)

            # SQL查询获取当月"一班"的所有记录，按时间排序
            sql = f"""
                SELECT inputTime, dianHao 
                FROM {table_name} 
                WHERE classes = '二班' 
                AND inputTime >= '{start_time}' 
                AND inputTime <= '{end_time}'
                ORDER BY inputTime
            """

            cursor.execute(sql)
            results = cursor.fetchall()

            month_dianhao = 0.0

            # 处理每条记录
            for row in results:
                current_time = row[0]  # 当前记录的时间
                current_value = float(row[1])  # 当前记录的电耗值

                # 计算前一个时间点
                if current_time.hour == 7 and current_time.minute == 30:
                    previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                               microsecond=0)
                elif current_time.hour == 15 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
                elif current_time.hour == 23 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    continue

                # 查找前一个非零电耗值
                found_previous_value = False
                skip_count = 0  # 记录跳过的有效时间点数量
                while not found_previous_value and previous_time >= start_time:
                    sql = f"""
                        SELECT dianHao 
                        FROM {table_name} 
                        WHERE inputTime = '{previous_time}'
                    """
                    cursor.execute(sql)
                    previous_result = cursor.fetchone()

                    if previous_result:
                        previous_value = float(previous_result[0])
                        if previous_value > 0:  # 找到非零值
                            found_previous_value = True
                            difference = current_value - previous_value
                            if difference > 0:  # 只累加正值
                                # 根据跳过的有效时间点数量调整差值
                                if skip_count > 0:
                                    adjusted_difference = difference / (skip_count + 1)
                                    month_dianhao += adjusted_difference
                                else:
                                    month_dianhao += difference
                        else:
                            skip_count += 1
                            # 计算更早的时间点
                            if previous_time.hour == 7 and previous_time.minute == 30:
                                previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30,
                                                                                            second=0, microsecond=0)
                            elif previous_time.hour == 15 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                            elif previous_time.hour == 23 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
                    else:
                        # 计算更早的时间点
                        if previous_time.hour == 7 and previous_time.minute == 30:
                            previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                        microsecond=0)
                        elif previous_time.hour == 15 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                        elif previous_time.hour == 23 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)

            # 将当月电耗存入数组
            monthly_data[month - 1] = round(month_dianhao, 1)

        cursor.close()
        conn.close()
        return monthly_data
    except Exception as e:
        logger.error(f"获取一班月度电耗时发生错误: {e}")
        return [0.0] * 12  # 发生错误时返回12个0


def cban_month_dianhao(table_name):
    """获取一班一年12个月每月的电耗"""
    try:
        current_time = datetime.now()
        conn = pool.connection()
        cursor = conn.cursor()

        # 初始化12个月的数据数组
        monthly_data = [0.0] * 12

        # 遍历每个月
        for month in range(1, 13):
            # 计算每月的起始和结束时间
            if month == current_time.month:
                # 当前月，结束时间为当前时间
                end_time = current_time
            else:
                # 其他月份，结束时间为当月最后一天
                if month == 12:
                    end_time = current_time.replace(year=current_time.year, month=12, day=31, hour=23, minute=59,
                                                    second=59)
                else:
                    next_month = current_time.replace(month=month + 1, day=1)
                    end_time = (next_month - timedelta(days=1)).replace(hour=23, minute=59, second=59)

            # 计算开始时间（上月25日）
            if month == 1:
                start_time = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=7, minute=30,
                                                  second=0)
            else:
                start_time = current_time.replace(month=month, day=25, hour=7, minute=30, second=0)

            # SQL查询获取当月"一班"的所有记录，按时间排序
            sql = f"""
                SELECT inputTime, dianHao 
                FROM {table_name} 
                WHERE classes = '三班' 
                AND inputTime >= '{start_time}' 
                AND inputTime <= '{end_time}'
                ORDER BY inputTime
            """

            cursor.execute(sql)
            results = cursor.fetchall()

            month_dianhao = 0.0

            # 处理每条记录
            for row in results:
                current_time = row[0]  # 当前记录的时间
                current_value = float(row[1])  # 当前记录的电耗值

                # 计算前一个时间点
                if current_time.hour == 7 and current_time.minute == 30:
                    previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                               microsecond=0)
                elif current_time.hour == 15 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
                elif current_time.hour == 23 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    continue

                # 查找前一个非零电耗值
                found_previous_value = False
                skip_count = 0  # 记录跳过的有效时间点数量
                while not found_previous_value and previous_time >= start_time:
                    sql = f"""
                        SELECT dianHao 
                        FROM {table_name} 
                        WHERE inputTime = '{previous_time}'
                    """
                    cursor.execute(sql)
                    previous_result = cursor.fetchone()

                    if previous_result:
                        previous_value = float(previous_result[0])
                        if previous_value > 0:  # 找到非零值
                            found_previous_value = True
                            difference = current_value - previous_value
                            if difference > 0:  # 只累加正值
                                # 根据跳过的有效时间点数量调整差值
                                if skip_count > 0:
                                    adjusted_difference = difference / (skip_count + 1)
                                    month_dianhao += adjusted_difference
                                else:
                                    month_dianhao += difference
                        else:
                            skip_count += 1
                            # 计算更早的时间点
                            if previous_time.hour == 7 and previous_time.minute == 30:
                                previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30,
                                                                                            second=0, microsecond=0)
                            elif previous_time.hour == 15 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                            elif previous_time.hour == 23 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
                    else:
                        # 计算更早的时间点
                        if previous_time.hour == 7 and previous_time.minute == 30:
                            previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                        microsecond=0)
                        elif previous_time.hour == 15 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                        elif previous_time.hour == 23 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)

            # 将当月电耗存入数组
            monthly_data[month - 1] = round(month_dianhao, 1)

        cursor.close()
        conn.close()
        return monthly_data
    except Exception as e:
        logger.error(f"获取一班月度电耗时发生错误: {e}")
        return [0.0] * 12  # 发生错误时返回12个0


def dban_month_dianhao(table_name):
    """获取一班一年12个月每月的电耗"""
    try:
        current_time = datetime.now()
        conn = pool.connection()
        cursor = conn.cursor()

        # 初始化12个月的数据数组
        monthly_data = [0.0] * 12

        # 遍历每个月
        for month in range(1, 13):
            # 计算每月的起始和结束时间
            if month == current_time.month:
                # 当前月，结束时间为当前时间
                end_time = current_time
            else:
                # 其他月份，结束时间为当月最后一天
                if month == 12:
                    end_time = current_time.replace(year=current_time.year, month=12, day=31, hour=23, minute=59,
                                                    second=59)
                else:
                    next_month = current_time.replace(month=month + 1, day=1)
                    end_time = (next_month - timedelta(days=1)).replace(hour=23, minute=59, second=59)

            # 计算开始时间（上月25日）
            if month == 1:
                start_time = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=7, minute=30,
                                                  second=0)
            else:
                start_time = current_time.replace(month=month, day=25, hour=7, minute=30, second=0)

            # SQL查询获取当月"一班"的所有记录，按时间排序
            sql = f"""
                SELECT inputTime, dianHao 
                FROM {table_name} 
                WHERE classes = '四班' 
                AND inputTime >= '{start_time}' 
                AND inputTime <= '{end_time}'
                ORDER BY inputTime
            """

            cursor.execute(sql)
            results = cursor.fetchall()

            month_dianhao = 0.0

            # 处理每条记录
            for row in results:
                current_time = row[0]  # 当前记录的时间
                current_value = float(row[1])  # 当前记录的电耗值

                # 计算前一个时间点
                if current_time.hour == 7 and current_time.minute == 30:
                    previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                               microsecond=0)
                elif current_time.hour == 15 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
                elif current_time.hour == 23 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    continue

                # 查找前一个非零电耗值
                found_previous_value = False
                skip_count = 0  # 记录跳过的有效时间点数量
                while not found_previous_value and previous_time >= start_time:
                    sql = f"""
                        SELECT dianHao 
                        FROM {table_name} 
                        WHERE inputTime = '{previous_time}'
                    """
                    cursor.execute(sql)
                    previous_result = cursor.fetchone()

                    if previous_result:
                        previous_value = float(previous_result[0])
                        if previous_value > 0:  # 找到非零值
                            found_previous_value = True
                            difference = current_value - previous_value
                            if difference > 0:  # 只累加正值
                                # 根据跳过的有效时间点数量调整差值
                                if skip_count > 0:
                                    adjusted_difference = difference / (skip_count + 1)
                                    month_dianhao += adjusted_difference
                                else:
                                    month_dianhao += difference
                        else:
                            skip_count += 1
                            # 计算更早的时间点
                            if previous_time.hour == 7 and previous_time.minute == 30:
                                previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30,
                                                                                            second=0, microsecond=0)
                            elif previous_time.hour == 15 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                            elif previous_time.hour == 23 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
                    else:
                        # 计算更早的时间点
                        if previous_time.hour == 7 and previous_time.minute == 30:
                            previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                        microsecond=0)
                        elif previous_time.hour == 15 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                        elif previous_time.hour == 23 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)

            # 将当月电耗存入数组
            monthly_data[month - 1] = round(month_dianhao, 1)

        cursor.close()
        conn.close()
        return monthly_data
    except Exception as e:
        logger.error(f"获取一班月度电耗时发生错误: {e}")
        return [0.0] * 12  # 发生错误时返回12个0

    """获取一班一年12个月每月的电耗"""
    try:
        current_time = datetime.now()
        conn = pool.connection()
        cursor = conn.cursor()

        # 初始化12个月的数据数组
        monthly_data = [0.0] * 12

        # 遍历每个月
        for month in range(1, 13):
            # 计算每月的起始和结束时间
            if month == current_time.month:
                # 当前月，结束时间为当前时间
                end_time = current_time
            else:
                # 其他月份，结束时间为当月最后一天
                if month == 12:
                    end_time = current_time.replace(year=current_time.year, month=12, day=31, hour=23, minute=59,
                                                    second=59)
                else:
                    next_month = current_time.replace(month=month + 1, day=1)
                    end_time = (next_month - timedelta(days=1)).replace(hour=23, minute=59, second=59)

            # 计算开始时间（上月25日）
            if month == 1:
                start_time = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=7, minute=30,
                                                  second=0)
            else:
                start_time = current_time.replace(month=month, day=25, hour=7, minute=30, second=0)

            # SQL查询获取当月"一班"的所有记录，按时间排序
            sql = f"""
                SELECT inputTime, dianHao 
                FROM {table_name} 
                WHERE classes = '一班' 
                AND inputTime >= '{start_time}' 
                AND inputTime <= '{end_time}'
                ORDER BY inputTime
            """

            cursor.execute(sql)
            results = cursor.fetchall()

            month_dianhao = 0.0

            # 处理每条记录
            for row in results:
                current_time = row[0]  # 当前记录的时间
                current_value = float(row[1])  # 当前记录的电耗值

                # 计算前一个时间点
                if current_time.hour == 7 and current_time.minute == 30:
                    previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                               microsecond=0)
                elif current_time.hour == 15 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
                elif current_time.hour == 23 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    continue

                # 查找前一个非零电耗值
                found_previous_value = False
                skip_count = 0  # 记录跳过的有效时间点数量
                while not found_previous_value and previous_time >= start_time:
                    sql = f"""
                        SELECT dianHao 
                        FROM {table_name} 
                        WHERE inputTime = '{previous_time}'
                    """
                    cursor.execute(sql)
                    previous_result = cursor.fetchone()

                    if previous_result:
                        previous_value = float(previous_result[0])
                        if previous_value > 0:  # 找到非零值
                            found_previous_value = True
                            difference = current_value - previous_value
                            if difference > 0:  # 只累加正值
                                # 根据跳过的有效时间点数量调整差值
                                if skip_count > 0:
                                    adjusted_difference = difference / (skip_count + 1)
                                    month_dianhao += adjusted_difference
                                else:
                                    month_dianhao += difference
                        else:
                            skip_count += 1
                            # 计算更早的时间点
                            if previous_time.hour == 7 and previous_time.minute == 30:
                                previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30,
                                                                                            second=0, microsecond=0)
                            elif previous_time.hour == 15 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                            elif previous_time.hour == 23 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
                    else:
                        # 计算更早的时间点
                        if previous_time.hour == 7 and previous_time.minute == 30:
                            previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                        microsecond=0)
                        elif previous_time.hour == 15 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                        elif previous_time.hour == 23 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)

            # 将当月电耗存入数组
            monthly_data[month - 1] = round(month_dianhao, 1)

        cursor.close()
        conn.close()
        return monthly_data
    except Exception as e:
        logger.error(f"获取一班月度电耗时发生错误: {e}")
        return [0.0] * 12  # 发生错误时返回12个0


def aban_month_qihao(table_name):
    """获取一班一年12个月每月的电耗"""
    try:
        current_time = datetime.now()
        conn = pool.connection()
        cursor = conn.cursor()

        # 初始化12个月的数据数组
        monthly_data = [0.0] * 12

        # 遍历每个月
        for month in range(1, 13):
            # 计算每月的起始和结束时间
            if month == current_time.month:
                # 当前月，结束时间为当前时间
                end_time = current_time
            else:
                # 其他月份，结束时间为当月最后一天
                if month == 12:
                    end_time = current_time.replace(year=current_time.year, month=12, day=31, hour=23, minute=59,
                                                    second=59)
                else:
                    next_month = current_time.replace(month=month + 1, day=1)
                    end_time = (next_month - timedelta(days=1)).replace(hour=23, minute=59, second=59)

            # 计算开始时间（上月25日）
            if month == 1:
                start_time = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=7, minute=30,
                                                  second=0)
            else:
                start_time = current_time.replace(month=month, day=25, hour=7, minute=30, second=0)

            # SQL查询获取当月"一班"的所有记录，按时间排序
            sql = f"""
                SELECT inputTime, qiHao 
                FROM {table_name} 
                WHERE classes = '一班' 
                AND inputTime >= '{start_time}' 
                AND inputTime <= '{end_time}'
                ORDER BY inputTime
            """

            cursor.execute(sql)
            results = cursor.fetchall()

            month_qihao = 0.0

            # 处理每条记录
            for row in results:
                current_time = row[0]  # 当前记录的时间
                current_value = float(row[1])  # 当前记录的电耗值

                # 计算前一个时间点
                if current_time.hour == 7 and current_time.minute == 30:
                    previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                               microsecond=0)
                elif current_time.hour == 15 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
                elif current_time.hour == 23 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    continue

                # 查找前一个非零电耗值
                found_previous_value = False
                skip_count = 0  # 记录跳过的有效时间点数量
                while not found_previous_value and previous_time >= start_time:
                    sql = f"""
                        SELECT qiHao 
                        FROM {table_name} 
                        WHERE inputTime = '{previous_time}'
                    """
                    cursor.execute(sql)
                    previous_result = cursor.fetchone()

                    if previous_result:
                        previous_value = float(previous_result[0])
                        if previous_value > 0:  # 找到非零值
                            found_previous_value = True
                            difference = current_value - previous_value
                            if difference > 0:  # 只累加正值
                                # 根据跳过的有效时间点数量调整差值
                                if skip_count > 0:
                                    adjusted_difference = difference / (skip_count + 1)
                                    month_qihao += adjusted_difference
                                else:
                                    month_qihao += difference
                        else:
                            skip_count += 1
                            # 计算更早的时间点
                            if previous_time.hour == 7 and previous_time.minute == 30:
                                previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30,
                                                                                            second=0, microsecond=0)
                            elif previous_time.hour == 15 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                            elif previous_time.hour == 23 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
                    else:
                        # 计算更早的时间点
                        if previous_time.hour == 7 and previous_time.minute == 30:
                            previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                        microsecond=0)
                        elif previous_time.hour == 15 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                        elif previous_time.hour == 23 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)

            # 将当月电耗存入数组
            monthly_data[month - 1] = round(month_qihao, 1)

        cursor.close()
        conn.close()
        return monthly_data
    except Exception as e:
        logger.error(f"获取一班月度电耗时发生错误: {e}")
        return [0.0] * 12  # 发生错误时返回12个0


def bban_month_qihao(table_name):
    """获取一班一年12个月每月的qi耗"""
    try:
        current_time = datetime.now()
        conn = pool.connection()
        cursor = conn.cursor()

        # 初始化12个月的数据数组
        monthly_data = [0.0] * 12

        # 遍历每个月
        for month in range(1, 13):
            # 计算每月的起始和结束时间
            if month == current_time.month:
                # 当前月，结束时间为当前时间
                end_time = current_time
            else:
                # 其他月份，结束时间为当月最后一天
                if month == 12:
                    end_time = current_time.replace(year=current_time.year, month=12, day=31, hour=23, minute=59,
                                                    second=59)
                else:
                    next_month = current_time.replace(month=month + 1, day=1)
                    end_time = (next_month - timedelta(days=1)).replace(hour=23, minute=59, second=59)

            # 计算开始时间（上月25日）
            if month == 1:
                start_time = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=7, minute=30,
                                                  second=0)
            else:
                start_time = current_time.replace(month=month, day=25, hour=7, minute=30, second=0)

            # SQL查询获取当月"一班"的所有记录，按时间排序
            sql = f"""
                SELECT inputTime, qiHao 
                FROM {table_name} 
                WHERE classes = '二班' 
                AND inputTime >= '{start_time}' 
                AND inputTime <= '{end_time}'
                ORDER BY inputTime
            """

            cursor.execute(sql)
            results = cursor.fetchall()

            month_qihao = 0.0

            # 处理每条记录
            for row in results:
                current_time = row[0]  # 当前记录的时间
                current_value = float(row[1])  # 当前记录的电耗值

                # 计算前一个时间点
                if current_time.hour == 7 and current_time.minute == 30:
                    previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                               microsecond=0)
                elif current_time.hour == 15 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
                elif current_time.hour == 23 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    continue

                # 查找前一个非零电耗值
                found_previous_value = False
                skip_count = 0  # 记录跳过的有效时间点数量
                while not found_previous_value and previous_time >= start_time:
                    sql = f"""
                        SELECT qiHao 
                        FROM {table_name} 
                        WHERE inputTime = '{previous_time}'
                    """
                    cursor.execute(sql)
                    previous_result = cursor.fetchone()

                    if previous_result:
                        previous_value = float(previous_result[0])
                        if previous_value > 0:  # 找到非零值
                            found_previous_value = True
                            difference = current_value - previous_value
                            if difference > 0:  # 只累加正值
                                # 根据跳过的有效时间点数量调整差值
                                if skip_count > 0:
                                    adjusted_difference = difference / (skip_count + 1)
                                    month_qihao += adjusted_difference
                                else:
                                    month_qihao += difference
                        else:
                            skip_count += 1
                            # 计算更早的时间点
                            if previous_time.hour == 7 and previous_time.minute == 30:
                                previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30,
                                                                                            second=0, microsecond=0)
                            elif previous_time.hour == 15 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                            elif previous_time.hour == 23 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
                    else:
                        # 计算更早的时间点
                        if previous_time.hour == 7 and previous_time.minute == 30:
                            previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                        microsecond=0)
                        elif previous_time.hour == 15 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                        elif previous_time.hour == 23 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)

            # 将当月电耗存入数组
            monthly_data[month - 1] = round(month_qihao, 1)

        cursor.close()
        conn.close()
        return monthly_data
    except Exception as e:
        logger.error(f"获取一班月度汽耗时发生错误: {e}")
        return [0.0] * 12  # 发生错误时返回12个0


def cban_month_qihao(table_name):
    """获取一班一年12个月每月的qi耗"""
    try:
        current_time = datetime.now()
        conn = pool.connection()
        cursor = conn.cursor()

        # 初始化12个月的数据数组
        monthly_data = [0.0] * 12

        # 遍历每个月
        for month in range(1, 13):
            # 计算每月的起始和结束时间
            if month == current_time.month:
                # 当前月，结束时间为当前时间
                end_time = current_time
            else:
                # 其他月份，结束时间为当月最后一天
                if month == 12:
                    end_time = current_time.replace(year=current_time.year, month=12, day=31, hour=23, minute=59,
                                                    second=59)
                else:
                    next_month = current_time.replace(month=month + 1, day=1)
                    end_time = (next_month - timedelta(days=1)).replace(hour=23, minute=59, second=59)

            # 计算开始时间（上月25日）
            if month == 1:
                start_time = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=7, minute=30,
                                                  second=0)
            else:
                start_time = current_time.replace(month=month, day=25, hour=7, minute=30, second=0)

            # SQL查询获取当月"一班"的所有记录，按时间排序
            sql = f"""
                SELECT inputTime, qiHao 
                FROM {table_name} 
                WHERE classes = '三班' 
                AND inputTime >= '{start_time}' 
                AND inputTime <= '{end_time}'
                ORDER BY inputTime
            """

            cursor.execute(sql)
            results = cursor.fetchall()

            month_qihao = 0.0

            # 处理每条记录
            for row in results:
                current_time = row[0]  # 当前记录的时间
                current_value = float(row[1])  # 当前记录的电耗值

                # 计算前一个时间点
                if current_time.hour == 7 and current_time.minute == 30:
                    previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                               microsecond=0)
                elif current_time.hour == 15 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
                elif current_time.hour == 23 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    continue

                # 查找前一个非零电耗值
                found_previous_value = False
                skip_count = 0  # 记录跳过的有效时间点数量
                while not found_previous_value and previous_time >= start_time:
                    sql = f"""
                        SELECT qiHao 
                        FROM {table_name} 
                        WHERE inputTime = '{previous_time}'
                    """
                    cursor.execute(sql)
                    previous_result = cursor.fetchone()

                    if previous_result:
                        previous_value = float(previous_result[0])
                        if previous_value > 0:  # 找到非零值
                            found_previous_value = True
                            difference = current_value - previous_value
                            if difference > 0:  # 只累加正值
                                # 根据跳过的有效时间点数量调整差值
                                if skip_count > 0:
                                    adjusted_difference = difference / (skip_count + 1)
                                    month_qihao += adjusted_difference
                                else:
                                    month_qihao += difference
                        else:
                            skip_count += 1
                            # 计算更早的时间点
                            if previous_time.hour == 7 and previous_time.minute == 30:
                                previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30,
                                                                                            second=0, microsecond=0)
                            elif previous_time.hour == 15 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                            elif previous_time.hour == 23 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
                    else:
                        # 计算更早的时间点
                        if previous_time.hour == 7 and previous_time.minute == 30:
                            previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                        microsecond=0)
                        elif previous_time.hour == 15 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                        elif previous_time.hour == 23 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)

            # 将当月电耗存入数组
            monthly_data[month - 1] = round(month_qihao, 1)

        cursor.close()
        conn.close()
        return monthly_data
    except Exception as e:
        logger.error(f"获取2班月度汽耗时发生错误: {e}")
        return [0.0] * 12  # 发生错误时返回12个0


def dban_month_qihao(table_name):
    """获取一班一年12个月每月的qi耗"""
    try:
        current_time = datetime.now()
        conn = pool.connection()
        cursor = conn.cursor()

        # 初始化12个月的数据数组
        monthly_data = [0.0] * 12

        # 遍历每个月
        for month in range(1, 13):
            # 计算每月的起始和结束时间
            if month == current_time.month:
                # 当前月，结束时间为当前时间
                end_time = current_time
            else:
                # 其他月份，结束时间为当月最后一天
                if month == 12:
                    end_time = current_time.replace(year=current_time.year, month=12, day=31, hour=23, minute=59,
                                                    second=59)
                else:
                    next_month = current_time.replace(month=month + 1, day=1)
                    end_time = (next_month - timedelta(days=1)).replace(hour=23, minute=59, second=59)

            # 计算开始时间（上月25日）
            if month == 1:
                start_time = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=7, minute=30,
                                                  second=0)
            else:
                start_time = current_time.replace(month=month, day=25, hour=7, minute=30, second=0)

            # SQL查询获取当月"一班"的所有记录，按时间排序
            sql = f"""
                SELECT inputTime, qiHao 
                FROM {table_name} 
                WHERE classes = '四班' 
                AND inputTime >= '{start_time}' 
                AND inputTime <= '{end_time}'
                ORDER BY inputTime
            """

            cursor.execute(sql)
            results = cursor.fetchall()

            month_qihao = 0.0

            # 处理每条记录
            for row in results:
                current_time = row[0]  # 当前记录的时间
                current_value = float(row[1])  # 当前记录的电耗值

                # 计算前一个时间点
                if current_time.hour == 7 and current_time.minute == 30:
                    previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                               microsecond=0)
                elif current_time.hour == 15 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
                elif current_time.hour == 23 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    continue

                # 查找前一个非零电耗值
                found_previous_value = False
                skip_count = 0  # 记录跳过的有效时间点数量
                while not found_previous_value and previous_time >= start_time:
                    sql = f"""
                        SELECT qiHao 
                        FROM {table_name} 
                        WHERE inputTime = '{previous_time}'
                    """
                    cursor.execute(sql)
                    previous_result = cursor.fetchone()

                    if previous_result:
                        previous_value = float(previous_result[0])
                        if previous_value > 0:  # 找到非零值
                            found_previous_value = True
                            difference = current_value - previous_value
                            if difference > 0:  # 只累加正值
                                # 根据跳过的有效时间点数量调整差值
                                if skip_count > 0:
                                    adjusted_difference = difference / (skip_count + 1)
                                    month_qihao += adjusted_difference
                                else:
                                    month_qihao += difference
                        else:
                            skip_count += 1
                            # 计算更早的时间点
                            if previous_time.hour == 7 and previous_time.minute == 30:
                                previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30,
                                                                                            second=0, microsecond=0)
                            elif previous_time.hour == 15 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                            elif previous_time.hour == 23 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
                    else:
                        # 计算更早的时间点
                        if previous_time.hour == 7 and previous_time.minute == 30:
                            previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                        microsecond=0)
                        elif previous_time.hour == 15 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                        elif previous_time.hour == 23 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)

            # 将当月电耗存入数组
            monthly_data[month - 1] = round(month_qihao, 1)

        cursor.close()
        conn.close()
        return monthly_data
    except Exception as e:
        logger.error(f"获取4班月度汽耗时发生错误: {e}")
        return [0.0] * 12  # 发生错误时返回12个0


def aban_month_luhao(table_name):
    """获取一班一年12个月每月的电耗"""
    try:
        current_time = datetime.now()
        conn = pool.connection()
        cursor = conn.cursor()

        # 初始化12个月的数据数组
        monthly_data = [0.0] * 12

        # 遍历每个月
        for month in range(1, 13):
            # 计算每月的起始和结束时间
            if month == current_time.month:
                # 当前月，结束时间为当前时间
                end_time = current_time
            else:
                # 其他月份，结束时间为当月最后一天
                if month == 12:
                    end_time = current_time.replace(year=current_time.year, month=12, day=31, hour=23, minute=59,
                                                    second=59)
                else:
                    next_month = current_time.replace(month=month + 1, day=1)
                    end_time = (next_month - timedelta(days=1)).replace(hour=23, minute=59, second=59)

            # 计算开始时间（上月25日）
            if month == 1:
                start_time = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=7, minute=30,
                                                  second=0)
            else:
                start_time = current_time.replace(month=month, day=25, hour=7, minute=30, second=0)

            # SQL查询获取当月"一班"的所有记录，按时间排序
            sql = f"""
                SELECT inputTime, luHao 
                FROM {table_name} 
                WHERE classes = '一班' 
                AND inputTime >= '{start_time}' 
                AND inputTime <= '{end_time}'
                ORDER BY inputTime
            """

            cursor.execute(sql)
            results = cursor.fetchall()

            month_luhao = 0.0

            # 处理每条记录
            for row in results:
                current_time = row[0]  # 当前记录的时间
                current_value = float(row[1])  # 当前记录的电耗值

                # 计算前一个时间点
                if current_time.hour == 7 and current_time.minute == 30:
                    previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                               microsecond=0)
                elif current_time.hour == 15 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
                elif current_time.hour == 23 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    continue

                # 查找前一个非零电耗值
                found_previous_value = False
                skip_count = 0  # 记录跳过的有效时间点数量
                while not found_previous_value and previous_time >= start_time:
                    sql = f"""
                        SELECT luHao 
                        FROM {table_name} 
                        WHERE inputTime = '{previous_time}'
                    """
                    cursor.execute(sql)
                    previous_result = cursor.fetchone()

                    if previous_result:
                        previous_value = float(previous_result[0])
                        if previous_value > 0:  # 找到非零值
                            found_previous_value = True
                            difference = current_value - previous_value
                            if difference > 0:  # 只累加正值
                                # 根据跳过的有效时间点数量调整差值
                                if skip_count > 0:
                                    adjusted_difference = difference / (skip_count + 1)
                                    month_luhao += adjusted_difference
                                else:
                                    month_luhao += difference
                        else:
                            skip_count += 1
                            # 计算更早的时间点
                            if previous_time.hour == 7 and previous_time.minute == 30:
                                previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30,
                                                                                            second=0, microsecond=0)
                            elif previous_time.hour == 15 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                            elif previous_time.hour == 23 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
                    else:
                        # 计算更早的时间点
                        if previous_time.hour == 7 and previous_time.minute == 30:
                            previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                        microsecond=0)
                        elif previous_time.hour == 15 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                        elif previous_time.hour == 23 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)

            # 将当月电耗存入数组
            monthly_data[month - 1] = round(month_luhao, 1)

        cursor.close()
        conn.close()
        return monthly_data
    except Exception as e:
        logger.error(f"获取一班月度电耗时发生错误: {e}")
        return [0.0] * 12  # 发生错误时返回12个0


def bban_month_luhao(table_name):
    """获取一班一年12个月每月的电耗"""
    try:
        current_time = datetime.now()
        conn = pool.connection()
        cursor = conn.cursor()

        # 初始化12个月的数据数组
        monthly_data = [0.0] * 12

        # 遍历每个月
        for month in range(1, 13):
            # 计算每月的起始和结束时间
            if month == current_time.month:
                # 当前月，结束时间为当前时间
                end_time = current_time
            else:
                # 其他月份，结束时间为当月最后一天
                if month == 12:
                    end_time = current_time.replace(year=current_time.year, month=12, day=31, hour=23, minute=59,
                                                    second=59)
                else:
                    next_month = current_time.replace(month=month + 1, day=1)
                    end_time = (next_month - timedelta(days=1)).replace(hour=23, minute=59, second=59)

            # 计算开始时间（上月25日）
            if month == 1:
                start_time = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=7, minute=30,
                                                  second=0)
            else:
                start_time = current_time.replace(month=month, day=25, hour=7, minute=30, second=0)

            # SQL查询获取当月"一班"的所有记录，按时间排序
            sql = f"""
                SELECT inputTime, luHao 
                FROM {table_name} 
                WHERE classes = '二班' 
                AND inputTime >= '{start_time}' 
                AND inputTime <= '{end_time}'
                ORDER BY inputTime
            """

            cursor.execute(sql)
            results = cursor.fetchall()

            month_luhao = 0.0

            # 处理每条记录
            for row in results:
                current_time = row[0]  # 当前记录的时间
                current_value = float(row[1])  # 当前记录的电耗值

                # 计算前一个时间点
                if current_time.hour == 7 and current_time.minute == 30:
                    previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                               microsecond=0)
                elif current_time.hour == 15 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
                elif current_time.hour == 23 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    continue

                # 查找前一个非零电耗值
                found_previous_value = False
                skip_count = 0  # 记录跳过的有效时间点数量
                while not found_previous_value and previous_time >= start_time:
                    sql = f"""
                        SELECT luHao 
                        FROM {table_name} 
                        WHERE inputTime = '{previous_time}'
                    """
                    cursor.execute(sql)
                    previous_result = cursor.fetchone()

                    if previous_result:
                        previous_value = float(previous_result[0])
                        if previous_value > 0:  # 找到非零值
                            found_previous_value = True
                            difference = current_value - previous_value
                            if difference > 0:  # 只累加正值
                                # 根据跳过的有效时间点数量调整差值
                                if skip_count > 0:
                                    adjusted_difference = difference / (skip_count + 1)
                                    month_luhao += adjusted_difference
                                else:
                                    month_luhao += difference
                        else:
                            skip_count += 1
                            # 计算更早的时间点
                            if previous_time.hour == 7 and previous_time.minute == 30:
                                previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30,
                                                                                            second=0, microsecond=0)
                            elif previous_time.hour == 15 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                            elif previous_time.hour == 23 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
                    else:
                        # 计算更早的时间点
                        if previous_time.hour == 7 and previous_time.minute == 30:
                            previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                        microsecond=0)
                        elif previous_time.hour == 15 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                        elif previous_time.hour == 23 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)

            # 将当月电耗存入数组
            monthly_data[month - 1] = round(month_luhao, 1)

        cursor.close()
        conn.close()
        return monthly_data
    except Exception as e:
        logger.error(f"获取一班月度电耗时发生错误: {e}")
        return [0.0] * 12  # 发生错误时返回12个0


def cban_month_luhao(table_name):
    """获取一班一年12个月每月的电耗"""
    try:
        current_time = datetime.now()
        conn = pool.connection()
        cursor = conn.cursor()

        # 初始化12个月的数据数组
        monthly_data = [0.0] * 12

        # 遍历每个月
        for month in range(1, 13):
            # 计算每月的起始和结束时间
            if month == current_time.month:
                # 当前月，结束时间为当前时间
                end_time = current_time
            else:
                # 其他月份，结束时间为当月最后一天
                if month == 12:
                    end_time = current_time.replace(year=current_time.year, month=12, day=31, hour=23, minute=59,
                                                    second=59)
                else:
                    next_month = current_time.replace(month=month + 1, day=1)
                    end_time = (next_month - timedelta(days=1)).replace(hour=23, minute=59, second=59)

            # 计算开始时间（上月25日）
            if month == 1:
                start_time = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=7, minute=30,
                                                  second=0)
            else:
                start_time = current_time.replace(month=month, day=25, hour=7, minute=30, second=0)

            # SQL查询获取当月"一班"的所有记录，按时间排序
            sql = f"""
                SELECT inputTime, luHao 
                FROM {table_name} 
                WHERE classes = '三班' 
                AND inputTime >= '{start_time}' 
                AND inputTime <= '{end_time}'
                ORDER BY inputTime
            """

            cursor.execute(sql)
            results = cursor.fetchall()

            month_luhao = 0.0

            # 处理每条记录
            for row in results:
                current_time = row[0]  # 当前记录的时间
                current_value = float(row[1])  # 当前记录的电耗值

                # 计算前一个时间点
                if current_time.hour == 7 and current_time.minute == 30:
                    previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                               microsecond=0)
                elif current_time.hour == 15 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
                elif current_time.hour == 23 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    continue

                # 查找前一个非零电耗值
                found_previous_value = False
                skip_count = 0  # 记录跳过的有效时间点数量
                while not found_previous_value and previous_time >= start_time:
                    sql = f"""
                        SELECT luHao 
                        FROM {table_name} 
                        WHERE inputTime = '{previous_time}'
                    """
                    cursor.execute(sql)
                    previous_result = cursor.fetchone()

                    if previous_result:
                        previous_value = float(previous_result[0])
                        if previous_value > 0:  # 找到非零值
                            found_previous_value = True
                            difference = current_value - previous_value
                            if difference > 0:  # 只累加正值
                                # 根据跳过的有效时间点数量调整差值
                                if skip_count > 0:
                                    adjusted_difference = difference / (skip_count + 1)
                                    month_luhao += adjusted_difference
                                else:
                                    month_luhao += difference
                        else:
                            skip_count += 1
                            # 计算更早的时间点
                            if previous_time.hour == 7 and previous_time.minute == 30:
                                previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30,
                                                                                            second=0, microsecond=0)
                            elif previous_time.hour == 15 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                            elif previous_time.hour == 23 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
                    else:
                        # 计算更早的时间点
                        if previous_time.hour == 7 and previous_time.minute == 30:
                            previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                        microsecond=0)
                        elif previous_time.hour == 15 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                        elif previous_time.hour == 23 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)

            # 将当月电耗存入数组
            monthly_data[month - 1] = round(month_luhao, 1)

        cursor.close()
        conn.close()
        return monthly_data
    except Exception as e:
        logger.error(f"获取一班月度电耗时发生错误: {e}")
        return [0.0] * 12  # 发生错误时返回12个0


def dban_month_luhao(table_name):
    """获取一班一年12个月每月的电耗"""
    try:
        current_time = datetime.now()
        conn = pool.connection()
        cursor = conn.cursor()

        # 初始化12个月的数据数组
        monthly_data = [0.0] * 12

        # 遍历每个月
        for month in range(1, 13):
            # 计算每月的起始和结束时间
            if month == current_time.month:
                # 当前月，结束时间为当前时间
                end_time = current_time
            else:
                # 其他月份，结束时间为当月最后一天
                if month == 12:
                    end_time = current_time.replace(year=current_time.year, month=12, day=31, hour=23, minute=59,
                                                    second=59)
                else:
                    next_month = current_time.replace(month=month + 1, day=1)
                    end_time = (next_month - timedelta(days=1)).replace(hour=23, minute=59, second=59)

            # 计算开始时间（上月25日）
            if month == 1:
                start_time = current_time.replace(year=current_time.year - 1, month=12, day=25, hour=7, minute=30,
                                                  second=0)
            else:
                start_time = current_time.replace(month=month, day=25, hour=7, minute=30, second=0)

            # SQL查询获取当月"一班"的所有记录，按时间排序
            sql = f"""
                SELECT inputTime, luHao 
                FROM {table_name} 
                WHERE classes = '四班' 
                AND inputTime >= '{start_time}' 
                AND inputTime <= '{end_time}'
                ORDER BY inputTime
            """

            cursor.execute(sql)
            results = cursor.fetchall()

            month_luhao = 0.0

            # 处理每条记录
            for row in results:
                current_time = row[0]  # 当前记录的时间
                current_value = float(row[1])  # 当前记录的电耗值

                # 计算前一个时间点
                if current_time.hour == 7 and current_time.minute == 30:
                    previous_time = (current_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                               microsecond=0)
                elif current_time.hour == 15 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=7, minute=30, second=0, microsecond=0)
                elif current_time.hour == 23 and current_time.minute == 30:
                    previous_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)
                else:
                    continue

                # 查找前一个非零电耗值
                found_previous_value = False
                skip_count = 0  # 记录跳过的有效时间点数量
                while not found_previous_value and previous_time >= start_time:
                    sql = f"""
                        SELECT luHao 
                        FROM {table_name} 
                        WHERE inputTime = '{previous_time}'
                    """
                    cursor.execute(sql)
                    previous_result = cursor.fetchone()

                    if previous_result:
                        previous_value = float(previous_result[0])
                        if previous_value > 0:  # 找到非零值
                            found_previous_value = True
                            difference = current_value - previous_value
                            if difference > 0:  # 只累加正值
                                # 根据跳过的有效时间点数量调整差值
                                if skip_count > 0:
                                    adjusted_difference = difference / (skip_count + 1)
                                    month_luhao += adjusted_difference
                                else:
                                    month_luhao += difference
                        else:
                            skip_count += 1
                            # 计算更早的时间点
                            if previous_time.hour == 7 and previous_time.minute == 30:
                                previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30,
                                                                                            second=0, microsecond=0)
                            elif previous_time.hour == 15 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                            elif previous_time.hour == 23 and previous_time.minute == 30:
                                previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)
                    else:
                        # 计算更早的时间点
                        if previous_time.hour == 7 and previous_time.minute == 30:
                            previous_time = (previous_time - timedelta(days=1)).replace(hour=23, minute=30, second=0,
                                                                                        microsecond=0)
                        elif previous_time.hour == 15 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=7, minute=30, second=0, microsecond=0)
                        elif previous_time.hour == 23 and previous_time.minute == 30:
                            previous_time = previous_time.replace(hour=15, minute=30, second=0, microsecond=0)

            # 将当月电耗存入数组
            monthly_data[month - 1] = round(month_luhao, 1)

        cursor.close()
        conn.close()
        return monthly_data
    except Exception as e:
        logger.error(f"获取一班月度电耗时发生错误: {e}")
        return [0.0] * 12  # 发生错误时返回12个0


def aban_month_dundianhao():
    """获取一班一年12个月每月的吨盐电耗（电耗/产量）"""
    # 获取一班每月电耗和产量
    dianhao_list = aban_month_dianhao('threehand')
    chanliang_list = aban_month_chanliang('output')
    # 计算吨盐电耗
    dundianhao_list = []
    for dianhao, chanliang in zip(dianhao_list, chanliang_list):
        if chanliang > 0:
            dundianhao = round(dianhao / chanliang, 2)
        else:
            dundianhao = 0
        dundianhao_list.append(dundianhao)
    return dundianhao_list


def bban_month_dundianhao():
    """获取二班一年12个月每月的吨盐电耗（电耗/产量）"""
    # 获取二班每月电耗和产量
    dianhao_list = bban_month_dianhao('threehand')
    chanliang_list = bban_month_chanliang('output')
    # 计算吨盐电耗
    dundianhao_list = []
    for dianhao, chanliang in zip(dianhao_list, chanliang_list):
        if chanliang > 0:
            dundianhao = round(dianhao / chanliang, 2)
        else:
            dundianhao = 0
        dundianhao_list.append(dundianhao)
    return dundianhao_list


def cban_month_dundianhao():
    """获取三班一年12个月每月的吨盐电耗（电耗/产量）"""
    # 获取三班每月电耗和产量
    dianhao_list = cban_month_dianhao('threehand')
    chanliang_list = cban_month_chanliang('output')
    # 计算吨盐电耗
    dundianhao_list = []
    for dianhao, chanliang in zip(dianhao_list, chanliang_list):
        if chanliang > 0:
            dundianhao = round(dianhao / chanliang, 2)
        else:
            dundianhao = 0
        dundianhao_list.append(dundianhao)
    return dundianhao_list


def dban_month_dundianhao():
    """获取四班一年12个月每月的吨盐电耗（电耗/产量）"""
    # 获取四班每月电耗和产量
    dianhao_list = dban_month_dianhao('threehand')
    chanliang_list = dban_month_chanliang('output')
    # 计算吨盐电耗
    dundianhao_list = []
    for dianhao, chanliang in zip(dianhao_list, chanliang_list):
        if chanliang > 0:
            dundianhao = round(dianhao / chanliang, 2)
        else:
            dundianhao = 0
        dundianhao_list.append(dundianhao)
    return dundianhao_list


def aban_month_dunluhao():
    """获取一班一年12个月每月的吨盐电耗（电耗/产量）"""
    # 获取一班每月电耗和产量
    luhao_list = aban_month_luhao('threehand')
    chanliang_list = aban_month_chanliang('output')
    # 计算吨盐电耗
    dunluhao_list = []
    for luhao, chanliang in zip(luhao_list, chanliang_list):
        if chanliang > 0:
            dunluhao = round(luhao / chanliang, 2)
        else:
            dunluhao = 0
        dunluhao_list.append(dunluhao)
    return dunluhao_list


def bban_month_dunluhao():
    """获取二班一年12个月每月的吨盐电耗（电耗/产量）"""
    # 获取二班每月电耗和产量
    luhao_list = bban_month_luhao('threehand')
    chanliang_list = bban_month_chanliang('output')
    # 计算吨盐电耗
    dunluhao_list = []
    for luhao, chanliang in zip(luhao_list, chanliang_list):
        if chanliang > 0:
            dunluhao = round(luhao / chanliang, 2)
        else:
            dunluhao = 0
        dunluhao_list.append(dunluhao)
    return dunluhao_list


def cban_month_dunluhao():
    """获取三班一年12个月每月的吨盐电耗（电耗/产量）"""
    # 获取三班每月电耗和产量
    luhao_list = cban_month_luhao('threehand')
    chanliang_list = cban_month_chanliang('output')
    # 计算吨盐电耗
    dunluhao_list = []
    for luhao, chanliang in zip(luhao_list, chanliang_list):
        if chanliang > 0:
            dunluhao = round(luhao / chanliang, 2)
        else:
            dunluhao = 0
        dunluhao_list.append(dunluhao)
    return dunluhao_list


def dban_month_dunluhao():
    """获取四班一年12个月每月的吨盐卤耗（电耗/产量）"""
    # 获取四班每月电耗和产量
    luhao_list = dban_month_luhao('threehand')
    chanliang_list = dban_month_chanliang('output')
    # 计算吨盐电耗
    dunluhao_list = []
    for luhao, chanliang in zip(luhao_list, chanliang_list):
        if chanliang > 0:
            dunluhao = round(luhao / chanliang, 2)
        else:
            dunluhao = 0
        dunluhao_list.append(dunluhao)
    return dunluhao_list


def aban_month_dunqihao():
    """获取一班一年12个月每月的期号"""
    # 获取一班每月电耗和产量
    qihao_list = aban_month_qihao('threehand')
    chanliang_list = aban_month_chanliang('output')
    # 计算吨盐电耗
    dunluhao_list = []
    for qihao, chanliang in zip(qihao_list, chanliang_list):
        if chanliang > 0:
            dunluhao = round(qihao / chanliang, 2)
        else:
            dunluhao = 0
        dunluhao_list.append(dunluhao)
    return dunluhao_list


def bban_month_dunqihao():
    """获取二班一年12个月每月的期号"""
    # 获取二班每月电耗和产量
    qihao_list = bban_month_qihao('threehand')
    chanliang_list = bban_month_chanliang('output')
    # 计算吨盐电耗
    dunluhao_list = []
    for qihao, chanliang in zip(qihao_list, chanliang_list):
        if chanliang > 0:
            dunluhao = round(qihao / chanliang, 2)
        else:
            dunluhao = 0
        dunluhao_list.append(dunluhao)
    return dunluhao_list


def cban_month_dunqihao():
    """获取三班一年12个月每月的期号"""
    # 获取三班每月电耗和产量
    qihao_list = cban_month_qihao('threehand')
    chanliang_list = cban_month_chanliang('output')
    # 计算吨盐电耗
    dunluhao_list = []
    for qihao, chanliang in zip(qihao_list, chanliang_list):
        if chanliang > 0:
            dunluhao = round(qihao / chanliang, 2)
        else:
            dunluhao = 0
        dunluhao_list.append(dunluhao)
    return dunluhao_list


def dban_month_dunqihao():
    """获取四班一年12个月每月的期号"""
    # 获取四班每月电耗和产量
    qihao_list = dban_month_qihao('threehand')
    chanliang_list = dban_month_chanliang('output')
    # 计算吨盐电耗
    dunluhao_list = []
    for qihao, chanliang in zip(qihao_list, chanliang_list):
        if chanliang > 0:
            dunluhao = round(qihao / chanliang, 2)
        else:
            dunluhao = 0
        dunluhao_list.append(dunluhao)
    return dunluhao_list


def fourban_defen():
    # 获取四个班每个月的各项数据
    # 产量
    a_chanliang = aban_month_chanliang('output')
    b_chanliang = bban_month_chanliang('output')
    c_chanliang = cban_month_chanliang('output')
    d_chanliang = dban_month_chanliang('output')
    # 吨盐电耗
    a_dianhao = aban_month_dundianhao()
    b_dianhao = bban_month_dundianhao()
    c_dianhao = cban_month_dundianhao()
    d_dianhao = dban_month_dundianhao()
    # 吨盐卤耗
    a_luhao = aban_month_dunluhao()
    b_luhao = bban_month_dunluhao()
    c_luhao = cban_month_dunluhao()
    d_luhao = dban_month_dunluhao()
    # 吨盐汽耗
    a_qihao = aban_month_dunqihao()
    b_qihao = bban_month_dunqihao()
    c_qihao = cban_month_dunqihao()
    d_qihao = dban_month_dunqihao()

    # 结果
    result = {
        "aban": [],
        "bban": [],
        "cban": [],
        "dban": []
    }

    # 每个月计算得分
    for i in range(12):
        # 产量排序
        chanliang_list = [a_chanliang[i], b_chanliang[i], c_chanliang[i], d_chanliang[i]]
        chanliang_sorted = sorted(chanliang_list, reverse=True)
        chanliang_scores = [10, 9.8, 9.6, 9.4]
        chanliang_ranks = [chanliang_sorted.index(x) for x in chanliang_list]
        chanliang_month_scores = [chanliang_scores[r] for r in chanliang_ranks]

        # 吨盐电耗排序
        dianhao_list = [a_dianhao[i], b_dianhao[i], c_dianhao[i], d_dianhao[i]]
        dianhao_sorted = sorted(dianhao_list)
        dianhao_scores = [10, 9.8, 9.6, 9.4]
        dianhao_ranks = [dianhao_sorted.index(x) for x in dianhao_list]
        dianhao_month_scores = [dianhao_scores[r] for r in dianhao_ranks]

        # 吨盐卤耗排序
        luhao_list = [a_luhao[i], b_luhao[i], c_luhao[i], d_luhao[i]]
        luhao_sorted = sorted(luhao_list)
        luhao_scores = [10, 9.8, 9.6, 9.4]
        luhao_ranks = [luhao_sorted.index(x) for x in luhao_list]
        luhao_month_scores = [luhao_scores[r] for r in luhao_ranks]

        # 吨盐汽耗排序
        qihao_list = [a_qihao[i], b_qihao[i], c_qihao[i], d_qihao[i]]
        qihao_sorted = sorted(qihao_list)
        qihao_scores = [10, 9.8, 9.6, 9.4]
        qihao_ranks = [qihao_sorted.index(x) for x in qihao_list]
        qihao_month_scores = [qihao_scores[r] for r in qihao_ranks]

        # 计算每个班当月的总分
        a_total = chanliang_month_scores[0] + dianhao_month_scores[0] + luhao_month_scores[0] + qihao_month_scores[0]
        b_total = chanliang_month_scores[1] + dianhao_month_scores[1] + luhao_month_scores[1] + qihao_month_scores[1]
        c_total = chanliang_month_scores[2] + dianhao_month_scores[2] + luhao_month_scores[2] + qihao_month_scores[2]
        d_total = chanliang_month_scores[3] + dianhao_month_scores[3] + luhao_month_scores[3] + qihao_month_scores[3]

        result["aban"].append(a_total)
        result["bban"].append(b_total)
        result["cban"].append(c_total)
        result["dban"].append(d_total)

    return result


@app.route('/api/data5/', methods=['GET'])
def get_dafen():
    try:
        defen = fourban_defen()

        respons_data = {
            "defen": defen,

        }

        return jsonify(respons_data)

    except Exception as e:
        print(f"Error in dafen: {str(e)}")
        return jsonify({
            "error": "数据获取失败",
            "message": str(e)
        }), 500


@app.route('/api/data6/', methods=['GET'])
def get_data6():
    try:
        data = fetch_data_from_db('tonghuanbi')

        if not data or len(data) < 12:
            return jsonify({
                "error": "数据不足",
                "message": "tonghuanbi 表中数据条数少于 12"
            }), 404

        all_month_data = []


        for month_entry in data[:24]:  # 避免数据太多只取前12个月
            chanliang = float(month_entry.get("chanliang", 0))
            ganyanchan = float(month_entry.get("ganyanchan", 0))
            qihao = float(month_entry.get("qihao", 0))
            dianhao = float(month_entry.get("dianhao", 0))
            luhao = float(month_entry.get("luhao", 0))
            totalhao = float(month_entry.get("totalhao", 0))

            net_chanliang = chanliang - ganyanchan

            month_data = {
                "month": month_entry.get("tS"),
                "chanliang": net_chanliang,
                "ganyanchan": ganyanchan,
                "qihao": qihao,
                "dianhao": dianhao,
                "luhao": luhao,
                "totalhao": totalhao
            }
            all_month_data.append(month_data)




        month_chanliang = get_month_chanliang('output')
        month_ganyan = get_month_ganyan('output')
        month_dianhao = get_month_dianhao('threehand', return_from_last=True)
        month_qihao = get_month_qihao('output', return_from_last=True)
        month_luhao = get_month_luhao('output', return_from_last=True) + get_month_taoxi('output')




        dandianhao = round(month_dianhao / (month_chanliang + month_ganyan), 2) if (
                                                                                               month_chanliang + month_ganyan) != 0 else 0
        danluhao = round((month_luhao) / (month_chanliang + month_ganyan), 2) if (
                                                                                             month_chanliang + month_ganyan) != 0 else 0
        danqihao = round(month_qihao / (month_chanliang + month_ganyan), 2) if (
                                                                                           month_chanliang + month_ganyan) != 0 else 0
        zonghenenghao = round((danqihao * 128.6 + dandianhao * 0.1229), 2)

        response_data = {
            "all_month_data": all_month_data,
            "summary": {
                "month_chanliang": month_chanliang,
                "month_ganyan": month_ganyan,
                "month_dianhao": month_dianhao,
                "month_qihao": month_qihao,
                "month_luhao": month_luhao,
                "dandianhao": dandianhao,
                "danluhao": danluhao,
                "danqihao": danqihao,
                "zonghenenghao": zonghenenghao
            }
        }

        return jsonify(response_data)

    except Exception as e:
        error_msg = str(e)
        print(f"Error in get_data6: {error_msg}")
        return jsonify({
            "error": "数据获取失败",
            "message": error_msg,
            "details": "请检查数据库连接和 tonghuanbi 表是否存在"
        }), 500


@app.route('/get_monitoring_points', methods=['GET'])
def get_monitoring_points():
    """获取所有监控点位数据，并统计报警类型和处理状态"""
    try:
        cursor = mysql.connection.cursor()

        # 查询alarm表中的所有点位数据，同时关联ignored_alarms表
        cursor.execute("""
            SELECT 
                a.id,
                a.PointId,
                a.possibleCause,
                a.Solution,
                a.naocan1,
                a.naocan2,
                a.handling,
                a.namee as name,
                a.valuee as value,
                a.unit,
                a.Typee as type,
                a.normalRange,
                i.expiry_time
            FROM js.alarm a
            LEFT JOIN js.ignored_alarms i ON a.id = i.point_id
            ORDER BY a.id
        """)

        # 获取列名
        columns = [desc[0] for desc in cursor.description]

        # 添加报警类型统计
        alarm_type_stats_local = {
            'device': 0,  # 设备类报警
            'craft': 0  # 工艺类报警
        }

        # 只统计处理状态
        status_stats = {
            'pending': 0,  # 待处理 (handling 为 warning 或 ignore)
            'handled': 0  # 已处理 (handling 为 resolved)
        }

        # 存储新检测到的报警点位
        new_alarms = []

        # 将结果转换为字典列表并统计
        points = []
        for row in cursor.fetchall():
            point = dict(zip(columns, row))

            # 统计处理状态
            if point['handling'] in ['warning', 'ignore']:
                status_stats['pending'] += 1
            elif point['handling'] == 'resolved':
                status_stats['handled'] += 1

            # 处理normalRange字段
            try:
                if isinstance(point['normalRange'], str) and point['normalRange'].strip():
                    range_str = point['normalRange'].strip('[]').split(',')
                    if len(range_str) == 2:
                        point['normalRange'] = [float(range_str[0]), float(range_str[1])]
                    else:
                        point['normalRange'] = [0, 100]
                else:
                    point['normalRange'] = [0, 100]
            except Exception as e:
                point['normalRange'] = [0, 100]

            # 获取当前值
            try:
                # 检查PointId是否包含减号"-"，如果有则表示是差值报警点位
                if "-" in point['PointId']:
                    # 分离被减数和减数的PointId
                    point_ids = point['PointId'].split("-")
                    if len(point_ids) == 2:
                        minuend_id = point_ids[0]  # 被减数
                        subtrahend_id = point_ids[1]  # 减数

                        # 获取两个点位的最新值
                        minuend_value = get_latest_value(minuend_id)
                        subtrahend_value = get_latest_value(subtrahend_id)

                        # 计算差值
                        if minuend_value is not None and subtrahend_value is not None:
                            current_value = round(minuend_value - subtrahend_value, 1)
                            point['value'] = current_value
                        else:
                            point['value'] = point['value'] if point['value'] else ''
                    else:
                        point['value'] = point['value'] if point['value'] else ''
                else:
                    # 普通单点报警，沿用原来的逻辑
                    current_value = get_latest_value(point['PointId'])
                    if current_value is not None:
                        point['value'] = current_value
                    else:
                        point['value'] = point['value'] if point['value'] else ''
            except Exception as e:
                point['value'] = point['value'] if point['value'] else ''

            # 检查ignored_alarms表中的过期时间
            if point.get('handling') in ['resolved', 'ignore', 'repair'] and point.get('expiry_time'):
                expiry_time = point['expiry_time']
                if isinstance(expiry_time, str):
                    expiry_time = datetime.strptime(expiry_time, '%Y-%m-%d %H:%M:%S')

                # 如果已过期，重置handling状态
                if expiry_time < datetime.now():
                    cursor.execute("""
                        UPDATE js.alarm 
                        SET handling = NULL 
                        WHERE id = %s
                    """, (point['id'],))
                    point['handling'] = None

                    # 删除过期的忽略记录
                    cursor.execute("""
                        DELETE FROM js.ignored_alarms 
                        WHERE point_id = %s
                    """, (point['id'],))

                    # 重新检查状态
                    point_status = check_alarm_status(point)
                    point['status'] = point_status
                    continue

            # 在后端进行报警判断
            point_status = check_alarm_status(point)
            point['status'] = point_status

            # 如果点位是'repair'状态，这里不需要特殊处理，前端会处理

            # 如果有handling值，可能需要覆盖状态
            if point.get('handling') == 'repair':
                point['status'] = 'repair'
            elif point.get('handling') in ['resolved', 'ignore'] and not point.get('expiry_time'):
                # 无论point_status是什么，如果点位已被标记为resolved或ignore且未过期，强制将状态设为normal
                point['status'] = 'normal'
                # 重要：这里不再检查point_status == 'alarm'条件，确保处理过的报警始终显示为normal

            # 如果是报警状态，统计报警类型
            if point_status == 'alarm' and not point.get('handling') in ['resolved', 'ignore', 'repair']:
                # 统计报警类型
                if point.get('type') == '设备类报警':
                    alarm_type_stats_local['device'] += 1
                elif point.get('type') == '工艺类报警':
                    alarm_type_stats_local['craft'] += 1

                # 更新报警状态前，先检查最新的处理状态
                try:
                    # 查询数据库中的最新状态
                    check_cursor = mysql.connection.cursor()
                    check_cursor.execute("""
                        SELECT a.handling, i.expiry_time
                        FROM js.alarm a
                        LEFT JOIN js.ignored_alarms i ON a.id = i.point_id
                        WHERE a.PointId = %s
                    """, (point['PointId'],))

                    current_status = check_cursor.fetchone()
                    check_cursor.close()

                    if current_status:
                        handling, expiry_time = current_status
                        # 只有当点位真的未被处理或处理已过期时才更新为warning
                        if not handling or (
                                handling in ['resolved', 'ignore'] and expiry_time and expiry_time < datetime.now()):
                            update_alarm_status(point['PointId'], 'warning')
                except Exception as e:
                    print(f"检查或更新报警状态失败: {e}")

                # 检查是否需要添加到新报警列表
                try:
                    # 先检查是否已存在未通知的记录
                    cursor.execute("""
                        SELECT id FROM js.alarm_notification 
                        WHERE point_id = %s AND notified = 0
                    """, (point['id'],))

                    not_notified = cursor.fetchone() is None

                    if not_notified:
                        # 首次检测到报警，增加月度计数
                        try:
                            increment_alarm_count(point['PointId'])
                        except Exception as e:
                            print(f"增加报警计数失败: {e}")
                            
                        # 构建新报警通知
                        abnormal_message = get_abnormal_phenomenon(point)
                        new_alarms.append({
                            'id': point['id'],
                            'name': point['name'],
                            'value': point['value'],
                            'unit': point['unit'],
                            'normalRange': point['normalRange'],
                            'abnormalMessage': abnormal_message
                        })

                        # 记录到通知表
                        try:
                            cursor.execute("""
                                INSERT INTO js.alarm_notification (point_id, notified, create_time)
                                VALUES (%s, 0, NOW())
                                ON DUPLICATE KEY UPDATE notified = 0, create_time = NOW()
                            """, (point['id'],))

                            mysql.connection.commit()
                        except Exception as e:
                            mysql.connection.rollback()
                except Exception as e:
                    pass

            points.append(point)

        cursor.close()

        # 转换统计数据为前端需要的格式
        type_stats_list = [
            {'type': 'device', 'count': alarm_type_stats_local['device']},
            {'type': 'craft', 'count': alarm_type_stats_local['craft']}
        ]

        status_stats_list = [
            {'status': '待处理', 'count': status_stats['pending']},
            {'status': '已处理', 'count': status_stats['handled']}
        ]

        return jsonify({
            'success': True,
            'data': points,
            'new_alarms': new_alarms,
            'type_stats': type_stats_list,
            'status_stats': status_stats_list
        })

    except Exception as e:
        print(f"获取监控点位数据失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# 检查报警状态
def check_alarm_status(point):
    try:
        # 先检查handling状态
        handling = point.get('handling')
        if handling == 'resolved' or handling == 'ignore':
            return 'normal'

        if point['value'] is None or point['value'] == '':
            return 'normal'

        # 转换为数值
        numericValue = float(point['value']) if isinstance(point['value'], str) else point['value']

        if numericValue is None or math.isnan(numericValue):
            return 'normal'

        # 检查值是否在正常范围内
        normalRange = point['normalRange']
        if numericValue < normalRange[0] or numericValue > normalRange[1]:
            # 检测到异常值，进行延迟验证
            if handling != 'resolved' and handling != 'ignore' and handling != 'repair':
                # 检查延迟验证状态，但前端仍然显示normal
                verification_status = check_delayed_alarm_verification(point)
                # 无论验证状态如何，前端都显示normal，直到验证通过
                return 'normal' if verification_status == 'pending' else verification_status
            else:
                return 'normal'
        
        # 如果值恢复正常，清除延迟验证记录
        clear_delayed_alarm_verification(point['PointId'])
        return 'normal'
        
    except Exception as e:
        return 'normal'

def check_delayed_alarm_verification(point):
    """检查延迟报警验证状态"""
    try:
        cursor = mysql.connection.cursor()
        
        # 检查是否已有延迟验证记录
        cursor.execute("""
            SELECT first_detected_time, verification_count, is_verified
            FROM js.delayed_alarm_verification 
            WHERE point_id = %s
        """, (point['PointId'],))
        
        record = cursor.fetchone()
        current_time = datetime.now()
        
        if record:
            first_detected_time, verification_count, is_verified = record
            
            # 如果已经验证通过，直接返回alarm
            if is_verified:
                return 'alarm'
            
            # 检查是否已经过了5秒
            time_diff = (current_time - first_detected_time).total_seconds()
            
            if time_diff >= 5:
                # 超过5秒，标记为已验证
                cursor.execute("""
                    UPDATE js.delayed_alarm_verification 
                    SET is_verified = 1, last_checked_time = NOW()
                    WHERE point_id = %s
                """, (point['PointId'],))
                
                # 创建报警通知
                cursor.execute("""
                    INSERT INTO js.alarm_notification (point_id, notified, create_time)
                    VALUES (%s, 0, NOW())
                    ON DUPLICATE KEY UPDATE notified = 0, create_time = NOW()
                """, (point['id'],))
                
                mysql.connection.commit()
                cursor.close()
                return 'alarm'
            else:
                # 未超过5秒，更新检查次数和时间
                cursor.execute("""
                    UPDATE js.delayed_alarm_verification 
                    SET verification_count = verification_count + 1, 
                        last_checked_time = NOW()
                    WHERE point_id = %s
                """, (point['PointId'],))
                mysql.connection.commit()
                cursor.close()
                return 'pending'  # 内部状态：等待验证
        else:
            # 首次检测到异常，创建延迟验证记录
            cursor.execute("""
                INSERT INTO js.delayed_alarm_verification 
                (point_id, first_detected_time, last_checked_time, verification_count)
                VALUES (%s, NOW(), NOW(), 1)
            """, (point['PointId'],))
            mysql.connection.commit()
            cursor.close()
            return 'pending'  # 内部状态：等待验证
            
    except Exception as e:
        print(f"延迟报警验证检查失败: {e}")
        return 'normal'

def clear_delayed_alarm_verification(point_id):
    """清除延迟验证记录"""
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            DELETE FROM js.delayed_alarm_verification 
            WHERE point_id = %s
        """, (point_id,))
        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        print(f"清除延迟验证记录失败: {e}")

# 获取异常现象描述
def get_abnormal_phenomenon(point):
    if not point:
        return ''

    try:
        # 确保point['value']是数值类型
        try:
            value = float(point['value']) if isinstance(point['value'], str) and point['value'] else 0
        except (ValueError, TypeError):
            # 如果无法转换为数值，则使用默认值0
            value = 0

        # 确保normalRange是列表类型
        normalRange = point.get('normalRange', [0, 100])
        if not isinstance(normalRange, list) or len(normalRange) != 2:
            # 尝试解析字符串格式的范围
            if isinstance(normalRange, str) and normalRange.strip():
                try:
                    range_str = normalRange.strip('[]').split(',')
                    if len(range_str) == 2:
                        normalRange = [float(range_str[0]), float(range_str[1])]
                    else:
                        normalRange = [0, 100]
                except:
                    normalRange = [0, 100]
            else:
                normalRange = [0, 100]

        # 生成异常描述
        if value > normalRange[1]:
            return f"{point['name']}数值过高，当前值({value}{point.get('unit', '')})超过正常范围上限({normalRange[1]}{point.get('unit', '')})"
        elif value < normalRange[0]:
            return f"{point['name']}数值过低，当前值({value}{point.get('unit', '')})低于正常范围下限({normalRange[0]}{point.get('unit', '')})"

        return ''
    except Exception as e:
        print(f"生成异常现象描述失败: {e}")
        return ''


# 添加新接口：获取需要语音播报的报警
@app.route('/get_alarm_notifications', methods=['GET'])
def get_alarm_notifications():
    """获取未通知的报警消息"""
    try:
        cursor = mysql.connection.cursor()

        # 查询未通知的报警
        cursor.execute("""
            SELECT an.id, an.point_id, a.namee as point_name, a.valuee as point_value, a.unit
            FROM js.alarm_notification an
            JOIN js.alarm a ON an.point_id = a.id
            WHERE an.notified = 0
            LIMIT 10
        """)

        notifications = []
        for row in cursor.fetchall():
            notification_id = row[0]
            point_id = row[1]
            point_name = row[2]
            point_value = row[3]
            unit = row[4]

            # 获取点位信息
            cursor.execute("""
                SELECT normalRange FROM js.alarm WHERE id = %s
            """, (point_id,))

            point_info = cursor.fetchone()
            normal_range = [0, 100]  # 默认范围

            if point_info and point_info[0]:
                try:
                    range_str = point_info[0].strip('[]').split(',')
                    if len(range_str) == 2:
                        normal_range = [float(range_str[0]), float(range_str[1])]
                except Exception as e:
                    print(f"解析正常范围出错: {e}")

            # 构建异常现象消息
            try:
                message = ""
                if point_value is not None:
                    try:
                        value = float(point_value)
                        if value > normal_range[1]:
                            message = f"{point_name}数值过高，当前值({value}{unit})超过正常范围上限({normal_range[1]}{unit})"
                        elif value < normal_range[0]:
                            message = f"{point_name}数值过低，当前值({value}{unit})低于正常范围下限({normal_range[0]}{unit})"
                    except (ValueError, TypeError) as e:
                        print(f"处理点位值出错: {e}")

                if message:
                    notifications.append({
                        'id': notification_id,
                        'point_id': point_id,
                        'message': message
                    })
            except Exception as e:
                print(f"构建通知消息出错: {e}")

        # 不标记为已通知，等待前端主动调用标记API

        cursor.close()

        return jsonify({
            'success': True,
            'notifications': notifications
        })

    except Exception as e:
        print(f"获取报警通知失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# 确认已创建报警通知表
def init_alarm_notification_table():
    """初始化报警通知表"""
    try:
        cursor = mysql.connection.cursor()

        # 创建报警通知表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS js.alarm_notification (
                id INT AUTO_INCREMENT PRIMARY KEY,
                point_id VARCHAR(50) NOT NULL,
                notified TINYINT(1) DEFAULT 0,
                create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                notify_time DATETIME NULL,
                UNIQUE KEY (point_id)
            )
        """)

        mysql.connection.commit()
        cursor.close()
        # print("成功初始化报警通知表")
    except Exception as e:
        # 记录错误但继续运行
        # print(f"初始化报警通知表失败: {e}")
        pass


# 启动时初始化表
init_alarm_notification_table()

@app.route('/update_alarm_handling', methods=['POST'])
def update_alarm_handling():
    """更新报警点位的处理状态"""
    max_retries = 3
    retry_count = 0
    
    # 添加详细的请求日志
    data = request.get_json()
    point_id = data.get('point_id')  # 这里仍然接收前端的point_id参数
    handling = data.get('handling')

    while retry_count < max_retries:
        try:
            # 移除全局变量声明
            
            if not point_id or not handling:
                return jsonify({
                    'success': False,
                    'error': 'Missing required parameters'
                }), 400

            cursor = mysql.connection.cursor()
            
            # 修改为使用PointId字段查询
            cursor.execute("""
                SELECT id, PointId, namee, handling 
                FROM js.alarm 
                WHERE PointId = %s
            """, (point_id,))
            
            point_exists = cursor.fetchone()
            if not point_exists:
                cursor.close()
                return jsonify({
                    'success': False,
                    'error': f"Point '{point_id}' not found in database"
                }), 404
                
            # 将id保存为变量，用于后续使用
            db_id = point_exists[0]

            # 移除对全局alarm_type_stats的更新代码
            if handling == 'warning':
                # 获取当前年月
                current_date = datetime.now()
                year_month = current_date.strftime('%Y-%m')

            # 更新alarm表中的handling字段，使用id字段作为条件
            cursor.execute("""
                UPDATE js.alarm 
                SET handling = %s 
                WHERE id = %s
            """, (handling, db_id))
            
            # 检查影响的行数
            affected_rows = cursor.rowcount
            
            if affected_rows == 0:
                # 检查数据库中当前的处理状态
                cursor.execute("""
                    SELECT handling FROM js.alarm WHERE id = %s
                """, (db_id,))
                current_status = cursor.fetchone()
                
                # 尝试强制更新
                if handling in ['resolved', 'ignore', 'repair']:
                    cursor.execute("""
                        UPDATE js.alarm 
                        SET handling = %s 
                        WHERE id = %s
                    """, (handling, db_id))
                    affected_rows = cursor.rowcount
            
            # 如果是处理或忽略报警，清除相关的报警通知
            if handling in ['resolved', 'ignore', 'repair']:
                try:
                    # 清除报警通知记录
                    cursor.execute("""
                        DELETE FROM js.alarm_notification 
                        WHERE point_id = %s
                    """, (db_id,))
                except Exception as e:
                    print(f"清除报警通知失败: {e}")
            
            # 提交事务
            mysql.connection.commit()
            cursor.close()

            return jsonify({
                'success': True,
                'message': f'Successfully updated handling status to {handling}',
                'debug': {
                    'point_id': point_id,
                    'handling': handling,
                    'affected_rows': affected_rows
                }
            })

        except Exception as e:
            mysql.connection.rollback()

            # 检查是否是死锁错误
            if "Deadlock found" in str(e) and retry_count < max_retries - 1:
                retry_count += 1
                time_module.sleep(0.5)  # 短暂延迟后重试
            else:
                return jsonify({
                    'success': False,
                    'error': str(e),
                    'debug': {
                        'point_id': point_id,
                        'handling': handling, 
                        'retry_count': retry_count
                    }
                }), 500

    # 如果所有重试都失败
    return jsonify({
        'success': False,
        'error': '更新报警状态失败，请稍后重试',
        'debug': {
            'point_id': point_id,
            'handling': handling,
            'max_retries': max_retries
        }
    }), 500

@app.route('/stop_alarm_count/<point_id>', methods=['POST'])
def stop_alarm_count(point_id):
    """停止报警计数，将指定点位标记为已处理"""
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            data = request.get_json()
            action = data.get('action', 'resolved')  # 默认为已解决
            expiry_time = data.get('expiry_time', None)

            # 如果没有提供过期时间，根据action类型设置默认过期时间
            if not expiry_time:
                now = datetime.now()
                if action == 'repair':
                    # 检修状态设置为1天后过期
                    expiry_time = now + timedelta(days=1)
                else:
                    # 其他状态设置为2小时后过期
                    expiry_time = now + timedelta(hours=2)
                expiry_time = expiry_time.timestamp() * 1000  # 转换为毫秒时间戳

            cursor = mysql.connection.cursor()
            
            # 先通过PointId查找数据库id
            cursor.execute("""
                SELECT id, PointId, namee, handling 
                FROM js.alarm 
                WHERE PointId = %s
            """, (point_id,))
            
            point_exists = cursor.fetchone()
            if not point_exists:
                cursor.close()
                return jsonify({
                    'success': False,
                    'error': f"Point '{point_id}' not found in database"
                }), 404
                
            # 获取数据库id
            db_id = point_exists[0]
            
            # 根据操作类型更新状态
            if action == 'resolved':
                status = '已处理'
            elif action == 'repair':
                status = '检修中'
            else:
                status = '已忽略'

            # 更新alarm表中的处理状态，使用id字段
            cursor.execute("""
                UPDATE js.alarm 
                SET handling = %s 
                WHERE id = %s
            """, (action, db_id))
            
            affected_rows = cursor.rowcount

            # 将点位添加到忽略表中，使用id字段
            expiry_datetime = datetime.fromtimestamp(expiry_time / 1000)

            cursor.execute("""
                INSERT INTO js.ignored_alarms (point_id, expiry_time, create_time)
                VALUES (%s, %s, NOW())
                ON DUPLICATE KEY UPDATE expiry_time = %s, create_time = NOW()
            """, (db_id, expiry_datetime, expiry_datetime))

            # 清除报警通知记录
            try:
                cursor.execute("""
                    DELETE FROM js.alarm_notification 
                    WHERE point_id = %s
                """, (db_id,))
            except Exception as e:
                print(f"清除报警通知失败: {e}")

            mysql.connection.commit()
            cursor.close()

            return jsonify({
                'success': True,
                'message': f'Successfully updated alarm status to {status}'
            })

        except Exception as e:
            mysql.connection.rollback()

            # 检查是否是死锁错误
            if "Deadlock found" in str(e) and retry_count < max_retries - 1:
                retry_count += 1
                time_module.sleep(0.5)  # 短暂延迟后重试
            else:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500

    # 如果所有重试都失败
    return jsonify({
        'success': False,
        'error': '停止报警计数失败，请稍后重试'
    }), 500


# 添加新的API端点用于标记通知为已通知
@app.route('/mark_notification_notified', methods=['POST'])
def mark_notification_notified():
    """标记点位的通知为已通知状态，避免重复通知"""
    try:
        data = request.get_json()
        point_id = data.get('point_id')

        if not point_id:
            return jsonify({
                'success': False,
                'error': '缺少必要参数'
            }), 400

        cursor = mysql.connection.cursor()
        
        # 先通过PointId查找数据库id
        cursor.execute("""
            SELECT id FROM js.alarm WHERE PointId = %s
        """, (point_id,))
        
        point_exists = cursor.fetchone()
        if not point_exists:
            cursor.close()
            return jsonify({
                'success': False,
                'error': f"Point '{point_id}' not found in database"
            }), 404
            
        # 获取数据库id
        db_id = point_exists[0]

        # 标记指定点位的通知为已通知，使用id字段
        cursor.execute("""
            UPDATE js.alarm_notification
            SET notified = 1, notify_time = NOW()
            WHERE point_id = %s
        """, (db_id,))

        affected_rows = cursor.rowcount
        mysql.connection.commit()
        cursor.close()

        return jsonify({
            'success': True,
            'message': f'成功标记点位{point_id}的通知为已通知状态',
            'affected_rows': affected_rows
        })

    except Exception as e:
        mysql.connection.rollback()
        print(f"标记通知状态失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route("/check_maintenance_status", methods=["GET"])
def check_maintenance_status():
    """API 路由: 检查系统是否处于检修状态，通过检测关键点位是否同时为0来判断"""
    try:
        # 需要检查的点位列表
        point_ids = [
            "YLY_DCS_S11_5A_A",
            "YLY_DCS_S11_5B_A",
            "YLY_DCS_S11_5C_A",
            "YLY_DCS_P201_A",
            "YLY_DCS_P202_A",
            "YLY_DCS_P203_A",
            "YLY_DCS_P204_A",
            "YLY_DCS_P205_A"
        ]

        # 用于存储点位的值
        point_values = {}

        # 获取所有点位的最新值
        for point_id in point_ids:
            value = get_latest_value(point_id)
            point_values[point_id] = value

        # 检查是否所有点位都为0
        all_zero = all(value == 0 for value in point_values.values())

        # 获取手动设置的检修状态
        maintenance_status = False
        try:
            with open("maintenance_status.json", "r") as f:
                status_data = json.load(f)
                maintenance_status = status_data.get("enabled", False)
        except (FileNotFoundError, json.JSONDecodeError):
            # 如果文件不存在或JSON解析错误，则创建新文件
            with open("maintenance_status.json", "w") as f:
                json.dump({"enabled": False}, f)

        # 如果手动开启检修或所有点位都为0，则认为系统处于检修状态
        is_maintenance = maintenance_status or all_zero

        return jsonify({
            "success": True,
            "is_maintenance": is_maintenance,
            "auto_detected": all_zero,
            "manual_enabled": maintenance_status,
            "point_values": point_values
        })
    except Exception as e:
        logger.error(f"检查系统检修状态失败: {e}")
        return jsonify({
            "success": False,
            "message": f"检查系统检修状态失败: {str(e)}"
        }), 500


@app.route("/toggle_maintenance_mode", methods=["POST"])
def toggle_maintenance_mode():
    """API 路由: 切换手动检修模式的状态"""
    try:
        data = request.get_json(force=True)
        enabled = data.get("enabled", False)

        # 保存状态到文件
        with open("maintenance_status.json", "w") as f:
            json.dump({"enabled": enabled}, f)

        return jsonify({
            "success": True,
            "enabled": enabled
        })
    except Exception as e:
        logger.error(f"切换检修模式失败: {e}")
        return jsonify({
            "success": False,
            "message": f"切换检修模式失败: {str(e)}"
        }), 500


# 添加一个定时更新函数
def scheduled_update():
    """
    定时更新函数，在后台运行并每5分钟更新一次数据
    """
    while True:
        try:
            if should_update_data():
                print(f"定时更新触发，当前时间：{datetime.now()}")
                # 更新所有数据
                get_today_chanliang('output', return_from_last=False)
                get_month_chanliang('output', return_from_last=False)
                get_year_chanliang('output', return_from_last=False)
                get_today_dianhao('threehand', return_from_last=False)
                get_month_dianhao('threehand', return_from_last=False)
                get_year_dianhao('threehand', return_from_last=False)
                get_today_qihao('output', return_from_last=False)
                get_month_qihao('output', return_from_last=False)
                get_year_qihao('output', return_from_last=False)
                get_today_luhao('output', return_from_last=False)
                get_month_luhao('output', return_from_last=False)
                get_year_luhao('output', return_from_last=False)
                print("数据更新完成")

        except Exception as e:
            print(f"定时更新出错：{str(e)}")

        # 每30秒检查一次是否需要更新
        time.sleep(30)


# 在应用启动时启动定时任务
def start_scheduled_update():
    """
    启动定时更新任务
    """
    update_thread = Thread(target=scheduled_update, daemon=True)
    update_thread.start()

@app.route('/gylc_normalrange', methods=['GET'])
def get_gylc_normalrange():
    """从MySQL数据库的js.alarm表中获取所有点位的阈值范围"""
    try:
        cursor = mysql.connection.cursor()
        
        # 查询alarm表中的所有点位阈值数据
        cursor.execute("""
            SELECT 
                PointId,
                normalRange,
                namee
            FROM js.alarm
        """)
        
        # 获取结果
        results = cursor.fetchall()
        cursor.close()
        
        # 将结果转换为字典格式
        thresholds = {}
        for row in results:
            point_id, normal_range, name = row
            
            # 检查point_id是否为空
            if point_id is None:
                continue
                
            # 处理name字段的空值
            if not name or (isinstance(name, str) and not name.strip()):
                name = f"点位_{point_id}"
            
            # 处理normalRange字段，转换为min和max
            try:
                if not normal_range or (isinstance(normal_range, str) and not normal_range.strip()):
                    min_threshold = 0
                    max_threshold = 100
                elif isinstance(normal_range, str):
                    range_str = normal_range.strip('[]').split(',')
                    if len(range_str) == 2:
                        min_threshold = float(range_str[0])
                        max_threshold = float(range_str[1])
                    else:
                        min_threshold = 0
                        max_threshold = 100
                else:
                    min_threshold = 0
                    max_threshold = 100
            except Exception as e:
                print(f"解析阈值范围失败，点位ID: {point_id}, 值: {normal_range}, 错误: {e}")
                min_threshold = 0
                max_threshold = 100
            
            thresholds[point_id] = {
                'name': name,
                'minThreshold': min_threshold,
                'maxThreshold': max_threshold
            }
        
        return jsonify({
            'success': True,
            'data': thresholds
        })
    except Exception as e:
        print(f"获取阈值数据失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/check_point_exists/<point_id>', methods=['GET'])
def check_point_exists(point_id):
    """检查点位是否存在以及其详细信息"""
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT id, PointId, namee, handling, valuee, unit, normalRange 
            FROM js.alarm 
            WHERE id = %s
        """, (point_id,))
        
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            # 转换结果为字典
            columns = ['id', 'PointId', 'name', 'handling', 'value', 'unit', 'normalRange']
            point_data = dict(zip(columns, result))
            
            return jsonify({
                'success': True,
                'point_exists': True,
                'point_data': point_data
            })
        else:
            # 尝试模糊查询
            cursor = mysql.connection.cursor()
            cursor.execute("""
                SELECT id, PointId, namee 
                FROM js.alarm 
                WHERE id LIKE %s OR PointId LIKE %s OR namee LIKE %s
                LIMIT 5
            """, (f'%{point_id}%', f'%{point_id}%', f'%{point_id}%'))
            
            similar_points = []
            for row in cursor.fetchall():
                similar_points.append({
                    'id': row[0],
                    'PointId': row[1],
                    'name': row[2]
                })
            
            cursor.close()
            
            return jsonify({
                'success': True,
                'point_exists': False,
                'similar_points': similar_points
            })
    except Exception as e:
        print(f"检查点位存在时出错: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# 获取系统启动时间
@app.route('/api/start_date', methods=['GET'])
def get_start_date():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT start_date FROM js.system_runtime ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return jsonify({
                'success': True,
                'start_date': result[0].strftime('%Y-%m-%d')
            })
        return jsonify({
            'success': False,
            'error': '未找到系统启动时间'
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# 获取运行时间信息
@app.route('/api/runtime_info', methods=['GET'])
def get_runtime_info():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT start_date, last_update, total_seconds, current_seconds 
            FROM js.system_runtime 
            ORDER BY id DESC LIMIT 1
        """)
        runtime = cursor.fetchone()
        
        if not runtime:
            return jsonify({
                'success': False,
                'error': '未找到运行时间记录'
            }), 404
            
        start_date, last_update, total_seconds, current_seconds = runtime
        now = datetime.now()
        time_diff = (now - last_update).total_seconds()
        
        new_total_seconds = total_seconds + time_diff
        new_current_seconds = current_seconds + time_diff
        
        cursor.execute("""
            UPDATE js.system_runtime 
            SET last_update = %s, total_seconds = %s, current_seconds = %s 
            WHERE id = (SELECT id FROM (SELECT id FROM js.system_runtime ORDER BY id DESC LIMIT 1) as t)
        """, (now, new_total_seconds, new_current_seconds))
        
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({
            'success': True,
            'total_seconds': int(new_total_seconds),
            'current_seconds': int(new_current_seconds)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/update_start_date', methods=['POST'])
def update_start_date():
    """API 路由: 更新系统启动时间"""
    try:
        new_date = request.json.get('start_date')
        if not new_date:
            return jsonify({
                'success': False,
                'error': '未提供启动时间'
            }), 400

        cursor = mysql.connection.cursor()
        # 更新system_runtime表中的start_date
        cursor.execute("""
            UPDATE js.system_runtime 
            SET start_date = %s,
                last_update = NOW(),
                total_seconds = 0,
                current_seconds = 0
            WHERE id = (SELECT id FROM (SELECT id FROM js.system_runtime ORDER BY id DESC LIMIT 1) as t)
        """, (new_date,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({
            'success': True,
            'message': '启动时间更新成功'
        })

    except Exception as e:
        mysql.connection.rollback()
        print(f"更新启动时间失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/dian_data', methods=['GET'])
def get_dian_data():
    try:
        date = request.args.get('date')
        if not date:
            return jsonify({'error': '请提供日期参数'}), 400
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 构建日期范围
        start_date = f"{date} 00:00:00"
        end_date = f"{date} 23:59:59"
        
        # 修改查询逻辑，确保每个数据点只被计算一次
        query = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE 
                    WHEN aValue >= 24 AND aValue <= 26 THEN 1 
                    ELSE 0 
                END) as excellent,
                SUM(CASE 
                    WHEN aValue >= 23 AND aValue <= 28 
                    AND NOT (aValue >= 24 AND aValue <= 26) THEN 1 
                    ELSE 0 
                END) as good,
                SUM(CASE 
                    WHEN aValue >= 20 AND aValue <= 31 
                    AND NOT (aValue >= 23 AND aValue <= 28) THEN 1 
                    ELSE 0 
                END) as qualified,
                SUM(CASE 
                    WHEN aValue < 20 OR aValue > 31 THEN 1 
                    ELSE 0 
                END) as unqualified
            FROM js.dian_mysql
            WHERE tS BETWEEN %s AND %s
            AND aValue > 0
        """
        
        cursor.execute(query, (start_date, end_date))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            return jsonify({
                'date': date,
                'total': result[0],
                'excellent': result[1],
                'good': result[2],
                'qualified': result[3],
                'unqualified': result[4]
            })
        else:
            return jsonify({
                'date': date,
                'total': 0,
                'excellent': 0,
                'good': 0,
                'qualified': 0,
                'unqualified': 0
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/update_current_runtime', methods=['POST'])
def update_current_runtime():
    """API 路由: 更新本周期运行时间"""
    try:
        current_seconds = request.json.get('current_seconds')
        if current_seconds is None:
            return jsonify({
                'success': False,
                'error': '未提供运行时间'
            }), 400

        cursor = mysql.connection.cursor()
        # 更新system_runtime表中的current_seconds
        cursor.execute("""
            UPDATE js.system_runtime 
            SET current_seconds = %s,
                last_update = NOW()
            WHERE id = (SELECT id FROM (SELECT id FROM js.system_runtime ORDER BY id DESC LIMIT 1) as t)
        """, (current_seconds,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({
            'success': True,
            'message': '本周期运行时间更新成功'
        })

    except Exception as e:
        mysql.connection.rollback()
        print(f"更新本周期运行时间失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/update_total_runtime', methods=['POST'])
def update_total_runtime():
    """API 路由: 更新累计运行时间"""
    try:
        total_seconds = request.json.get('total_seconds')
        if total_seconds is None:
            return jsonify({
                'success': False,
                'error': '未提供运行时间'
            }), 400

        cursor = mysql.connection.cursor()
        # 更新system_runtime表中的total_seconds
        cursor.execute("""
            UPDATE js.system_runtime 
            SET total_seconds = %s,
                last_update = NOW()
            WHERE id = (SELECT id FROM (SELECT id FROM js.system_runtime ORDER BY id DESC LIMIT 1) as t)
        """, (total_seconds,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({
            'success': True,
            'message': '累计运行时间更新成功'
        })

    except Exception as e:
        mysql.connection.rollback()
        print(f"更新累计运行时间失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ratio', methods=['POST'])
def save_ratio():
    """API 路由: 存储校正后的比率"""
    try:
        data = request.get_json()
        if not data or 'ratio' not in data:
            return jsonify({'success': False, 'error': '未提供比率'}), 400

        ratio = data['ratio']

        cursor = mysql.connection.cursor()
        # 将比率存储到js.dian_ratio表中
        cursor.execute("""
            INSERT INTO js.dian_ratio (inputTime, ratio) 
            VALUES (NOW(), %s)
        """, (ratio,))

        mysql.connection.commit()
        cursor.close()

        return jsonify({
            'success': True,
            'message': '比率存储成功',
        })

    except Exception as e:
        mysql.connection.rollback()
        print(f"存储比率失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def _auto_calculate_and_save_ratio():
    """
    后台任务：计算当天 01:00-07:00 的人工/机器测碘均值并自动写入比率
    """
    conn = None
    try:
        # 使用连接池获取连接（后台线程中不能用 Flask 的 mysql.connection）
        conn = pool.connection()
        cursor = conn.cursor()
        
        today = datetime.now().date()
        start_dt = datetime.combine(today, dt_time(hour=1, minute=0))
        end_dt = datetime.combine(today, dt_time(hour=7, minute=0))
        start_str = start_dt.strftime('%Y-%m-%d %H:%M:%S')
        end_str = end_dt.strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("""
            SELECT dianhanliang,
                   dianhan_mysql,
                   CONCAT(biaoDate, ' ', biaoTime, ':00') AS measure_time
            FROM js.dianhan
            WHERE CONCAT(biaoDate, ' ', biaoTime, ':00') BETWEEN %s AND %s
            ORDER BY CONCAT(biaoDate, ' ', biaoTime, ':00') ASC
        """, (start_str, end_str))
        rows = cursor.fetchall()

        if not rows:
            print("自动校正：未找到当天 01:00-07:00 的测碘数据，跳过写入。")
            cursor.close()
            if conn:
                conn.close()
            return

        manual_values = []
        machine_values = []

        for manual_raw, machine_raw, _ in rows:
            manual_value = _safe_float(manual_raw)
            if manual_value is not None:
                manual_values.append(manual_value)

            machine_value = _safe_float(machine_raw)
            if machine_value is not None:
                machine_values.append(machine_value)

        if len(manual_values) < 3 or len(machine_values) < 3:
            print("自动校正：有效人工/机器测碘数据少于 3 条，跳过写入。")
            cursor.close()
            if conn:
                conn.close()
            return

        manual_avg = _trimmed_mean(manual_values)
        machine_avg = _trimmed_mean(machine_values)

        if machine_avg is None or machine_avg == 0:
            print("自动校正：机器测碘均值无效，无法计算比率，跳过写入。")
            cursor.close()
            if conn:
                conn.close()
            return

        ratio = round(manual_avg / machine_avg, 2)

        cursor.execute("""
            INSERT INTO js.dian_ratio (inputTime, ratio)
            VALUES (NOW(), %s)
        """, (ratio,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"自动校正：已自动写入比率 {ratio}。")

    except Exception as e:
        try:
            if conn:
                conn.rollback()
                conn.close()
        except Exception:
            pass
        print(f"自动校正：计算或写入比率失败：{e}")


def _daily_ratio_scheduler():
    """
    每天 07:30 触发一次自动计算并写入比率
    """
    while True:
        now = datetime.now()
        target = now.replace(hour=7, minute=30, second=0, microsecond=0)
        if now >= target:
            # 今天已经过了 7:30，则等到明天 7:30
            target = target + timedelta(days=1)
        sleep_seconds = (target - now).total_seconds()
        print(f"自动校正调度器：下次执行时间为 {target.strftime('%Y-%m-%d %H:%M:%S')}，等待 {sleep_seconds:.0f} 秒")
        time.sleep(sleep_seconds)
        _auto_calculate_and_save_ratio()


def _safe_float(value):
    """将值安全转换为 float，非数字返回 None"""
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    value_str = str(value).strip()
    if not value_str:
        return None

    try:
        return float(value_str)
    except (TypeError, ValueError):
        return None


def _trimmed_mean(values):
    """去掉最大最小值后的均值"""
    if not values:
        return None

    if len(values) <= 2:
        return sum(values) / len(values)

    ordered = sorted(values)
    trimmed = ordered[1:-1]
    return sum(trimmed) / len(trimmed) if trimmed else None


@app.route('/api/ratio/preview', methods=['GET'])
def get_ratio_preview():
    """API 路由: 获取用于校正预览的数据"""
    try:
        cursor = mysql.connection.cursor()
        today = datetime.now().date()
        start_dt = datetime.combine(today, dt_time(hour=1, minute=0))
        end_dt = datetime.combine(today, dt_time(hour=7, minute=0))
        start_str = start_dt.strftime('%Y-%m-%d %H:%M:%S')
        end_str = end_dt.strftime('%Y-%m-%d %H:%M:%S')

        # 获取当天 01:00-07:00 的人工与机器测碘值
        cursor.execute("""
            SELECT dianhanliang,
                   dianhan_mysql,
                   CONCAT(biaoDate, ' ', biaoTime, ':00') AS measure_time
            FROM js.dianhan
            WHERE CONCAT(biaoDate, ' ', biaoTime, ':00') BETWEEN %s AND %s
            ORDER BY CONCAT(biaoDate, ' ', biaoTime, ':00') ASC
        """, (start_str, end_str))
        rows = cursor.fetchall()
        cursor.close()

        if not rows:
            return jsonify({
                'success': False,
                'error': '未找到足够的相关值进行计算，将使用上一次测得的校正系数'
            }), 404

        manual_values = []
        machine_values = []

        for manual_raw, machine_raw, _ in rows:
            manual_value = _safe_float(manual_raw)
            if manual_value is not None:
                manual_values.append(manual_value)

            machine_value = _safe_float(machine_raw)
            if machine_value is not None:
                machine_values.append(machine_value)

        if len(manual_values) < 3 or len(machine_values) < 3:
            return jsonify({
                'success': False,
                'error': '未找到足够的相关值进行计算，将使用上一次测得的校正系数'
            }), 400

        manual_avg = _trimmed_mean(manual_values)
        machine_avg = _trimmed_mean(machine_values)

        if machine_avg is None or machine_avg == 0:
            return jsonify({
                'success': False,
                'error': '机器测碘均值无效，无法计算校正系数'
            }), 400

        ratio = manual_avg / machine_avg

        return jsonify({
            'success': True,
            'data': {
                'manual_avg': round(manual_avg, 2),
                'machine_avg': round(machine_avg, 2),
                'ratio': round(ratio, 2),
                'manual_count': len(manual_values),
                'machine_count': len(machine_values),
                'time_range': {
                    'start': start_str,
                    'end': end_str
                }
            }
        })

    except Exception as e:
        print(f"获取校正预览数据失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ratio/latest', methods=['GET'])
def get_latest_ratio():
    """API 路由: 获取最新的碘含量比率"""
    try:
        cursor = mysql.connection.cursor()

        # 从js.dian_ratio表中获取最新的ratio值
        cursor.execute("""
            SELECT ratio 
            FROM js.dian_ratio 
            WHERE ratio IS NOT NULL
            ORDER BY inputTime DESC 
            LIMIT 1
        """)
        result = cursor.fetchone()

        cursor.close()

        if result:
            return jsonify({
                'success': True,
                'ratio': float(result[0]),
                'message': '成功获取最新比率'
            })
        else:
            return jsonify({
                'success': True,
                'ratio': 1.0,
                'message': '未找到比率数据，使用默认值1'
            })

    except Exception as e:
        print(f"获取最新比率失败: {e}")
        return jsonify({
            'success': False,
            'ratio': 1.0,
            'error': str(e)
        }), 500
@app.route('/api/dianye/latest', methods=['GET'])

@app.route('/api/history_data', methods=['POST'])
def get_history_data():
    """查询历史数据API接口"""
    try:
        data = request.get_json()
        point_id = data.get('point_id')
        date = data.get('date')  # 格式: YYYY-MM-DD
        interval = data.get('interval', 30)  # 时间间隔，单位：分钟

        if not point_id or not date:
            return jsonify({
                'success': False,
                'error': '缺少必要参数：point_id 和 date'
            })

        # 检查TDengine连接
        if not tdengine_conn:
            init_tdengine_connection()

        if not tdengine_conn:
            return jsonify({
                'success': False,
                'error': '数据库连接失败'
            })

        # 构建查询时间范围
        # 注意：TDengine存储的是UTC时间，但显示的是北京时间
        # 查询时需要将北京时间转换为UTC时间
        start_time = f"{date} 00:00:00"
        end_time = f"{date} 23:59:59"

        # 将北京时间转换为UTC时间（减去8小时）
        from datetime import datetime, timedelta
        start_dt = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end_dt = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

        # 转换为UTC时间
        start_utc = start_dt + timedelta(hours=8)
        end_utc = end_dt + timedelta(hours=8)

        start_utc_str = start_utc.strftime('%Y-%m-%d %H:%M:%S')
        end_utc_str = end_utc.strftime('%Y-%m-%d %H:%M:%S')

        # 构建查询SQL
        # 根据时间间隔进行数据采样
        if interval <= 5:
            # 5分钟以内，直接查询原始数据
            sql = f"""
            SELECT ts, fvalue
            FROM jinshen.{point_id}
            WHERE ts >= '{start_utc_str}' AND ts <= '{end_utc_str}'
            ORDER BY ts
            """
        else:
            # 大于5分钟，使用INTERVAL进行数据采样
            sql = f"""
            SELECT _wstart as ts, AVG(fvalue) as fvalue
            FROM jinshen.{point_id}
            WHERE ts >= '{start_utc_str}' AND ts <= '{end_utc_str}'
            INTERVAL({interval}m)
            ORDER BY ts
            """

        logger.info(f"查询历史数据SQL: {sql}")

        # 执行查询
        cursor = tdengine_conn.cursor()
        cursor.execute(sql)

        # 获取数据
        results = cursor.fetchall()
        cursor.close()

        # 处理查询结果
        data_list = []
        for row in results:
            if row and len(row) >= 2:
                data_list.append({
                    'tS': row[0].strftime('%Y-%m-%d %H:%M:%S') if row[0] else None,
                    'fvalue': float(row[1]) if row[1] is not None else 0
                })

        logger.info(f"查询到 {len(data_list)} 条历史数据")

        return jsonify({
            'success': True,
            'data': data_list,
            'count': len(data_list),
            'point_id': point_id,
            'date': date,
            'interval': interval
        })

    except Exception as e:
        # logger.error(f"查询历史数据失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'查询历史数据失败: {str(e)}'
        })

def get_latest_dianye():
    """API 路由: 获取最新的碘液含量"""
    try:
        cursor = mysql.connection.cursor()

        # 从 js.dianhan 表中获取最新的 dianye 字段值，按 id 倒序
        cursor.execute("""
            SELECT yanliang 
            FROM js.dianhan 
            WHERE yanliang IS NOT NULL AND yanliang != ''
            ORDER BY id DESC 
            LIMIT 1
        """)
        result = cursor.fetchone()

        cursor.close()

        if result:
            return jsonify({
                'success': True,
                'dianye': float(result[0]),
                'message': '成功获取最新碘液含量'
            })
        else:
            return jsonify({
                'success': True,
                'dianye': 0.0,
                'message': '未找到碘液数据，使用默认值0'
            })

    except Exception as e:
        print(f"获取最新碘液含量失败: {e}")
        return jsonify({
            'success': False,
            'dianye': 0.0,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    init_tdengine_connection()
    start_heartbeat()  # 启动心跳线程
    start_scheduled_update()  # 启动定时更新任务
    # 启动每日 07:30 自动计算并写入比率的任务
    Thread(target=_daily_ratio_scheduler, daemon=True).start()
    print(get_today_taoxi('output'))
    app.run(debug=False, host='0.0.0.0', port=9072)