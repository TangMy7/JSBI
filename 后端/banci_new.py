import pymysql
from datetime import datetime, timedelta
import time


def assign_class(date: datetime, time_str: str) -> str:
    """
    根据日期和时间分配班次信息。
    :param date: 日期对象
    :param time_str: 时间字符串，如 "07:30:00"
    :return: 对应的班次（字符串）
    """
    # 设定每个周期的日期和班次
    base_date = datetime(2024, 12, 27)  # 设定开始的基准日期
    day_offset = (date - base_date).days  # 当前日期距离基准日期的天数差
    cycle_day = day_offset % 8  # 获取周期内的天数（每8天循环一次）

    # 班次对应关系
    class_schedule = {
        0: {"07:30": "一班", "15:30": "三班", "23:30": "四班"},
        1: {"07:30": "一班", "15:30": "二班", "23:30": "三班"},
        2: {"07:30": "四班", "15:30": "二班", "23:30": "三班"},
        3: {"07:30": "四班", "15:30": "一班", "23:30": "二班"},
        4: {"07:30": "三班", "15:30": "一班", "23:30": "二班"},
        5: {"07:30": "三班", "15:30": "四班", "23:30": "一班"},
        6: {"07:30": "二班", "15:30": "四班", "23:30": "一班"},
        7: {"07:30": "二班", "15:30": "三班", "23:30": "四班"}
    }

    # 打印调试信息，查看班次表的内容
    #print(f"Class Schedule for day {cycle_day}: {class_schedule[cycle_day]}")

    # 只取小时和分钟部分进行比较
    time_str_minutes = time_str[:5]  # 获取前五个字符：例如 "07:30"

    # 获取当前时间的班次
    if time_str_minutes in class_schedule[cycle_day]:
        return class_schedule[cycle_day][time_str_minutes]
    else:
        print(f"Time {time_str_minutes} not found in schedule for day {cycle_day}.")
        return None  # 如果时间不匹配（理应不会发生）


def write_classes_to_mysql():
    # 连接MySQL数据库（本机）
    try:
        mysql_conn = pymysql.connect(
            host='127.0.0.1', port=3306, user='root', passwd='123456', db='js',
            charset='utf8'
        )
        mysql_cursor = mysql_conn.cursor()
        print("Successfully connected to MySQL")
    except Exception as e:
        print(f"MySQL connection error: {e}")
        return

    while True:  # 无限循环
        try:
            # 获取当前日期和时间
            now = datetime.now()
            # 获取查询的开始和结束时间
            start_date = datetime.combine((now - timedelta(days=5)).date(), datetime.min.time())  # 当前日期往前推五天的0点
            end_date = datetime.combine(now.date(), datetime.max.time())  # 当前日期的结束时间到23:59:59

            # 打印调试信息，确认日期范围
            #print(f"Start date: {start_date}, End date: {end_date}")

            # 查询 `threehand` 表中，classes 为 NULL 且 inputTIme 在设定范围内的数据
            mysql_cursor.execute("""
                SELECT inputTIme FROM threehand 
                WHERE classes IS NULL AND inputTIme BETWEEN %s AND %s
            """, (start_date, end_date))

            rows = mysql_cursor.fetchall()

            for row in rows:
                input_time = row[0]  # 获取 inputTIme 字段
                if isinstance(input_time, datetime):  # 确保 inputTIme 是 datetime 类型
                    date_str = input_time.strftime("%Y-%m-%d")
                    time_str = input_time.strftime("%H:%M:%S")

                    # 打印调试信息，检查格式
                    #print(f"Input Time: {input_time}, Date: {date_str}, Time: {time_str}")

                    # 获取班次信息
                    class_info = assign_class(input_time, time_str)

                    if class_info:
                        # 更新班次信息
                        update_query = "UPDATE threehand SET classes = %s WHERE inputTIme = %s"
                        mysql_cursor.execute(update_query, (class_info, input_time))
                        #print(f"Updated inputTIme: {date_str} {time_str} to class: {class_info}")
                    else:
                        print(f"No class found for time: {date_str} {time_str}")

            # 提交事务
            mysql_conn.commit()

            # 额外查询 `output` 表并更新 `banci` 字段
            mysql_cursor.execute("""
                SELECT dataTime FROM output 
                WHERE banci IS NULL AND dataTime BETWEEN %s AND %s
            """, (start_date, end_date))

            rows = mysql_cursor.fetchall()

            for row in rows:
                data_time = row[0]  # 获取 dataTime 字段
                if isinstance(data_time, datetime):  # 确保 dataTime 是 datetime 类型
                    date_str = data_time.strftime("%Y-%m-%d")
                    time_str = data_time.strftime("%H:%M:%S")

                    # 打印调试信息，检查格式
                    #print(f"Data Time: {data_time}, Date: {date_str}, Time: {time_str}")

                    # 获取班次信息
                    class_info = assign_class(data_time, time_str)

                    if class_info:
                        # 更新班次信息
                        update_query = "UPDATE output SET banci = %s WHERE dataTime = %s"
                        mysql_cursor.execute(update_query, (class_info, data_time))
                        #print(f"Updated dataTime: {date_str} {time_str} to banci: {class_info}")
                    else:
                        print(f"No class found for time: {date_str} {time_str}")

            # 提交事务
            mysql_conn.commit()

            # 额外查询 `biao_7` 表并更新 `groupp` 字段
            mysql_cursor.execute("""
                SELECT inputTime, classes FROM biao_7 
                WHERE groupp IS NULL AND inputTime BETWEEN %s AND %s
            """, (start_date, end_date))

            rows = mysql_cursor.fetchall()

            for row in rows:
                input_time = row[0]  # 获取 inputTime 字段
                classes_time = row[1]  # 获取 classes 字段

                if isinstance(input_time, datetime) and isinstance(classes_time, str):  # 确保 inputTime 和 classes 是正确类型
                    date_str = input_time.strftime("%Y-%m-%d")
                    time_str = input_time.strftime("%H:%M:%S")

                    # 打印调试信息，检查格式
                    #print(f"Input Time: {input_time}, Classes: {classes_time}, Date: {date_str}, Time: {time_str}")

                    # 将 classes 字段映射到时间格式
                    classes_to_time = {"早班": "07:30:00", "中班": "15:30:00", "晚班": "23:30:00"}
                    mapped_time_str = classes_to_time.get(classes_time, None)

                    if mapped_time_str:
                        # 获取班次信息
                        class_info = assign_class(input_time, mapped_time_str)

                        if class_info:
                            # 检查 groupp 字段是否已经存在值
                            mysql_cursor.execute("""
                                SELECT groupp FROM biao_7 WHERE inputTime = %s AND classes = %s
                            """, (input_time, classes_time))
                            existing_groupp = mysql_cursor.fetchone()

                            if existing_groupp and existing_groupp[0] is None:
                                # 更新班次信息
                                update_query = "UPDATE biao_7 SET groupp = %s WHERE inputTime = %s AND classes = %s"
                                mysql_cursor.execute(update_query, (class_info, input_time, classes_time))
                                #print(f"Updated inputTime: {date_str} {time_str} to groupp: {class_info}")
                            else:
                                print(f"groupp already has a value for inputTime: {date_str} {time_str} and classes: {classes_time}")
                        else:
                            print(f"No class found for time: {date_str} {time_str}")
                    else:
                        print(f"No mapped time found for classes: {classes_time}")

            # 提交事务
            mysql_conn.commit()

        except Exception as e:
            print(f"Error querying or updating data: {e}")

        # 等待一段时间后再检查
        time.sleep(2)  # 每2秒检查一次

    # 关闭连接
    mysql_cursor.close()
    mysql_conn.close()


# 执行函数
write_classes_to_mysql()

# 执行函数  往电气卤 还有cql 里面都是5s一次检测，因为我设定了 仅查五天的日期，数据也不多
# 对于成品送库单的提交，也每5s吧，反正内存那么大，设定范围是基于当天的一月之内的（毕竟不可能停一月不用吧）
# 仅是班次里面为null的时候，为空也不会插入，但想一想，全都是为null的情况

# 目前都设定五天的了，成品送库单没有弄为一月