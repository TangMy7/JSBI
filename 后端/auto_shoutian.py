import pymysql
import time
import threading

# 数据库连接配置
db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': '123456',
    'db': 'js',
    'charset': 'utf8',
    'connect_timeout': 10  # 设置连接超时时间为10秒
}

# 监控并同步数据的函数
def monitor_and_sync():
    while True:
        try:
            connection = pymysql.connect(**db_config)
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            while True:
                # 查询 total_biao 所有需要更新的数据
                cursor.execute("SELECT * FROM total_biao ORDER BY inputTime DESC")
                total_biao_records = cursor.fetchall()
                #print("Total total_biao records:", len(total_biao_records))  # 调试信息

                for total_biao_record in total_biao_records:
                    input_time = total_biao_record['inputTime']

                    # 查询其他表中是否存在相同的 inputTime
                    cursor.execute("SELECT COUNT(*) AS count FROM biao_1 WHERE inputTime = %s", (input_time,))
                    biao_1_exists = cursor.fetchone()['count'] > 0
                    #print(f"biao_1_exists for inputTime {input_time}:", biao_1_exists)  # 调试信息

                    cursor.execute("SELECT COUNT(*) AS count FROM biao_2 WHERE inputTime = %s", (input_time,))
                    biao_2_exists = cursor.fetchone()['count'] > 0
                    #print(f"biao_2_exists for inputTime {input_time}:", biao_2_exists)  # 调试信息

                    cursor.execute("SELECT COUNT(*) AS count FROM nowaterc WHERE inputTime = %s", (input_time,))
                    nowaterc_exists = cursor.fetchone()['count'] > 0
                    #print(f"nowaterc_exists for inputTime {input_time}:", nowaterc_exists)  # 调试信息

                    cursor.execute("SELECT COUNT(*) AS count FROM drytwo WHERE inputTime = %s", (input_time,))
                    drytwo_exists = cursor.fetchone()['count'] > 0
                    #print(f"drytwo_exists for inputTime {input_time}:", drytwo_exists)  # 调试信息

                    # 仅在所有表中都存在相同的 inputTime 时进行更新
                    if biao_1_exists and biao_2_exists and nowaterc_exists and drytwo_exists:
                        # 更新 biao_1
                        try:
                            cursor.execute("""
                                UPDATE biao_1 SET centrifugeOilPressureA = %s, centrifugeOilTemperatureA = %s, centrifugeOilLevelA = %s,
                                centrifugeWashingTimeA = %s, centrifugeLooseAgentConsumptionA = %s, centrifugeOilPressureB = %s,
                                centrifugeOilTemperatureB = %s, centrifugeOilLevelB = %s, centrifugeWashingTimeB = %s,
                                centrifugeLooseAgentConsumptionB = %s, centrifugeOilPressureC = %s, centrifugeOilTemperatureC = %s,
                                centrifugeOilLevelC = %s, centrifugeWashingTimeC = %s, centrifugeLooseAgentConsumptionC = %s
                                WHERE inputTime = %s
                            """, (
                                total_biao_record['centrifugeOilPressureA'], total_biao_record['centrifugeOilTemperatureA'],
                                total_biao_record['centrifugeOilLevelA'], total_biao_record['centrifugeWashingTimeA'],
                                total_biao_record['centrifugeLooseAgentConsumptionA'],
                                total_biao_record['centrifugeOilPressureB'],
                                total_biao_record['centrifugeOilTemperatureB'], total_biao_record['centrifugeOilLevelB'],
                                total_biao_record['centrifugeWashingTimeB'],
                                total_biao_record['centrifugeLooseAgentConsumptionB'],
                                total_biao_record['centrifugeOilPressureC'], total_biao_record['centrifugeOilTemperatureC'],
                                total_biao_record['centrifugeOilLevelC'], total_biao_record['centrifugeWashingTimeC'],
                                total_biao_record['centrifugeLooseAgentConsumptionC'], input_time
                            ))
                            #print(f"Updated data in biao_1 for inputTime {input_time}")  # 调试信息
                        except Exception as e:
                            print(f"Error updating biao_1 for inputTime {input_time}: {e}")

                        # 更新 biao_2
                        try:
                            cursor.execute("""
                                UPDATE biao_2 SET condensatePumpOnePressureA = %s, condensatePumpOnePressureB = %s, condensatePumpVPressureA = %s,
                                condensatePumpVPressureB = %s, vacuumPumpingDegreeA = %s, vacuumPumpingDegreeB = %s,
                                flushPumpPressureA = %s, flushPumpPressureB = %s
                                WHERE inputTime = %s
                            """, (
                                total_biao_record['condensatePumpOnePressureA'],
                                total_biao_record['condensatePumpOnePressureB'],
                                total_biao_record['condensatePumpVPressureA'],
                                total_biao_record['condensatePumpVPressureB'],
                                total_biao_record['vacuumPumpingDegreeA'], total_biao_record['vacuumPumpingDegreeB'],
                                total_biao_record['flushPumpPressureA'], total_biao_record['flushPumpPressureB'], input_time
                            ))
                            #print(f"Updated data in biao_2 for inputTime {input_time}")  # 调试信息
                        except Exception as e:
                            print(f"Error updating biao_2 for inputTime {input_time}: {e}")

                        # 更新 nowaterc
                        try:
                            cursor.execute("""
                                UPDATE nowaterc SET ApressureA = %s, ApressureB = %s, CpressureA = %s, CpressureB = %s
                                WHERE inputTime = %s
                            """, (
                                total_biao_record['ApressureA'], total_biao_record['ApressureB'],

                                total_biao_record['CpressureA'], total_biao_record['CpressureB'], input_time
                            ))
                            #print(f"Updated data in nowaterc for inputTime {input_time}")  # 调试信息
                        except Exception as e:
                            print(f"Error updating nowaterc for inputTime {input_time}: {e}")

                        # 更新 drytwo
                        try:
                            cursor.execute("""
                                UPDATE drytwo SET impurityA = %s, impurityB = %s
                                WHERE inputTime = %s
                            """, (
                                total_biao_record['impurityA'], total_biao_record['impurityB'], input_time
                            ))
                            #print(f"Updated data in drytwo for inputTime {input_time}")  # 调试信息
                        except Exception as e:
                            print(f"Error updating drytwo for inputTime {input_time}: {e}")

                        # 提交事务
                        try:
                            connection.commit()
                            #print(f"Transaction committed for inputTime {input_time}")  # 调试信息
                        except Exception as e:
                            print(f"Error committing transaction for inputTime {input_time}: {e}")
                            connection.rollback()

                # 休眠一段时间后再次检查
                time.sleep(1)  # 2s检测一次

        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()



# 运行监控函数
if __name__ == "__main__":
    thread1 = threading.Thread(target=monitor_and_sync)
    #thread2 = threading.Thread(target=monitor_and_sync_beizhu_total)

    thread1.start()
    #thread2.start()

    thread1.join()
    #thread2.join()