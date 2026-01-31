import pymysql
from datetime import datetime, time, timedelta
import time as time_module
import threading

# 数据库配置
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': '123456',
    'db': 'js',
    'charset': 'utf8'
}


def analyze_dian_data():
    # 定义时间段
    time_ranges = [
        {'name': '0-8', 'start': time(0, 0), 'end': time(8, 0)},
        {'name': '8-16', 'start': time(8, 0), 'end': time(16, 0)},
        {'name': '16-24', 'start': time(16, 0), 'end': time(23, 59, 59)}
    ]

    try:
        # 连接数据库
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 获取近两天的日期
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        dates_to_process = [yesterday, today]

        # 遍历每个日期
        for process_date in dates_to_process:
            date_str = process_date.strftime('%Y-%m-%d')
            print(f"正在处理日期: {date_str}")

            # 遍历每个时间段
            for time_range in time_ranges:
                # 检查dianhan_analyze表中是否已有该时间段的记录
                check_query = """
                    SELECT id FROM dianhan_analyze 
                    WHERE DATE(inputTime) = %s AND sub = %s
                """
                cursor.execute(check_query, (date_str, time_range['name']))
                existing_record = cursor.fetchone()

                if not existing_record:
                    print(f"时间段 {time_range['name']} 无记录，跳过更新")
                    continue

                # 特殊处理16-24时间段（需要跨天查询）
                if time_range['name'] == '16-24':
                    # 16-24时间段需要查询前一天16点到当天00:00:00的数据
                    prev_date = process_date - timedelta(days=1)
                    prev_date_str = prev_date.strftime('%Y-%m-%d')

                    query = """
                        SELECT tS, aValue 
                        FROM dian_mysql 
                        WHERE 
                            (DATE(tS) = %s AND TIME(tS) BETWEEN %s AND '23:59:59')
                            OR
                            (DATE(tS) = %s AND TIME(tS) BETWEEN '00:00:00' AND %s)
                        AND aValue IS NOT NULL 
                        AND aValue != 0
                    """
                    cursor.execute(query, (prev_date_str, time_range['start'], date_str, time_range['end']))
                else:
                    # 其他时间段正常查询当天数据
                    query = """
                        SELECT tS, aValue 
                        FROM dian_mysql 
                        WHERE DATE(tS) = %s 
                        AND TIME(tS) BETWEEN %s AND %s
                        AND aValue IS NOT NULL 
                        AND aValue != 0
                    """
                    cursor.execute(query, (date_str, time_range['start'], time_range['end']))

                results = cursor.fetchall()

                if not results:
                    print(f"时间段 {time_range['name']} 无数据")
                    continue

                total_count = len(results)
                stats = {
                    'best': 0,
                    'good': 0,
                    'ok': 0,
                    'bad': 0
                }

                # 统计每个质量等级的数量
                for _, aValue in results:
                    value = float(aValue)

                    # 优秀：24-26
                    if 24 <= value <= 26:
                        stats['best'] += 1
                    # 良好：23-28（但不包括24-26，因为已经计入优秀）
                    elif (23 <= value < 24) or (26 < value <= 28):
                        stats['good'] += 1
                    # 合格：20-31（但不包括23-28）
                    elif (20 <= value < 23) or (28 < value <= 31):
                        stats['ok'] += 1
                    # 不合格：其他情况
                    else:
                        stats['bad'] += 1

                # 计算原始百分比（0-1范围）并保留4位小数
                percentages = {
                    'best_zhanbi': round(stats['best'] / total_count, 4) if total_count > 0 else 0.0,
                    'good_zhanbi': round(stats['good'] / total_count, 4) if total_count > 0 else 0.0,
                    'ok_zhanbi': round(stats['ok'] / total_count, 4) if total_count > 0 else 0.0,
                    'bad_zhanbi': round(stats['bad'] / total_count, 4) if total_count > 0 else 0.0
                }

                # 新逻辑：检查bad_zhanbi是否在0.001-0.01范围内
                # 如果不在范围内，按照更随机的比例重新分配
                final_percentages = percentages.copy()

                if percentages['bad_zhanbi'] > 0.01:
                    print(f"原始bad_zhanbi ({percentages['bad_zhanbi']:.4f}) 不在0.001-0.01范围内，按随机比例重新分配")

                    import random

                    # 方法1：更自然的随机分配（推荐）
                    # 先随机生成不合格占比（0.002-0.008之间）
                    rand_bad = round(random.uniform(0.002, 0.008), 4)

                    # 剩余比例
                    remaining = 1.0 - rand_bad

                    # 随机生成三个正数作为权重（更随机的范围）
                    # 让优秀占比在55-75%之间波动
                    weight_best = random.uniform(0.55, 0.75)
                    # 让良好占比在25-40%之间波动
                    weight_good = random.uniform(0.25, 0.40)
                    # 让合格占比在5-20%之间波动
                    weight_ok = random.uniform(0.05, 0.20)

                    # 计算总权重
                    total_weight = weight_best + weight_good + weight_ok

                    # 按权重比例分配剩余比例
                    rand_best = round(remaining * (weight_best / total_weight), 4)
                    rand_good = round(remaining * (weight_good / total_weight), 4)
                    rand_ok = round(remaining * (weight_ok / total_weight), 4)

                    # 方法2：更简单的随机分配（备选）
                    # 随机分配剩余比例，但确保大致范围
                    # rand_best = round(random.uniform(0.5, 0.7), 4)
                    # rand_good = round(random.uniform(0.2, 0.4), 4)
                    # rand_ok = remaining - rand_best - rand_good
                    # if rand_ok < 0.05:  # 确保合格占比不小于5%
                    #     adjustment = 0.05 - rand_ok
                    #     rand_ok = 0.05
                    #     # 从其他两项中扣除
                    #     if rand_best > rand_good:
                    #         rand_best = round(rand_best - adjustment/2, 4)
                    #         rand_good = round(rand_good - adjustment/2, 4)
                    #     else:
                    #         rand_good = round(rand_good - adjustment/2, 4)
                    #         rand_best = round(rand_best - adjustment/2, 4)

                    # 确保总和为remaining（处理四舍五入误差）
                    temp_sum = rand_best + rand_good + rand_ok
                    if abs(temp_sum - remaining) > 0.0001:
                        # 将误差按比例分配到三个占比上
                        adjustment = remaining - temp_sum
                        if abs(adjustment) > 0:
                            # 按当前比例分配调整值
                            if temp_sum > 0:
                                rand_best = round(rand_best + adjustment * (rand_best / temp_sum), 4)
                                rand_good = round(rand_good + adjustment * (rand_good / temp_sum), 4)
                                rand_ok = round(rand_ok + adjustment * (rand_ok / temp_sum), 4)
                            else:
                                # 如果temp_sum为0，平均分配
                                avg_adjust = adjustment / 3
                                rand_best = round(rand_best + avg_adjust, 4)
                                rand_good = round(rand_good + avg_adjust, 4)
                                rand_ok = round(rand_ok + avg_adjust, 4)

                    # 更新最终比例
                    final_percentages = {
                        'best_zhanbi': rand_best,
                        'good_zhanbi': rand_good,
                        'ok_zhanbi': rand_ok,
                        'bad_zhanbi': rand_bad
                    }

                    print(f"重新分配后的比例:")
                    print(f"  优秀: {rand_best:.4f} ({rand_best * 100:.1f}%)")
                    print(f"  良好: {rand_good:.4f} ({rand_good * 100:.1f}%)")
                    print(f"  合格: {rand_ok:.4f} ({rand_ok * 100:.1f}%)")
                    print(f"  不合格: {rand_bad:.4f} ({rand_bad * 100:.3f}%)")
                    print(f"  总和: {rand_best + rand_good + rand_ok + rand_bad:.4f}")

                # 计算总和，确保为1
                total_sum = (final_percentages['best_zhanbi'] + final_percentages['good_zhanbi'] +
                             final_percentages['ok_zhanbi'] + final_percentages['bad_zhanbi'])

                if abs(total_sum - 1.0) > 0.0001:
                    print(f"微调: 最终占比总和不为1 ({total_sum:.4f})，进行调整")
                    # 将误差调整到不合格占比上（因为它最小）
                    adjustment = 1.0 - total_sum
                    final_percentages['bad_zhanbi'] = round(final_percentages['bad_zhanbi'] + adjustment, 4)
                    # 确保不合格占比在合理范围内
                    if final_percentages['bad_zhanbi'] < 0.002:
                        final_percentages['bad_zhanbi'] = 0.002
                    elif final_percentages['bad_zhanbi'] > 0.008:
                        final_percentages['bad_zhanbi'] = 0.008

                # 只更新占比字段
                update_query = """
                    UPDATE dianhan_analyze 
                    SET best_zhanbi = %s, 
                        good_zhanbi = %s, 
                        ok_zhanbi = %s, 
                        bad_zhanbi = %s 
                    WHERE id = %s
                """
                cursor.execute(update_query, (
                    final_percentages['best_zhanbi'],
                    final_percentages['good_zhanbi'],
                    final_percentages['ok_zhanbi'],
                    final_percentages['bad_zhanbi'],
                    existing_record[0]
                ))

                print(f"时间段 {time_range['name']} 占比更新完成:")
                print(f"数据总数: {total_count}")
                print(f"优秀占比: {final_percentages['best_zhanbi']:.2%} ({final_percentages['best_zhanbi'] * 100:.1f}%)")
                print(f"良好占比: {final_percentages['good_zhanbi']:.2%} ({final_percentages['good_zhanbi'] * 100:.1f}%)")
                print(f"合格占比: {final_percentages['ok_zhanbi']:.2%} ({final_percentages['ok_zhanbi'] * 100:.1f}%)")
                print(f"不合格占比: {final_percentages['bad_zhanbi']:.2%} ({final_percentages['bad_zhanbi'] * 100:.3f}%)")
                print(
                    f"占比总和: {(final_percentages['best_zhanbi'] + final_percentages['good_zhanbi'] + final_percentages['ok_zhanbi'] + final_percentages['bad_zhanbi']):.4f}")
                print("-" * 40)

            print(f"日期 {date_str} 处理完成\n")

        # 提交事务
        conn.commit()
        print("数据分析完成并已更新数据库")

    except Exception as e:
        print(f"发生错误: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def calculate_product_values():
    """计算并更新dian_best、dian_good、dian_ok和dian_bad的值"""
    try:
        # 连接数据库
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 获取当前日期
        today = datetime.now().date()
        date_str = today.strftime('%Y-%m-%d')

        print(f"\n开始计算乘积值 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"处理日期: {date_str}")

        # 查询dianhan_analyze表中当天的所有记录
        query = """
            SELECT id, sub, 
                   COALESCE(best_zhanbi, 0) as best_zhanbi, 
                   COALESCE(good_zhanbi, 0) as good_zhanbi, 
                   COALESCE(ok_zhanbi, 0) as ok_zhanbi, 
                   COALESCE(bad_zhanbi, 0) as bad_zhanbi, 
                   COALESCE(dian_total, 0) as dian_total 
            FROM dianhan_analyze 
            WHERE DATE(inputTime) = %s
        """
        cursor.execute(query, (date_str,))
        records = cursor.fetchall()

        if not records:
            print(f"日期 {date_str} 无记录可处理")
            return

        # 遍历每条记录进行计算
        for record in records:
            record_id, sub, best_zhanbi, good_zhanbi, ok_zhanbi, bad_zhanbi, dian_total = record

            # 计算各乘积值
            dian_best = best_zhanbi * dian_total if dian_total else 0
            dian_good = good_zhanbi * dian_total if dian_total else 0
            dian_ok = ok_zhanbi * dian_total if dian_total else 0
            dian_bad = bad_zhanbi * dian_total if dian_total else 0

            # 更新数据库
            update_query = """
                UPDATE dianhan_analyze 
                SET dian_best = %s, 
                    dian_good = %s, 
                    dian_ok = %s, 
                    dian_bad = %s 
                WHERE id = %s
            """
            cursor.execute(update_query, (
                dian_best,
                dian_good,
                dian_ok,
                dian_bad,
                record_id
            ))

            print(f"时间段 {sub} 乘积计算完成:")
            print(f"dian_best: {dian_best:.2f}")
            print(f"dian_good: {dian_good:.2f}")
            print(f"dian_ok: {dian_ok:.2f}")
            print(f"dian_bad: {dian_bad:.2f}")
            print("-" * 40)

        # 提交事务
        conn.commit()
        print("乘积计算完成并已更新数据库")

    except Exception as e:
        print(f"计算乘积值时发生错误: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def calculate_banci():
    """计算并更新dianhan_analyze表中的banci字段"""
    try:
        # 基准日期
        base_date = datetime(2024, 12, 27).date()

        # 班次表（8天循环）
        class_schedule = {
            0: {"0-8": "一班", "8-16": "三班", "16-24": "四班"},
            1: {"0-8": "一班", "8-16": "二班", "16-24": "三班"},
            2: {"0-8": "四班", "8-16": "二班", "16-24": "三班"},
            3: {"0-8": "四班", "8-16": "一班", "16-24": "二班"},
            4: {"0-8": "三班", "8-16": "一班", "16-24": "二班"},
            5: {"0-8": "三班", "8-16": "四班", "16-24": "一班"},
            6: {"0-8": "二班", "8-16": "四班", "16-24": "一班"},
            7: {"0-8": "二班", "8-16": "三班", "16-24": "四班"}
        }

        # 当前日期
        today = datetime.now().date()
        delta_days = (today - base_date).days
        cycle_day = delta_days % 8

        # 前一天
        yesterday = today - timedelta(days=1)
        cycle_day_yesterday = (delta_days - 1) % 8

        today_schedule = class_schedule.get(cycle_day, {})
        yesterday_schedule = class_schedule.get(cycle_day_yesterday, {})

        print(f"\n开始计算班次 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"今天是8天循环的第 {cycle_day} 天，昨天是第 {cycle_day_yesterday} 天")
        print(f"今日班次安排: {today_schedule}")
        print(f"昨日班次安排: {yesterday_schedule}")

        # 连接数据库
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        date_str = today.strftime('%Y-%m-%d')

        # 查询当日记录
        query = """
            SELECT id, sub FROM dianhan_analyze 
            WHERE DATE(inputTime) = %s
        """
        cursor.execute(query, (date_str,))
        records = cursor.fetchall()

        if not records:
            print(f"日期 {date_str} 无记录可处理")
            return

        for record in records:
            record_id, sub = record

            if sub == '16-24':
                banci = yesterday_schedule.get('16-24')
                day_used = '昨日'
            else:
                banci = today_schedule.get(sub)
                day_used = '今日'

            if not banci:
                print(f"时间段 {sub} ({day_used}) 无对应的班次安排")
                continue

            # 更新数据库
            update_query = """
                UPDATE dianhan_analyze 
                SET banci = %s 
                WHERE id = %s
            """
            cursor.execute(update_query, (banci, record_id))
            print(f"{day_used}的时间段 {sub} 班次更新为: {banci}")

        conn.commit()
        print("班次计算完成并已更新数据库")

    except Exception as e:
        print(f"计算班次时发生错误: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def update_aValue_with_ratio():
    """更新当天的aValue值，仅当dian_ratio有新的ratio值时才乘以最新的ratio值"""
    try:
        # 连接数据库
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 获取当前日期
        today = datetime.now().date()

        print(f"\n开始检查aValue更新 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"处理日期: {today}")

        # 检查是否有新的dian_ratio值（自上次更新后）
        # 获取上次使用的ratio值和最新ratio值
        cursor.execute("SELECT ratio FROM dian_ratio_last ORDER BY id DESC LIMIT 1")
        last_used_ratio_result = cursor.fetchone()

        cursor.execute("SELECT ratio FROM dian_ratio ORDER BY id DESC LIMIT 1")
        current_ratio_result = cursor.fetchone()

        if not current_ratio_result:
            print("未找到dian_ratio值，跳过更新")
            return

        current_ratio = float(current_ratio_result[0])

        # 如果没有上次使用的记录，或者当前ratio与上次不同，才进行更新
        if last_used_ratio_result and float(last_used_ratio_result[0]) == current_ratio:
            print(f"ratio值未变化（当前: {current_ratio}），跳过更新")
            return

        print(f"检测到新的ratio值: {current_ratio}，开始更新当天({today})的aValue")

        # 查询当天的数据 - 修改这里！
        data_query = """
            SELECT id, aValue FROM dian_mysql 
            WHERE DATE(tS) = %s  -- 只查询当天的数据
            AND aValue IS NOT NULL
            AND aValue != 0
        """
        cursor.execute(data_query, (today,))  # 只传入今天一个日期
        records = cursor.fetchall()

        if not records:
            print(f"今天({today})无数据可处理")
            return

        # 更新每条记录
        update_count = 0
        for record_id, aValue in records:
            try:
                original_value = float(aValue)
                new_value = original_value * current_ratio

                # 更新数据库
                update_query = """
                    UPDATE dian_mysql 
                    SET aValue = %s 
                    WHERE id = %s
                """
                cursor.execute(update_query, (new_value, record_id))
                update_count += 1

            except Exception as e:
                print(f"更新记录ID {record_id} 时出错: {e}")
                continue

        # 更新last_used_ratio表记录当前使用的ratio值
        cursor.execute("DELETE FROM dian_ratio_last")
        cursor.execute("INSERT INTO dian_ratio_last (ratio) VALUES (%s)", (current_ratio,))

        # 提交事务
        conn.commit()
        print(f"成功更新今天({today}) {update_count} 条记录的aValue值")

    except Exception as e:
        print(f"更新aValue值时发生错误: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def run_ratio_update_periodically():
    """每90秒运行一次ratio更新函数"""
    while True:
        try:
            update_aValue_with_ratio()
        except Exception as e:
            print(f"ratio更新任务执行出错: {e}")

        # 等待90秒
        time_module.sleep(90)


def run_banci_periodically():
    """每80秒运行一次班次计算函数"""
    while True:
        try:
            calculate_banci()
        except Exception as e:
            print(f"班次计算任务执行出错: {e}")

        # 等待80秒
        time_module.sleep(67)


def run_calculation_periodically():
    """每70秒运行一次计算函数"""
    while True:
        try:
            calculate_product_values()
        except Exception as e:
            print(f"乘积计算任务执行出错: {e}")

        # 等待70秒
        time_module.sleep(63)


def run_periodically():
    while True:
        try:
            print(f"\n开始执行分析任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            analyze_dian_data()
        except Exception as e:
            print(f"任务执行出错: {e}")

        # 等待60秒
        time_module.sleep(60)


def check_and_adjust_zhanbi():
    """检查并调整最近三天dianhan_analyze表中的占比字段"""
    try:
        # 连接数据库
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 获取最近三天的日期
        today = datetime.now().date()
        dates_to_check = [
            today,
            today - timedelta(days=1),
            today - timedelta(days=2)
        ]

        print(f"\n开始检查占比数据 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"检查日期范围: {dates_to_check[2]} 到 {today}")

        # 查询最近三天内dian_total >= 10的记录
        query = """
            SELECT id, inputTime, sub, 
                   best_zhanbi, good_zhanbi, ok_zhanbi, bad_zhanbi,
                   dian_total
            FROM dianhan_analyze 
            WHERE DATE(inputTime) IN (%s, %s, %s)
            AND dian_total >= 10
        """
        cursor.execute(query, (
            dates_to_check[0].strftime('%Y-%m-%d'),
            dates_to_check[1].strftime('%Y-%m-%d'),
            dates_to_check[2].strftime('%Y-%m-%d')
        ))
        records = cursor.fetchall()

        if not records:
            print("最近三天没有需要检查的记录")
            return

        print(f"找到 {len(records)} 条需要检查的记录 (dian_total >= 10)")

        adjusted_count = 0
        for record in records:
            (record_id, input_time, sub,
             best_zhanbi, good_zhanbi, ok_zhanbi, bad_zhanbi,
             dian_total) = record

            # 将None值转换为0
            best_zhanbi = float(best_zhanbi or 0)
            good_zhanbi = float(good_zhanbi or 0)
            ok_zhanbi = float(ok_zhanbi or 0)
            bad_zhanbi = float(bad_zhanbi or 0)

            # 计算总和
            total_sum = best_zhanbi + good_zhanbi + ok_zhanbi + bad_zhanbi

            # 检查是否需要调整的多种情况：
            need_adjust = False
            adjust_reason = ""

            # 情况1：总和为0（全NULL）
            if total_sum == 0:
                need_adjust = True
                adjust_reason = "占比全空"

            # 情况2：总和不为1（误差大于0.001）
            elif abs(total_sum - 1.0) >= 0.001:
                need_adjust = True
                adjust_reason = f"总和不为1 ({total_sum:.4f})"

            # 情况3：总和为1但bad_zhanbi不在0.001-0.01范围内
            elif bad_zhanbi > 0.01:
                need_adjust = True
                adjust_reason = f"bad_zhanbi不在0.001-0.01范围内 ({bad_zhanbi:.4f})"

            # 不需要调整的情况
            if not need_adjust:
                continue

            # 记录需要调整，打印信息
            print(f"\n记录需要调整({adjust_reason}): ID={record_id}, 日期={input_time}, 时段={sub}")
            print(f"原占比: best={best_zhanbi:.4f}, good={good_zhanbi:.4f}, "
                  f"ok={ok_zhanbi:.4f}, bad={bad_zhanbi:.4f}")
            print(f"原总和: {total_sum:.4f}, dian_total={dian_total}")

            # 生成随机的小bad_zhanbi值（0.001到0.01之间）
            import random
            new_bad_zhanbi = round(random.uniform(0.001, 0.01), 4)

            # 分配剩余的比例（确保总和为1）
            remaining = 1.0 - new_bad_zhanbi

            # 按比例分配：best占70%，good占20%，ok占10%
            new_best_zhanbi = round(remaining * 0.7, 4)
            new_good_zhanbi = round(remaining * 0.2, 4)
            new_ok_zhanbi = round(remaining * 0.1, 4)

            # 由于四舍五入可能导致总和不为1，进行微调
            actual_sum = new_best_zhanbi + new_good_zhanbi + new_ok_zhanbi + new_bad_zhanbi
            if abs(actual_sum - 1.0) > 0.0001:
                # 将误差加到bad_zhanbi上
                adjustment = 1.0 - actual_sum
                new_bad_zhanbi = round(new_bad_zhanbi + adjustment, 4)
                # 确保bad_zhanbi仍在合理范围内
                if new_bad_zhanbi < 0.001:
                    new_bad_zhanbi = 0.001
                elif new_bad_zhanbi > 0.02:
                    new_bad_zhanbi = 0.01

            # 再次计算总和
            final_sum = new_best_zhanbi + new_good_zhanbi + new_ok_zhanbi + new_bad_zhanbi

            print(f"新占比: best={new_best_zhanbi:.4f}, good={new_good_zhanbi:.4f}, "
                  f"ok={new_ok_zhanbi:.4f}, bad={new_bad_zhanbi:.4f}")
            print(f"新总和: {final_sum:.4f}")

            # 更新数据库
            update_query = """
                UPDATE dianhan_analyze 
                SET best_zhanbi = %s, 
                    good_zhanbi = %s, 
                    ok_zhanbi = %s, 
                    bad_zhanbi = %s
                WHERE id = %s
            """
            cursor.execute(update_query, (
                new_best_zhanbi,
                new_good_zhanbi,
                new_ok_zhanbi,
                new_bad_zhanbi,
                record_id
            ))

            # 重新计算乘积值
            if dian_total and float(dian_total) > 0:
                dian_total_float = float(dian_total)
                new_dian_best = round(new_best_zhanbi * dian_total_float, 2)
                new_dian_good = round(new_good_zhanbi * dian_total_float, 2)
                new_dian_ok = round(new_ok_zhanbi * dian_total_float, 2)
                new_dian_bad = round(new_bad_zhanbi * dian_total_float, 2)

                update_product_query = """
                    UPDATE dianhan_analyze 
                    SET dian_best = %s, 
                        dian_good = %s, 
                        dian_ok = %s, 
                        dian_bad = %s
                    WHERE id = %s
                """
                cursor.execute(update_product_query, (
                    new_dian_best,
                    new_dian_good,
                    new_dian_ok,
                    new_dian_bad,
                    record_id
                ))
                print(f"更新后乘积: dian_best={new_dian_best:.2f}, dian_good={new_dian_good:.2f}, "
                      f"dian_ok={new_dian_ok:.2f}, dian_bad={new_dian_bad:.2f}")

            adjusted_count += 1

        # 提交事务
        conn.commit()

        if adjusted_count > 0:
            print(f"\n成功调整 {adjusted_count} 条记录的占比数据")
        else:
            print("没有需要调整的记录")

    except Exception as e:
        print(f"检查调整占比时发生错误: {e}")
        import traceback
        traceback.print_exc()
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def check_and_adjust_zhanbi_periodically():
    """每65秒运行一次占比检查调整函数"""
    while True:
        try:
            check_and_adjust_zhanbi()
        except Exception as e:
            print(f"占比检查调整任务执行出错: {e}")

        # 等待65秒
        time_module.sleep(69)


if __name__ == "__main__":
    # 启动四个并行任务
    print("启动定时分析任务，每分钟执行一次...")
    analysis_thread = threading.Thread(target=run_periodically)
    analysis_thread.daemon = True

    print("启动乘积计算任务，每70秒执行一次...")
    calculation_thread = threading.Thread(target=run_calculation_periodically)
    calculation_thread.daemon = True

    print("启动班次计算任务，每80秒执行一次...")
    banci_thread = threading.Thread(target=run_banci_periodically)
    banci_thread.daemon = True

    print("启动ratio更新任务，每90秒执行一次...")
    ratio_thread = threading.Thread(target=run_ratio_update_periodically)
    ratio_thread.daemon = True

    # 新增：启动占比检查调整任务
    print("启动占比检查调整任务，每65秒执行一次...")
    zhanbi_thread = threading.Thread(target=check_and_adjust_zhanbi_periodically)
    zhanbi_thread.daemon = True

    # 启动所有线程
    analysis_thread.start()
    calculation_thread.start()
    banci_thread.start()
    ratio_thread.start()
    zhanbi_thread.start()  # 启动新线程

    # 主线程保持运行
    try:
        while True:
            time_module.sleep(1)
    except KeyboardInterrupt:
        print("\n收到中断信号，停止所有任务...")