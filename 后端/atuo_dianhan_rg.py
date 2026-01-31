import pymysql
import time
import threading
from datetime import datetime, timedelta

DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': '123456',
    'db': 'js',
    'charset': 'utf8'
}

# 严格定义的班次时间段
BANCI_SEGMENTS = [
    (0, 8, "夜班"),  # 夜班 0:00-8:00
    (8, 16, "早班"),  # 早班 8:00-16:00
    (16, 24, "中班"),  # 中班 16:00-24:00
]


def get_connection(retry=5, delay=2):
    for i in range(retry):
        try:
            return pymysql.connect(**DB_CONFIG)
        except Exception as e:
            print(f"{datetime.now()} 数据库连接失败，第{i + 1}次重试... 错误:{e}")
            time.sleep(delay)
    raise Exception("数据库多次重连失败！")


def get_current_banci():
    """获取当前时间对应的班次"""
    now = datetime.now()
    current_hour = now.hour
    for seg_start, seg_end, banci in BANCI_SEGMENTS:
        if seg_start <= current_hour < seg_end:
            return banci, seg_start, seg_end
    return "中班", 16, 24  # 默认返回中班


def generate_time_slots(start_time, end_hour):
    """生成从start_time开始到end_hour的半小时间隔时间列表"""
    slots = []
    current = datetime.strptime(start_time, "%H:%M")
    if end_hour == 24:
        end_time = current.replace(hour=0, minute=0) + timedelta(days=1)
    else:
        end_time = current.replace(hour=end_hour, minute=0)

    while current < end_time:
        slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=30)

    return slots


def get_modified_start_time(db, today, banci):
    """检测用户修改的起始时间"""
    cursor = db.cursor()
    # 查询该班次所有记录按时间排序
    cursor.execute(
        "SELECT biaoTime FROM dianhan WHERE biaoDate=%s AND banci=%s ORDER BY STR_TO_DATE(biaoTime, '%%H:%%i')",
        (today, banci)
    )
    times = [row[0] for row in cursor.fetchall()]

    # 如果没有记录，返回None表示需要全新生成
    if not times:
        return None

    # 计算理论上的标准时间序列
    _, seg_start, seg_end = get_banci_segment(banci)
    standard_start = f"{seg_start:02d}:00"
    standard_slots = generate_time_slots(standard_start, seg_end)

    # 比较实际记录和标准记录，找出第一个不同的时间点
    for actual, expected in zip(times, standard_slots):
        if actual != expected:
            return actual  # 返回用户修改的起始时间

    # 如果没有修改，返回标准起始时间
    return standard_start


def get_banci_segment(banci):
    """获取班次的时间段"""
    for seg_start, seg_end, name in BANCI_SEGMENTS:
        if name == banci:
            return name, seg_start, seg_end
    return "中班", 16, 24  # 默认返回中班


def auto_fill_dianhan_loop(sleep_seconds=2):
    """自动补齐电焊记录的主循环"""
    print(f"自动补齐进程启动，每隔{sleep_seconds}秒检测一次...")
    while True:
        try:
            db = get_connection()
            cursor = db.cursor()
            today = datetime.now().strftime("%Y-%m-%d")

            # 1. 获取当前班次信息
            current_banci, seg_start, seg_end = get_current_banci()
            #print(f"{datetime.now()} 当前班次: {current_banci} ({seg_start}:00-{seg_end}:00)")

            # 2. 检测用户是否修改了起始时间
            modified_start = get_modified_start_time(db, today, current_banci)

            # 3. 确定要使用的起始时间
            if modified_start:
                start_time = modified_start
                #print(f"检测到用户修改的起始时间: {start_time}")
            else:
                start_time = f"{seg_start:02d}:00"
                print(f"使用标准起始时间: {start_time}")

            # 4. 生成应该存在的时间槽
            expected_slots = generate_time_slots(start_time, seg_end)

            # 5. 查询实际存在的记录
            cursor.execute(
                "SELECT id, biaoTime FROM dianhan WHERE biaoDate=%s AND banci=%s ORDER BY STR_TO_DATE(biaoTime, '%%H:%%i')",
                (today, current_banci)
            )
            existing_records = {row[1]: row[0] for row in cursor.fetchall()}

            # 6. 找出需要删除的多余记录
            to_delete = []
            for time_str, record_id in existing_records.items():
                if time_str not in expected_slots:
                    to_delete.append(record_id)

            # 7. 找出需要新增的记录
            to_add = [t for t in expected_slots if t not in existing_records]

            # 8. 执行删除操作
            if to_delete:
                print(f"将删除{len(to_delete)}条多余记录")
                placeholders = ','.join(['%s'] * len(to_delete))
                cursor.execute(
                    f"DELETE FROM dianhan WHERE id IN ({placeholders})",
                    tuple(to_delete)
                )
                db.commit()

            # 9. 执行新增操作
            if to_add:
                # 获取操作人（从现有记录中获取或使用默认）
                cursor.execute(
                    "SELECT People FROM dianhan WHERE biaoDate=%s AND banci=%s LIMIT 1",
                    (today, current_banci)
                )
                people = cursor.fetchone()
                people = people[0] if people else ""

                new_rows = []
                for time_str in to_add:
                    new_rows.append((
                        today,
                        time_str,
                        current_banci,
                        '', '', '', people, ''
                    ))

                sql = """INSERT INTO dianhan (biaoDate, biaoTime, banci, yanliang, dianliang, dianhanliang, People, dianhan_mysql)
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.executemany(sql, new_rows)
                db.commit()
                print(f"新增{len(new_rows)}条记录: {', '.join(to_add)}")

            cursor.close()
            db.close()

        except Exception as e:
            print(f"{datetime.now()} 自动补齐出错：", e)
            try:
                db.rollback()
            except:
                pass

        time.sleep(sleep_seconds)


def sync_dianhan_mysql_loop(sleep_seconds=60):
    print(f"同步dianhan_mysql进程启动，每隔{sleep_seconds}秒检测一次...")
    while True:
        try:
            db = get_connection()
            cursor = db.cursor()
            # 获取当天日期字符串，格式和数据库中biaoDate一致，假设是 'YYYY-MM-DD'
            today_str = datetime.now().strftime('%Y-%m-%d')

            # 1. 查询当天所有dianhan记录
            cursor.execute("SELECT id, biaoDate, biaoTime FROM dianhan WHERE biaoDate = %s", (today_str,))
            rows = cursor.fetchall()

            for row in rows:
                id_, biaoDate, biaoTime = row
                ts_str = f"{biaoDate} {biaoTime}:00"
                cursor.execute("SELECT aValue FROM dian_mysql WHERE tS=%s", (ts_str,))
                result = cursor.fetchone()
                if result is not None:
                    aValue = result[0]
                    write_value = "非加碘" if (aValue is None or aValue == 0) else str(aValue)
                    cursor.execute("UPDATE dianhan SET dianhan_mysql=%s WHERE id=%s", (write_value, id_))

            db.commit()
            cursor.close()
            db.close()
        except Exception as e:
            print(f"{datetime.now()} 同步dianhan_mysql出错：", e)
        time.sleep(sleep_seconds)


if __name__ == '__main__':
    # 启动两个线程
    t1 = threading.Thread(target=auto_fill_dianhan_loop, args=(2,))
    t2 = threading.Thread(target=sync_dianhan_mysql_loop, args=(60,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()