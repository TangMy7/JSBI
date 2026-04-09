import pymysql
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from datetime import datetime, timedelta
import threading
import time
from gevent import pywsgi
import logging
import tkinter as tk
from tkinter import messagebox
import schedule

#-------

# ---- 全局数据库连接 ----
db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='XX', db='XX', charset='utf8')
cursor = db.cursor()


def keep_alive():  #  心跳检测且加上重连机制
    global db, cursor
    while True:
        try:
            if db is None or not db.open:
                print("数据库连接不存在或已断开，正在自动重连...")
                # 重新连接
                db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='XX', db='XX', charset='utf8')
                cursor = db.cursor()
                print("数据库重连成功。")
            with db.cursor() as cur:
                cur.execute("SELECT 1")
            # print("Heartbeat sent successfully")
            time.sleep(180)
        except Exception as e:
            print("Error during keep-alive:", e)
            try:
                if db:
                    db.close()
            except Exception:
                pass
            db = None
            cursor = None
            time.sleep(5)  # 防止重连太快

# 后端服务启动
app = Flask(__name__)
app.secret_key="123456"
#---------------------
# 启动心跳线程
heartbeat_thread = threading.Thread(target=keep_alive)
heartbeat_thread.daemon = True
heartbeat_thread.start()
#-------------------
CORS(app, resources=r'/*')

def show_startup_message():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    messagebox.showinfo("提示", "程序已启动！")
    root.mainloop()







#  校准比例修改

@app.route('/dian_ratio/del', methods=['GET'])  # 删除离心机表的数据,根据数据库里面的id来删除
def dian_ratio_del():

    #id = request.form.get("id")

    try:
        id = request.args.get('id')  # 这个原本在外面，诺到里面来了
        sql = "DELETE FROM dian_ratio WHERE id = %s"
        cursor.execute(sql, [id])
        db.commit()
        print("del a data successfully ",id)
        return jsonify(msg="删除数据成功")
    except Exception as e:
        print("del a data failed: ", e)
        db.rollback()  # 把前面操作撤回
        return jsonify(msg="删除数据失败")

@app.route('/dian_ratio/list', methods=['GET'])  # 用户管理表显示  svip
def dian_ratio_list():
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)  # 默认第1页
        perPage = request.args.get('perPage', 10, type=int)  # 默认每页10条

        # 计算查询的偏移量
        offset = (page - 1) * perPage

        # 构造查询
        query = "SELECT  inputTime,ratio,id FROM dian_ratio LIMIT %s OFFSET %s"
        params = [perPage, offset]

        # 执行查询
        cursor.execute(query, params)
        data = cursor.fetchall()
        db.commit()

        # 获取总记录数（用于分页计算）
        total_query = "SELECT COUNT(*) FROM dian_ratio"
        cursor.execute(total_query)
        db.commit()
        totalCount = cursor.fetchone()[0]

        # 计算总页数
        totalPages = (totalCount // perPage) + (1 if totalCount % perPage > 0 else 0)

        # 转换数据为字典列表
        result = []
        if data:
            for i in data:
                result.append({
                    "id": i[2],
                    "inputTime": i[0],
                    "ratio": i[1],


                })

        # 构造包含分页信息的响应
        response = {
            'data': result,
            'pagination': {
                'page': page,
                'perPage': perPage,
                'totalCount': totalCount,
                'totalPages': totalPages
            }
        }

        return jsonify(response)
    except Exception as e:
        print("Error fetching data:", e)
        return jsonify({"error": "服务器内部错误"}), 500



# 更新记录的函数      备注表的更新！ 注意函数名字别重复了 ！！！！！！！！！！
def update_dian_ratio(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE dian_ratio SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()


@app.route('/dian_ratio/update', methods=['GET'])
def dian_ratio_update():
    try:
        id_to_update = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

        # Filter out the fields we want to update
        update_fields = {
            #'inputTime': request.args.get('inputTime'),
            'ratio': request.args.get('ratio'),
            'id': request.args.get('id'),
        }

        # Filter out fields with None values (optional)
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # Call the function to update the record
        success, message = update_dian_ratio(id_to_update, update_fields)

        # Return different JSON responses based on the result
        if success:
            return jsonify({"msg": "修改成功"}), 200
        else:
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

#  校准比例修改




#离心机-----------------------------------------------------------------------------------

@app.route('/biaodan/list', methods=['GET']) # 按查询时间范围列出表biao_1（离心机）的全部信息（默认每页10条数据）
def biaodan_list():
    try:
        # 获取分页参数和查询时间范围
        page = request.args.get('page', 1, type=int)  # 默认第1页
        perPage = request.args.get('perPage', 24, type=int)  # 默认每页10条
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print(type(start_time))
        print("Received start time:", start_time)
        print("Received end time:", end_time)

        # 计算查询的偏移量
        offset = (page - 1) * perPage

        # 构造查询
        query_base = "SELECT * FROM biao_1"
        params = []

        if start_time and end_time:
            query = f"{query_base} WHERE inputTime BETWEEN %s AND %s LIMIT %s OFFSET %s"
            params = [start_time, end_time, perPage, offset]
        else:
            # query = f"{query_base} LIMIT %s OFFSET %s"
            query = f"{query_base} WHERE inputTime BETWEEN %s AND %s LIMIT %s OFFSET %s"

            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")
            print("start_time", start_time)
            # print(type(start_time))

            end_time = d1_at_midnight + timedelta(hours=23, minutes=59, seconds=59)  # 这要是24的话，第二天0点数据也被查看到了
            # 但是这个却是，默认显示今天的，除非第二天有数据，只有像我这种人为测试数据库写入 当天第二天0点数据情况才会出现，但还是顺手修改为23了
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
            print("end_time", end_time)
            # print(type(end_time))

            params = [start_time, end_time, perPage, offset]
            # print("perPage",perPage)
            # print("offset",offset)
            # params = [perPage, offset]

            # 执行查询
        cursor.execute(query, params)
        data = cursor.fetchall()

        # 获取总记录数（用于分页计算）
        total_query = "SELECT COUNT(*) FROM biao_1"
        if start_time and end_time:
            total_query += " WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(total_query, (start_time, end_time))
            db.commit()
        else:
            cursor.execute(total_query)
            db.commit()
        totalCount = cursor.fetchone()[0]

        # 计算总页数
        totalPages = (totalCount // perPage) + (1 if totalCount % perPage > 0 else 0)

        # 转换数据为字典列表
        result = []
        if data:
            for i in data:
                result.append({
                    "id": i[0],
                    "inputTime": i[1],
                    "submitTime": i[2],
                    "centrifugeOilPumpCurrentA": i[3],
                    "centrifugeMainCurrentA": i[4],
                    "centrifugeOilPressureA": i[5],
                    "centrifugeOilTemperatureA": i[6],
                    "centrifugeOilLevelA": i[7],
                    "centrifugeWashingTimeA": i[8],
                    "centrifugeLooseAgentConsumptionA": i[9],
                    "centrifugeOilPumpCurrentB": i[10],
                    "centrifugeMainCurrentB": i[11],
                    "centrifugeOilPressureB": i[12],
                    "centrifugeOilTemperatureB": i[13],
                    "centrifugeOilLevelB": i[14],
                    "centrifugeWashingTimeB": i[15],
                    "centrifugeLooseAgentConsumptionB": i[16],
                    "centrifugeOilPumpCurrentC": i[17],
                    "centrifugeMainCurrentC": i[18],
                    "centrifugeOilPressureC": i[19],
                    "centrifugeOilTemperatureC": i[20],
                    "centrifugeOilLevelC": i[21],
                    "centrifugeWashingTimeC": i[22],
                    "centrifugeLooseAgentConsumptionC": i[23]
                })

        # 构造包含分页信息的响应
        response = {
            'data': result,
            'pagination': {
                'page': page,
                'perPage': perPage,
                'totalCount': totalCount,
                'totalPages': totalPages
            }
        }

        return jsonify(response)
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': '服务器内部错误', 'message': str(e)}), 500

@app.route('/biaodan/del', methods=['GET'])  # 删除离心机表的数据,根据数据库里面的id来删除
def biaodan_del():

    #id = request.form.get("id")

    try:
        id = request.args.get('id')  # 这个原本在外面，诺到里面来了
        sql = "DELETE FROM biao_1 WHERE id = %s"
        cursor.execute(sql, [id])
        db.commit()
        print(request.args)
        print("del a data successfully ",id)
        return jsonify(msg="删除数据成功")
    except Exception as e:
        print("del a data failed: ", e)
        db.rollback()  # 把前面操作撤回
        return jsonify(msg="删除数据失败")

# 数据库连接信息     (下面三个与update绑定)
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': '123456',
    'db': 'js',
    'charset': 'utf8'
}


# 获取数据库连接的函数
def get_db_connection(max_retries=5, retry_interval=3):
    """获取数据库连接，断开时自动重连若干次"""
    attempt = 0
    while attempt < max_retries:
        try:
            conn = pymysql.connect(**DB_CONFIG)
            return conn
        except pymysql.Error as e:
            attempt += 1
            print(f"Error connecting to the database (attempt {attempt}): {e}")
            if attempt >= max_retries:
                print("超过最大重试次数，连接失败。")
                raise
            else:
                print(f"{retry_interval}秒后重试...")
                time.sleep(retry_interval)


# 更新记录的函数
def update_record(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE biao_1 SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()


@app.route('/biaodan/update', methods=['GET']) # 更新离心机表的数据,根据数据库里面的id来更新
def biaodan_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'inputTime': request.args.get('inputTime'),
            'submitTime': request.args.get('submitTime'),
            'centrifugeOilPumpCurrentA': request.args.get('centrifugeOilPumpCurrentA'),
            'centrifugeMainCurrentA': request.args.get('centrifugeMainCurrentA'),
            'centrifugeOilPressureA': request.args.get('centrifugeOilPressureA'),
            'centrifugeOilTemperatureA': request.args.get('centrifugeOilTemperatureA'),
            'centrifugeOilLevelA': request.args.get('centrifugeOilLevelA'),
            'centrifugeWashingTimeA': request.args.get('centrifugeWashingTimeA'),
            'centrifugeLooseAgentConsumptionA': request.args.get('centrifugeLooseAgentConsumptionA'),
            'centrifugeOilPumpCurrentB': request.args.get('centrifugeOilPumpCurrentB'),
            'centrifugeMainCurrentB': request.args.get('centrifugeMainCurrentB'),
            'centrifugeOilPressureB': request.args.get('centrifugeOilPressureB'),
            'centrifugeOilTemperatureB': request.args.get('centrifugeOilTemperatureB'),
            'centrifugeOilLevelB': request.args.get('centrifugeOilLevelB'),
            'centrifugeWashingTimeB': request.args.get('centrifugeWashingTimeB'),
            'centrifugeLooseAgentConsumptionB': request.args.get('centrifugeLooseAgentConsumptionB'),
            'centrifugeOilPumpCurrentC': request.args.get('centrifugeOilPumpCurrentC'),
            'centrifugeMainCurrentC': request.args.get('centrifugeMainCurrentC'),
            'centrifugeOilPressureC': request.args.get('centrifugeOilPressureC'),
            'centrifugeOilTemperatureC': request.args.get('centrifugeOilTemperatureC'),
            'centrifugeOilLevelC': request.args.get('centrifugeOilLevelC'),
            'centrifugeWashingTimeC': request.args.get('centrifugeWashingTimeC'),
            'centrifugeLooseAgentConsumptionC': request.args.get('centrifugeLooseAgentConsumptionC')
        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            # return jsonify({"error": "失败"}), 500
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error updating record:", e)
        return jsonify({"error": "服务器内部错误"}), 500


@app.route('/beizhu1/list', methods=['GET']) # 列出离心机备注表的信息，用group区分组号
def beizhu1_list():
    try:
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print("Received start time:", start_time)
        print("Received end time:", end_time)
        # 构造查询
        # query_base = "SELECT * FROM beizhu_1"

        if start_time and end_time:
            query = "SELECT * FROM beizhu_1 WHERE inputTime BETWEEN %s AND %s"
            # query = f"{query_base} WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()  # 文心一言写的这个就给我删掉了  (这个不写就无法实时更新)
        else:
            # cursor.execute("SELECT * FROM beizhu_1")
            query = "SELECT * FROM beizhu_1 WHERE inputTime BETWEEN %s AND %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")
            print("start_time", start_time)
            print(type(start_time))

            end_time = d1_at_midnight + timedelta(hours=23, minutes=59, seconds=59)
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
            print("end_time", end_time)
            print(type(end_time))

            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()
        temp = {}
        result = []
        if data:
            for i in data:
                temp["id"] = i[0]
                temp["inputTime"] = i[1]
                temp["handoverTool"] = i[2]
                temp["deviceHealth"] = i[3]
                temp["environmentHealth"] = i[4]
                temp["successor"] = i[5]
                temp["handoverPerson"] = i[6]
                temp["groupp"] = i[7]
                temp["classes"] = i[8]
                temp["looseAgentConsumptionTotal"] = i[9]
                temp["subTime"] = i[10]
                temp["sub"] = i[11]
                result.append(temp.copy())
            print("result: ", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])
    except Exception as e:
        print("Error fetching data:", e)
        return jsonify({"error": "服务器内部错误"}), 500


@app.route('/beizhu1/add', methods=['GET'])  # 离心机备注表添加  group是必填的
def beizhu1_add():
    try:
        # 获取请求参数
        # inputTime = request.args.get("inputTime") 这个注释掉
        handoverTool = request.args.get("handoverTool")
        deviceHealth = request.args.get("deviceHealth")
        environmentHealth = request.args.get("environmentHealth")
        successor = request.args.get("successor")
        handoverPerson = request.args.get("handoverPerson")
        groupp = request.args.get("groupp")
        classes = request.args.get("classes")
        looseAgentConsumptionTotal = request.args.get("looseAgentConsumptionTotal")
        subTime = request.args.get("subTime")
        sub = request.args.get("sub")

        # 获取当前时间段的 inputTime 和 sub
        inputTime, default_sub = get_time_and_sub()

        if not sub:
            sub = default_sub  # 使用函数返回的默认值

        # 检查是否已经有该时间段的记录
        if inputTime:
            if check_existing_record(inputTime):
                return jsonify({"error": "数据已存在，添加失败"}), 400

        try:
            sql = "INSERT INTO beizhu_1(inputTime, handoverTool,deviceHealth,environmentHealth,successor,handoverPerson,groupp,classes,looseAgentConsumptionTotal,subTime,sub) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s,%s,%s)"  # 修改SQL语句以包含password字段
            cursor.execute(sql,
                           [inputTime, handoverTool, deviceHealth, environmentHealth, successor, handoverPerson, groupp,
                            classes, looseAgentConsumptionTotal, subTime, sub])
            db.commit()
            print("add a new successfully")
            return jsonify({"msg": "添加成功"}), 200  # 使用标准的HTTP状态码
        except Exception as e:
            print("add a new failed:", e)
            db.rollback()  # 把前面操作撤回
            return jsonify({"error": "添加失败", "exception": str(e)}), 500
    except Exception as e:
        print("Error adding record:", e)
        return jsonify({"error": "服务器内部错误"}), 500


# 辅助函数：检查当前时间并返回对应的 inputTime 和 sub
def get_time_and_sub():
    try:
        # 获取当前日期和时间
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式

        # 7:00 到 9:00
        if 7 <= current_time.hour < 9:
            return f"{current_date} 07:30:00", "8:00"

        # 15:00 到 17:00
        elif 15 <= current_time.hour < 17:
            return f"{current_date} 15:30:00", "16:00"

        # 22:00 到 23:59
        elif 22 <= current_time.hour < 24:
            return f"{current_date} 23:30:00", "0:00"

        # 其他时间不允许插入
        else:
            return None, None
    except Exception as e:
        print("Error adding record:", e)
        return jsonify({"error": "服务器内部错误"}), 500

# 检查是否已存在该时间段的记录
def check_existing_record(inputTime):
    try:
        sql = "SELECT COUNT(*) FROM beizhu_1 WHERE inputTime = %s"
        cursor.execute(sql, (inputTime,))
        count = cursor.fetchone()[0]
        if count > 0:
            return True  # 数据已存在
        else:
            return False  # 数据不存在
    except Exception as e:
        print(f"Error checking existing record: {e}")
        return False




@app.route('/beizhu1/del', methods=['GET'])  # 离心机备注表删除
def beizhu1_del():
    #id = request.form.get("id")
    try:
        id = request.args.get('id')
        sql = "DELETE FROM beizhu_1 WHERE id = %s"
        cursor.execute(sql, [id])
        db.commit()
        print("del a user successfully")
        return jsonify(msg="删除成功")
    except Exception as e:
        print("del a user failed: ", e)
        db.rollback()  # 把前面操作撤回
        return jsonify(msg="删除失败")


# 更新记录的函数      备注表的更新！ 注意函数名字别重复了 ！！！！！！！！！！
def update_record_beizhu(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE beizhu_1 SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()


@app.route('/beizhu1/update', methods=['GET']) # 更新备注表表的数据,根据数据库里面的id来更新
def beizhu1_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')
        groupp = request.args.get('groupp')
        print(type(groupp))

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'inputTime': request.args.get('inputTime'),
            'handoverTool': request.args.get('handoverTool'),
            'deviceHealth': request.args.get('deviceHealth'),
            'environmentHealth': request.args.get('environmentHealth'),
            'successor': request.args.get('successor'),
            'handoverPerson': request.args.get('handoverPerson'),
            'groupp': request.args.get('groupp'),
            'classes': request.args.get('classes'),
            'looseAgentConsumptionTotal': request.args.get('looseAgentConsumptionTotal'),
            'subTime': request.args.get('subTime')
            , 'sub': request.args.get('sub')
        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_beizhu(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)
        return jsonify({"error": "服务器内部错误"}), 500



@app.route('/personManage/list', methods=['GET']) # 列出离心机表的组全部用户信息，一共四组
def personManage_list():
    try:
        cursor.execute("SELECT * FROM yonghu1")
        data = cursor.fetchall()
        result = []
        if data:
            for i in data:
                # 创建一个新的字典来存储当前用户的信息
                temp = {
                    "id": i[0],
                    "username": i[1],
                    "password": i[2],
                    "role": i[3]
                }
                # 检查角色是否为 admin，如果不是则添加到结果列表中
                if temp["username"] != "admin":
                    result.append(temp)
            # print("result: ", len(result))  # 打印过滤后的结果数量
            return jsonify(result)
        else:
            # print("result: NULL")
            return jsonify([])
    except Exception as e:
        print("Error adding record:", e)
        return jsonify({"error": "服务器内部错误"}), 500







#离心机--------------------------------------------------------------------------------------------


#表2----------------------------------------------------------------------------------------------

@app.route('/biao2/list', methods=['GET']) # 按查询时间范围列出表biao_2的全部信息（默认每页10条数据）
def biao2_list():
    try:
        # 获取分页参数和查询时间范围
        page = request.args.get('page', 1, type=int)  # 默认第1页
        perPage = request.args.get('perPage', 24, type=int)  # 默认每页10条
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print(type(start_time))
        print("Received start time:", start_time)
        print("Received end time:", end_time)

        # 计算查询的偏移量
        offset = (page - 1) * perPage

        # 构造查询
        query_base = "SELECT * FROM biao_2"
        params = []

        if start_time and end_time:
            query = f"{query_base} WHERE inputTime BETWEEN %s AND %s LIMIT %s OFFSET %s"
            params = [start_time, end_time, perPage, offset]
        else:

            query = f"{query_base} WHERE inputTime BETWEEN %s AND %s LIMIT %s OFFSET %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")

            end_time = d1_at_midnight + timedelta(hours=23, minutes=59, seconds=59)
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

            params = [start_time, end_time, perPage, offset]

            # 执行查询
        cursor.execute(query, params)
        data = cursor.fetchall()

        # 获取总记录数（用于分页计算）
        total_query = "SELECT COUNT(*) FROM biao_2"
        if start_time and end_time:
            total_query += " WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(total_query, (start_time, end_time))
            db.commit()
        else:
            cursor.execute(total_query)
            db.commit()
        totalCount = cursor.fetchone()[0]

        # 计算总页数
        totalPages = (totalCount // perPage) + (1 if totalCount % perPage > 0 else 0)

        # 转换数据为字典列表
        result = []
        if data:
            for i in data:
                result.append({
                    "id": i[0],
                    "inputTime": i[1],
                    "submitTime": i[2],
                    "circulatingPumpCurrentA": i[3],
                    "circulatingPumpCurrentB": i[4],
                    "circulatingPumpCurrentC": i[5],
                    "circulatingPumpCurrentD": i[6],
                    "circulatingPumpCurrentE": i[7],
                    "circulatingPumpWaterPressureA": i[8],
                    "circulatingPumpWaterPressureB": i[9],
                    "circulatingPumpWaterPressureC": i[10],
                    "circulatingPumpWaterPressureD": i[11],
                    "circulatingPumpWaterPressureE": i[12],
                    "condensatePumpOneCurrentA": i[13],
                    "condensatePumpOnePressureA": i[14],
                    "condensatePumpOneCurrentB": i[15],
                    "condensatePumpOnePressureB": i[16],
                    "condensatePumpVCurrentA": i[17],
                    "condensatePumpVPressureA": i[18],
                    "condensatePumpVCurrentB": i[19],
                    "condensatePumpVPressureB": i[20],
                    "solidLiquidRatioOfTankA": i[21],
                    "solidLiquidRatioOfTankB": i[22],
                    "solidLiquidRatioOfTankC": i[23],
                    "solidLiquidRatioOfTankD": i[24],
                    "solidLiquidRatioOfTankE": i[25],
                    "vacuumPumpingDegreeA": i[26],
                    "vacuumPumpingCurrentA": i[27],
                    "vacuumPumpingDegreeB": i[28],
                    "vacuumPumpingCurrentB": i[29],
                    "sealPumpCurrentA": i[30],
                    "sealPumpPressureA": i[31],
                    "sealPumpCurrentB": i[32],
                    "sealPumpPressureB": i[33],
                    "flushPumpCurrentA": i[34],
                    "flushPumpPressureA": i[35],
                    "flushPumpCurrentB": i[36],
                    "flushPumpPressureB": i[37],
                    "balanceA": i[38],
                    "balanceB": i[39],
                    "balanceC": i[40],
                    "balanceD": i[41],
                    "balanceE": i[42],
                })

        # 构造包含分页信息的响应
        response = {
            'data': result,
            'pagination': {
                'page': page,
                'perPage': perPage,
                'totalCount': totalCount,
                'totalPages': totalPages
            }
        }

        return jsonify(response)
    except Exception as e:
        print("list biao_2 failed: ", e)
        return jsonify(msg="查询数据失败"), 500

@app.route('/biao2/del', methods=['GET'])  # 删除表2的数据,根据数据库里面的id来删除
def biao2_del():

    #id = request.form.get("id")

    try:
        id = request.args.get('id')
        sql = "DELETE FROM biao_2 WHERE id = %s"
        cursor.execute(sql, [id])
        db.commit()
        print(request.args)
        print("del a data successfully ",id)
        return jsonify(msg="删除数据成功")
    except Exception as e:
        print("del a data failed: ", e)
        db.rollback()  # 把前面操作撤回
        return jsonify(msg="删除数据失败")


@app.route('/biao2/update', methods=['GET']) # 更新表2的数据,根据数据库里面的id来更新
def biao2_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'inputTime': request.args.get('inputTime'),
            'submitTime': request.args.get('submitTime'),
            'circulatingPumpCurrentA': request.args.get('circulatingPumpCurrentA'),
            'circulatingPumpCurrentB': request.args.get('circulatingPumpCurrentB'),
            'circulatingPumpCurrentC': request.args.get('circulatingPumpCurrentC'),
            'circulatingPumpCurrentD': request.args.get('circulatingPumpCurrentD'),
            'circulatingPumpCurrentE': request.args.get('circulatingPumpCurrentE'),
            'circulatingPumpWaterPressureA': request.args.get('circulatingPumpWaterPressureA'),
            'circulatingPumpWaterPressureB': request.args.get('circulatingPumpWaterPressureB'),
            'circulatingPumpWaterPressureC': request.args.get('circulatingPumpWaterPressureC'),
            'circulatingPumpWaterPressureD': request.args.get('circulatingPumpWaterPressureD'),
            'circulatingPumpWaterPressureE': request.args.get('circulatingPumpWaterPressureE'),
            'condensatePumpOneCurrentA': request.args.get('condensatePumpOneCurrentA'),
            'condensatePumpOnePressureA': request.args.get('condensatePumpOnePressureA'),
            'condensatePumpOneCurrentB': request.args.get('condensatePumpOneCurrentB'),
            'condensatePumpOnePressureB': request.args.get('condensatePumpOnePressureB'),
            'condensatePumpVCurrentA': request.args.get('condensatePumpVCurrentA'),
            'condensatePumpVPressureA': request.args.get('condensatePumpVPressureA'),
            'condensatePumpVCurrentB': request.args.get('condensatePumpVCurrentB'),
            'condensatePumpVPressureB': request.args.get('condensatePumpVPressureB'),
            'solidLiquidRatioOfTankA': request.args.get('solidLiquidRatioOfTankA'),
            'solidLiquidRatioOfTankB': request.args.get('solidLiquidRatioOfTankB'),
            'solidLiquidRatioOfTankC': request.args.get('solidLiquidRatioOfTankC'),
            'solidLiquidRatioOfTankD': request.args.get('solidLiquidRatioOfTankD'),
            'solidLiquidRatioOfTankE': request.args.get('solidLiquidRatioOfTankE'),
            'vacuumPumpingDegreeA': request.args.get('vacuumPumpingDegreeA'),
            'vacuumPumpingCurrentA': request.args.get('vacuumPumpingCurrentA'),
            'vacuumPumpingDegreeB': request.args.get('vacuumPumpingDegreeB'),
            'vacuumPumpingCurrentB': request.args.get('vacuumPumpingCurrentB'),
            'sealPumpCurrentA': request.args.get('sealPumpCurrentA'),
            'sealPumpCurrentB': request.args.get('sealPumpCurrentB'),
            'sealPumpPressureA': request.args.get('sealPumpPressureA'),
            'sealPumpPressureB': request.args.get('sealPumpPressureB'),
            'flushPumpCurrentA': request.args.get('flushPumpCurrentA'),
            'flushPumpPressureA': request.args.get('flushPumpPressureA'),
            'flushPumpCurrentB': request.args.get('flushPumpCurrentB'),
            'flushPumpPressureB': request.args.get('flushPumpPressureB'),
            'balanceA': request.args.get('balanceA'),
            'balanceB': request.args.get('balanceB'),
            'balanceC': request.args.get('balanceC'),
            'balanceD': request.args.get('balanceD'),
            'balanceE': request.args.get('balanceE'),
        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_biao2(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)
        return jsonify({"error": "服务器内部错误"}), 500


# 更新记录的函数
def update_record_biao2(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE biao_2 SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()




@app.route('/beizhu2/list', methods=['GET']) # 列出表2备注表的信息，用group区分组号
def beizhu2_list():
    try:
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print("Received start time:", start_time)
        print("Received end time:", end_time)
        # 构造查询
        # query_base = "SELECT * FROM beizhu_1"

        if start_time and end_time:
            query = "SELECT * FROM beizhu_2 WHERE inputTime BETWEEN %s AND %s"
            # query = f"{query_base} WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()  # (这个不写就无法实时更新)
        else:
            # cursor.execute("SELECT * FROM beizhu_1")
            query = "SELECT * FROM beizhu_2 WHERE inputTime BETWEEN %s AND %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")

            end_time = d1_at_midnight + timedelta(hours=23, minutes=59, seconds=59)
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()
        temp = {}
        result = []
        if data:
            for i in data:
                temp["id"] = i[0]
                temp["inputTime"] = i[1]
                temp["handoverTool"] = i[2]
                temp["deviceHealth"] = i[3]
                temp["environmentHealth"] = i[4]
                temp["successor"] = i[5]
                temp["handoverPerson"] = i[6]
                temp["groupp"] = i[7]
                temp["classes"] = i[8]
                temp["subTime"] = i[9]
                temp["sub"] = i[10]
                result.append(temp.copy())
            print("result: ", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])
    except Exception as e:
        print("Error adding record:", e)
        return jsonify({"error": "服务器内部错误"}), 500

@app.route('/beizhu2/add', methods=['GET'])  # 表2备注表添加
def beizhu2_add():
    try:
        # inputTime = request.args.get("inputTime")  # 这里使用form获取数据,可能后面要用json？,现在改为params,也就是args
        handoverTool = request.args.get("handoverTool")
        deviceHealth = request.args.get("deviceHealth")
        environmentHealth = request.args.get("environmentHealth")
        successor = request.args.get("successor")
        handoverPerson = request.args.get("handoverPerson")
        groupp = request.args.get("groupp")
        classes = request.args.get("classes")
        subTime = request.args.get("subTime")
        sub = request.args.get("sub")

        # 获取当前时间段的 inputTime 和 sub
        inputTime, default_sub = get_time_and_sub1()

        if not sub:
            sub = default_sub  # 使用函数返回的默认值

        # 检查是否已经有该时间段的记录
        if inputTime:
            if check_existing_record1(inputTime):
                return jsonify({"error": "数据已存在，添加失败"}), 400

        try:
            sql = "INSERT INTO beizhu_2(inputTime, handoverTool,deviceHealth,environmentHealth,successor,handoverPerson,groupp,classes,subTime,sub) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s,%s)"  # 修改SQL语句以包含password字段
            cursor.execute(sql,
                           [inputTime, handoverTool, deviceHealth, environmentHealth, successor, handoverPerson, groupp,
                            classes, subTime, sub])
            db.commit()
            print("add a new successfully")
            return jsonify({"msg": "添加成功"}), 200  # 使用标准的HTTP状态码
        except Exception as e:
            print("add a new failed:", e)
            db.rollback()  # 把前面操作撤回
            return jsonify({"error": "添加失败", "exception": str(e)}), 500
    except Exception as e:
        print("Error adding record:", e)
        return jsonify({"error": "服务器内部错误"}), 500

# 辅助函数：检查当前时间并返回对应的 inputTime 和 sub
def get_time_and_sub1():
    try:
        # 获取当前日期和时间
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式

        # 7:00 到 9:00
        if 7 <= current_time.hour < 9:
            return f"{current_date} 07:30:00", "8:00"

        # 15:00 到 17:00
        elif 15 <= current_time.hour < 17:
            return f"{current_date} 15:30:00", "16:00"

        # 22:00 到 23:59
        elif 22 <= current_time.hour < 24:
            return f"{current_date} 23:30:00", "0:00"

        # 其他时间不允许插入
        else:
            return None, None
    except Exception as e:
        print("Error adding record:", e)
        return jsonify({"error": "服务器内部错误"}), 500

# 检查是否已存在该时间段的记录
def check_existing_record1(inputTime):
    try:
        sql = "SELECT COUNT(*) FROM beizhu_2 WHERE inputTime = %s"
        cursor.execute(sql, (inputTime,))
        count = cursor.fetchone()[0]
        if count > 0:
            return True  # 数据已存在
        else:
            return False  # 数据不存在
    except Exception as e:
        print(f"Error checking existing record: {e}")
        return False


@app.route('/beizhu2/del', methods=['GET'])  # 表2备注表删除
def beizhu2_del():
    #id = request.form.get("id")
    try:
        id = request.args.get('id')
        sql = "DELETE FROM beizhu_2 WHERE id = %s"
        cursor.execute(sql, [id])
        db.commit()
        print("del a user successfully")
        return jsonify(msg="删除成功")
    except Exception as e:
        print("del a user failed: ", e)
        db.rollback()  # 把前面操作撤回
        return jsonify(msg="删除失败")


# 更新记录的函数      备注表的更新！ 注意函数名字别重复了 ！！！！！！！！！！
def update_record_beizhu2(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE beizhu_2 SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()


@app.route('/beizhu2/update', methods=['GET']) # 更新表2备注表表的数据,根据数据库里面的id来更新
def beizhu2_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')
        groupp = request.args.get('groupp')
        print(type(groupp))

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'inputTime': request.args.get('inputTime'),
            'handoverTool': request.args.get('handoverTool'),
            'deviceHealth': request.args.get('deviceHealth'),
            'environmentHealth': request.args.get('environmentHealth'),
            'successor': request.args.get('successor'),
            'handoverPerson': request.args.get('handoverPerson'),
            'groupp': request.args.get('groupp'),
            'classes': request.args.get('classes'),
            'subTime': request.args.get('subTime'),
            'sub': request.args.get('sub')
        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_beizhu2(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)
        return jsonify({"error": "服务器内部错误"}), 500






#表2-----------------------------------------------------------------------------------------------


#干燥二-----------------------------------------------------------------------------------------------


@app.route('/dryTwo/list', methods=['GET']) # 按查询时间范围列出干燥二的全部信息
def dryTwo_list():
    try:
        # 获取分页参数和查询时间范围
        page = request.args.get('page', 1, type=int)  # 默认第1页
        perPage = request.args.get('perPage', 24, type=int)  # 默认每页10条
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print(type(start_time))
        print("Received start time:", start_time)
        print("Received end time:", end_time)

        # 计算查询的偏移量
        offset = (page - 1) * perPage

        # 构造查询
        query_base = "SELECT * FROM drytwo"
        params = []

        if start_time and end_time:
            query = f"{query_base} WHERE inputTime BETWEEN %s AND %s LIMIT %s OFFSET %s"
            params = [start_time, end_time, perPage, offset]
        else:

            query = f"{query_base} WHERE inputTime BETWEEN %s AND %s LIMIT %s OFFSET %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")

            end_time = d1_at_midnight + timedelta(hours=23, minutes=59, seconds=59)
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

            params = [start_time, end_time, perPage, offset]

            # 执行查询
        cursor.execute(query, params)
        data = cursor.fetchall()

        # 获取总记录数（用于分页计算）
        total_query = "SELECT COUNT(*) FROM drytwo"
        if start_time and end_time:
            total_query += " WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(total_query, (start_time, end_time))
            db.commit()
        else:
            cursor.execute(total_query)
            db.commit()
        totalCount = cursor.fetchone()[0]

        # 计算总页数
        totalPages = (totalCount // perPage) + (1 if totalCount % perPage > 0 else 0)

        # 转换数据为字典列表
        result = []
        if data:
            for i in data:
                result.append({
                    "id": i[0],
                    "inputTime": i[1],
                    "submitTime": i[2],
                    "waterPumpA": i[3],
                    "waterPumpB": i[4],
                    "fanA": i[5],
                    "hotA": i[6],
                    "coldA": i[7],
                    "hotTempA": i[8],
                    "weiTempA": i[9],
                    "dryTempA": i[10],
                    "dryPressureA": i[11],
                    "deyTempA": i[12],
                    "impurityA": i[13],
                    "fanB": i[14],
                    "hotB": i[15],
                    "coldB": i[16],
                    "hotTempB": i[17],
                    "weiTempB": i[18],
                    "dryTempB": i[19],
                    "dryPressureB": i[20],
                    "deyTempB": i[21],
                    "impurityB": i[22],
                })

        # 构造包含分页信息的响应
        response = {
            'data': result,
            'pagination': {
                'page': page,
                'perPage': perPage,
                'totalCount': totalCount,
                'totalPages': totalPages
            }
        }

        return jsonify(response)
    except Exception as e:
        print("Error adding record:", e)
        return jsonify({"error": "服务器内部错误"}), 500


@app.route('/dryTwo/update', methods=['GET']) # 更新表2的数据,根据数据库里面的id来更新
def dryTwo_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'inputTime': request.args.get('inputTime'),
            'submitTime': request.args.get('submitTime'),
            'waterPumpA': request.args.get('waterPumpA'),
            'waterPumpB': request.args.get('waterPumpB'),
            'fanA': request.args.get('fanA'),
            'hotA': request.args.get('hotA'),
            'coldA': request.args.get('coldA'),
            'hotTempA': request.args.get('hotTempA'),
            'weiTempA': request.args.get('weiTempA'),
            'dryTempA': request.args.get('dryTempA'),
            'dryPressureA': request.args.get('dryPressureA'),
            'deyTempA': request.args.get('deyTempA'),
            'impurityA': request.args.get('impurityA'),
            'fanB': request.args.get('fanB'),
            'hotB': request.args.get('hotB'),
            'coldB': request.args.get('coldB'),
            'hotTempB': request.args.get('hotTempB'),
            'weiTempB': request.args.get('weiTempB'),
            'dryTempB': request.args.get('dryTempB'),
            'dryPressureB': request.args.get('dryPressureB'),
            'deyTempB': request.args.get('deyTempB'),
            'impurityB': request.args.get('impurityB'),
        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_dryTwo(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)
        return jsonify({"error": "服务器内部错误"}), 500


# 更新记录的函数
def update_record_dryTwo(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE dryTwo SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()


@app.route('/dryTwoA/list', methods=['GET']) # 列出干燥二备注
def dryTwoA_list():
    try:
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print("Received start time:", start_time)
        print("Received end time:", end_time)
        # 构造查询
        # query_base = "SELECT * FROM beizhu_1"

        if start_time and end_time:
            query = "SELECT * FROM drytwoa WHERE inputTime BETWEEN %s AND %s"
            # query = f"{query_base} WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()  # (这个不写就无法实时更新)
        else:
            # cursor.execute("SELECT * FROM beizhu_1")
            query = "SELECT * FROM drytwoa WHERE inputTime BETWEEN %s AND %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")

            end_time = d1_at_midnight + timedelta(hours=23, minutes=59, seconds=59)
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()
        temp = {}
        result = []
        if data:
            for i in data:
                temp["id"] = i[0]
                temp["inputTime"] = i[1]
                temp["handoverTool"] = i[2]
                temp["deviceHealth"] = i[3]
                temp["environmentHealth"] = i[4]
                temp["successor"] = i[5]
                temp["handoverPerson"] = i[6]
                temp["groupp"] = i[7]
                temp["classes"] = i[8]
                temp["subTime"] = i[9]
                temp["sub"] = i[10]
                result.append(temp.copy())
            print("result: ", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

@app.route('/dryTwoA/add', methods=['GET'])  # 表2备注表添加
def dryTwoA_add():
    try:
        # inputTime = request.args.get("inputTime")  # 这里使用form获取数据,可能后面要用json？,现在改为params,也就是args
        handoverTool = request.args.get("handoverTool")
        deviceHealth = request.args.get("deviceHealth")
        environmentHealth = request.args.get("environmentHealth")
        successor = request.args.get("successor")
        handoverPerson = request.args.get("handoverPerson")
        groupp = request.args.get("groupp")
        classes = request.args.get("classes")
        subTime = request.args.get("subTime")
        sub = request.args.get("sub")

        # 获取当前时间段的 inputTime 和 sub
        inputTime, default_sub = get_time_and_sub2()

        if not sub:
            sub = default_sub  # 使用函数返回的默认值

        # 检查是否已经有该时间段的记录
        if inputTime:
            if check_existing_record2(inputTime):
                return jsonify({"error": "数据已存在，添加失败"}), 400

        try:
            sql = "INSERT INTO drytwoa(inputTime, handoverTool,deviceHealth,environmentHealth,successor,handoverPerson,groupp,classes,subTime,sub) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s,%s)"  # 修改SQL语句以包含password字段
            cursor.execute(sql,
                           [inputTime, handoverTool, deviceHealth, environmentHealth, successor, handoverPerson, groupp,
                            classes, subTime, sub])
            db.commit()
            print("add a new successfully")
            return jsonify({"msg": "添加成功"}), 200  # 使用标准的HTTP状态码
        except Exception as e:
            print("add a new failed:", e)
            db.rollback()  # 把前面操作撤回
            return jsonify({"error": "添加失败", "exception": str(e)}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

# 辅助函数：检查当前时间并返回对应的 inputTime 和 sub
def get_time_and_sub2():
    try:
        # 获取当前日期和时间
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式

        # 7:00 到 9:00
        if 7 <= current_time.hour < 9:
            return f"{current_date} 07:30:00", "8:00"

        # 15:00 到 17:00
        elif 15 <= current_time.hour < 17:
            return f"{current_date} 15:30:00", "16:00"

        # 22:00 到 23:59
        elif 22 <= current_time.hour < 24:
            return f"{current_date} 23:30:00", "0:00"

        # 其他时间不允许插入
        else:
            return None, None
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

# 检查是否已存在该时间段的记录
def check_existing_record2(inputTime):
    try:
        sql = "SELECT COUNT(*) FROM drytwoa WHERE inputTime = %s"
        cursor.execute(sql, (inputTime,))
        count = cursor.fetchone()[0]
        if count > 0:
            return True  # 数据已存在
        else:
            return False  # 数据不存在
    except Exception as e:
        print(f"Error checking existing record: {e}")
        return False


@app.route('/dryTwoA/del', methods=['GET'])  # 表2备注表删除
def dryTwoA_del():
    #id = request.form.get("id")
    try:
        id = request.args.get('id')
        sql = "DELETE FROM drytwoa WHERE id = %s"
        cursor.execute(sql, [id])
        db.commit()
        print("del a user successfully")
        return jsonify(msg="删除成功")
    except Exception as e:
        print("del a user failed: ", e)
        db.rollback()  # 把前面操作撤回
        return jsonify(msg="删除失败")


# 更新记录的函数      备注表的更新！ 注意函数名字别重复了 ！！！！！！！！！！
def update_record_dryTwoA(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE drytwoa SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()


@app.route('/dryTwoA/update', methods=['GET']) # 更新表2备注表表的数据,根据数据库里面的id来更新
def dryTwoA_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')
        groupp = request.args.get('groupp')
        print(type(groupp))

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'inputTime': request.args.get('inputTime'),
            'handoverTool': request.args.get('handoverTool'),
            'deviceHealth': request.args.get('deviceHealth'),
            'environmentHealth': request.args.get('environmentHealth'),
            'successor': request.args.get('successor'),
            'handoverPerson': request.args.get('handoverPerson'),
            'groupp': request.args.get('groupp'),
            'classes': request.args.get('classes'),
            'subTime': request.args.get('subTime'),
            'sub': request.args.get('sub')
        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_dryTwoA(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误



#干燥二-----------------------------------------------------------------------------------------------


#蒸发一-----------------------------------------------------------------------------------------------



@app.route('/noWatterA/list', methods=['GET']) # 按查询时间范围列出蒸发的全部信息
def noWatterA_list():
    try:
        # 获取分页参数和查询时间范围
        page = request.args.get('page', 1, type=int)  # 默认第1页
        perPage = request.args.get('perPage', 24, type=int)  # 默认每页10条
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print(type(start_time))
        print("Received start time:", start_time)
        print("Received end time:", end_time)

        # 计算查询的偏移量
        offset = (page - 1) * perPage

        # 构造查询
        query_base = "SELECT * FROM nowatera"
        params = []

        if start_time and end_time:
            query = f"{query_base} WHERE inputTime BETWEEN %s AND %s LIMIT %s OFFSET %s"
            params = [start_time, end_time, perPage, offset]
        else:

            query = f"{query_base} WHERE inputTime BETWEEN %s AND %s LIMIT %s OFFSET %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")

            end_time = d1_at_midnight + timedelta(hours=23, minutes=59, seconds=59)
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

            params = [start_time, end_time, perPage, offset]

            # 执行查询
        cursor.execute(query, params)
        data = cursor.fetchall()

        # 获取总记录数（用于分页计算）
        total_query = "SELECT COUNT(*) FROM nowatera"
        if start_time and end_time:
            total_query += " WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(total_query, (start_time, end_time))
            db.commit()
        else:
            cursor.execute(total_query)
            db.commit()
        totalCount = cursor.fetchone()[0]

        # 计算总页数
        totalPages = (totalCount // perPage) + (1 if totalCount % perPage > 0 else 0)

        # 转换数据为字典列表
        result = []
        if data:
            for i in data:
                result.append({
                    "id": i[0],
                    "inputTime": i[1],
                    "submitTime": i[2],
                    "mainPreesure": i[3],
                    "mainTemp": i[4],
                    "mainliu": i[5],
                    "EVPressureA": i[6],
                    "EVJinA": i[7],
                    "EVChuA": i[8],
                    "EVPressureB": i[9],
                    "EVJinB": i[10],
                    "EVChuB": i[11],
                    "EVPressureC": i[12],
                    "EVJinC": i[13],
                    "EVChuC": i[14],
                    "EVPressureD": i[15],
                    "EVJinD": i[16],
                    "EVChuD": i[17],
                    "EVPressureE": i[18],
                    "EVJinE": i[19],
                    "EVChuE": i[20],
                    "HDJin": i[21],
                    "HDChu": i[22],
                    'HDkpa': i[23],
                    'totalliu': i[24],
                    'totalTemp': i[25],
                })

        # 构造包含分页信息的响应
        response = {
            'data': result,
            'pagination': {
                'page': page,
                'perPage': perPage,
                'totalCount': totalCount,
                'totalPages': totalPages
            }
        }

        return jsonify(response)
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500


@app.route('/noWaterA/update', methods=['GET']) # 更新表2的数据,根据数据库里面的id来更新
def noWaterA_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'inputTime': request.args.get('inputTime'),
            'submitTime': request.args.get('submitTime'),
            'mainPreesure': request.args.get('mainPreesure'),
            'mainTemp': request.args.get('mainTemp'),
            'mainliu': request.args.get('mainliu'),
            'EVPressureA': request.args.get('EVPressureA'),
            'EVJinA': request.args.get('EVJinA'),
            'EVChuA': request.args.get('EVChuA'),
            'EVPressureB': request.args.get('EVPressureB'),
            'EVJinB': request.args.get('EVJinB'),
            'EVChuB': request.args.get('EVChuB'),
            'EVPressureC': request.args.get('EVPressureC'),
            'EVJinC': request.args.get('EVJinC'),
            'EVChuC': request.args.get('EVChuC'),
            'EVPressureD': request.args.get('EVPressureD'),
            'EVJinD': request.args.get('EVJinD'),
            'EVChuD': request.args.get('EVChuD'),
            'EVPressureE': request.args.get('EVPressureE'),
            'EVJinE': request.args.get('EVJinE'),
            'EVChuE': request.args.get('EVChuE'),
            'HDJin': request.args.get('HDJin'),
            'HDChu': request.args.get('HDChu'),
            'HDkpa': request.args.get('HDkpa'),
            'totalliu': request.args.get('totalliu'),
            'totalTemp': request.args.get('totalTemp'),

        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_noWaterA(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误


# 更新记录的函数
def update_record_noWaterA(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE nowatera SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()


@app.route('/noWaterAa/list', methods=['GET']) # 列出干燥二备注
def noWaterAa_list():
    try:
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print("Received start time:", start_time)
        print("Received end time:", end_time)
        # 构造查询
        # query_base = "SELECT * FROM beizhu_1"

        if start_time and end_time:
            query = "SELECT * FROM nowateraa WHERE inputTime BETWEEN %s AND %s"
            # query = f"{query_base} WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()  # (这个不写就无法实时更新)
        else:
            # cursor.execute("SELECT * FROM beizhu_1")
            query = "SELECT * FROM nowateraa WHERE inputTime BETWEEN %s AND %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")

            end_time = d1_at_midnight + timedelta(hours=23, minutes=59, seconds=59)
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()
        temp = {}
        result = []
        if data:
            for i in data:
                temp["id"] = i[0]
                temp["inputTime"] = i[1]
                temp["handoverTool"] = i[2]
                temp["deviceHealth"] = i[3]
                temp["environmentHealth"] = i[4]
                temp["successor"] = i[5]
                temp["handoverPerson"] = i[6]
                temp["groupp"] = i[7]
                temp["classes"] = i[8]
                temp["subTime"] = i[9]
                temp["sub"] = i[10]
                result.append(temp.copy())
            print("result: ", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

@app.route('/noWaterAa/add', methods=['GET'])  # 表2备注表添加
def noWaterAa_add():
    try:
        # inputTime = request.args.get("inputTime")  # 这里使用form获取数据,可能后面要用json？,现在改为params,也就是args
        handoverTool = request.args.get("handoverTool")
        deviceHealth = request.args.get("deviceHealth")
        environmentHealth = request.args.get("environmentHealth")
        successor = request.args.get("successor")
        handoverPerson = request.args.get("handoverPerson")
        groupp = request.args.get("groupp")
        classes = request.args.get("classes")
        subTime = request.args.get("subTime")
        sub = request.args.get("sub")

        # 获取当前时间段的 inputTime 和 sub
        inputTime, default_sub = get_time_and_sub3()

        if not sub:
            sub = default_sub  # 使用函数返回的默认值

        # 检查是否已经有该时间段的记录
        if inputTime:
            if check_existing_record3(inputTime):
                return jsonify({"error": "数据已存在，添加失败"}), 400

        try:
            sql = "INSERT INTO nowateraa(inputTime, handoverTool,deviceHealth,environmentHealth,successor,handoverPerson,groupp,classes,subTime,sub) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s,%s)"  # 修改SQL语句以包含password字段
            cursor.execute(sql,
                           [inputTime, handoverTool, deviceHealth, environmentHealth, successor, handoverPerson, groupp,
                            classes, subTime, sub])
            db.commit()
            print("add a new successfully")
            return jsonify({"msg": "添加成功"}), 200  # 使用标准的HTTP状态码
        except Exception as e:
            print("add a new failed:", e)
            db.rollback()  # 把前面操作撤回
            return jsonify({"error": "添加失败", "exception": str(e)}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

# 辅助函数：检查当前时间并返回对应的 inputTime 和 sub
def get_time_and_sub3():
    try:
        # 获取当前日期和时间
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式

        # 7:00 到 9:00
        if 7 <= current_time.hour < 9:
            return f"{current_date} 07:30:00", "8:00"

        # 15:00 到 17:00
        elif 15 <= current_time.hour < 17:
            return f"{current_date} 15:30:00", "16:00"

        # 22:00 到 23:59
        elif 22 <= current_time.hour < 24:
            return f"{current_date} 23:30:00", "0:00"

        # 其他时间不允许插入
        else:
            return None, None
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

# 检查是否已存在该时间段的记录
def check_existing_record3(inputTime):
    try:
        sql = "SELECT COUNT(*) FROM nowateraa WHERE inputTime = %s"
        cursor.execute(sql, (inputTime,))
        count = cursor.fetchone()[0]
        if count > 0:
            return True  # 数据已存在
        else:
            return False  # 数据不存在
    except Exception as e:
        print(f"Error checking existing record: {e}")
        return False


@app.route('/noWaterAa/del', methods=['GET'])  # 表2备注表删除
def noWaterAa_del():
    #id = request.form.get("id")
    try:
        id = request.args.get('id')
        sql = "DELETE FROM nowateraa WHERE id = %s"
        cursor.execute(sql, [id])
        db.commit()
        print("del a user successfully")
        return jsonify(msg="删除成功")
    except Exception as e:
        print("del a user failed: ", e)
        db.rollback()  # 把前面操作撤回
        return jsonify(msg="删除失败")


# 更新记录的函数      备注表的更新！ 注意函数名字别重复了 ！！！！！！！！！！
def update_record_noWaterAa(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE nowateraa SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()


@app.route('/noWaterAa/update', methods=['GET']) # 更新表2备注表表的数据,根据数据库里面的id来更新
def noWaterAa_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')
        groupp = request.args.get('groupp')
        print(type(groupp))

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'inputTime': request.args.get('inputTime'),
            'handoverTool': request.args.get('handoverTool'),
            'deviceHealth': request.args.get('deviceHealth'),
            'environmentHealth': request.args.get('environmentHealth'),
            'successor': request.args.get('successor'),
            'handoverPerson': request.args.get('handoverPerson'),
            'groupp': request.args.get('groupp'),
            'classes': request.args.get('classes'),
            'subTime': request.args.get('subTime'),
            'sub': request.args.get('sub')
        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_noWaterAa(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误




#蒸发一-----------------------------------------------------------------------------------------------


#蒸发二-----------------------------------------------------------------------------------------------



@app.route('/noWatterB/list', methods=['GET']) # 按查询时间范围列出蒸发的全部信息
def noWatterB_list():
    try:
        # 获取分页参数和查询时间范围
        page = request.args.get('page', 1, type=int)  # 默认第1页
        perPage = request.args.get('perPage', 24, type=int)  # 默认每页10条
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print(type(start_time))
        print("Received start time:", start_time)
        print("Received end time:", end_time)

        # 计算查询的偏移量
        offset = (page - 1) * perPage

        # 构造查询
        query_base = "SELECT * FROM nowaterb"
        params = []

        if start_time and end_time:
            query = f"{query_base} WHERE inputTime BETWEEN %s AND %s LIMIT %s OFFSET %s"
            params = [start_time, end_time, perPage, offset]
        else:

            query = f"{query_base} WHERE inputTime BETWEEN %s AND %s LIMIT %s OFFSET %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")

            end_time = d1_at_midnight + timedelta(hours=23, minutes=59, seconds=59)
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

            params = [start_time, end_time, perPage, offset]

            # 执行查询
        cursor.execute(query, params)
        data = cursor.fetchall()

        # 获取总记录数（用于分页计算）
        total_query = "SELECT COUNT(*) FROM nowaterb"
        if start_time and end_time:
            total_query += " WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(total_query, (start_time, end_time))
            db.commit()
        else:
            cursor.execute(total_query)
            db.commit()
        totalCount = cursor.fetchone()[0]

        # 计算总页数
        totalPages = (totalCount // perPage) + (1 if totalCount % perPage > 0 else 0)

        # 转换数据为字典列表
        result = []
        if data:
            for i in data:
                result.append({
                    "id": i[0],
                    "inputTime": i[1],
                    "submitTime": i[2],
                    "TempA": i[3],
                    "TempB": i[4],
                    "TempC": i[5],
                    "TempD": i[6],
                    "TempE": i[7],
                    "TempAA": i[8],
                    "TempBB": i[9],
                    "TempCC": i[10],
                    "TempDD": i[11],
                    "TempEE": i[12],

                    "TempAAA": i[13],
                    "TempBBB": i[14],
                    "TempCCC": i[15],
                    "TempDDD": i[16],
                    "TempEEE": i[17],

                    "TempAAAA": i[18],
                    "TempBBBB": i[19],
                    "TempCCCC": i[20],
                    "TempDDDD": i[21],
                    "TempEEEE": i[22],

                    'TempAAAAA': i[23],
                    'TempBBBBB': i[24],
                    'TempCCCCC': i[25],
                    'TempDDDDD': i[26],
                    'TempEEEEE': i[27],
                    'TempX': i[28],
                    'TempXX': i[29],
                    'TempXXX': i[30],
                    'TempXXXX': i[31],
                    'TempXXXXX': i[32],
                    'TempLow': i[33],
                    'TempLowa': i[34],

                })

        # 构造包含分页信息的响应
        response = {
            'data': result,
            'pagination': {
                'page': page,
                'perPage': perPage,
                'totalCount': totalCount,
                'totalPages': totalPages
            }
        }

        return jsonify(response)
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500


@app.route('/noWaterB/update', methods=['GET']) # 更新表2的数据,根据数据库里面的id来更新
def noWaterB_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'inputTime': request.args.get('inputTime'),
            'submitTime': request.args.get('submitTime'),
            'TempA': request.args.get('TempA'),
            'TempB': request.args.get('TempB'),
            'TempC': request.args.get('TempC'),
            'TempD': request.args.get('TempD'),
            'TempE': request.args.get('TempE'),
            'TempAA': request.args.get('TempAA'),
            'TempBB': request.args.get('TempBB'),
            'TempCC': request.args.get('TempCC'),
            'TempDD': request.args.get('TempDD'),
            'TempEE': request.args.get('TempEE'),
            'TempAAA': request.args.get('TempAAA'),
            'TempBBB': request.args.get('TempBBB'),
            'TempCCC': request.args.get('TempCCC'),
            'TempDDD': request.args.get('TempDDD'),
            'TempEEE': request.args.get('TempEEE'),
            'TempAAAA': request.args.get('TempAAAA'),
            'TempBBBB': request.args.get('TempBBBB'),
            'TempCCCC': request.args.get('TempCCCC'),
            'TempDDDD': request.args.get('TempDDDD'),
            'TempEEEE': request.args.get('TempEEEE'),
            'TempAAAAA': request.args.get('TempAAAAA'),
            'TempBBBBB': request.args.get('TempBBBBB'),
            'TempCCCCC': request.args.get('TempCCCCC'),
            'TempDDDDD': request.args.get('TempDDDDD'),
            'TempEEEEE': request.args.get('TempEEEEE'),
            'TempX': request.args.get('TempX'),
            'TempXX': request.args.get('TempXX'),
            'TempXXX': request.args.get('TempXXX'),
            'TempXXXX': request.args.get('TempXXXX'),
            'TempXXXXX': request.args.get('TempXXXXX'),
            'TempLow': request.args.get('TempLow'),
            'TempLowa': request.args.get('TempLowa'),

        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_noWaterB(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误


# 更新记录的函数
def update_record_noWaterB(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE nowaterb SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()


@app.route('/noWaterBb/list', methods=['GET']) # 列出干燥二备注
def noWaterBb_list():
    try:
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print("Received start time:", start_time)
        print("Received end time:", end_time)
        # 构造查询
        # query_base = "SELECT * FROM beizhu_1"

        if start_time and end_time:
            query = "SELECT * FROM nowaterbb WHERE inputTime BETWEEN %s AND %s"
            # query = f"{query_base} WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()  # (这个不写就无法实时更新)
        else:
            # cursor.execute("SELECT * FROM beizhu_1")
            query = "SELECT * FROM nowaterbb WHERE inputTime BETWEEN %s AND %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")

            end_time = d1_at_midnight + timedelta(hours=23, minutes=59, seconds=59)
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()
        temp = {}
        result = []
        if data:
            for i in data:
                temp["id"] = i[0]
                temp["inputTime"] = i[1]
                temp["handoverTool"] = i[2]
                temp["deviceHealth"] = i[3]
                temp["environmentHealth"] = i[4]
                temp["successor"] = i[5]
                temp["handoverPerson"] = i[6]
                temp["groupp"] = i[7]
                temp["classes"] = i[8]
                temp["subTime"] = i[9]
                temp["sub"] = i[10]
                result.append(temp.copy())
            print("result: ", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

@app.route('/noWaterBb/add', methods=['GET'])  # 表2备注表添加
def noWaterBb_add():
    try:
        # inputTime = request.args.get("inputTime")  # 这里使用form获取数据,可能后面要用json？,现在改为params,也就是args
        handoverTool = request.args.get("handoverTool")
        deviceHealth = request.args.get("deviceHealth")
        environmentHealth = request.args.get("environmentHealth")
        successor = request.args.get("successor")
        handoverPerson = request.args.get("handoverPerson")
        groupp = request.args.get("groupp")
        classes = request.args.get("classes")
        subTime = request.args.get("subTime")
        sub = request.args.get("sub")

        # 获取当前时间段的 inputTime 和 sub
        inputTime, default_sub = get_time_and_sub4()

        if not sub:
            sub = default_sub  # 使用函数返回的默认值

        # 检查是否已经有该时间段的记录
        if inputTime:
            if check_existing_record4(inputTime):
                return jsonify({"error": "数据已存在，添加失败"}), 400

        try:
            sql = "INSERT INTO nowaterbb(inputTime, handoverTool,deviceHealth,environmentHealth,successor,handoverPerson,groupp,classes,subTime,sub) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s,%s)"  # 修改SQL语句以包含password字段
            cursor.execute(sql,
                           [inputTime, handoverTool, deviceHealth, environmentHealth, successor, handoverPerson, groupp,
                            classes, subTime, sub])
            db.commit()
            print("add a new successfully")
            return jsonify({"msg": "添加成功"}), 200  # 使用标准的HTTP状态码
        except Exception as e:
            print("add a new failed:", e)
            db.rollback()  # 把前面操作撤回
            return jsonify({"error": "添加失败", "exception": str(e)}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

# 辅助函数：检查当前时间并返回对应的 inputTime 和 sub
def get_time_and_sub4():
    try:
        # 获取当前日期和时间
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式

        # 7:00 到 9:00
        if 7 <= current_time.hour < 9:
            return f"{current_date} 07:30:00", "8:00"

        # 15:00 到 17:00
        elif 15 <= current_time.hour < 17:
            return f"{current_date} 15:30:00", "16:00"

        # 22:00 到 23:59
        elif 22 <= current_time.hour < 24:
            return f"{current_date} 23:30:00", "0:00"

        # 其他时间不允许插入
        else:
            return None, None
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

# 检查是否已存在该时间段的记录
def check_existing_record4(inputTime):
    try:
        sql = "SELECT COUNT(*) FROM nowaterbb WHERE inputTime = %s"
        cursor.execute(sql, (inputTime,))
        count = cursor.fetchone()[0]
        if count > 0:
            return True  # 数据已存在
        else:
            return False  # 数据不存在
    except Exception as e:
        print(f"Error checking existing record: {e}")
        return False


@app.route('/noWaterBb/del', methods=['GET'])  # 表2备注表删除
def noWaterBb_del():
    #id = request.form.get("id")
    try:
        id = request.args.get('id')
        sql = "DELETE FROM nowaterbb WHERE id = %s"
        cursor.execute(sql, [id])
        db.commit()
        print("del a user successfully")
        return jsonify(msg="删除成功")
    except Exception as e:
        print("del a user failed: ", e)
        db.rollback()  # 把前面操作撤回
        return jsonify(msg="删除失败")


# 更新记录的函数      备注表的更新！ 注意函数名字别重复了 ！！！！！！！！！！
def update_record_noWaterBb(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE nowaterbb SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()


@app.route('/noWaterBb/update', methods=['GET']) # 更新表2备注表表的数据,根据数据库里面的id来更新
def noWaterBb_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')
        groupp = request.args.get('groupp')
        print(type(groupp))

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'inputTime': request.args.get('inputTime'),
            'handoverTool': request.args.get('handoverTool'),
            'deviceHealth': request.args.get('deviceHealth'),
            'environmentHealth': request.args.get('environmentHealth'),
            'successor': request.args.get('successor'),
            'handoverPerson': request.args.get('handoverPerson'),
            'groupp': request.args.get('groupp'),
            'classes': request.args.get('classes'),
            'subTime': request.args.get('subTime'),
            'sub': request.args.get('sub')
        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_noWaterBb(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误




#蒸发二-----------------------------------------------------------------------------------------------


#蒸发四-----------------------------------------------------------------------------------------------


@app.route('/noWatterD/list', methods=['GET']) # 按查询时间范围列出蒸发的全部信息
def noWatterD_list():
    try:
        # 获取分页参数和查询时间范围
        page = request.args.get('page', 1, type=int)  # 默认第1页
        perPage = request.args.get('perPage', 24, type=int)  # 默认每页10条
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print(type(start_time))
        print("Received start time:", start_time)
        print("Received end time:", end_time)

        # 计算查询的偏移量
        offset = (page - 1) * perPage

        # 构造查询
        query_base = "SELECT * FROM nowaterc"
        params = []

        if start_time and end_time:
            query = f"{query_base} WHERE inputTime BETWEEN %s AND %s LIMIT %s OFFSET %s"
            params = [start_time, end_time, perPage, offset]
        else:

            query = f"{query_base} WHERE inputTime BETWEEN %s AND %s LIMIT %s OFFSET %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")

            end_time = d1_at_midnight + timedelta(hours=23, minutes=59, seconds=59)
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

            params = [start_time, end_time, perPage, offset]

            # 执行查询
        cursor.execute(query, params)
        data = cursor.fetchall()

        # 获取总记录数（用于分页计算）
        total_query = "SELECT COUNT(*) FROM nowaterc"
        if start_time and end_time:
            total_query += " WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(total_query, (start_time, end_time))
            db.commit()
        else:
            cursor.execute(total_query)
            db.commit()
        totalCount = cursor.fetchone()[0]

        # 计算总页数
        totalPages = (totalCount // perPage) + (1 if totalCount % perPage > 0 else 0)

        # 转换数据为字典列表
        result = []
        if data:
            for i in data:
                result.append({
                    "id": i[0],
                    "inputTime": i[1],
                    "submitTime": i[2],
                    "AcurrentA": i[3],
                    "ApressureA": i[4],
                    "AcurrentB": i[5],
                    "ApressureB": i[6],
                    "BcurrentA": i[7],
                    "BpressureA": i[8],
                    "BcurrentB": i[9],
                    "BpressureB": i[10],
                    "BcurrentC": i[11],
                    "BpressureC": i[12],

                    "CcurrentA": i[13],
                    "CpressureA": i[14],
                    "CcurrentB": i[15],
                    "CpressureB": i[16],
                    "DcurrentA": i[17],

                    "DpressureA": i[18],
                    "DcurrentB": i[19],
                    "DpressureB": i[20],
                    "BpressureA1": i[21],
                    "BpressureB1": i[22],
                    "BpressureC1": i[23],
                    "DpressureB1": i[24],
                    "DpressureA1": i[25],


                })

        # 构造包含分页信息的响应
        response = {
            'data': result,
            'pagination': {
                'page': page,
                'perPage': perPage,
                'totalCount': totalCount,
                'totalPages': totalPages
            }
        }

        return jsonify(response)
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500


@app.route('/noWaterD/update', methods=['GET']) # 更新表2的数据,根据数据库里面的id来更新
def noWaterD_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'inputTime': request.args.get('inputTime'),
            'submitTime': request.args.get('submitTime'),
            'AcurrentA': request.args.get('AcurrentA'),
            'ApressureA': request.args.get('ApressureA'),
            'AcurrentB': request.args.get('AcurrentB'),
            'ApressureB': request.args.get('ApressureB'),
            'BcurrentA': request.args.get('BcurrentA'),
            'BpressureA': request.args.get('BpressureA'),
            'BcurrentB': request.args.get('BcurrentB'),
            'BpressureB': request.args.get('BpressureB'),
            'BcurrentC': request.args.get('BcurrentC'),
            'BpressureC': request.args.get('BpressureC'),
            'CcurrentA': request.args.get('CcurrentA'),
            'CpressureA': request.args.get('CpressureA'),
            'CcurrentB': request.args.get('CcurrentB'),
            'CpressureB': request.args.get('CpressureB'),
            'DcurrentA': request.args.get('DcurrentA'),
            'DpressureA': request.args.get('DpressureA'),
            'DcurrentB': request.args.get('DcurrentB'),
            'DpressureB': request.args.get('DpressureB'),

            'BpressureA1': request.args.get('BpressureA1'),
            'BpressureB1': request.args.get('BpressureB1'),
            'BpressureC1': request.args.get('BpressureC1'),
            'DpressureB1': request.args.get('DpressureB1'),
            'DpressureA1': request.args.get('DpressureA1'),

        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_noWaterD(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500


# 更新记录的函数
def update_record_noWaterD(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE nowaterc SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()


@app.route('/noWaterDd/list', methods=['GET']) # 列出干燥二备注
def noWaterCc_list():
    try:
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print("Received start time:", start_time)
        print("Received end time:", end_time)
        # 构造查询
        # query_base = "SELECT * FROM beizhu_1"

        if start_time and end_time:
            query = "SELECT * FROM nowatercc WHERE inputTime BETWEEN %s AND %s"
            # query = f"{query_base} WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()  # (这个不写就无法实时更新)
        else:
            # cursor.execute("SELECT * FROM beizhu_1")
            query = "SELECT * FROM nowatercc WHERE inputTime BETWEEN %s AND %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")

            end_time = d1_at_midnight + timedelta(hours=23, minutes=59, seconds=59)
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()
        temp = {}
        result = []
        if data:
            for i in data:
                temp["id"] = i[0]
                temp["inputTime"] = i[1]
                temp["handoverTool"] = i[2]
                temp["deviceHealth"] = i[3]
                temp["environmentHealth"] = i[4]
                temp["successor"] = i[5]
                temp["handoverPerson"] = i[6]
                temp["groupp"] = i[7]
                temp["classes"] = i[8]
                temp["subTime"] = i[9]
                temp["sub"] = i[10]
                result.append(temp.copy())
            print("result: ", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

@app.route('/noWaterDd/add', methods=['GET'])  # 表2备注表添加
def noWaterCc_add():
    try:
        # inputTime = request.args.get("inputTime")  # 这里使用form获取数据,可能后面要用json？,现在改为params,也就是args
        handoverTool = request.args.get("handoverTool")
        deviceHealth = request.args.get("deviceHealth")
        environmentHealth = request.args.get("environmentHealth")
        successor = request.args.get("successor")
        handoverPerson = request.args.get("handoverPerson")
        groupp = request.args.get("groupp")
        classes = request.args.get("classes")
        subTime = request.args.get("subTime")
        sub = request.args.get("sub")

        # 获取当前时间段的 inputTime 和 sub
        inputTime, default_sub = get_time_and_sub5()

        if not sub:
            sub = default_sub  # 使用函数返回的默认值

        # 检查是否已经有该时间段的记录
        if inputTime:
            if check_existing_record5(inputTime):
                return jsonify({"error": "数据已存在，添加失败"}), 400

        try:
            sql = "INSERT INTO nowatercc(inputTime, handoverTool,deviceHealth,environmentHealth,successor,handoverPerson,groupp,classes,subTime,sub) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s,%s)"  # 修改SQL语句以包含password字段
            cursor.execute(sql,
                           [inputTime, handoverTool, deviceHealth, environmentHealth, successor, handoverPerson, groupp,
                            classes, subTime, sub])
            db.commit()
            print("add a new successfully")
            return jsonify({"msg": "添加成功"}), 200  # 使用标准的HTTP状态码
        except Exception as e:
            print("add a new failed:", e)
            db.rollback()  # 把前面操作撤回
            return jsonify({"error": "添加失败", "exception": str(e)}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500

# 辅助函数：检查当前时间并返回对应的 inputTime 和 sub
def get_time_and_sub5():
    try:
        # 获取当前日期和时间
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式

        # 7:00 到 9:00
        if 7 <= current_time.hour < 9:
            return f"{current_date} 07:30:00", "8:00"

        # 15:00 到 17:00
        elif 15 <= current_time.hour < 17:
            return f"{current_date} 15:30:00", "16:00"

        # 22:00 到 23:59
        elif 22 <= current_time.hour < 24:
            return f"{current_date} 23:30:00", "0:00"

        # 其他时间不允许插入
        else:
            return None, None
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

# 检查是否已存在该时间段的记录
def check_existing_record5(inputTime):
    try:
        sql = "SELECT COUNT(*) FROM nowatercc WHERE inputTime = %s"
        cursor.execute(sql, (inputTime,))
        count = cursor.fetchone()[0]
        if count > 0:
            return True  # 数据已存在
        else:
            return False  # 数据不存在
    except Exception as e:
        print(f"Error checking existing record: {e}")
        return False


@app.route('/noWaterDd/del', methods=['GET'])  # 表2备注表删除
def noWaterCc_del():
    #id = request.form.get("id")
    try:
        id = request.args.get('id')
        sql = "DELETE FROM nowatercc WHERE id = %s"
        cursor.execute(sql, [id])
        db.commit()
        print("del a user successfully")
        return jsonify(msg="删除成功")
    except Exception as e:
        print("del a user failed: ", e)
        db.rollback()  # 把前面操作撤回
        return jsonify(msg="删除失败")


# 更新记录的函数      备注表的更新！ 注意函数名字别重复了 ！！！！！！！！！！
def update_record_noWaterCc(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE nowatercc SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()


@app.route('/noWaterDd/update', methods=['GET']) # 更新表2备注表表的数据,根据数据库里面的id来更新
def noWaterCc_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')
        groupp = request.args.get('groupp')
        print(type(groupp))

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'inputTime': request.args.get('inputTime'),
            'handoverTool': request.args.get('handoverTool'),
            'deviceHealth': request.args.get('deviceHealth'),
            'environmentHealth': request.args.get('environmentHealth'),
            'successor': request.args.get('successor'),
            'handoverPerson': request.args.get('handoverPerson'),
            'groupp': request.args.get('groupp'),
            'classes': request.args.get('classes'),
            'subTime': request.args.get('subTime'),
            'sub': request.args.get('sub')
        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_noWaterCc(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error updating record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500


#蒸发四-----------------------------------------------------------------------------------------------



#空压机-----------------------------------------------------------------------------------------------


@app.route('/noWatterE/list', methods=['GET']) # 按查询时间范围列出蒸发的全部信息
def noWatterE_list():
    try:
        # 获取分页参数和查询时间范围
        page = request.args.get('page', 1, type=int)  # 默认第1页
        perPage = request.args.get('perPage', 24, type=int)  # 默认每页10条
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print(type(start_time))
        print("Received start time:", start_time)
        print("Received end time:", end_time)

        # 计算查询的偏移量
        offset = (page - 1) * perPage

        # 构造查询
        query_base = "SELECT * FROM airpressure"
        params = []

        if start_time and end_time:
            query = f"{query_base} WHERE inputTime BETWEEN %s AND %s LIMIT %s OFFSET %s"
            params = [start_time, end_time, perPage, offset]
        else:

            query = f"{query_base} WHERE inputTime BETWEEN %s AND %s LIMIT %s OFFSET %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")

            end_time = d1_at_midnight + timedelta(hours=23, minutes=59, seconds=59)
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

            params = [start_time, end_time, perPage, offset]

            # 执行查询
        cursor.execute(query, params)
        data = cursor.fetchall()

        # 获取总记录数（用于分页计算）
        total_query = "SELECT COUNT(*) FROM airpressure"
        if start_time and end_time:
            total_query += " WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(total_query, (start_time, end_time))
            db.commit()
        else:
            cursor.execute(total_query)
            db.commit()
        totalCount = cursor.fetchone()[0]

        # 计算总页数
        totalPages = (totalCount // perPage) + (1 if totalCount % perPage > 0 else 0)

        # 转换数据为字典列表
        result = []
        if data:
            for i in data:
                result.append({
                    "id": i[0],
                    "inputTime": i[1],
                    "submitTime": i[2],
                    "TempA": i[3],
                    "TempB": i[4],
                    "TempC": i[5],
                    "TempD": i[6],
                    "TempE": i[7],
                    "TempAA": i[8],
                    "TempBB": i[9],
                    "TempCC": i[10],
                    "TempDD": i[11],
                    "TempEE": i[12],

                    "TempAAA": i[13],
                    "TempBBB": i[14],
                    "TempCCC": i[15],
                    "TempDDD": i[16],
                    "TempEEE": i[17],

                    "TempAAAA": i[18],
                    "TempBBBB": i[19],
                    "TempCCCC": i[20],
                    "TempDDDD": i[21],
                    "TempEEEE": i[22],
                    'TempAAAAA': i[23],
                    'TempBBBBB': i[24],
                    'TempCCCCC': i[25],
                    'TempDDDDD': i[26],
                    'TempEEEEE': i[27],
                    'TempX': i[28],
                    'TempXX': i[29],

                })

        # 构造包含分页信息的响应
        response = {
            'data': result,
            'pagination': {
                'page': page,
                'perPage': perPage,
                'totalCount': totalCount,
                'totalPages': totalPages
            }
        }

        return jsonify(response)
    except Exception as e:
        print("Error reading data:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500


@app.route('/noWaterE/update', methods=['GET']) # 更新表2的数据,根据数据库里面的id来更新
def noWaterE_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'inputTime': request.args.get('inputTime'),
            'submitTime': request.args.get('submitTime'),
            'TempA': request.args.get('TempA'),
            'TempB': request.args.get('TempB'),
            'TempC': request.args.get('TempC'),
            'TempD': request.args.get('TempD'),
            'TempE': request.args.get('TempE'),
            'TempAA': request.args.get('TempAA'),
            'TempBB': request.args.get('TempBB'),
            'TempCC': request.args.get('TempCC'),
            'TempDD': request.args.get('TempDD'),
            'TempEE': request.args.get('TempEE'),
            'TempAAA': request.args.get('TempAAA'),
            'TempBBB': request.args.get('TempBBB'),
            'TempCCC': request.args.get('TempCCC'),
            'TempDDD': request.args.get('TempDDD'),
            'TempEEE': request.args.get('TempEEE'),
            'TempAAAA': request.args.get('TempAAAA'),
            'TempBBBB': request.args.get('TempBBBB'),
            'TempCCCC': request.args.get('TempCCCC'),
            'TempDDDD': request.args.get('TempDDDD'),
            'TempEEEE': request.args.get('TempEEEE'),
            'TempAAAAA': request.args.get('TempAAAAA'),
            'TempBBBBB': request.args.get('TempBBBBB'),
            'TempCCCCC': request.args.get('TempCCCCC'),
            'TempDDDDD': request.args.get('TempDDDDD'),
            'TempEEEEE': request.args.get('TempEEEEE'),
            'TempX': request.args.get('TempX'),
            'TempXX': request.args.get('TempXX'),

        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_noWaterE(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error updating record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500


# 更新记录的函数
def update_record_noWaterE(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE airpressure SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()


@app.route('/noWaterEE/list', methods=['GET']) # 列出干燥二备注
def noWaterEE_list():
    try:
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print("Received start time:", start_time)
        print("Received end time:", end_time)
        # 构造查询
        # query_base = "SELECT * FROM beizhu_1"

        if start_time and end_time:
            query = "SELECT * FROM airpressurea WHERE inputTime BETWEEN %s AND %s"
            # query = f"{query_base} WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()  # (这个不写就无法实时更新)
        else:
            # cursor.execute("SELECT * FROM beizhu_1")
            query = "SELECT * FROM airpressurea WHERE inputTime BETWEEN %s AND %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")

            end_time = d1_at_midnight + timedelta(hours=23, minutes=59, seconds=59)
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()
        temp = {}
        result = []
        if data:
            for i in data:
                temp["id"] = i[0]
                temp["inputTime"] = i[1]
                temp["handoverTool"] = i[2]
                temp["deviceHealth"] = i[3]
                temp["environmentHealth"] = i[4]
                temp["successor"] = i[5]
                temp["handoverPerson"] = i[6]
                temp["groupp"] = i[7]
                temp["classes"] = i[8]
                temp["subTime"] = i[9]
                temp["sub"] = i[10]
                result.append(temp.copy())
            print("result: ", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

@app.route('/noWaterEE/add', methods=['GET'])  # 表2备注表添加
def noWaterEE_add():
    try:
        # inputTime = request.args.get("inputTime")  # 这里使用form获取数据,可能后面要用json？,现在改为params,也就是args
        handoverTool = request.args.get("handoverTool")
        deviceHealth = request.args.get("deviceHealth")
        environmentHealth = request.args.get("environmentHealth")
        successor = request.args.get("successor")
        handoverPerson = request.args.get("handoverPerson")
        groupp = request.args.get("groupp")
        classes = request.args.get("classes")
        subTime = request.args.get("subTime")
        sub = request.args.get("sub")

        # 获取当前时间段的 inputTime 和 sub
        inputTime, default_sub = get_time_and_sub6()

        if not sub:
            sub = default_sub  # 使用函数返回的默认值

        # 检查是否已经有该时间段的记录
        if inputTime:
            if check_existing_record6(inputTime):
                return jsonify({"error": "数据已存在，添加失败"}), 400

        try:
            sql = "INSERT INTO airpressurea(inputTime, handoverTool,deviceHealth,environmentHealth,successor,handoverPerson,groupp,classes,subTime,sub) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s,%s)"  # 修改SQL语句以包含password字段
            cursor.execute(sql,
                           [inputTime, handoverTool, deviceHealth, environmentHealth, successor, handoverPerson, groupp,
                            classes, subTime, sub])
            db.commit()
            print("add a new successfully")
            return jsonify({"msg": "添加成功"}), 200  # 使用标准的HTTP状态码
        except Exception as e:
            print("add a new failed:", e)
            db.rollback()  # 把前面操作撤回
            return jsonify({"error": "添加失败", "exception": str(e)}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

# 辅助函数：检查当前时间并返回对应的 inputTime 和 sub
def get_time_and_sub6():
    try:
        # 获取当前日期和时间
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式

        # 7:00 到 9:00
        if 7 <= current_time.hour < 9:
            return f"{current_date} 07:30:00", "8:00"

        # 15:00 到 17:00
        elif 15 <= current_time.hour < 17:
            return f"{current_date} 15:30:00", "16:00"

        # 22:00 到 23:59
        elif 22 <= current_time.hour < 24:
            return f"{current_date} 23:30:00", "0:00"

        # 其他时间不允许插入
        else:
            return None, None
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

# 检查是否已存在该时间段的记录
def check_existing_record6(inputTime):
    try:
        sql = "SELECT COUNT(*) FROM airpressurea WHERE inputTime = %s"
        cursor.execute(sql, (inputTime,))
        count = cursor.fetchone()[0]
        if count > 0:
            return True  # 数据已存在
        else:
            return False  # 数据不存在
    except Exception as e:
        print(f"Error checking existing record: {e}")
        return False

@app.route('/noWaterEE/del', methods=['GET'])  # 表2备注表删除
def noWaterEE_del():
    #id = request.form.get("id")
    try:
        id = request.args.get('id')
        sql = "DELETE FROM airpressurea WHERE id = %s"
        cursor.execute(sql, [id])
        db.commit()
        print("del a user successfully")
        return jsonify(msg="删除成功")
    except Exception as e:
        print("del a user failed: ", e)
        db.rollback()  # 把前面操作撤回
        return jsonify(msg="删除失败")


# 更新记录的函数      备注表的更新！ 注意函数名字别重复了 ！！！！！！！！！！
def update_record_noWaterEE(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE airpressurea SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()


@app.route('/noWaterEE/update', methods=['GET']) # 更新表2备注表表的数据,根据数据库里面的id来更新
def noWaterEE_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')
        groupp = request.args.get('groupp')
        print(type(groupp))

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'inputTime': request.args.get('inputTime'),
            'handoverTool': request.args.get('handoverTool'),
            'deviceHealth': request.args.get('deviceHealth'),
            'environmentHealth': request.args.get('environmentHealth'),
            'successor': request.args.get('successor'),
            'handoverPerson': request.args.get('handoverPerson'),
            'groupp': request.args.get('groupp'),
            'classes': request.args.get('classes'),
            'subTime': request.args.get('subTime'),
            'sub': request.args.get('sub')
        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_noWaterEE(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误



#空压机-----------------------------------------------------------------------------------------------




#表3 原料盐车间亚铁氰化钾管理台账----------------------------------------------------------------------------------------


@app.route('/biao3/list', methods=['GET']) # 列出表3信息，默认查询当天，以及一周的数据
def biao3_list():
    try:
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print("Received start time:", start_time)
        print("Received end time:", end_time)
        # 构造查询
        # query_base = "SELECT * FROM beizhu_1"

        if start_time and end_time:
            query = "SELECT * FROM biao_3 WHERE collectionDate BETWEEN %s AND %s"
            # query = f"{query_base} WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()  # (这个不写就无法实时更新)
        else:
            # cursor.execute("SELECT * FROM beizhu_1")
            query = "SELECT * FROM biao_3 WHERE collectionDate BETWEEN %s AND %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")

            end_time = d1_at_midnight + timedelta(hours=24 * 30)
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()
        temp = {}
        result = []
        if data:
            for i in data:
                temp["id"] = i[0]
                temp["collectionDate"] = i[1]
                temp["manufacturer"] = i[2]
                temp["batchNumber"] = i[3]
                temp["fetchVolume"] = i[4]
                temp["deployDate"] = i[5]
                temp["deployVolume"] = i[6]
                temp["margin"] = i[7]
                temp["getMaterials"] = i[8]
                temp["supervisor"] = i[9]
                temp["storekeeper"] = i[10]
                temp["validity"] = i[11]
                temp["environment"] = i[12]
                result.append(temp.copy())
            print("result: ", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

@app.route('/biao3/del', methods=['GET'])  # 表3删除
def biao3_del():
    try:
        id = request.args.get('id')
        sql = "DELETE FROM biao_3 WHERE id = %s"
        cursor.execute(sql, [id])
        db.commit()
        print("del a user successfully")
        return jsonify(msg="删除成功")
    except Exception as e:
        print("del a user failed: ", e)
        db.rollback()  # 把前面操作撤回
        return jsonify(msg="删除失败")

def update_record_biao3(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE biao_3 SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()


@app.route('/biao3/update', methods=['GET']) # 更新表3的数据
def biao3_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'collectionDate': request.args.get('collectionDate'),
            'manufacturer': request.args.get('manufacturer'),
            'batchNumber': request.args.get('batchNumber'),
            'fetchVolume': request.args.get('fetchVolume'),
            'deployDate': request.args.get('deployDate'),
            'deployVolume': request.args.get('deployVolume'),
            'margin': request.args.get('margin'),
            'getMaterials': request.args.get('getMaterials'),
            'supervisor': request.args.get('supervisor'),
            'storekeeper': request.args.get('storekeeper'),
            'validity': request.args.get('validity'),
            'environment': request.args.get('environment'),
        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_biao3(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误


@app.route('/biao3/add', methods=['GET'])  # 表3添加
def biao3_add():
    try:
        collectionDate = request.args.get("collectionDate")  # 这里使用form获取数据,可能后面要用json？,现在改为params,也就是args
        manufacturer = request.args.get("manufacturer")
        batchNumber = request.args.get("batchNumber")
        fetchVolume = request.args.get("fetchVolume")
        deployDate = request.args.get("deployDate")
        deployVolume = request.args.get("deployVolume")
        margin = request.args.get("margin")
        getMaterials = request.args.get("getMaterials")
        supervisor = request.args.get("supervisor")
        storekeeper = request.args.get("storekeeper")
        validity = request.args.get("validity")
        environment = request.args.get("environment")

        try:
            sql = "INSERT INTO biao_3(collectionDate,manufacturer,batchNumber,fetchVolume,deployDate,deployVolume,margin,getMaterials,supervisor,storekeeper,validity,environment) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s,%s,%s,%s)"  # 修改SQL语句以包含password字段
            cursor.execute(sql,
                           [collectionDate, manufacturer, batchNumber, fetchVolume, deployDate, deployVolume, margin,
                            getMaterials, supervisor, storekeeper, validity, environment])
            db.commit()
            print("add a new successfully")
            return jsonify({"msg": "添加成功"}), 200  # 使用标准的HTTP状态码
        except Exception as e:
            print("add a new failed:", e)
            db.rollback()  # 把前面操作撤回
            return jsonify({"error": "添加失败", "exception": str(e)}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误



#表3 原料盐车间亚铁氰化钾管理台账----------------------------------------------------------------------------------------


#表4 add碘酸钾消耗记录  add (表示岗位记录)----------------------------------------------------------------------------------


@app.route('/biao4_add/list', methods=['GET']) # 列出表4信息，默认查询当天
def biao4_add_list():
    try:
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print("Received start time:", start_time)
        print("Received end time:", end_time)
        # 构造查询
        # query_base = "SELECT * FROM beizhu_1"

        if start_time and end_time:
            query = "SELECT * FROM biao_4_add WHERE biaoDate BETWEEN %s AND %s"
            # query = f"{query_base} WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()  # (这个不写就无法实时更新)
        else:
            # cursor.execute("SELECT * FROM beizhu_1")
            query = "SELECT * FROM biao_4_add WHERE biaoDate BETWEEN %s AND %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d")

            end_time = d1_at_midnight + timedelta(hours=23)
            end_time = end_time.strftime("%Y-%m-%d")

            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()
        temp = {}
        result = []
        if data:
            for i in data:
                temp["id"] = i[0]
                temp["biaoDate"] = i[1]
                temp["biaoTime"] = i[2]
                temp["pihao"] = i[3]
                temp["peijiliang"] = i[4]
                temp["tiji"] = i[5]
                temp["weizi"] = i[6]
                temp["peiR"] = i[7]
                temp["jiandur"] = i[8]
                temp["qingli"] = i[9]
                temp["jiandur1"] = i[10]
                temp["nongdu"] = i[11]
                temp["huayanR"] = i[12]
                result.append(temp.copy())
            print("result: ", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

@app.route('/biao4_add/del', methods=['GET'])  # 表4删除
def biao4_add_del():
    try:
        id = request.args.get('id')
        sql = "DELETE FROM biao_4_add WHERE id = %s"
        cursor.execute(sql, [id])
        db.commit()
        print("del a user successfully")
        return jsonify(msg="删除成功")
    except Exception as e:
        print("del a user failed: ", e)
        db.rollback()  # 把前面操作撤回
        return jsonify(msg="删除失败")


def update_record_biao4_add(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE biao_4_add SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()

@app.route('/biao4_add/update', methods=['GET']) # 更新表3的数据
def biao4_add_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'biaoDate': request.args.get('biaoDate'),
            'biaoTime': request.args.get('biaoTime'),
            'pihao': request.args.get('pihao'),
            'peijiliang': request.args.get('peijiliang'),
            'tiji': request.args.get('tiji'),
            'weizi': request.args.get('weizi'),
            'peiR': request.args.get('peiR'),
            'jiandur': request.args.get('jiandur'),
            'qingli': request.args.get('qingli'),
            'jiandur1': request.args.get('jiandur1'),
            'nongdu': request.args.get('nongdu'),
            'huayanR': request.args.get('huayanR')

        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_biao4_add(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误


@app.route('/biao4_add/add', methods=['GET'])  # 表4添加
def biao4_add_add():
    try:
        biaoDate = request.args.get("biaoDate")  # 这里使用form获取数据,可能后面要用json？,现在改为params,也就是args
        biaoTime = request.args.get("biaoTime")
        pihao = request.args.get("pihao")
        peijiliang = request.args.get("peijiliang")
        tiji = request.args.get("tiji")
        weizi = request.args.get("weizi")
        peiR = request.args.get("peiR")
        jiandur = request.args.get("jiandur")
        qingli = request.args.get("qingli")
        jiandur1 = request.args.get("jiandur1")
        nongdu = request.args.get("nongdu")
        huayanR = request.args.get("huayanR")

        try:  # 这里sql语句，表名很容易忘记要改
            sql = "INSERT INTO biao_4_add(biaoDate,biaoTime,pihao,peijiliang,tiji,weizi,peiR,jiandur,qingli,jiandur1,nongdu,huayanR) VALUES (%s, %s, %s, %s,%s, %s, %s,%s, %s, %s, %s,%s)"  # 修改SQL语句以包含password字段
            cursor.execute(sql,
                           [biaoDate, biaoTime, pihao, peijiliang, tiji, weizi, peiR, jiandur, qingli, jiandur1, nongdu,
                            huayanR])
            db.commit()
            print("add a new successfully")
            return jsonify({"msg": "添加成功"}), 200  # 使用标准的HTTP状态码
        except Exception as e:
            print("add a new failed:", e)
            db.rollback()  # 把前面操作撤回
            return jsonify({"error": "添加失败", "exception": str(e)}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误



#表4 add碘酸钾消耗记录  add (表示岗位记录)----------------------------------------------------------------------------------------


#表5 add亚铁氰化钾消耗记录  add (表示岗位记录)----------------------------------------------------------------------------------


@app.route('/biao5_add/list', methods=['GET']) # 列出表4信息，默认查询当天
def biao5_add_list():
    try:
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print("Received start time:", start_time)
        print("Received end time:", end_time)
        # 构造查询
        # query_base = "SELECT * FROM beizhu_1"

        if start_time and end_time:
            query = "SELECT * FROM biao_5_add WHERE biaoDate BETWEEN %s AND %s"
            # query = f"{query_base} WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()  # (这个不写就无法实时更新)
        else:
            # cursor.execute("SELECT * FROM beizhu_1")
            query = "SELECT * FROM biao_5_add WHERE biaoDate BETWEEN %s AND %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d")

            end_time = d1_at_midnight + timedelta(hours=23)
            end_time = end_time.strftime("%Y-%m-%d")

            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()
        temp = {}
        result = []
        if data:
            for i in data:
                temp["id"] = i[0]
                temp["biaoDate"] = i[1]
                temp["biaoTime"] = i[2]
                temp["pihao"] = i[3]
                temp["peijiliang"] = i[4]
                temp["tiji"] = i[5]
                temp["weizi"] = i[6]
                temp["peiR"] = i[7]
                temp["jiandur"] = i[8]
                temp["qingli"] = i[9]
                temp["jiandur1"] = i[10]
                result.append(temp.copy())
            print("result: ", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

@app.route('/biao5_add/del', methods=['GET'])  # 表4删除
def biao5_add_del():
    try:
        id = request.args.get('id')
        sql = "DELETE FROM biao_5_add WHERE id = %s"
        cursor.execute(sql, [id])
        db.commit()
        print("del a user successfully")
        return jsonify(msg="删除成功")
    except Exception as e:
        print("del a user failed: ", e)
        db.rollback()  # 把前面操作撤回
        return jsonify(msg="删除失败")


def update_record_biao5_add(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE biao_5_add SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()

@app.route('/biao5_add/update', methods=['GET']) # 更新表3的数据
def biao5_add_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'biaoDate': request.args.get('biaoDate'),
            'biaoTime': request.args.get('biaoTime'),
            'pihao': request.args.get('pihao'),
            'peijiliang': request.args.get('peijiliang'),
            'tiji': request.args.get('tiji'),
            'weizi': request.args.get('weizi'),
            'peiR': request.args.get('peiR'),
            'jiandur': request.args.get('jiandur'),
            'qingli': request.args.get('qingli'),
            'jiandur1': request.args.get('jiandur1'),

        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_biao5_add(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误


@app.route('/biao5_add/add', methods=['GET'])  # 表4添加
def biao5_add_add():
    try:
        biaoDate = request.args.get("biaoDate")  # 这里使用form获取数据,可能后面要用json？,现在改为params,也就是args
        biaoTime = request.args.get("biaoTime")
        pihao = request.args.get("pihao")
        peijiliang = request.args.get("peijiliang")
        tiji = request.args.get("tiji")
        weizi = request.args.get("weizi")
        peiR = request.args.get("peiR")
        jiandur = request.args.get("jiandur")
        qingli = request.args.get("qingli")
        jiandur1 = request.args.get("jiandur1")

        try:  # 这里sql语句，表名很容易忘记要改
            sql = "INSERT INTO biao_5_add(biaoDate,biaoTime,pihao,peijiliang,tiji,weizi,peiR,jiandur,qingli,jiandur1) VALUES ( %s, %s,%s, %s, %s,%s, %s, %s, %s,%s)"  # 修改SQL语句以包含password字段
            cursor.execute(sql, [biaoDate, biaoTime, pihao, peijiliang, tiji, weizi, peiR, jiandur, qingli, jiandur1])
            db.commit()
            print("add a new successfully")
            return jsonify({"msg": "添加成功"}), 200  # 使用标准的HTTP状态码
        except Exception as e:
            print("add a new failed:", e)
            db.rollback()  # 把前面操作撤回
            return jsonify({"error": "添加失败", "exception": str(e)}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误



#表5 亚铁氰化钾消耗记录  add (表示岗位记录)----------------------------------------------------------------------------------------




#表4 碘酸钾消耗记录----------------------------------------------------------------------------------------


@app.route('/biao4/list', methods=['GET']) # 列出表4信息，默认查询当天
def biao4_list():
    try:
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print("Received start time:", start_time)
        print("Received end time:", end_time)
        # 构造查询
        # query_base = "SELECT * FROM beizhu_1"

        if start_time and end_time:
            query = "SELECT * FROM biao_4 WHERE biaoDate BETWEEN %s AND %s"
            # query = f"{query_base} WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()  # (这个不写就无法实时更新)
        else:
            # cursor.execute("SELECT * FROM beizhu_1")
            query = "SELECT * FROM biao_4 WHERE biaoDate BETWEEN %s AND %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d")

            end_time = d1_at_midnight + timedelta(hours=23)
            end_time = end_time.strftime("%Y-%m-%d")

            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()
        temp = {}
        result = []
        if data:
            for i in data:
                temp["id"] = i[0]
                temp["biaoDate"] = i[1]
                temp["biaoTime"] = i[2]
                temp["disposition"] = i[3]
                temp["expend"] = i[4]
                temp["margin"] = i[5]
                temp["handoverPerson"] = i[6]
                temp["successor"] = i[7]
                result.append(temp.copy())
            print("result: ", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

@app.route('/biao4/del', methods=['GET'])  # 表4删除
def biao4_del():
    try:
        id = request.args.get('id')
        sql = "DELETE FROM biao_4 WHERE id = %s"
        cursor.execute(sql, [id])
        db.commit()
        print("del a user successfully")
        return jsonify(msg="删除成功")
    except Exception as e:
        print("del a user failed: ", e)
        db.rollback()  # 把前面操作撤回
        return jsonify(msg="删除失败")


def update_record_biao4(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE biao_4 SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()

@app.route('/biao4/update', methods=['GET']) # 更新表3的数据
def biao4_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'biaoDate': request.args.get('biaoDate'),
            'biaoTime': request.args.get('biaoTime'),
            'disposition': request.args.get('disposition'),
            'expend': request.args.get('expend'),
            'margin': request.args.get('margin'),
            'handoverPerson': request.args.get('handoverPerson'),
            'successor': request.args.get('successor'),

        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_biao4(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error updating record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误


@app.route('/biao4/add', methods=['GET'])  # 表4添加
def biao4_add():
    try:
        biaoDate = request.args.get("biaoDate")  # 这里使用form获取数据,可能后面要用json？,现在改为params,也就是args
        biaoTime = request.args.get("biaoTime")
        disposition = request.args.get("disposition")
        expend = request.args.get("expend")
        margin = request.args.get("margin")
        handoverPerson = request.args.get("handoverPerson")
        successor = request.args.get("successor")

        try:
            sql = "INSERT INTO biao_4(biaoDate,biaoTime,disposition,expend,margin,handoverPerson,successor) VALUES (%s, %s, %s, %s,%s, %s, %s)"  # 修改SQL语句以包含password字段
            cursor.execute(sql, [biaoDate, biaoTime, disposition, expend, margin, handoverPerson, successor])
            db.commit()
            print("add a new successfully")
            return jsonify({"msg": "添加成功"}), 200  # 使用标准的HTTP状态码
        except Exception as e:
            print("add a new failed:", e)
            db.rollback()  # 把前面操作撤回
            return jsonify({"error": "添加失败", "exception": str(e)}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误



#表4 碘酸钾消耗记录----------------------------------------------------------------------------------------



#表5 亚铁氰化钾消耗记录----------------------------------------------------------------------------------------


@app.route('/biao5/list', methods=['GET']) # 列出表4信息，默认查询当天
def biao5_list():
    try:
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print("Received start time:", start_time)
        print("Received end time:", end_time)
        # 构造查询
        # query_base = "SELECT * FROM beizhu_1"

        if start_time and end_time:
            query = "SELECT * FROM biao_5 WHERE biaoDate BETWEEN %s AND %s"
            # query = f"{query_base} WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()  # (这个不写就无法实时更新)
        else:
            # cursor.execute("SELECT * FROM beizhu_1")
            query = "SELECT * FROM biao_5 WHERE biaoDate BETWEEN %s AND %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d")

            end_time = d1_at_midnight + timedelta(hours=23)
            end_time = end_time.strftime("%Y-%m-%d")

            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()
        temp = {}
        result = []
        if data:
            for i in data:
                temp["id"] = i[0]
                temp["biaoDate"] = i[1]
                temp["biaoTime"] = i[2]
                temp["disposition"] = i[3]
                temp["expend"] = i[4]
                temp["margin"] = i[5]
                temp["handoverPerson"] = i[6]
                temp["successor"] = i[7]
                result.append(temp.copy())
            print("result: ", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

@app.route('/biao5/del', methods=['GET'])  # 表4删除
def biao5_del():
    try:
        id = request.args.get('id')
        sql = "DELETE FROM biao_5 WHERE id = %s"
        cursor.execute(sql, [id])
        db.commit()
        print("del a user successfully")
        return jsonify(msg="删除成功")
    except Exception as e:
        print("del a user failed: ", e)
        db.rollback()  # 把前面操作撤回
        return jsonify(msg="删除失败")


def update_record_biao5(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE biao_5 SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()

@app.route('/biao5/update', methods=['GET']) # 更新表4的数据
def biao5_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'biaoDate': request.args.get('biaoDate'),
            'biaoTime': request.args.get('biaoTime'),
            'disposition': request.args.get('disposition'),
            'expend': request.args.get('expend'),
            'margin': request.args.get('margin'),
            'handoverPerson': request.args.get('handoverPerson'),
            'successor': request.args.get('successor'),

        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_biao5(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误


@app.route('/biao5/add', methods=['GET'])  # 表4添加
def biao5_add():
    try:
        biaoDate = request.args.get("biaoDate")  # 这里使用form获取数据,可能后面要用json？,现在改为params,也就是args
        biaoTime = request.args.get("biaoTime")
        disposition = request.args.get("disposition")
        expend = request.args.get("expend")
        margin = request.args.get("margin")
        handoverPerson = request.args.get("handoverPerson")
        successor = request.args.get("successor")

        try:
            sql = "INSERT INTO biao_5(biaoDate,biaoTime,disposition,expend,margin,handoverPerson,successor) VALUES (%s, %s, %s, %s,%s, %s, %s)"  # 修改SQL语句以包含password字段
            cursor.execute(sql, [biaoDate, biaoTime, disposition, expend, margin, handoverPerson, successor])
            db.commit()
            print("add a new successfully")
            return jsonify({"msg": "添加成功"}), 200  # 使用标准的HTTP状态码
        except Exception as e:
            print("add a new failed:", e)
            db.rollback()  # 把前面操作撤回
            return jsonify({"error": "添加失败", "exception": str(e)}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误



#表5 亚铁氰化钾消耗记录----------------------------------------------------------------------------------------



#表6 剂量抽检这里是全删了



#表7 成品送库单----------------------------------------------------------------------------------------


@app.route('/biao7/list', methods=['GET']) # 列出表6信息，以班次，计量号，时间 三者作为查询条件,确保了唯一性
def biao7_list():
    try:
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        classes = request.args.get('classes')

        # 构建查询
        # query = "SELECT * FROM biao_6 WHERE measureTime BETWEEN %s AND %s AND measureNumber = %s AND classes = %s"
        query = "SELECT * FROM biao_7 WHERE inputTime BETWEEN %s AND %s AND classes = %s"
        query_params = [start_time, end_time, classes]

        # 执行查询
        cursor.execute(query, query_params)
        data = cursor.fetchall()
        db.commit()
        temp = {}
        result = []
        if data:
            for i in data:
                temp["id"] = i[0]
                temp["inputTime"] = i[1]
                temp["name"] = i[2]
                temp["sizee"] = i[3]
                temp["amount"] = i[4]
                temp["groupp"] = i[5]
                temp["timePoint"] = i[6]
                temp["stack"] = i[7]
                temp["classes"] = i[8]
                temp["explainn"] = i[9]
                temp["mentor"] = i[10]
                temp["handoverPerson"] = i[11]
                result.append(temp.copy())
            print("result: ", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误


@app.route('/biao7/del', methods=['GET'])  # 表6删除
def biao7_del():
    try:
        id = request.args.get('id')
        sql = "DELETE FROM biao_7 WHERE id = %s"
        cursor.execute(sql, [id])
        db.commit()
        print("del a user successfully")
        return jsonify(msg="删除成功")
    except Exception as e:
        print("del a user failed: ", e)
        db.rollback()  # 把前面操作撤回
        return jsonify(msg="删除失败")


def update_record_biao7(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE biao_7 SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()

@app.route('/biao7/update', methods=['GET']) # 更新表6的数据
def biao7_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'name': request.args.get('name'),
            'sizee': request.args.get('sizee'),
            'amount': request.args.get('amount'),
            'groupp': request.args.get('groupp'),
            'stack': request.args.get('stack'),
            'classes': request.args.get('classes'),
            'explainn': request.args.get('explainn'),
            'mentor': request.args.get('mentor'),
            'handoverPerson': request.args.get('handoverPerson'),
        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_biao7(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误


@app.route('/biao7/add', methods=['POST'])
def biao7_add():
    try:
        data = request.get_json()
        print("data", data.get("params"))

        groupp = data.get("params").get('groupp')
        handoverPerson = data.get("params").get('handoverPerson')
        mentor = data.get("params").get('mentor')
        explainn = data.get("params").get('explainn')
        inputTime = data.get("params").get("inputTime")
        classes = data.get("params").get('classes')
        tableData = data.get("params").get('tableData')

        print("tableData:", tableData)
        print("inputTime", inputTime)
        print("classes", classes)
        print("groupp", groupp)

        # 先根据inputTime和classes检测数据库中是否已存在该数据
        check_sql = "SELECT COUNT(*) FROM biao_7 WHERE inputTime = %s AND classes = %s"
        cursor.execute(check_sql, (inputTime, classes))
        count = cursor.fetchone()[0]
        if count > 0:
            return jsonify({"msg": "请不要重复添加"}), 400

        # 遍历 tableData
        for item in tableData:  # 列表里面是多个字典的方式，把但个字典取出来，通过键值对的方式获取值
            try:
                # 构建 SQL 语句的参数列表
                params = [
                    inputTime,
                    item['name'],
                    item['sizee'],
                    item['amount'],
                    groupp,
                    item['timePoint'],
                    item['stack'],
                    classes,
                    explainn,
                    mentor,
                    handoverPerson,
                ]

                sql = """  
                                INSERT INTO biao_7 (  
                                    inputTime, name, sizee, amount,  
                                    groupp, timePoint, stack,classes,explainn,mentor,handoverPerson
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)  
                            """
                cursor.execute(sql, params)
                db.commit()
            except Exception as e:
                db.rollback()
                return jsonify({"error": "添加失败", "exception": str(e)}), 500

        return jsonify({"msg": "添加成功"}), 200
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500


#表7 成品送库单----------------------------------------------------------------------------------------




# 主控电话通知记录单----------------------------------------------------------------------------------------


@app.route('/mainControl/list', methods=['GET']) # 列出表4信息，默认查询当天
def mainControl_list():
    try:
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print("Received start time:", start_time)
        print("Received end time:", end_time)
        # 构造查询
        # query_base = "SELECT * FROM beizhu_1"

        if start_time and end_time:
            query = "SELECT * FROM iphonemain WHERE Timee BETWEEN %s AND %s"
            # query = f"{query_base} WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()  # (这个不写就无法实时更新)
        else:
            # cursor.execute("SELECT * FROM beizhu_1")
            query = "SELECT * FROM iphonemain WHERE Timee BETWEEN %s AND %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d")

            end_time = d1_at_midnight + timedelta(hours=23, minutes=59, seconds=59)
            end_time = end_time.strftime("%Y-%m-%d")

            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()
        temp = {}
        result = []
        if data:
            for i in data:
                temp["id"] = i[0]
                temp["conTent"] = i[1]
                temp["Timee"] = i[2]
                temp["tongzhi"] = i[3]
                temp["zhixing"] = i[4]
                temp["results"] = i[5]
                temp["beizhu"] = i[6]
                temp["conTentTime"] = i[7]
                temp["suT"] = i[8]
                result.append(temp.copy())
            print("result: ", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误


@app.route('/mainControl/del', methods=['GET'])  # 表3删除
def mainControl_del():
    try:
        id = request.args.get('id')
        sql = "DELETE FROM iphonemain WHERE id = %s"
        cursor.execute(sql, [id])
        db.commit()
        print("del a user successfully")
        return jsonify(msg="删除成功")
    except Exception as e:
        print("del a user failed: ", e)
        db.rollback()  # 把前面操作撤回
        return jsonify(msg="删除失败")

def update_record_mainControl(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE iphonemain SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()


@app.route('/mainControl/update', methods=['GET']) # 更新表3的数据
def mainControl_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'conTent': request.args.get('conTent'),
            'tongzhi': request.args.get('tongzhi'),
            'zhixing': request.args.get('zhixing'),
            'results': request.args.get('results'),
            'beizhu': request.args.get('beizhu'),
            'suT': request.args.get('suT'),
            'Timee': request.args.get('Timee'),

        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_mainControl(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误


@app.route('/mainControl/add', methods=['GET'])  # 表3添加
def mainControl_add():
    try:
        conTent = request.args.get("conTent")  # 这里使用form获取数据,可能后面要用json？,现在改为params,也就是args
        Timee = request.args.get("Timee")
        tongzhi = request.args.get("tongzhi")
        zhixing = request.args.get("zhixing")
        results = request.args.get("results")
        beizhu = request.args.get("beizhu")

        suT = request.args.get("suT")

        try:
            sql = "INSERT INTO iphonemain(conTent,Timee,tongzhi,zhixing,results,beizhu,suT) VALUES ( %s,%s, %s, %s,%s, %s, %s)"  # 修改SQL语句以包含password字段
            cursor.execute(sql, [conTent, Timee, tongzhi, zhixing, results, beizhu, suT])
            db.commit()
            print("add a new successfully")
            return jsonify({"msg": "添加成功"}), 200  # 使用标准的HTTP状态码
        except Exception as e:
            print("add a new failed:", e)
            db.rollback()  # 把前面操作撤回
            return jsonify({"error": "添加失败", "exception": str(e)}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误



# 主控电话通知记录单----------------------------------------------------------------------------------------


# 产量情况统计表----------------------------------------------------------------------------------------


@app.route('/analyze/list', methods=['GET'])
def analyze_list():
    try:
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print("Received start time:", start_time)
        print("Received end time:", end_time)
        # 构造查询
        # query_base = "SELECT * FROM beizhu_1"

        if start_time and end_time:
            query = "SELECT * FROM output WHERE dataTime BETWEEN %s AND %s"
            # query = f"{query_base} WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()  # (这个不写就无法实时更新)
        else:
            # cursor.execute("SELECT * FROM beizhu_1")
            query = "SELECT * FROM output WHERE dataTime BETWEEN %s AND %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")

            end_time = d1_at_midnight + timedelta(hours=24)
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()
        temp = {}
        result = []
        if data:
            for i in data:
                temp["id"] = i[0]
                temp["timePoint"] = i[1]
                temp["dataTime"] = i[2]
                temp["banci"] = i[3]
                temp["aban"] = i[4]
                temp["bban"] = i[5]
                temp["aqi"] = i[6]
                temp["bqi"] = i[7]
                temp["ahao"] = i[8]
                temp["bhao"] = i[9]
                temp["atao"] = i[10]
                temp["btao"] = i[11]
                temp["amu"] = i[12]
                temp["bmu"] = i[13]
                temp["ahui"] = i[14]
                temp["bhui"] = i[15]
                temp["acold"] = i[16]
                temp["bcold"] = i[17]
                temp["aWater"] = i[18]
                temp["bWater"] = i[19]
                temp["aban1"] = i[20]
                temp["bban1"] = i[21]
                result.append(temp.copy())
            print("result: ", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

def update_record_analyze(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE output SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()

@app.route('/analyze/update', methods=['GET']) # 更新表3的数据
def analyze_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'timePoint': request.args.get('timePoint'),
            'banci': request.args.get('banci'),
            'aban': request.args.get('aban'),
            'bban': request.args.get('bban'),
            'aban1': request.args.get('aban1'),
            'bban1': request.args.get('bban1'),
            'aqi': request.args.get('aqi'),
            'bqi': request.args.get('bqi'),
            'ahao': request.args.get('ahao'),
            'bhao': request.args.get('bhao'),
            'atao': request.args.get('atao'),
            'btao': request.args.get('btao'),
            'amu': request.args.get('amu'),
            'bmu': request.args.get('bmu'),
            'ahui': request.args.get('ahui'),
            'bhui': request.args.get('bhui'),
            'acold': request.args.get('acold'),
            'bcold': request.args.get('bcold'),
            'aWater': request.args.get('aWater'),
            'bWater': request.args.get('bWater'),

        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_analyze(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error updating record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误




# 产量情况统计表----------------------------------------------------------------------------------------


# 报警---------------------------


@app.route('/alarmList/list', methods=['GET'])  # 用户管理表显示  svip
def alarmList_list():
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)  # 默认第1页
        perPage = request.args.get('perPage', 10, type=int)  # 默认每页10条

        # 计算查询的偏移量
        offset = (page - 1) * perPage

        # 构造查询
        query = "SELECT id, PointId, possibleCause, Solution, handling,namee,valuee,unit,Typee,normalRange,naocan1,naocan2 FROM alarm LIMIT %s OFFSET %s"
        params = [perPage, offset]

        # 执行查询
        cursor.execute(query, params)
        data = cursor.fetchall()
        db.commit()

        # 获取总记录数（用于分页计算）
        total_query = "SELECT COUNT(*) FROM alarm"
        cursor.execute(total_query)
        db.commit()
        totalCount = cursor.fetchone()[0]

        # 计算总页数
        totalPages = (totalCount // perPage) + (1 if totalCount % perPage > 0 else 0)

        # 转换数据为字典列表
        result = []
        if data:
            for i in data:
                result.append({
                    "id": i[0],
                    "PointId": i[1],
                    "possibleCause": i[2],
                    "Solution": i[3],
                    "handling": i[4],  # index 4 for 'post' based on SELECT
                    "namee": i[5],
                    "valuee": i[6],
                    "unit": i[7],
                    "Typee": i[8],
                    "normalRange": i[9],
                    "naocan1": i[10],
                    "naocan2": i[11]
                })

        # 构造包含分页信息的响应
        response = {
            'data': result,
            'pagination': {
                'page': page,
                'perPage': perPage,
                'totalCount': totalCount,
                'totalPages': totalPages
            }
        }

        return jsonify(response)
    except Exception as e:
        print("Error fetching data:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500


@app.route('/alarmList/add', methods=['GET'])  # 用户表添加
def alarmList_add():
    try:
        PointId = request.args.get("PointId")  # 这里使用form获取数据,可能后面要用json？,现在改为params,也就是args
        possibleCause = request.args.get("possibleCause")
        Solution = request.args.get("Solution")
        handling = request.args.get("handling")
        namee = request.args.get("namee")
        valuee = request.args.get("valuee")
        unit = request.args.get("unit")
        Typee = request.args.get("Typee")
        normalRange = request.args.get("normalRange")
        naocan1 = request.args.get("naocan1")
        naocan2 = request.args.get("naocan2")

        try:
            sql = "INSERT INTO alarm(PointId, possibleCause,Solution,handling,namee,valuee,unit,Typee,normalRange,naocan1,naocan2) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s,%s,%s)"  # 修改SQL语句以包含password字段
            cursor.execute(sql, [PointId, possibleCause, Solution, handling, namee, valuee, unit, Typee, normalRange,
                                 naocan1, naocan2])
            db.commit()
            print("add a new successfully")
            return jsonify({"msg": "添加成功"}), 200  # 使用标准的HTTP状态码
        except Exception as e:
            print("add a new failed:", e)
            db.rollback()  # 把前面操作撤回
            return jsonify({"error": "添加失败", "exception": str(e)}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误


@app.route('/alarmList/del', methods=['GET'])  # 用户表删除
def alarmList_del():
    try:
        id = request.args.get('id')
        sql = "DELETE FROM alarm WHERE id = %s"
        cursor.execute(sql, [id])
        db.commit()
        print("del a user successfully")
        return jsonify(msg="删除成功")
    except Exception as e:
        print("del a user failed: ", e)
        db.rollback()  # 把前面操作撤回
        return jsonify(msg="删除失败")


# 更新记录的函数      备注表的更新！ 注意函数名字别重复了 ！！！！！！！！！！
def update_record_alarm(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE alarm SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()


@app.route('/alarmList/update', methods=['GET'])
def alarmList_update():
    try:
        id_to_update = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

        # Filter out the fields we want to update
        update_fields = {
            'PointId': request.args.get('PointId'),
            'possibleCause': request.args.get('possibleCause'),
            'Solution': request.args.get('Solution'),
            'handling': request.args.get('handling'),
            'namee': request.args.get('namee'),
            'valuee': request.args.get('valuee'),
            'unit': request.args.get('unit'),
            'Typee': request.args.get('Typee'),
            'normalRange': request.args.get('normalRange'),
            'naocan1': request.args.get('naocan1'),
            'naocan2': request.args.get('naocan2')
        }

        # Filter out fields with None values (optional)
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # Call the function to update the record
        success, message = update_record_alarm(id_to_update, update_fields)

        # Return different JSON responses based on the result
        if success:
            return jsonify({"msg": "修改成功"}), 200
        else:
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误




#  报警-------------------

#  工艺流程

@app.route('/gylc/list', methods=['GET'])  # 用户管理表显示  svip
def gylc_list():
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)  # 默认第1页
        perPage = request.args.get('perPage', 10, type=int)  # 默认每页10条

        # 计算查询的偏移量
        offset = (page - 1) * perPage

        # 构造查询
        query = "SELECT id, PointId,normalRange,namee FROM gylc LIMIT %s OFFSET %s"
        params = [perPage, offset]

        # 执行查询
        cursor.execute(query, params)
        data = cursor.fetchall()
        db.commit()

        # 获取总记录数（用于分页计算）
        total_query = "SELECT COUNT(*) FROM gylc"
        cursor.execute(total_query)
        db.commit()
        totalCount = cursor.fetchone()[0]

        # 计算总页数
        totalPages = (totalCount // perPage) + (1 if totalCount % perPage > 0 else 0)

        # 转换数据为字典列表
        result = []
        if data:
            for i in data:
                result.append({
                    "id": i[0],
                    "PointId": i[1],
                    "normalRange": i[2],
                    "namee": i[3],

                })

        # 构造包含分页信息的响应
        response = {
            'data': result,
            'pagination': {
                'page': page,
                'perPage': perPage,
                'totalCount': totalCount,
                'totalPages': totalPages
            }
        }

        return jsonify(response)
    except Exception as e:
        print("Error fetching data:", e)
        return jsonify({"error": "服务器内部错误"}), 500



# 更新记录的函数      备注表的更新！ 注意函数名字别重复了 ！！！！！！！！！！
def update_record_gylc(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE gylc SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()


@app.route('/gylc/update', methods=['GET'])
def gylc_update():
    try:
        id_to_update = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

        # Filter out the fields we want to update
        update_fields = {
            'PointId': request.args.get('PointId'),
            'namee': request.args.get('namee'),
            'normalRange': request.args.get('normalRange'),
        }

        # Filter out fields with None values (optional)
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # Call the function to update the record
        success, message = update_record_gylc(id_to_update, update_fields)

        # Return different JSON responses based on the result
        if success:
            return jsonify({"msg": "修改成功"}), 200
        else:
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

#  工艺流程

# 数据分析修改表----------------------------------------------------------------------------------------


@app.route('/qianduan/list', methods=['GET'])
def qianduan_list():
    try:
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print("Received start time:", start_time)
        print("Received end time:", end_time)
        # 构造查询
        # query_base = "SELECT * FROM beizhu_1"

        if start_time and end_time:
            query = "SELECT * FROM last WHERE tS BETWEEN %s AND %s"
            # query = f"{query_base} WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()  # (这个不写就无法实时更新)
        else:
            # cursor.execute("SELECT * FROM beizhu_1")
            query = "SELECT * FROM last WHERE tS BETWEEN %s AND %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")

            end_time = d1_at_midnight + timedelta(hours=23, minutes=59, seconds=59)
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

            # 判断是否为当天数据，如果是，则限制返回的数据小于等于当前时间
            if d1.date() == datetime.now().date():
                query = f"SELECT * FROM last WHERE tS BETWEEN %s AND %s AND tS <= %s"
                cursor.execute(query, (start_time, end_time, d1.strftime("%Y-%m-%d %H:%M:%S")))
            else:
                cursor.execute(query, (start_time, end_time))

            data = cursor.fetchall()
            db.commit()
        temp = {}
        result = []
        if data:
            for i in data:
                temp["id"] = i[0]
                temp["tS"] = i[1]
                temp["todaychanliang"] = i[2]
                temp["monthchanliang"] = i[3]
                temp["yearchanliang"] = i[4]
                temp["todaydianhao"] = i[5]
                temp["monthdianhao"] = i[6]
                temp["yeardianhao"] = i[7]
                temp["todayqihao"] = i[8]
                temp["monthqihao"] = i[9]
                temp["yearqihao"] = i[10]
                temp["todayluhao"] = i[11]
                temp["monthluhao"] = i[12]
                temp["yearluhao"] = i[13]
                result.append(temp.copy())
            print("result: ", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

def update_record_qianduan(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE last SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()

@app.route('/qianduan/update', methods=['GET']) # 更新表3的数据
def qianduan_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'todaychanliang': request.args.get('todaychanliang'),
            'monthchanliang': request.args.get('monthchanliang'),
            'yearchanliang': request.args.get('yearchanliang'),
            'todaydianhao': request.args.get('todaydianhao'),
            'monthdianhao': request.args.get('monthdianhao'),
            'yeardianhao': request.args.get('yeardianhao'),
            'todayqihao': request.args.get('todayqihao'),
            'monthqihao': request.args.get('monthqihao'),
            'yearqihao': request.args.get('yearqihao'),
            'todayluhao': request.args.get('todayluhao'),
            'monthluhao': request.args.get('monthluhao'),
            'yearluhao': request.args.get('yearluhao'),
        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_qianduan(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误




# 数据分析修改表统计表----------------------------------------------------------------------------------------


# 3.27_new

@app.route('/dianhananalyze/list', methods=['GET'])
def dianhananalyze_list():
    try:
        date_type = request.args.get('date_type', 'month')
        date_value = request.args.get('date_value')
        #print("date_type", date_type)
        #print("date_value", date_value)

        query = "SELECT * FROM dianhan_analyze"
        params = []

        if date_type and date_value:
            if date_type == 'date':
                # 修改这里：使用DATE()函数提取日期部分进行比较
                query += " WHERE DATE(inputTime) = %s"
                params.append(date_value)
            elif date_type == 'month':
                # 只取前两个字段，避免拆包报错
                year_month = date_value.split('-')
                year = year_month[0]
                month = year_month[1] if len(year_month) > 1 else '01'
                query += " WHERE YEAR(inputTime) = %s AND MONTH(inputTime) = %s"
                params.extend([year, month])
            elif date_type == 'year':
                # 修改这里：使用YEAR函数进行比较
                query += " WHERE YEAR(inputTime) = %s"
                params.append(date_value)

        cursor.execute(query, params)
        data = cursor.fetchall()
        db.commit()

        banci_sums = {}
        for i in data:
            banci = i[11]
            if banci not in banci_sums:
                banci_sums[banci] = {
                    "dian_total": 0,
                    "dian_best": 0,
                    "dian_good": 0,
                    "dian_ok": 0,
                    "dian_bad": 0,
                }
            banci_sums[banci]["dian_total"] += round(float(i[2] or 0), 2)
            banci_sums[banci]["dian_best"] += round(float(i[3] or 0), 2)
            banci_sums[banci]["dian_good"] += round(float(i[5] or 0), 2)
            banci_sums[banci]["dian_ok"] += round(float(i[7] or 0), 2)
            banci_sums[banci]["dian_bad"] += round(float(i[9] or 0), 2)

        result = []
        for banci, sums in banci_sums.items():
            dian_total = sums["dian_total"]
            dian_best = sums["dian_best"]
            dian_good = sums["dian_good"]
            dian_ok = sums["dian_ok"]
            dian_bad = sums["dian_bad"]
            temp = {
                "banci": banci,
                "dian_total": round(dian_total, 2),
                "dian_best": round(dian_best, 2),
                "best_zhanbi": f"{round(dian_best / dian_total * 100, 2)}%" if dian_total else "0.00%",
                "dian_good": round(dian_good, 2),
                "good_zhanbi": f"{round(dian_good / dian_total * 100, 2)}%" if dian_total else "0.00%",
                "dian_ok": round(dian_ok, 2),
                "ok_zhanbi": f"{round(dian_ok / dian_total * 100, 2)}%" if dian_total else "0.00%",
                "dian_bad": round(dian_bad, 2),
                "bad_zhanbi": f"{round(dian_bad / dian_total * 100, 2)}%" if dian_total else "0.00%",
            }
            result.append(temp)
        print("result: ", len(result))
        return jsonify(result)
    except Exception as e:
        print("Error adding record:", e)
        return jsonify({"error": "服务器内部错误"}), 500


@app.route('/dianhan/list', methods=['GET']) # 列出表4信息，默认查询当天
def dianhan_list():
    db = None
    cursor = None
    try:
        db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='js', charset='utf8')
        cursor = db.cursor()
        # 获取分页参数和查询时间范围
        page = request.args.get('page', 1, type=int)
        perPage = request.args.get('perPage', 1000, type=int)
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        banci = request.args.get('banci')

        print("Received start time:", start_time)
        print("Received end time:", end_time)

        offset = (page - 1) * perPage

        query_base = "SELECT * FROM dianhan"
        where_clauses = []
        params = []

        # 时间范围处理
        if start_time and end_time:
            where_clauses.append("biaoDate BETWEEN %s AND %s")
            params.extend([start_time, end_time])
        else:
            d1 = datetime.now()
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")
            end_time = (d1_at_midnight + timedelta(hours=23, minutes=59, seconds=59)).strftime("%Y-%m-%d %H:%M:%S")
            where_clauses.append("biaoDate BETWEEN %s AND %s")
            params.extend([start_time, end_time])

        # 班次处理
        if banci:
            where_clauses.append("banci = %s")
            params.append(banci)

        # 组装最终SQL
        if where_clauses:
            where_sql = " WHERE " + " AND ".join(where_clauses)
        else:
            where_sql = ""

        query = f"{query_base}{where_sql} LIMIT %s OFFSET %s"
        params.extend([perPage, offset])

        cursor.execute(query, params)
        data = cursor.fetchall()

        # 总数统计
        total_query = "SELECT COUNT(*) FROM dianhan"
        total_params = []
        if where_clauses:
            total_query += where_sql
            total_params = params[:len(params)-2]  # 去掉 limit offset

        cursor.execute(total_query, total_params)
        totalCount = cursor.fetchone()[0]

        totalPages = (totalCount // perPage) + (1 if totalCount % perPage > 0 else 0)

        result = []
        if data:
            for i in data:
                result.append({
                    "id": i[0],
                    "biaoDate": i[1],
                    "biaoTime": i[2],
                    "yanliang": i[3],
                    "dianliang": i[4],
                    "dianhanliang": i[5],
                    "banci": i[6],
                    "People": i[7],
                    "dianhan_mysql": i[8],
                })

        response = {
            'data': result,
            'pagination': {
                'page': page,
                'perPage': perPage,
                'totalCount': totalCount,
                'totalPages': totalPages
            }
        }

        return jsonify(response)

    except Exception as e:
        print("Error listing records:", e)
        return jsonify({"error": "服务器内部错误"}), 500
    finally:
        if cursor:
            try:
                cursor.close()
            except:
                pass
        if db:
            try:
                db.close()
            except:
                pass



@app.route('/dianhan/del', methods=['GET'])  # 表4删除
def dianhan_del():
    try:
        id = request.args.get('id')
        sql = "DELETE FROM dianhan WHERE id = %s"
        cursor.execute(sql, [id])
        db.commit()
        print("del a user successfully")
        return jsonify(msg="删除成功")
    except Exception as e:
        print("del a user failed: ", e)
        db.rollback()  # 把前面操作撤回
        return jsonify(msg="删除失败")


def update_record_dianhan(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE dianhan SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()

@app.route('/dianhan/update', methods=['GET']) # 更新表3的数据
def dianhan_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'biaoDate': request.args.get('biaoDate'),
            'biaoTime': request.args.get('biaoTime'),
            'yanliang': request.args.get('yanliang'),
            'dianliang': request.args.get('dianliang'),
            'dianhanliang': request.args.get('dianhanliang'),
            'banci': request.args.get('banci'),
            'People': request.args.get('People'),
            'dianhan_mysql': request.args.get('dianhan_mysql'),

        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_dianhan(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error updating record:", e)
        return jsonify({"error": "服务器内部错误"}), 500


@app.route('/dianhan/add', methods=['GET'])  # 表4添加
def dianhan_add():
    try:
        biaoDate = request.args.get("biaoDate")  # 这里使用form获取数据,可能后面要用json？,现在改为params,也就是args
        biaoTime = request.args.get("biaoTime")
        yanliang = request.args.get("yanliang")
        dianliang = request.args.get("dianliang")
        dianhanliang = request.args.get("dianhanliang")
        banci = request.args.get("banci")
        People = request.args.get("People")
        dianhan_mysql = request.args.get("dianhan_mysql")

        try:
            sql = "INSERT INTO dianhan(biaoDate,biaoTime,yanliang,dianliang,dianhanliang,banci,People,dianhan_mysql) VALUES (%s, %s, %s, %s,%s, %s, %s,%s)"  # 修改SQL语句以包含password字段
            cursor.execute(sql, [biaoDate, biaoTime, yanliang, dianliang, dianhanliang, banci, People,dianhan_mysql])
            db.commit()
            print("add a new successfully")
            return jsonify({"msg": "添加成功"}), 200  # 使用标准的HTTP状态码
        except Exception as e:
            print("add a new failed:", e)
            db.rollback()  # 把前面操作撤回
            return jsonify({"error": "添加失败", "exception": str(e)}), 500
    except Exception as e:
        print("Error adding record:", e)
        return jsonify({"error": "服务器内部错误"}), 500



#表 碘含量----------------------------------------------------------------------------------------


#total_biao----------------------------------------------------------------------------------------------

@app.route('/total_biao/list', methods=['GET'])
def total_biao_list():
    try:
        # 获取分页参数和查询时间范围
        page = request.args.get('page', 1, type=int)  # 默认第1页
        perPage = request.args.get('perPage', 24, type=int)  # 默认每页10条
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print(type(start_time))
        print("Received start time:", start_time)
        print("Received end time:", end_time)

        # 计算查询的偏移量
        offset = (page - 1) * perPage

        # 构造查询
        query_base = "SELECT * FROM total_biao"
        params = []

        if start_time and end_time:
            query = f"{query_base} WHERE inputTime BETWEEN %s AND %s LIMIT %s OFFSET %s"
            params = [start_time, end_time, perPage, offset]
        else:

            query = f"{query_base} WHERE inputTime BETWEEN %s AND %s LIMIT %s OFFSET %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")

            end_time = d1_at_midnight + timedelta(hours=23, minutes=59, seconds=59)
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

            params = [start_time, end_time, perPage, offset]

            # 执行查询
        cursor.execute(query, params)
        data = cursor.fetchall()

        # 获取总记录数（用于分页计算）
        total_query = "SELECT COUNT(*) FROM total_biao"
        if start_time and end_time:
            total_query += " WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(total_query, (start_time, end_time))
            db.commit()
        else:
            cursor.execute(total_query)
            db.commit()
        totalCount = cursor.fetchone()[0]

        # 计算总页数
        totalPages = (totalCount // perPage) + (1 if totalCount % perPage > 0 else 0)

        # 转换数据为字典列表
        result = []
        if data:
            for i in data:
                result.append({
                    "id": i[0],
                    "inputTime": i[1],
                    "submitTime": i[2],
                    "centrifugeOilPressureA": i[3],
                    "centrifugeOilTemperatureA": i[4],
                    "centrifugeOilLevelA": i[5],
                    "centrifugeWashingTimeA": i[6],
                    "centrifugeLooseAgentConsumptionA": i[7],
                    "centrifugeOilPressureB": i[8],
                    "centrifugeOilTemperatureB": i[9],
                    "centrifugeOilLevelB": i[10],
                    "centrifugeWashingTimeB": i[11],
                    "centrifugeLooseAgentConsumptionB": i[12],
                    "centrifugeOilPressureC": i[13],
                    "centrifugeOilTemperatureC": i[14],
                    "centrifugeOilLevelC": i[15],
                    "centrifugeWashingTimeC": i[16],
                    "centrifugeLooseAgentConsumptionC": i[17],
                    "impurityA": i[18],
                    "impurityB": i[19],
                    "condensatePumpOnePressureA": i[20],
                    "condensatePumpOnePressureB": i[21],
                    "condensatePumpVPressureA": i[22],
                    "condensatePumpVPressureB": i[23],
                    "vacuumPumpingDegreeA": i[24],
                    "vacuumPumpingDegreeB": i[25],
                    "flushPumpPressureA": i[26],
                    "flushPumpPressureB": i[27],
                    "ApressureA": i[28],
                    "ApressureB": i[29],
                    "BpressureA": i[30],
                    "BpressureB": i[31],
                    "BpressureC": i[32],
                    "CpressureA": i[33],
                    "CpressureB": i[34],
                })

        # 构造包含分页信息的响应
        response = {
            'data': result,
            'pagination': {
                'page': page,
                'perPage': perPage,
                'totalCount': totalCount,
                'totalPages': totalPages
            }
        }

        return jsonify(response)
    except Exception as e:
        print("Error fetching records:", e)
        return jsonify({"error": "服务器内部错误"}), 500


@app.route('/total_biao/update', methods=['GET']) # 更新表2的数据,根据数据库里面的id来更新
def total_biao_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'inputTime': request.args.get('inputTime'),
            'submitTime': request.args.get('submitTime'),
            'centrifugeOilPressureA': request.args.get('centrifugeOilPressureA'),
            'centrifugeOilTemperatureA': request.args.get('centrifugeOilTemperatureA'),
            'centrifugeOilLevelA': request.args.get('centrifugeOilLevelA'),
            'centrifugeWashingTimeA': request.args.get('centrifugeWashingTimeA'),
            'centrifugeLooseAgentConsumptionA': request.args.get('centrifugeLooseAgentConsumptionA'),
            'centrifugeOilPressureB': request.args.get('centrifugeOilPressureB'),
            'centrifugeOilTemperatureB': request.args.get('centrifugeOilTemperatureB'),
            'centrifugeOilLevelB': request.args.get('centrifugeOilLevelB'),
            'centrifugeWashingTimeB': request.args.get('centrifugeWashingTimeB'),
            'centrifugeLooseAgentConsumptionB': request.args.get('centrifugeLooseAgentConsumptionB'),
            'centrifugeOilPressureC': request.args.get('centrifugeOilPressureC'),
            'centrifugeOilTemperatureC': request.args.get('centrifugeOilTemperatureC'),
            'centrifugeOilLevelC': request.args.get('centrifugeOilLevelC'),
            'centrifugeWashingTimeC': request.args.get('centrifugeWashingTimeC'),
            'centrifugeLooseAgentConsumptionC': request.args.get('centrifugeLooseAgentConsumptionC'),
            'impurityA': request.args.get('impurityA'),
            'impurityB': request.args.get('impurityA'),  # 这里就是让impurityA和impurityB的值相同
            'condensatePumpOnePressureA': request.args.get('condensatePumpOnePressureA'),
            'condensatePumpOnePressureB': request.args.get('condensatePumpOnePressureB'),
            'condensatePumpVPressureA': request.args.get('condensatePumpVPressureA'),
            'condensatePumpVPressureB': request.args.get('condensatePumpVPressureB'),
            'vacuumPumpingDegreeA': request.args.get('vacuumPumpingDegreeA'),
            'vacuumPumpingDegreeB': request.args.get('vacuumPumpingDegreeB'),
            'flushPumpPressureA': request.args.get('flushPumpPressureA'),
            'flushPumpPressureB': request.args.get('flushPumpPressureB'),
            'ApressureA': request.args.get('ApressureA'),
            'ApressureB': request.args.get('ApressureB'),
            'BpressureA': request.args.get('BpressureA'),
            'BpressureB': request.args.get('BpressureB'),
            'BpressureC': request.args.get('BpressureC'),
            'CpressureA': request.args.get('CpressureA'),
            'CpressureB': request.args.get('CpressureB'),
        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_total_biao(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误


# 更新记录的函数
def update_record_total_biao(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE total_biao SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()

#---------------------------total_biao

# beizhu_totoal---------------------------


@app.route('/beizhu_total/list', methods=['GET']) # 列出离心机备注表的信息，用group区分组号
def beizhu_total_list():
    try:
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print("Received start time:", start_time)
        print("Received end time:", end_time)
        # 构造查询
        # query_base = "SELECT * FROM beizhu_1"

        if start_time and end_time:
            query = "SELECT * FROM beizhu_total WHERE inputTime BETWEEN %s AND %s"
            # query = f"{query_base} WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()  # 文心一言写的这个就给我删掉了  (这个不写就无法实时更新)
        else:
            # cursor.execute("SELECT * FROM beizhu_1")
            query = "SELECT * FROM beizhu_total WHERE inputTime BETWEEN %s AND %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")
            print("start_time", start_time)
            print(type(start_time))

            end_time = d1_at_midnight + timedelta(hours=23, minutes=59, seconds=59)
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
            print("end_time", end_time)
            print(type(end_time))

            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()
        temp = {}
        result = []
        if data:
            for i in data:
                temp["id"] = i[0]
                temp["inputTime"] = i[1]
                temp["handoverTool"] = i[2]
                temp["deviceHealth"] = i[3]
                temp["environmentHealth"] = i[4]
                temp["successor"] = i[5]
                temp["handoverPerson"] = i[6]
                temp["groupp"] = i[7]
                temp["classes"] = i[8]
                temp["looseAgentConsumptionTotal"] = i[9]
                temp["subTime"] = i[10]
                temp["sub"] = i[11]
                result.append(temp.copy())
            print("result: ", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误



# 更新记录的函数      备注表的更新！ 注意函数名字别重复了 ！！！！！！！！！！
def update_record_beizhu_total(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE beizhu_total SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()


@app.route('/beizhu_total/update', methods=['GET']) # 更新备注表表的数据,根据数据库里面的id来更新
def beizhu_total_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')
        groupp = request.args.get('groupp')
        # print(type(groupp))

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'inputTime': request.args.get('inputTime'),
            'handoverTool': request.args.get('handoverTool'),
            'deviceHealth': request.args.get('deviceHealth'),
            'environmentHealth': request.args.get('environmentHealth'),
            'successor': request.args.get('successor'),
            'handoverPerson': request.args.get('handoverPerson'),
            'groupp': request.args.get('groupp'),
            'classes': request.args.get('classes'),
            'looseAgentConsumptionTotal': request.args.get('looseAgentConsumptionTotal'),
            'subTime': request.args.get('subTime')
            , 'sub': request.args.get('sub')
        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_beizhu_total(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误




# beizhu_total -----------------------

# 同环比----------------------------------------------------------------------------------------


@app.route('/tonghuanbi/list', methods=['GET'])
def tonghuanbi_list():
    try:
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print("Received start time:", start_time)
        print("Received end time:", end_time)

        # 构造查询
        if start_time and end_time:
            query = "SELECT * FROM tonghuanbi WHERE tS BETWEEN %s AND %s"
            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()  # 确保实时更新
        else:
            # 如果没有传入 start_time 和 end_time，则默认按当年的时间段查询
            # 获取当前年份的起始时间
            current_year = datetime.now().year
            start_time = f"{current_year}-01-01 00:00:00"
            end_time = f"{current_year}-12-31 23:59:59"

            query = "SELECT * FROM tonghuanbi WHERE tS BETWEEN %s AND %s"
            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()

        temp = {}
        result = []
        if data:
            for i in data:
                temp["id"] = i[0]
                temp["tS"] = i[1]
                temp["chanliang"] = i[2]
                temp["ganyanchan"] = i[3]
                temp["ganyanzhanbi"] = i[4]
                temp["qihao"] = i[5]
                temp["luhao"] = i[6]
                temp["dianhao"] = i[7]
                temp["totalhao"] = i[8]
                result.append(temp.copy())
            print("result: ", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

def update_record_tonghuanbi(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE tonghuanbi SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()

@app.route('/tonghuanbi/update', methods=['GET']) # 更新表3的数据
def tonghuanbi_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'tS': request.args.get('tS'),
            'chanliang': request.args.get('chanliang'),
            'ganyanchan': request.args.get('ganyanchan'),
            'ganyanzhanbi': request.args.get('ganyanzhanbi'),
            'qihao': request.args.get('qihao'),
            'luhao': request.args.get('luhao'),
            'dianhao': request.args.get('dianhao'),
            'totalhao': request.args.get('totalhao'),
        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_tonghuanbi(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误



@app.route('/tonghuanbi/add', methods=['GET'])  # 用户表添加
def tonghuanbi_add():
    try:
        tS = request.args.get("tS")  # 这里使用form获取数据,可能后面要用json？,现在改为params,也就是args
        chanliang = request.args.get("chanliang")
        ganyanchan = request.args.get("ganyanchan")
        ganyanzhanbi = request.args.get("ganyanzhanbi")
        qihao = request.args.get("qihao")
        luhao = request.args.get("luhao")
        dianhao = request.args.get("dianhao")
        totalhao = request.args.get("totalhao")

        try:
            sql = "INSERT INTO tonghuanbi(tS, chanliang,ganyanchan,ganyanzhanbi,qihao,luhao,dianhao,totalhao) VALUES (%s, %s, %s, %s,%s, %s, %s, %s)"  # 修改SQL语句以包含password字段
            cursor.execute(sql, [tS, chanliang, ganyanchan, ganyanzhanbi, qihao, luhao, dianhao, totalhao])
            db.commit()
            print("add a new successfully")
            return jsonify({"msg": "添加成功"}), 200  # 使用标准的HTTP状态码
        except Exception as e:
            print("add a new failed:", e)
            db.rollback()  # 把前面操作撤回
            return jsonify({"error": "添加失败", "exception": str(e)}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误


@app.route('/tonghuanbi/del', methods=['GET'])  # 表3删除
def tonghuanbi_del():
    try:
        id = request.args.get('id')
        sql = "DELETE FROM tonghuanbi WHERE id = %s"
        cursor.execute(sql, [id])
        db.commit()
        print("del a user successfully")
        return jsonify(msg="删除成功")
    except Exception as e:
        print("del a user failed: ", e)
        db.rollback()  # 把前面操作撤回
        return jsonify(msg="删除失败")



# 同环比----------------------------------------------------------------------------------------




# ----- 3.27 new






# 权限部分--------------------------------------------------------------------------------------



@app.route('/permission', methods=['GET'])
def get_dataAdmin():
    try:
        role = session.get('role')  # 从 session 获取用户角色
        username = session.get('username')  # 从 session 获取用户名
        post = session.get('post')  # 从 session 获取用户 post

        all_data = [
            {
                "name": "成品送库单",
                "children": [
                    {"name": "成品送库单数据修改"},
                    {"name": "成品送库单数据汇总"},
                    {"name": "添加成品送库单"}
                ]
            },
            {
                "name": "主控电话通知",
                "children": [
                    {"name": "添加主控电话通知"},
                    {"name": "主控通知数据汇总"},
                    {"name": "主控通知数据修改"},
                ]
            },
            {
                "name": "干燥二数据管理",
                "children": [
                    {"name": "干燥二数据编辑"},
                    {"name": "干燥二备注修改"},
                    {"name": "干燥二数据汇总"},
                    {"name": "干燥二备注添加"}
                ]
            },
            {
                "name": "蒸发四数据管理",
                "children": [
                    {"name": "蒸发四数据编辑"},
                    {"name": "蒸发四备注修改"},
                    {"name": "蒸发四数据汇总"},
                    {"name": "蒸发四备注添加"}
                ]
            },
            {
                "name": "蒸发二数据管理",
                "children": [
                    {"name": "蒸发二数据编辑"},
                    {"name": "蒸发二备注修改"},
                    {"name": "蒸发二数据汇总"},
                    {"name": "蒸发二备注添加"}
                ]
            },
            {
                "name": "蒸发一数据管理",
                "children": [
                    {"name": "蒸发一数据编辑"},
                    {"name": "蒸发一备注修改"},
                    {"name": "蒸发一数据汇总"},
                    {"name": "蒸发一备注添加"}
                ]
            },
            {
                "name": "干燥一数据管理",
                "children": [
                    {"name": "干燥一数据编辑"},
                    {"name": "干燥一备注修改"},
                    {"name": "干燥一数据汇总"},
                    {"name": "干燥一备注添加"},
                ]
            },
            {
                "name": "蒸发三数据管理",
                "children": [
                    {"name": "蒸发三数据编辑"},
                    {"name": "蒸发三备注修改"},
                    {"name": "蒸发三数据汇总"},
                    {"name": "蒸发三备注添加"}
                ]
            },
            {
                "name": "产量情况统计表",
                "children": [
                    {"name": "产量统计表数据编辑"},
                    {"name": "产量统计表数据汇总"}
                ]
            },
            {
                "name": "空压机数据管理",
                "children": [
                    {"name": "空压机数据编辑"},
                    {"name": "空压机备注修改"},
                    {"name": "空压机数据汇总"},
                    {"name": "空压机备注添加"}
                ]
            },
            {
                "name": "用户与报警设置",
                "children": [
                    {"name": "用户编辑"},
                    {"name": "用户添加"},
                    {"name": "工艺流程"},
                    {"name": "报警编辑"},
                    {"name": "报警添加"},
                ]
            },
            # {
            #     "name": "报警管理",
            #     # "children": [
            #     #     {"name": "报警编辑"},
            #     #     {"name": "报警添加"},
            #     # ]
            # },
            {
                "name": "年度同环比",
                "children": [
                    {"name": "年度同环比编辑"},
                ]
            },
            {
                "name": "电汽卤数据管理",
                "children": [
                    {"name": "电汽卤数据添加"},
                    {"name": "电汽卤数据汇总"},
                ]
            },
            {
                "name": "碘含量检测",
                "children": [
                    {"name": "数据编辑"},
                    {"name": "历史记录"},
                ]
            },
            {
                "name": "备注录入",
                "children": [
                    # {"name": "数据录入"},
                    {"name": "蒸三、四、空压机"},
                    {"name": "干燥一备注录入"},
                    {"name": "干燥二备注录入"},
                    {"name": "蒸发一、二录入"},
                ]
            },
            {
                "name": "亚铁氰化钾",
                "children": [
                    {
                        "name": "消耗记录",
                        "children": [
                            {"name": "数据编辑"},
                            {"name": "数据汇总"}
                        ]
                    },
                    {
                        "name": "岗位记录",
                        "children": [
                            {"name": "数据编辑"},
                            {"name": "数据汇总"}
                        ]
                    }
                ]
            },
            {
                "name": "录入",
                "children": [
                ]
            },
            {
                "name": "查询",
                "children": [
                    #     {"name": "数据汇总"},
                    #     {"name": "干燥二"},
                    #     {"name": "蒸发一"},
                    #     {"name": "蒸发二"},
                    #     {"name": "蒸发三"},
                    #     {"name": "蒸发四"},
                    #     {"name": "空压机"},
                    #     {"name": "产量情况统计表"},
                    #     {"name": "主控电话通知"},
                    #     {"name": "碘酸钾消耗记录"},
                    #     {"name": "碘酸钾岗位记录"},
                    #     {"name": "亚铁氰化钾消耗记录"},
                    #     {"name": "亚铁氰化钾岗位记录"},
                    #     {"name": "成品送库单"},
                ]
            },
            {
                "name": "干燥二",
                "children": [

                ]
            },
            {
                "name": "蒸发一",
                "children": [

                ]
            },
            {
                "name": "蒸发二",
                "children": [

                ]
            },
            {
                "name": "蒸发三",
                "children": [

                ]
            },
            {
                "name": "蒸发四",
                "children": [

                ]
            },
            {
                "name": "空压机",
                "children": [

                ]
            },
            {
                "name": "产量情况统计表",
                "children": [

                ]
            },
            {
                "name": "主控电话通知",
                "children": [

                ]
            },
            {
                "name": "碘酸钾消耗记录",
                "children": [

                ]
            },
            {
                "name": "碘酸钾岗位记录",
                "children": [

                ]
            },
            {
                "name": "亚铁氰化钾消耗记录",
                "children": [

                ]
            },
            {
                "name": "亚铁氰化钾岗位记录",
                "children": [

                ]
            },
            {
                "name": "成品送库单",
                "children": [

                ]
            },

            {
                "name": "碘酸钾",
                "children": [
                    {
                        "name": "消耗记录",
                        "children": [
                            {"name": "数据编辑"},
                            {"name": "数据汇总"}
                        ]
                    },
                    {
                        "name": "岗位记录",
                        "children": [
                            {"name": "数据编辑"},
                            {"name": "数据汇总"}
                        ]
                    }
                ]
            }
        ]

        # 定义需要排除的菜单
        excluded_admin = ["用户与报警设置", "年度同环比", "备注录入"]
        excluded_roles = ["用户与报警设置", "年度同环比", "工艺流程"]

        # 特殊逻辑处理 admin 用户
        # if username == "admin":
        # 仅显示查询和录入顶级菜单，但数据中仍包含完整的子菜单
        # filtered_data = [item for item in all_data if item["name"] not in excluded_admin]
        # response_data = {
        # "code": 0,
        # "message": "获取权限成功",
        # "data": filtered_data
        # }
        if role == "管理员":
            # 超级管理员获取全部数据
            response_data = {
                "code": 0,
                "message": "获取权限成功",
                "data": all_data
            }
        elif role in ["班长", "员工"]:
            # 班长和员工获取所有数据，但不包括用户与报警以及数据分析
            filtered_data = [item for item in all_data if item["name"] not in excluded_roles]
            response_data = {
                "code": 0,
                "message": "获取权限成功",
                "data": filtered_data
            }
        else:
            # 如果角色不匹配或没有 post
            response_data = {
                "code": 1,
                "message": "没有权限或未指定post或未登录",
                "data": []
            }

        return jsonify(response_data)
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误


# beizhu_zhengfa1_2---------------------------


@app.route('/beizhu_zhengfa1_2/list', methods=['GET']) # 列出离心机备注表的信息，用group区分组号
def beizhu_zhengfa1_2_list():
    try:
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print("Received start time:", start_time)
        print("Received end time:", end_time)
        # 构造查询
        # query_base = "SELECT * FROM beizhu_1"

        if start_time and end_time:
            query = "SELECT * FROM beizhu_zhengfa1_2 WHERE inputTime BETWEEN %s AND %s"
            # query = f"{query_base} WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()  # 文心一言写的这个就给我删掉了  (这个不写就无法实时更新)
        else:
            # cursor.execute("SELECT * FROM beizhu_1")
            query = "SELECT * FROM beizhu_zhengfa1_2 WHERE inputTime BETWEEN %s AND %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")
            print("start_time", start_time)
            print(type(start_time))

            end_time = d1_at_midnight + timedelta(hours=23, minutes=59, seconds=59)
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
            print("end_time", end_time)
            print(type(end_time))

            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()
        temp = {}
        result = []
        if data:
            for i in data:
                temp["id"] = i[0]
                temp["inputTime"] = i[1]
                temp["handoverTool"] = i[2]
                temp["deviceHealth"] = i[3]
                temp["environmentHealth"] = i[4]
                temp["successor"] = i[5]
                temp["handoverPerson"] = i[6]
                temp["groupp"] = i[7]
                temp["classes"] = i[8]
                temp["looseAgentConsumptionTotal"] = i[9]
                temp["subTime"] = i[10]
                temp["sub"] = i[11]
                result.append(temp.copy())
            print("result: ", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误



# 更新记录的函数      备注表的更新！ 注意函数名字别重复了 ！！！！！！！！！！
def update_record_beizhu_zhengfa1_2(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE beizhu_zhengfa1_2 SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()


@app.route('/beizhu_zhengfa1_2/update', methods=['GET']) # 更新备注表表的数据,根据数据库里面的id来更新
def beizhu_zhengfa1_2_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')
        groupp = request.args.get('groupp')
        # print(type(groupp))

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'inputTime': request.args.get('inputTime'),
            'handoverTool': request.args.get('handoverTool'),
            'deviceHealth': request.args.get('deviceHealth'),
            'environmentHealth': request.args.get('environmentHealth'),
            'successor': request.args.get('successor'),
            'handoverPerson': request.args.get('handoverPerson'),
            'groupp': request.args.get('groupp'),
            'classes': request.args.get('classes'),
            'looseAgentConsumptionTotal': request.args.get('looseAgentConsumptionTotal'),
            'subTime': request.args.get('subTime')
            , 'sub': request.args.get('sub')
        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_beizhu_zhengfa1_2(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误




# beizhu_zhengfa1_2 -----------------------



# 碘含量历史数据  ----------------------

@app.route('/dianhan_mysql/list', methods=['GET']) # 列出表4信息，默认查询当天
def dianhan_mysql_list():
    db = None
    cursor = None
    try:
        # 每次请求新建数据库连接和游标
        db = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='123456',
            db='js',
            charset='utf8'
        )
        cursor = db.cursor()

        # 获取分页参数和查询时间范围
        page = request.args.get('page', 1, type=int)  # 默认第1页
        perPage = request.args.get('perPage', 15000, type=int)  # 默认每页9000条
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print(type(start_time))
        print("Received start time:", start_time)
        print("Received end time:", end_time)

        # 计算查询的偏移量
        offset = (page - 1) * perPage

        # 构造查询
        query_base = "SELECT * FROM dian_mysql"
        params = []

        if start_time and end_time:
            query = f"{query_base} WHERE tS BETWEEN %s AND %s LIMIT %s OFFSET %s"
            params = [start_time, end_time, perPage, offset]
        else:
            query = f"{query_base} WHERE tS BETWEEN %s AND %s LIMIT %s OFFSET %s"
            # 获取当前时间
            d1 = datetime.now()
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")
            end_time = (d1_at_midnight + timedelta(hours=23, minutes=59, seconds=59)).strftime("%Y-%m-%d %H:%M:%S")
            print("start_time", start_time)
            print("end_time", end_time)
            params = [start_time, end_time, perPage, offset]

        # 执行查询
        cursor.execute(query, params)
        data = cursor.fetchall()

        # 获取总记录数（用于分页计算）
        total_query = "SELECT COUNT(*) FROM dian_mysql"
        if start_time and end_time:
            total_query += " WHERE tS BETWEEN %s AND %s"
            cursor.execute(total_query, (start_time, end_time))
        else:
            cursor.execute(total_query)
        totalCount = cursor.fetchone()[0]

        # 计算总页数
        totalPages = (totalCount // perPage) + (1 if totalCount % perPage > 0 else 0)

        # 转换数据为字典列表
        result = []
        if data:
            for i in data:
                result.append({
                    "id": i[0],
                    "tS": i[1],
                    "aValue": i[2],
                })

        # 构造包含分页信息的响应
        response = {
            'data': result,
            'pagination': {
                'page': page,
                'perPage': perPage,
                'totalCount': totalCount,
                'totalPages': totalPages
            }
        }

        return jsonify(response)
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500
    finally:
        if cursor:
            try:
                cursor.close()
            except:
                pass
        if db:
            try:
                db.close()
            except:
                pass

# 碘含量历史数据 --------------------------






@app.route('/login', methods=['POST'])  # 登录,从yonghu1这个用户表中
def login():
    try:
        # username = request.args.get('user')
        # password = request.args.get('pwd')

        data = request.get_json()
        # print("data", data.get("params")) //这是字典

        username = data.get("params").get('user')
        password = data.get("params").get('pwd')

        if not username or not password:
            return jsonify({"error": "请输入用户名或者密码"}), 400

        try:
            sql = "SELECT * FROM yonghu1 WHERE username = %s"
            cursor.execute(sql, (username,))
            db.commit()  # 这个要是不加就无法实时更新
            data = cursor.fetchone()  # 使用fetchone()因为我们只需要匹配的一个用户

            if data:
                # 假设表中的列顺序是 (id, username, password, role, other_fields...)
                db_username, db_password, db_role = data[1], data[2], data[3]
                if db_username == username and db_password == password:
                    session['username'] = username  # 将用户名保存到session中
                    session['role'] = db_role
                    session['post'] = data[5]

                    # 构建返回的JSON对象，包含角色和其他字段
                    response_data = {
                        "status": 200,
                        "message": "登录成功",
                        "role": db_role,
                        "post": data[5],
                    }
                    return jsonify(response_data), 200
                else:
                    return jsonify({"error": "密码错误"}), 200
            else:
                return jsonify({"error": "账户不存在"}), 200
        except Exception as e:
            return jsonify({"error": "Login failed", "exception": str(e)}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500


@app.route('/adminList/list', methods=['GET'])  # 用户管理表显示  svip
def adminList_list():
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)  # 默认第1页
        perPage = request.args.get('perPage', 10, type=int)  # 默认每页10条

        # 计算查询的偏移量
        offset = (page - 1) * perPage

        # 构造查询
        query = "SELECT id, username, password, role, post FROM yonghu1 LIMIT %s OFFSET %s"
        params = [perPage, offset]

        # 执行查询
        cursor.execute(query, params)
        data = cursor.fetchall()
        db.commit()

        # 获取总记录数（用于分页计算）
        total_query = "SELECT COUNT(*) FROM yonghu1"
        cursor.execute(total_query)
        db.commit()
        totalCount = cursor.fetchone()[0]

        # 计算总页数
        totalPages = (totalCount // perPage) + (1 if totalCount % perPage > 0 else 0)

        # 转换数据为字典列表
        result = []
        if data:
            for i in data:
                result.append({
                    "id": i[0],
                    "username": i[1],
                    "password": i[2],
                    "role": i[3],
                    "post": i[4],  # index 4 for 'post' based on SELECT
                })

        # 构造包含分页信息的响应
        response = {
            'data': result,
            'pagination': {
                'page': page,
                'perPage': perPage,
                'totalCount': totalCount,
                'totalPages': totalPages
            }
        }

        return jsonify(response)
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500


@app.route('/adminList/add', methods=['GET'])  # 用户表添加
def adminList_add():
    try:
        username = request.args.get("username")  # 这里使用form获取数据,可能后面要用json？,现在改为params,也就是args
        password = request.args.get("password")
        role = request.args.get("role")
        post = request.args.get("post")

        try:
            sql = "INSERT INTO yonghu1(username, password,role,post) VALUES (%s, %s, %s, %s)"  # 修改SQL语句以包含password字段
            cursor.execute(sql, [username, password, role, post])
            db.commit()
            print("add a new successfully")
            return jsonify({"msg": "添加成功"}), 200  # 使用标准的HTTP状态码
        except Exception as e:
            print("add a new failed:", e)
            db.rollback()  # 把前面操作撤回
            return jsonify({"error": "添加失败", "exception": str(e)}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误


@app.route('/adminList/del', methods=['GET'])  # 用户表删除
def adminList_del():
    try:
        id = request.args.get('id')
        sql = "DELETE FROM yonghu1 WHERE id = %s"
        cursor.execute(sql, [id])
        db.commit()
        print("del a user successfully")
        return jsonify(msg="删除成功")
    except Exception as e:
        print("del a user failed: ", e)
        db.rollback()  # 把前面操作撤回
        return jsonify(msg="删除失败")


# 更新记录的函数      备注表的更新！ 注意函数名字别重复了 ！！！！！！！！！！
def update_record_admin(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE yonghu1 SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()


@app.route('/adminList/update', methods=['GET'])
def adminList_update():
    try:
        id_to_update = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

        # Check if the ID is 1 and return a specific message
        if id_to_update == '1':
            return jsonify({"error": "admin不可修改的操作"}), 400

        # Filter out the fields we want to update
        update_fields = {
            'username': request.args.get('username'),
            'password': request.args.get('password'),
            'role': request.args.get('role'),
            'post': request.args.get('post'),
        }

        # Filter out fields with None values (optional)
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # Call the function to update the record
        success, message = update_record_admin(id_to_update, update_fields)

        # Return different JSON responses based on the result
        if success:
            return jsonify({"msg": "修改成功"}), 200
        else:
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误




# 权限部分--------------------------------------------------------------------------------------


# 电气卤 填写------------------------------------------------------------------------


@app.route('/threeHand/list', methods=['GET']) # 列出离心机备注表的信息，用group区分组号
def threeHand_list():
    try:
        start_time = request.args.get('start')
        end_time = request.args.get('end')
        # print("Received start time:", start_time)
        # print("Received end time:", end_time)
        # 构造查询
        # query_base = "SELECT * FROM beizhu_1"

        if start_time and end_time:
            query = "SELECT * FROM threehand WHERE inputTime BETWEEN %s AND %s"
            # query = f"{query_base} WHERE inputTime BETWEEN %s AND %s"
            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()  # 文心一言写的这个就给我删掉了  (这个不写就无法实时更新)
        else:
            # cursor.execute("SELECT * FROM beizhu_1")
            query = "SELECT * FROM threehand WHERE inputTime BETWEEN %s AND %s"
            # 获取当前时间
            d1 = datetime.now()
            # 将当前时间转换为当天的零点
            d1_at_midnight = d1.replace(hour=0, minute=0, second=0, microsecond=0)
            # 格式化输出零点时间
            start_time = d1_at_midnight.strftime("%Y-%m-%d %H:%M:%S")
            print("start_time", start_time)
            print(type(start_time))

            end_time = d1_at_midnight + timedelta(hours=23, minutes=59, seconds=59)
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
            print("end_time", end_time)
            print(type(end_time))

            cursor.execute(query, (start_time, end_time))
            data = cursor.fetchall()
            db.commit()
        temp = {}
        result = []
        if data:
            for i in data:
                temp["id"] = i[0]
                temp["inputTime"] = i[1]
                temp["dianHao"] = i[2]
                temp["qiHao"] = i[3]
                temp["luHao"] = i[4]
                temp["classes"] = i[5]
                temp["sub"] = i[6]
                result.append(temp.copy())
            print("result: ", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

@app.route('/threeHand/add', methods=['GET'])  # 离心机备注表添加  group是必填的
def threeHand_add():
    try:
        # inputTime = request.args.get("inputTime")  # 这里使用form获取数据,可能后面要用json？,现在改为params,也就是args
        dianHao = request.args.get("dianHao")
        qiHao = request.args.get("qiHao")
        luHao = request.args.get("luHao")
        sub = request.args.get("sub")
        classes = request.args.get("classes")

        # 获取当前时间段的 inputTime 和 sub
        inputTime, default_sub = get_time_and_sub66()

        if not sub:
            sub = default_sub  # 使用函数返回的默认值

        # 检查是否已经有该时间段的记录
        if inputTime:
            if check_existing_record66(inputTime):
                return jsonify({"error": "数据已存在，添加失败"}), 400

        try:
            sql = "INSERT INTO threehand(inputTime, dianHao,qiHao,luHao,classes,sub) VALUES (%s, %s, %s, %s,%s, %s)"  # 修改SQL语句以包含password字段
            cursor.execute(sql, [inputTime, dianHao, qiHao, luHao, classes, sub])
            db.commit()
            print("add a new successfully")
            return jsonify({"msg": "添加成功"}), 200  # 使用标准的HTTP状态码
        except Exception as e:
            print("add a new failed:", e)
            db.rollback()  # 把前面操作撤回
            return jsonify({"error": "添加失败", "exception": str(e)}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

# 辅助函数：检查当前时间并返回对应的 inputTime 和 sub
def get_time_and_sub66():
    try:
        # 获取当前日期和时间
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式

        # 7:00 到 9:00
        if 7 <= current_time.hour < 9:
            return f"{current_date} 07:30:00", "0-8"

        # 15:00 到 17:00
        elif 15 <= current_time.hour < 17:
            return f"{current_date} 15:30:00", "8-16"

        # 22:00 到 23:59
        elif 22 <= current_time.hour < 24:
            return f"{current_date} 23:30:00", "16-24"

        # 其他时间不允许插入
        else:
            return None, None
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

# 检查是否已存在该时间段的记录
def check_existing_record66(inputTime):
    try:
        sql = "SELECT COUNT(*) FROM threehand WHERE inputTime = %s"
        cursor.execute(sql, (inputTime,))
        count = cursor.fetchone()[0]
        if count > 0:
            return True  # 数据已存在
        else:
            return False  # 数据不存在
    except Exception as e:
        print(f"Error checking existing record: {e}")
        return False


@app.route('/threeHand/del', methods=['GET'])
def threeHand_del():
    try:
        id = request.args.get('id')
        sql = "DELETE FROM threehand WHERE id = %s"
        cursor.execute(sql, [id])
        db.commit()
        print("del a user successfully")
        return jsonify(msg="删除成功")
    except Exception as e:
        print("del a user failed: ", e)
        db.rollback()  # 把前面操作撤回
        return jsonify(msg="删除失败")


# 更新记录的函数      备注表的更新！ 注意函数名字别重复了 ！！！！！！！！！！
def update_record_threeHand(id_to_update, update_fields):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建 SET 子句
            set_clause = ', '.join(f"{key} = %s" for key in update_fields.keys())

            # 构建完整的 UPDATE 语句
            query = f"UPDATE threehand SET {set_clause} WHERE id = %s"

            # 准备参数（更新值和 id）
            params = list(update_fields.values()) + [id_to_update]

            print(query,params)
            # 执行查询
            cursor.execute(query, params)

            # 提交更改
            connection.commit()

            return True, "Record updated successfully"
    except pymysql.Error as e:
        return False, f"Error updating record: {e}"
    finally:
        # 关闭连接（虽然使用 with 语句时连接通常会自动关闭，但显式关闭是个好习惯）
        connection.close()


@app.route('/threeHand/update', methods=['GET']) # 更新备注表表的数据,根据数据库里面的id来更新
def threeHand_update():
    try:
        id_to_update = request.args.get('id')
        # id = request.args.get('id')

        if not id_to_update:
            return jsonify({"error": "Missing 'id' field"}), 400

            # 过滤出我们想要更新的字段和值
        update_fields = {
            'inputTime': request.args.get('inputTime'),
            'dianHao': request.args.get('dianHao'),
            'qiHao': request.args.get('qiHao'),
            'luHao': request.args.get('luHao'),
            'classes': request.args.get('classes')
            , 'sub': request.args.get('sub')
        }

        # 过滤掉值为 None 的字段（可选，取决于你的需求） （有这个代码就表示，比如只需要修改401_1这一个值的时候i，其他你不填，如何数据库里面的也不会改动）
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        # 调用更新记录函数
        success, message = update_record_threeHand(id_to_update, update_fields)

        # 根据操作结果返回不同的JSON响应
        if success:
            # 如果成功，就给前端返回json修改成功
            return jsonify({"msg": "修改成功"}), 200
        else:
            # 反之就是修改失败
            return jsonify({"error": message}), 500
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误



# 电气卤 填写------------------------------------------------------------------------


# 每隔一小时向空压机写入空数据---------------------------------------------------------------------

#DB_CONFIG 这里原本也有的，但删了，上面有一个就行了，调用的也都是get_db_connection

def insert_empty_values():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        now = datetime.now()
        current_hour = now.hour

        for hour in range(current_hour + 1):
            check_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            query = "SELECT * FROM airpressure WHERE inputTime = %s"
            cursor.execute(query, (check_time,))

            if cursor.rowcount == 0:
                insert_query = "INSERT INTO airpressure (inputTime, submitTime) VALUES (%s, %s)"
                cursor.execute(insert_query, (check_time, check_time))
                db.commit()

        # 提前半小时插入下一小时的数据
        next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        query = "SELECT * FROM airpressure WHERE inputTime = %s"
        cursor.execute(query, (next_hour,))

        if cursor.rowcount == 0:
            insert_query = "INSERT INTO airpressure (inputTime, submitTime) VALUES (%s, %s)"
            cursor.execute(insert_query, (next_hour, next_hour))
            db.commit()

        cursor.close()
        db.close()

    except Exception as e:
        logging.error(f"发生错误: {e}")


def insert_empty_values_total():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        now = datetime.now()
        current_hour = now.hour

        for hour in range(current_hour + 1):
            check_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            query = "SELECT * FROM total_biao WHERE inputTime = %s"
            cursor.execute(query, (check_time,))

            if cursor.rowcount == 0:
                insert_query = "INSERT INTO total_biao (inputTime, submitTime) VALUES (%s, %s)"
                cursor.execute(insert_query, (check_time, check_time))
                db.commit()

        # 提前半小时插入下一小时的数据
        next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        query = "SELECT * FROM total_biao WHERE inputTime = %s"
        cursor.execute(query, (next_hour,))

        if cursor.rowcount == 0:
            insert_query = "INSERT INTO total_biao (inputTime, submitTime) VALUES (%s, %s)"
            cursor.execute(insert_query, (next_hour, next_hour))
            db.commit()

        cursor.close()
        db.close()

    except Exception as e:
        logging.error(f"发生错误: {e}")


def insert_empty_values11():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        now = datetime.now()
        this_hour = now.replace(minute=0, second=0, microsecond=0)

        # 检查当前整点是否有数据
        query = "SELECT * FROM biao_1 WHERE inputTime = %s"
        cursor.execute(query, (this_hour,))

        if cursor.rowcount == 0:
            insert_query = "INSERT INTO biao_1 (inputTime, submitTime) VALUES (%s, %s)"
            cursor.execute(insert_query, (this_hour, this_hour))
            db.commit()

        cursor.close()
        db.close()

    except Exception as e:
        logging.error(f"发生错误: {e}")

def insert_empty_values22():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        now = datetime.now()
        this_hour = now.replace(minute=0, second=0, microsecond=0)

        # 检查当前整点是否有数据
        query = "SELECT * FROM biao_2 WHERE inputTime = %s"
        cursor.execute(query, (this_hour,))

        if cursor.rowcount == 0:
            insert_query = "INSERT INTO biao_2 (inputTime, submitTime) VALUES (%s, %s)"
            cursor.execute(insert_query, (this_hour, this_hour))
            db.commit()

        cursor.close()
        db.close()

    except Exception as e:
        logging.error(f"发生错误: {e}")

def insert_empty_values33():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        now = datetime.now()
        this_hour = now.replace(minute=0, second=0, microsecond=0)

        # 检查当前整点是否有数据
        query = "SELECT * FROM nowatera WHERE inputTime = %s"
        cursor.execute(query, (this_hour,))

        if cursor.rowcount == 0:
            insert_query = "INSERT INTO nowatera (inputTime, submitTime) VALUES (%s, %s)"
            cursor.execute(insert_query, (this_hour, this_hour))
            db.commit()

        cursor.close()
        db.close()

    except Exception as e:
        logging.error(f"发生错误: {e}")

def insert_empty_values44():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        now = datetime.now()
        this_hour = now.replace(minute=0, second=0, microsecond=0)

        # 检查当前整点是否有数据
        query = "SELECT * FROM nowaterb WHERE inputTime = %s"
        cursor.execute(query, (this_hour,))

        if cursor.rowcount == 0:
            insert_query = "INSERT INTO nowaterb (inputTime, submitTime) VALUES (%s, %s)"
            cursor.execute(insert_query, (this_hour, this_hour))
            db.commit()

        cursor.close()
        db.close()

    except Exception as e:
        logging.error(f"发生错误: {e}")

def insert_empty_values55():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        now = datetime.now()
        this_hour = now.replace(minute=0, second=0, microsecond=0)

        # 检查当前整点是否有数据
        query = "SELECT * FROM nowaterc WHERE inputTime = %s"
        cursor.execute(query, (this_hour,))

        if cursor.rowcount == 0:
            insert_query = "INSERT INTO nowaterc (inputTime, submitTime) VALUES (%s, %s)"
            cursor.execute(insert_query, (this_hour, this_hour))
            db.commit()

        cursor.close()
        db.close()

    except Exception as e:
        logging.error(f"发生错误: {e}")

def insert_empty_values66():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        now = datetime.now()
        this_hour = now.replace(minute=0, second=0, microsecond=0)

        # 检查当前整点是否有数据
        query = "SELECT * FROM drytwo WHERE inputTime = %s"
        cursor.execute(query, (this_hour,))

        if cursor.rowcount == 0:
            insert_query = "INSERT INTO drytwo (inputTime, submitTime) VALUES (%s, %s)"
            cursor.execute(insert_query, (this_hour, this_hour))
            db.commit()

        cursor.close()
        db.close()

    except Exception as e:
        logging.error(f"发生错误: {e}")


def run_schedule():
    try:
        # 每小时的59分钟执行一次 insert_empty_values11
        schedule.every().hour.at(":59").do(insert_empty_values11)
        schedule.every().hour.at(":59").do(insert_empty_values22)
        schedule.every().hour.at(":59").do(insert_empty_values33)
        schedule.every().hour.at(":59").do(insert_empty_values44)
        schedule.every().hour.at(":59").do(insert_empty_values55)
        schedule.every().hour.at(":59").do(insert_empty_values66)
        # 每半小时执行一次 insert_empty_values
        schedule.every().hour.at(":30").do(insert_empty_values)

        # 每半小时执行一次
        schedule.every().hour.at(":30").do(insert_empty_values_total)

        # 新建的total_beizhu 7.30 15.30 23.30 就直接插入数据，然后它再映射到下面的备注表中，下面的也都改为7.30 15.30 23.30就自动生成了，只不过他们数据为空

        schedule.every().day.at("07:30").do(check_and_insert_data_total1)

        schedule.every().day.at("15:30").do(check_and_insert_data_total2)

        schedule.every().day.at("23:30").do(check_and_insert_data_total3)

        schedule.every().day.at("07:30").do(check_and_insert_data_total4)

        schedule.every().day.at("15:30").do(check_and_insert_data_total5)

        schedule.every().day.at("23:30").do(check_and_insert_data_total6)

        schedule.every().day.at("23:55").do(check_and_insert_data_total7)

        schedule.every().day.at("07:55").do(check_and_insert_data_total8)

        schedule.every().day.at("15:55").do(check_and_insert_data_total9)

        schedule.every().day.at("23:55").do(check_and_insert_data_total10)

        schedule.every().day.at("07:55").do(check_and_insert_data_total11)

        schedule.every().day.at("15:55").do(check_and_insert_data_total12)

        # 每天9点执行 check_and_insert_data  干燥一的
        schedule.every().day.at("07:30").do(check_and_insert_data)

        # 每天17点执行 check_and_insert_data  干燥一的
        schedule.every().day.at("15:30").do(check_and_insert_data1)

        # 每天23:59点执行 check_and_insert_data  干燥一的
        schedule.every().day.at("23:30").do(check_and_insert_data2)

        # 每天9点执行 check_and_insert_data  蒸发三的
        schedule.every().day.at("07:30").do(check_and_insert_data3)

        # 每天17点执行 check_and_insert_data  蒸发三的
        schedule.every().day.at("15:30").do(check_and_insert_data4)

        # 每天23:59点执行 check_and_insert_data  蒸发三的
        schedule.every().day.at("23:30").do(check_and_insert_data5)

        # 每天9点执行 check_and_insert_data  空压机
        schedule.every().day.at("07:30").do(check_and_insert_data6)

        # 每天17点执行 check_and_insert_data  空压机
        schedule.every().day.at("15:30").do(check_and_insert_data7)

        # 每天23:59点执行 check_and_insert_data  空压机
        schedule.every().day.at("23:30").do(check_and_insert_data8)

        # 每天9点执行 check_and_insert_data  蒸发四
        schedule.every().day.at("07:30").do(check_and_insert_data9)

        # 每天17点执行 check_and_insert_data  蒸发四
        schedule.every().day.at("15:30").do(check_and_insert_data10)

        # 每天23:59点执行 check_and_insert_data  蒸发四
        schedule.every().day.at("23:30").do(check_and_insert_data11)

        # 每天9点执行 check_and_insert_data  蒸发二
        schedule.every().day.at("07:30").do(check_and_insert_data12)

        # 每天17点执行 check_and_insert_data  蒸发二
        schedule.every().day.at("15:30").do(check_and_insert_data13)

        # 每天23:59点执行 check_and_insert_data  蒸发二
        schedule.every().day.at("23:30").do(check_and_insert_data14)

        # 每天9点执行 check_and_insert_data  蒸发一
        schedule.every().day.at("07:30").do(check_and_insert_data15)

        # 每天17点执行 check_and_insert_data  蒸发一
        schedule.every().day.at("15:30").do(check_and_insert_data16)

        # 每天23:59点执行 check_and_insert_data  蒸发一
        schedule.every().day.at("23:30").do(check_and_insert_data17)

        # 每天9点执行 check_and_insert_data  干燥二
        schedule.every().day.at("07:30").do(check_and_insert_data18)

        # 每天17点执行 check_and_insert_data  干燥二
        schedule.every().day.at("15:30").do(check_and_insert_data19)

        # 每天23:59点执行 check_and_insert_data  干燥二
        schedule.every().day.at("23:30").do(check_and_insert_data20)

        # # 每天9点执行 check_and_insert_data  电气卤
        # schedule.every().day.at("09:00").do(check_and_insert_data21)
        # # 每天17点执行 check_and_insert_data  电气卤
        # schedule.every().day.at("17:00").do(check_and_insert_data22)
        # # 每天23:59点执行 check_and_insert_data  电气卤
        # schedule.every().day.at("23:59").do(check_and_insert_data23)
        # 电汽卤变为 从时许里面直接取到了，无须自动添加

        while True:
            schedule.run_pending()  # 只需要一个线程来执行所有任务
            time.sleep(59)  # 每分钟检查一次，实际任务会在整点或9点触发
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误


def get_db_connection_1():
    """获取数据库连接，如果连接失效则重新连接"""
    try:
        connection = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='123456',
            db='js',
            port=3306,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=10  # 设置连接超时
        )
        return connection
    except pymysql.MySQLError as e:
        logging.error(f"数据库连接失败: {e}")
        return None


def check_and_insert_data_total1():
    try:
        # 日志输出当前线程的名称
        logging.info(f"当前线程：{threading.current_thread().name}")

        logging.info("开始检查数据...")

        # 数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 07:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM beizhu_total WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有7:30的数据，正在插入...")
                    sub = "8:00"
                    handoverTool = "齐全"
                    deviceHealth = "干净"
                    environmentHealth = "干净"
                    sql = """
                            INSERT INTO beizhu_total(inputTime, sub, handoverTool, deviceHealth, environmentHealth)
                            VALUES (%s, %s, %s, %s, %s)
                        """
                    cursor.execute(sql, [input_time, sub, handoverTool, deviceHealth, environmentHealth])
                    connection.commit()
                    logging.info("成功插入7:30的数据")
                else:
                    logging.info("今天7:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

def check_and_insert_data_total2():
    try:
        # 日志输出当前线程的名称
        logging.info(f"当前线程：{threading.current_thread().name}")

        logging.info("开始检查数据...")

        # 数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 15:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM beizhu_total WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有15:30的数据，正在插入...")
                    sub = "16:00"
                    handoverTool = "齐全"
                    deviceHealth = "干净"
                    environmentHealth = "干净"
                    sql = """
                            INSERT INTO beizhu_total(inputTime, sub, handoverTool, deviceHealth, environmentHealth)
                            VALUES (%s, %s, %s, %s, %s)
                        """
                    cursor.execute(sql, [input_time, sub, handoverTool, deviceHealth, environmentHealth])
                    connection.commit()
                    logging.info("成功插入15:30的数据")
                else:
                    logging.info("今天15:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

def check_and_insert_data_total3():
    try:
        # 日志输出当前线程的名称
        logging.info(f"当前线程：{threading.current_thread().name}")

        logging.info("开始检查数据...")

        # 数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 23:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM beizhu_total WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有23:30的数据，正在插入...")
                    sub = "0:00"
                    handoverTool = "齐全"
                    deviceHealth = "干净"
                    environmentHealth = "干净"
                    sql = """
                            INSERT INTO beizhu_total(inputTime, sub, handoverTool, deviceHealth, environmentHealth)
                            VALUES (%s, %s, %s, %s, %s)
                        """
                    cursor.execute(sql, [input_time, sub, handoverTool, deviceHealth, environmentHealth])
                    connection.commit()
                    logging.info("成功插入23:30的数据")
                else:
                    logging.info("今天23:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

#---------------------------------------------total_beizhu的备注（三个是因为这分为三个时间段）

def check_and_insert_data_total4():
    try:
        # 日志输出当前线程的名称
        logging.info(f"当前线程：{threading.current_thread().name}")

        logging.info("开始检查数据...")

        # 数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 07:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM beizhu_zhengfa1_2 WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有7:30的数据，正在插入...")
                    sub = "8:00"
                    handoverTool = "齐全"
                    deviceHealth = "干净"
                    environmentHealth = "干净"
                    sql = """
                            INSERT INTO beizhu_zhengfa1_2(inputTime, sub, handoverTool, deviceHealth, environmentHealth)
                            VALUES (%s, %s, %s, %s, %s)
                        """
                    cursor.execute(sql, [input_time, sub, handoverTool, deviceHealth, environmentHealth])
                    connection.commit()
                    logging.info("成功插入7:30的数据")
                else:
                    logging.info("今天7:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

def check_and_insert_data_total5():
    try:
        # 日志输出当前线程的名称
        logging.info(f"当前线程：{threading.current_thread().name}")

        logging.info("开始检查数据...")

        # 数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 15:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM beizhu_zhengfa1_2 WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有15:30的数据，正在插入...")
                    sub = "16:00"
                    handoverTool = "齐全"
                    deviceHealth = "干净"
                    environmentHealth = "干净"
                    sql = """
                            INSERT INTO beizhu_zhengfa1_2(inputTime, sub, handoverTool, deviceHealth, environmentHealth)
                            VALUES (%s, %s, %s, %s, %s)
                        """
                    cursor.execute(sql, [input_time, sub, handoverTool, deviceHealth, environmentHealth])
                    connection.commit()
                    logging.info("成功插入15:30的数据")
                else:
                    logging.info("今天15:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

def check_and_insert_data_total6():
    try:
        # 日志输出当前线程的名称
        logging.info(f"当前线程：{threading.current_thread().name}")

        logging.info("开始检查数据...")

        # 数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 23:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM beizhu_zhengfa1_2 WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有23:30的数据，正在插入...")
                    sub = "0:00"
                    handoverTool = "齐全"
                    deviceHealth = "干净"
                    environmentHealth = "干净"
                    sql = """
                            INSERT INTO beizhu_zhengfa1_2(inputTime, sub, handoverTool, deviceHealth, environmentHealth)
                            VALUES (%s, %s, %s, %s, %s)
                        """
                    cursor.execute(sql, [input_time, sub, handoverTool, deviceHealth, environmentHealth])
                    connection.commit()
                    logging.info("成功插入23:30的数据")
                else:
                    logging.info("今天23:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

def check_and_insert_data_total7():
    try:
        logging.info(f"当前线程：{threading.current_thread().name}")
        logging.info("开始检查数据...")

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        # 当前日期
        current_date = datetime.now().strftime('%Y-%m-%d')

        # 要检查的时间点列表
        time_points = ['23:30:00']

        try:
            with connection.cursor() as cursor:
                for time_str in time_points:
                    input_time = f"{current_date} {time_str}"
                    logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                    cursor.execute("SELECT COUNT(*) AS count FROM output WHERE dataTime = %s", [input_time])
                    result = cursor.fetchone()
                    logging.info(f"{input_time} 查询结果：{result}")

                    if result['count'] == 0:
                        logging.info(f"{input_time} 没有数据，正在插入...")

                        sql = """
                            INSERT INTO output(
                                dataTime, timePoint, banci, aban, bban, aqi, bqi, ahao, bhao,
                                atao, btao, amu, bmu, ahui, bhui, acold, bcold,
                                aWater, bWater, aban1, bban1
                            ) VALUES (
                                %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                %s, %s, %s, %s, %s, %s, %s, %s,
                                %s, %s, %s, %s
                            )
                        """
                        # 假设其他字段可以为空或为 NULL，则传入 None
                        cursor.execute(sql, [input_time, '16-24点', None, None, None, None, None,
                                             None, None, None, None, None, None, None, None,
                                             None, None, None, None, None, None])
                        logging.info(f"成功插入 {input_time} 数据")
                    else:
                        logging.info(f"{input_time} 的数据已存在，跳过插入。")

                connection.commit()
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()

    except Exception as e:
        logging.error(f"Error adding record: {e}")
        return jsonify({"error": "服务器内部错误"}), 500

def check_and_insert_data_total8():
    try:
        logging.info(f"当前线程：{threading.current_thread().name}")
        logging.info("开始检查数据...")

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        # 当前日期
        current_date = datetime.now().strftime('%Y-%m-%d')

        # 要检查的时间点列表
        time_points = ['07:30:00']

        try:
            with connection.cursor() as cursor:
                for time_str in time_points:
                    input_time = f"{current_date} {time_str}"
                    logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                    cursor.execute("SELECT COUNT(*) AS count FROM output WHERE dataTime = %s", [input_time])
                    result = cursor.fetchone()
                    logging.info(f"{input_time} 查询结果：{result}")

                    if result['count'] == 0:
                        logging.info(f"{input_time} 没有数据，正在插入...")

                        sql = """
                            INSERT INTO output(
                                dataTime, timePoint, banci, aban, bban, aqi, bqi, ahao, bhao,
                                atao, btao, amu, bmu, ahui, bhui, acold, bcold,
                                aWater, bWater, aban1, bban1
                            ) VALUES (
                                %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                %s, %s, %s, %s, %s, %s, %s, %s,
                                %s, %s, %s, %s
                            )
                        """
                        # 假设其他字段可以为空或为 NULL，则传入 None
                        cursor.execute(sql, [input_time, '0-8点', None, None, None, None, None,
                                             None, None, None, None, None, None, None, None,
                                             None, None, None, None, None, None])
                        logging.info(f"成功插入 {input_time} 数据")
                    else:
                        logging.info(f"{input_time} 的数据已存在，跳过插入。")

                connection.commit()
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()

    except Exception as e:
        logging.error(f"Error adding record: {e}")
        return jsonify({"error": "服务器内部错误"}), 500

def check_and_insert_data_total9():
    try:
        logging.info(f"当前线程：{threading.current_thread().name}")
        logging.info("开始检查数据...")

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        # 当前日期
        current_date = datetime.now().strftime('%Y-%m-%d')

        # 要检查的时间点列表
        time_points = ['15:30:00']

        try:
            with connection.cursor() as cursor:
                for time_str in time_points:
                    input_time = f"{current_date} {time_str}"
                    logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                    cursor.execute("SELECT COUNT(*) AS count FROM output WHERE dataTime = %s", [input_time])
                    result = cursor.fetchone()
                    logging.info(f"{input_time} 查询结果：{result}")

                    if result['count'] == 0:
                        logging.info(f"{input_time} 没有数据，正在插入...")

                        sql = """
                            INSERT INTO output(
                                dataTime, timePoint, banci, aban, bban, aqi, bqi, ahao, bhao,
                                atao, btao, amu, bmu, ahui, bhui, acold, bcold,
                                aWater, bWater, aban1, bban1
                            ) VALUES (
                                %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                %s, %s, %s, %s, %s, %s, %s, %s,
                                %s, %s, %s, %s
                            )
                        """
                        # 假设其他字段可以为空或为 NULL，则传入 None
                        cursor.execute(sql, [input_time, '8-16点', None, None, None, None, None,
                                             None, None, None, None, None, None, None, None,
                                             None, None, None, None, None, None])
                        logging.info(f"成功插入 {input_time} 数据")
                    else:
                        logging.info(f"{input_time} 的数据已存在，跳过插入。")

                connection.commit()
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()

    except Exception as e:
        logging.error(f"Error adding record: {e}")
        return jsonify({"error": "服务器内部错误"}), 500

def check_and_insert_data_total10():
    try:
        logging.info(f"当前线程：{threading.current_thread().name}")
        logging.info("开始检查数据...")

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        # 当前日期
        current_date = datetime.now().strftime('%Y-%m-%d')

        # 要检查的时间点列表
        time_points = ['23:30:00']

        try:
            with connection.cursor() as cursor:
                for time_str in time_points:
                    input_time = f"{current_date} {time_str}"
                    logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                    cursor.execute("SELECT COUNT(*) AS count FROM threehand WHERE inputTime = %s", [input_time])
                    result = cursor.fetchone()
                    logging.info(f"{input_time} 查询结果：{result}")

                    if result['count'] == 0:
                        logging.info(f"{input_time} 没有数据，正在插入...")

                        sql = """
                            INSERT INTO threehand(
                                inputTime, sub, dianHao, qiHao, luHao, classes
                            ) VALUES (
                                %s, %s, %s, %s, %s, %s
                            )
                        """
                        # 假设其他字段可以为空或为 NULL，则传入 None
                        cursor.execute(sql, [input_time, '16-24', None, None, None, None])
                        logging.info(f"成功插入 {input_time} 数据")
                    else:
                        logging.info(f"{input_time} 的数据已存在，跳过插入。")

                connection.commit()
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()

    except Exception as e:
        logging.error(f"Error adding record: {e}")
        return jsonify({"error": "服务器内部错误"}), 500

def check_and_insert_data_total11():
    try:
        logging.info(f"当前线程：{threading.current_thread().name}")
        logging.info("开始检查数据...")

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        # 当前日期
        current_date = datetime.now().strftime('%Y-%m-%d')

        # 要检查的时间点列表
        time_points = ['7:30:00']

        try:
            with connection.cursor() as cursor:
                for time_str in time_points:
                    input_time = f"{current_date} {time_str}"
                    logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                    cursor.execute("SELECT COUNT(*) AS count FROM threehand WHERE inputTime = %s", [input_time])
                    result = cursor.fetchone()
                    logging.info(f"{input_time} 查询结果：{result}")

                    if result['count'] == 0:
                        logging.info(f"{input_time} 没有数据，正在插入...")

                        sql = """
                            INSERT INTO threehand(
                                inputTime,  dianHao, qiHao, luHao, classes,sub
                            ) VALUES (
                                %s, %s, %s, %s, %s, %s
                            )
                        """
                        # 假设其他字段可以为空或为 NULL，则传入 None
                        cursor.execute(sql, [input_time , None , None, None, None, '0-8'])
                        logging.info(f"成功插入 {input_time} 数据")
                    else:
                        logging.info(f"{input_time} 的数据已存在，跳过插入。")

                connection.commit()
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()

    except Exception as e:
        logging.error(f"Error adding record: {e}")
        return jsonify({"error": "服务器内部错误"}), 500


def check_and_insert_data_total12():
    try:
        logging.info(f"当前线程：{threading.current_thread().name}")
        logging.info("开始检查数据...")

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        # 当前日期
        current_date = datetime.now().strftime('%Y-%m-%d')

        # 要检查的时间点列表
        time_points = ['15:30:00']

        try:
            with connection.cursor() as cursor:
                for time_str in time_points:
                    input_time = f"{current_date} {time_str}"
                    logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                    cursor.execute("SELECT COUNT(*) AS count FROM threehand WHERE inputTime = %s", [input_time])
                    result = cursor.fetchone()
                    logging.info(f"{input_time} 查询结果：{result}")

                    if result['count'] == 0:
                        logging.info(f"{input_time} 没有数据，正在插入...")

                        sql = """
                            INSERT INTO threehand(
                                inputTime, sub, dianHao, qiHao, luHao, classes
                            ) VALUES (
                                %s, %s, %s, %s, %s, %s
                            )
                        """
                        # 假设其他字段可以为空或为 NULL，则传入 None
                        cursor.execute(sql, [input_time, '8-16', None, None, None, None])
                        logging.info(f"成功插入 {input_time} 数据")
                    else:
                        logging.info(f"{input_time} 的数据已存在，跳过插入。")

                connection.commit()
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()

    except Exception as e:
        logging.error(f"Error adding record: {e}")
        return jsonify({"error": "服务器内部错误"}), 500


# 修改你的 check_and_insert_data 函数
def check_and_insert_data():
    try:
        # 日志输出当前线程的名称
        logging.info(f"当前线程：{threading.current_thread().name}")

        logging.info("开始检查数据...")

        # 数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 07:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM beizhu_1 WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有7:30的数据，正在插入...")
                    sub = "8:00"
                    handoverTool = "齐全"
                    deviceHealth = "干净"
                    environmentHealth = "干净"
                    sql = """
                            INSERT INTO beizhu_1(inputTime, sub, handoverTool, deviceHealth, environmentHealth)
                            VALUES (%s, %s, %s, %s, %s)
                        """
                    cursor.execute(sql, [input_time, sub, handoverTool, deviceHealth, environmentHealth])
                    connection.commit()
                    logging.info("成功插入7:30的数据")
                else:
                    logging.info("今天7:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

def check_and_insert_data1():
    try:
        # 日志输出当前线程的名称
        logging.info(f"当前线程：{threading.current_thread().name}")

        logging.info("开始检查数据...")

        # 数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 15:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM beizhu_1 WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有15:30的数据，正在插入...")
                    sub = "16:00"
                    handoverTool = "齐全"
                    deviceHealth = "干净"
                    environmentHealth = "干净"
                    sql = """
                            INSERT INTO beizhu_1(inputTime, sub, handoverTool, deviceHealth, environmentHealth)
                            VALUES (%s, %s, %s, %s, %s)
                        """
                    cursor.execute(sql, [input_time, sub, handoverTool, deviceHealth, environmentHealth])
                    connection.commit()
                    logging.info("成功插入15:30的数据")
                else:
                    logging.info("今天15:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

def check_and_insert_data2():
    try:
        # 日志输出当前线程的名称
        logging.info(f"当前线程：{threading.current_thread().name}")

        logging.info("开始检查数据...")

        # 数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 23:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM beizhu_1 WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有23:30的数据，正在插入...")
                    sub = "0:00"
                    handoverTool = "齐全"
                    deviceHealth = "干净"
                    environmentHealth = "干净"
                    sql = """
                            INSERT INTO beizhu_1(inputTime, sub, handoverTool, deviceHealth, environmentHealth)
                            VALUES (%s, %s, %s, %s, %s)
                        """
                    cursor.execute(sql, [input_time, sub, handoverTool, deviceHealth, environmentHealth])
                    connection.commit()
                    logging.info("成功插入23:30的数据")
                else:
                    logging.info("今天23:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

#---------------------------------------------干燥一的备注

#  蒸发三的备注

def check_and_insert_data3():
    try:
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 07:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM beizhu_2 WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                # logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有7:30的数据，正在插入...")
                    sub = "8:00"
                    sql = "INSERT INTO beizhu_2(inputTime, sub) VALUES (%s, %s)"
                    cursor.execute(sql, [input_time, sub])
                    connection.commit()
                    logging.info("成功插入7:30的数据")
                else:
                    logging.info("今天7:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

def check_and_insert_data4():
    try:
        # 日志输出当前线程的名称
        # logging.info(f"当前线程：{threading.current_thread().name}")

        # logging.info("开始检查数据...")

        # 你的数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 15:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM beizhu_2 WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                # logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有15:30的数据，正在插入...")
                    sub = "16:00"
                    sql = "INSERT INTO beizhu_2(inputTime, sub) VALUES (%s, %s)"
                    cursor.execute(sql, [input_time, sub])
                    connection.commit()
                    logging.info("成功插入15:30的数据")
                else:
                    logging.info("今天15:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

def check_and_insert_data5():
    try:
        # 日志输出当前线程的名称
        # logging.info(f"当前线程：{threading.current_thread().name}")

        # logging.info("开始检查数据...")

        # 你的数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 23:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM beizhu_2 WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                # logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有23:30的数据，正在插入...")
                    sub = "0:00"
                    sql = "INSERT INTO beizhu_2(inputTime, sub) VALUES (%s, %s)"
                    cursor.execute(sql, [input_time, sub])
                    connection.commit()
                    logging.info("成功插入23:30的数据")
                else:
                    logging.info("今天23:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

# 蒸发三的备注

def check_and_insert_data6():
    try:
        # 日志输出当前线程的名称
        # logging.info(f"当前线程：{threading.current_thread().name}")

        # logging.info("开始检查数据...")

        # 你的数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 07:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM airpressurea WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                # logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有7:30的数据，正在插入...")
                    sub = "8:00"
                    sql = "INSERT INTO airpressurea(inputTime, sub) VALUES (%s, %s)"
                    cursor.execute(sql, [input_time, sub])
                    connection.commit()
                    logging.info("成功插入7:30的数据")
                else:
                    logging.info("今天7:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

def check_and_insert_data7():
    try:
        # 日志输出当前线程的名称
        # logging.info(f"当前线程：{threading.current_thread().name}")

        # logging.info("开始检查数据...")

        # 你的数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 15:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM airpressurea WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                # logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有15:30的数据，正在插入...")
                    sub = "16:00"
                    sql = "INSERT INTO airpressurea(inputTime, sub) VALUES (%s, %s)"
                    cursor.execute(sql, [input_time, sub])
                    connection.commit()
                    logging.info("成功插入15:30的数据")
                else:
                    logging.info("今天15:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

def check_and_insert_data8():
    try:
        # 日志输出当前线程的名称
        # logging.info(f"当前线程：{threading.current_thread().name}")

        # logging.info("开始检查数据...")

        # 你的数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 23:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM airpressurea WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                # logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有23:30的数据，正在插入...")
                    sub = "0:00"
                    sql = "INSERT INTO airpressurea(inputTime, sub) VALUES (%s, %s)"
                    cursor.execute(sql, [input_time, sub])
                    connection.commit()
                    logging.info("成功插入23:30的数据")
                else:
                    logging.info("今天23:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

#  空压机备注自动添加

def check_and_insert_data9():
    try:
        # 日志输出当前线程的名称
        # logging.info(f"当前线程：{threading.current_thread().name}")

        # logging.info("开始检查数据...")

        # 你的数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 07:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM nowatercc WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                # logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有7:30的数据，正在插入...")
                    sub = "8:00"
                    sql = "INSERT INTO nowatercc(inputTime, sub) VALUES (%s, %s)"
                    cursor.execute(sql, [input_time, sub])
                    connection.commit()
                    logging.info("成功插入7:30的数据")
                else:
                    logging.info("今天7:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

def check_and_insert_data10():
    try:
        # 日志输出当前线程的名称
        # logging.info(f"当前线程：{threading.current_thread().name}")

        # logging.info("开始检查数据...")

        # 你的数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 15:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM nowatercc WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                # logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有15:30的数据，正在插入...")
                    sub = "16:00"
                    sql = "INSERT INTO nowatercc(inputTime, sub) VALUES (%s, %s)"
                    cursor.execute(sql, [input_time, sub])
                    connection.commit()
                    logging.info("成功插入15:30的数据")
                else:
                    logging.info("今天15:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

def check_and_insert_data11():
    try:
        # 日志输出当前线程的名称
        # logging.info(f"当前线程：{threading.current_thread().name}")

        # logging.info("开始检查数据...")

        # 你的数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 23:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM nowatercc WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                # logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有23:30的数据，正在插入...")
                    sub = "0:00"
                    sql = "INSERT INTO nowatercc(inputTime, sub) VALUES (%s, %s)"
                    cursor.execute(sql, [input_time, sub])
                    connection.commit()
                    logging.info("成功插入23:30的数据")
                else:
                    logging.info("今天23:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

#  蒸发四备注自动添加


def check_and_insert_data12():
    try:
        # 日志输出当前线程的名称
        # logging.info(f"当前线程：{threading.current_thread().name}")

        # logging.info("开始检查数据...")

        # 你的数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 07:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM nowaterbb WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                # logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有7:30的数据，正在插入...")
                    sub = "8:00"
                    sql = "INSERT INTO nowaterbb(inputTime, sub) VALUES (%s, %s)"
                    cursor.execute(sql, [input_time, sub])
                    connection.commit()
                    logging.info("成功插入7:30的数据")
                else:
                    logging.info("今天7:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

def check_and_insert_data13():
    try:
        # 日志输出当前线程的名称
        # logging.info(f"当前线程：{threading.current_thread().name}")

        # logging.info("开始检查数据...")

        # 你的数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 15:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM nowaterbb WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                # logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有15:30的数据，正在插入...")
                    sub = "16:00"
                    sql = "INSERT INTO nowaterbb(inputTime, sub) VALUES (%s, %s)"
                    cursor.execute(sql, [input_time, sub])
                    connection.commit()
                    logging.info("成功插入15:30的数据")
                else:
                    logging.info("今天15:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

def check_and_insert_data14():
    try:
        # 日志输出当前线程的名称
        # logging.info(f"当前线程：{threading.current_thread().name}")

        # logging.info("开始检查数据...")

        # 你的数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 23:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM nowaterbb WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                # logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有23:30的数据，正在插入...")
                    sub = "0:00"
                    sql = "INSERT INTO nowaterbb(inputTime, sub) VALUES (%s, %s)"
                    cursor.execute(sql, [input_time, sub])
                    connection.commit()
                    logging.info("成功插入23:30的数据")
                else:
                    logging.info("今天23:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

#  蒸发二备注自动添加

def check_and_insert_data15():
    try:
        # 日志输出当前线程的名称
        # logging.info(f"当前线程：{threading.current_thread().name}")

        # logging.info("开始检查数据...")

        # 你的数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 07:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM nowateraa WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                # logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有7:30的数据，正在插入...")
                    sub = "8:00"
                    sql = "INSERT INTO nowateraa(inputTime, sub) VALUES (%s, %s)"
                    cursor.execute(sql, [input_time, sub])
                    connection.commit()
                    logging.info("成功插入7:30的数据")
                else:
                    logging.info("今天7:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

def check_and_insert_data16():
    try:
        # 日志输出当前线程的名称
        # logging.info(f"当前线程：{threading.current_thread().name}")

        # logging.info("开始检查数据...")

        # 你的数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 15:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM nowateraa WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                # logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有15:30的数据，正在插入...")
                    sub = "16:00"
                    sql = "INSERT INTO nowateraa(inputTime, sub) VALUES (%s, %s)"
                    cursor.execute(sql, [input_time, sub])
                    connection.commit()
                    logging.info("成功插入15:30的数据")
                else:
                    logging.info("今天15:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

def check_and_insert_data17():
    try:
        # 日志输出当前线程的名称
        # logging.info(f"当前线程：{threading.current_thread().name}")

        # logging.info("开始检查数据...")

        # 你的数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 23:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM nowateraa WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                # logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有23:30的数据，正在插入...")
                    sub = "0:00"
                    sql = "INSERT INTO nowateraa(inputTime, sub) VALUES (%s, %s)"
                    cursor.execute(sql, [input_time, sub])
                    connection.commit()
                    logging.info("成功插入23:30的数据")
                else:
                    logging.info("今天23:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

#  蒸发一备注自动添加

def check_and_insert_data18():
    try:
        # 日志输出当前线程的名称
        logging.info(f"当前线程：{threading.current_thread().name}")

        logging.info("开始检查数据...")

        # 数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 07:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM drytwoa WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有7:30的数据，正在插入...")
                    sub = "8:00"
                    handoverTool = "齐全"
                    deviceHealth = "干净"
                    environmentHealth = "干净"
                    sql = """
                            INSERT INTO drytwoa(inputTime, sub, handoverTool, deviceHealth, environmentHealth)
                            VALUES (%s, %s, %s, %s, %s)
                        """
                    cursor.execute(sql, [input_time, sub, handoverTool, deviceHealth, environmentHealth])
                    connection.commit()
                    logging.info("成功插入7:30的数据")
                else:
                    logging.info("今天7:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

def check_and_insert_data19():
    try:
        # 日志输出当前线程的名称
        logging.info(f"当前线程：{threading.current_thread().name}")

        logging.info("开始检查数据...")

        # 数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 15:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM drytwoa WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有15:30的数据，正在插入...")
                    sub = "16:00"
                    handoverTool = "齐全"
                    deviceHealth = "干净"
                    environmentHealth = "干净"
                    sql = """
                            INSERT INTO drytwoa(inputTime, sub, handoverTool, deviceHealth, environmentHealth)
                            VALUES (%s, %s, %s, %s, %s)
                        """
                    cursor.execute(sql, [input_time, sub, handoverTool, deviceHealth, environmentHealth])
                    connection.commit()
                    logging.info("成功插入15:30的数据")
                else:
                    logging.info("今天15:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

def check_and_insert_data20():
    try:
        # 日志输出当前线程的名称
        logging.info(f"当前线程：{threading.current_thread().name}")

        logging.info("开始检查数据...")

        # 数据库查询和插入逻辑
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')  # 获取当前日期 YYYY-MM-DD 格式
        input_time = f"{current_date} 23:30:00"  # 要检查的时间

        # 获取数据库连接
        connection = get_db_connection_1()
        if connection is None:
            logging.error("数据库连接失败，任务中止")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(f"查询数据库，检查 {input_time} 是否存在数据...")

                cursor.execute("SELECT COUNT(*) AS count FROM drytwoa WHERE inputTime = %s", [input_time])
                result = cursor.fetchone()
                logging.info(f"查询结果：{result}")

                if result['count'] == 0:  # 如果没有数据
                    logging.info("没有23:30的数据，正在插入...")
                    sub = "0:00"
                    handoverTool = "齐全"
                    deviceHealth = "干净"
                    environmentHealth = "干净"
                    sql = """
                            INSERT INTO drytwoa(inputTime, sub, handoverTool, deviceHealth, environmentHealth)
                            VALUES (%s, %s, %s, %s, %s)
                        """
                    cursor.execute(sql, [input_time, sub, handoverTool, deviceHealth, environmentHealth])
                    connection.commit()
                    logging.info("成功插入23:30的数据")
                else:
                    logging.info("今天23:30的数据已存在，跳过插入。")
        except pymysql.MySQLError as e:
            logging.error(f"执行查询失败: {e}")
        finally:
            connection.close()
    except Exception as e:
        print("Error adding record:", e)  # 这里打印日志
        return jsonify({"error": "服务器内部错误"}), 500  # 这里返回统一错误

#  干燥二备注自动添加



if __name__ == '__main__':
    # 启动提示框线程
    #threading.Thread(target=show_startup_message).start()
    # 设置日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    threading.Thread(target=run_schedule, daemon=True).start()

    try:
        server = pywsgi.WSGIServer(('0.0.0.0', 8899), app)
        logging.info("Server started on port 8899")
        server.serve_forever()
    except Exception as e:
        logging.error(f"Failed to start server: {e}")
    finally:
        cursor.close()
        db.close()
        print("数据库连接已关闭。")