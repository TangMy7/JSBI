import requests
import pymysql
import time
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# === TDengine 配置 ===
TDENGINE_URL = "http://10.10.10.130:6041/rest/sql"
AUTH_HEADER = "Basic cm9vdDp0YW9zZGF0YQ=="  # base64 for root:taosdata

# === MySQL 配置 ===
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "js",
    "port": 3306,
    "charset": "utf8mb4",
    "autocommit": True,
    "connect_timeout": 60,
    "read_timeout": 60,
    "write_timeout": 60
}

# 固定查询时间点（24小时制）
TARGET_HOURS = [0, 8, 16]


# 创建带重试机制的requests session
def create_requests_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


# 全局requests session
requests_session = create_requests_session()


# 获取 MySQL 连接
def get_mysql_connection():
    max_retries = 5
    retry_count = 0

    while retry_count < max_retries:
        try:
            conn = pymysql.connect(**MYSQL_CONFIG)
            # 测试连接是否有效
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            print("✅ MySQL连接成功")
            return conn
        except Exception as e:
            retry_count += 1
            print(f"❌ MySQL连接失败 (尝试 {retry_count}/{max_retries}): {e}")
            if retry_count < max_retries:
                time.sleep(5)
            else:
                print("❌ MySQL连接失败，已达到最大重试次数")
                raise


# 检查MySQL连接是否有效
def is_mysql_connection_valid(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return True
    except Exception:
        return False


# 查询 TDengine 指定时间点数据
def query_fvalue(table_name, target_time):
    ts_str = target_time.strftime("%Y-%m-%d %H:%M:%S")
    sql = f"SELECT ts, fvalue FROM jinshen.{table_name} WHERE ts = '{ts_str}' LIMIT 1"

    headers = {
        "Authorization": AUTH_HEADER,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests_session.post(
                TDENGINE_URL,
                data=sql.encode("utf-8"),
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict) and "data" in data and len(data["data"]) > 0:
                row = data["data"][0]
                return float(row[1]) if row[1] is not None else 0.0
            else:
                return 0.0
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"⚠️ TDengine 查询失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                time.sleep(2)
            else:
                print(f"❌ TDengine 查询最终失败: {e}")
                return 0.0
        except Exception as e:
            print(f"❌ TDengine 查询异常: {e}")
            return 0.0


# 获取上一行 MySQL 数据（如无则为 0）
def get_last_mysql_values(conn):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # 检查连接是否有效
            if not is_mysql_connection_valid(conn):
                print("⚠️ MySQL连接已断开，尝试重连...")
                conn = get_mysql_connection()

            with conn.cursor() as cursor:
                sql = "SELECT belt, iodine FROM dianhan_analyze ORDER BY inputTime DESC LIMIT 1"
                cursor.execute(sql)
                row = cursor.fetchone()
                if row:
                    # 统一保留两位小数，避免后续计算时产生细小浮点误差
                    belt = round(float(row[0] or 0), 2)
                    iodine = round(float(row[1] or 0), 2)
                    return belt, iodine
                else:
                    return 0.0, 0.0
        except pymysql.err.OperationalError as e:
            if attempt < max_retries - 1:
                print(f"⚠️ MySQL查询失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                try:
                    conn = get_mysql_connection()
                except:
                    time.sleep(2)
            else:
                print(f"❌ MySQL查询最终失败: {e}")
                return 0.0, 0.0
        except Exception as e:
            print(f"⚠️ 查询上一行数据失败: {e}")
            return 0.0, 0.0


# 根据当前小时计算 sub 字段
def get_sub_by_hour(hour):
    if hour == 0:
        return "16-24"
    elif hour == 8:
        return "0-8"
    elif hour == 16:
        return "8-16"
    else:
        return f"{hour - 1}-{hour}"


# 插入数据到 MySQL 表
def insert_into_mysql(conn, input_time, current_belt, current_iodine, sub):
    # 获取上一行数据用于计算dian_total差值
    last_belt, last_iodine = get_last_mysql_values(conn)

    # 统一保留两位小数，避免浮点数精度导致的 0.01 / -0.01 误差
    current_belt = round(float(current_belt or 0), 2)
    current_iodine = round(float(current_iodine or 0), 2)
    last_belt = round(float(last_belt or 0), 2)
    last_iodine = round(float(last_iodine or 0), 2)

    # 计算dian_total差值：(当前belt+iodine) - (上一行belt+iodine)
    current_total = round(current_belt + current_iodine, 2)
    last_total = round(last_belt + last_iodine, 2)
    dian_total = round(current_total - last_total, 2)

    max_retries = 3

    for attempt in range(max_retries):
        try:
            # 检查连接是否有效
            if not is_mysql_connection_valid(conn):
                print("⚠️ MySQL连接已断开，尝试重连...")
                conn = get_mysql_connection()

            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO dianhan_analyze (inputTime, belt, iodine, dian_total, sub)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        belt = VALUES(belt),
                        iodine = VALUES(iodine),
                        dian_total = VALUES(dian_total),
                        sub = VALUES(sub)
                """
                cursor.execute(sql, (input_time, current_belt, current_iodine, dian_total, sub))
                print(
                    f"✅ 写入 MySQL 成功：belt={current_belt}, iodine={current_iodine}, dian_total={dian_total}, sub='{sub}'")
                return True
        except pymysql.err.OperationalError as e:
            if attempt < max_retries - 1:
                print(f"⚠️ MySQL写入失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                try:
                    conn = get_mysql_connection()
                except:
                    time.sleep(2)
            else:
                print(f"❌ MySQL写入最终失败: {e}")
                return False
        except Exception as e:
            print(f"❌ 写入 MySQL 异常: {e}")
            return False

    return False


# 主循环
def main():
    last_run_time = None
    conn = None

    print("🚀 启动电耗数据采集服务...")

    while True:
        try:
            # 确保MySQL连接可用
            if conn is None or not is_mysql_connection_valid(conn):
                conn = get_mysql_connection()

            now = datetime.now()
            current_hour = now.hour
            current_minute = now.minute

            if current_hour in TARGET_HOURS and current_minute == 0:
                target_time = now.replace(minute=0, second=0, microsecond=0)
                if last_run_time != target_time:
                    print(f"\n⏰ 执行查询：{target_time.strftime('%Y-%m-%d %H:%M:%S')}")

                    try:
                        # 当前 TDengine 数据
                        current_belt = query_fvalue("cy_plc3_003", target_time)
                        current_iodine = query_fvalue("cy_plc3_006", target_time)

                        # 上一次 MySQL 数据（用于显示对比）
                        last_belt, last_iodine = get_last_mysql_values(conn)

                        print(f"📊 当前值: belt={current_belt}, iodine={current_iodine}")
                        print(f"📉 上一值: belt={last_belt}, iodine={last_iodine}")

                        # sub 字段
                        sub = get_sub_by_hour(current_hour)

                        # 写入 MySQL（直接写入当前值，dian_total在函数内部计算）
                        if insert_into_mysql(conn, target_time, current_belt, current_iodine, sub):
                            last_run_time = target_time
                        else:
                            print("⚠️ 数据写入失败，下次重试")

                    except Exception as e:
                        print(f"❌ 主循环异常: {e}")
                        # 重置连接
                        try:
                            if conn:
                                conn.close()
                        except:
                            pass
                        conn = None

            time.sleep(10)

        except KeyboardInterrupt:
            print("\n🛑 收到中断信号，正在退出...")
            break
        except Exception as e:
            print(f"❌ 主循环严重异常: {e}")
            time.sleep(30)  # 等待30秒后重试

    # 清理资源
    try:
        if conn:
            conn.close()
        requests_session.close()
    except:
        pass
    print("👋 服务已停止")


if __name__ == "__main__":
    main()
