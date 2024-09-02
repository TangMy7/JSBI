from flask_cors import CORS
from flask import Flask, jsonify, make_response, request
import mysql.connector
import taos

app = Flask(__name__)
CORS(app)

@app.route('/api/mysqldata', methods=['GET'])
def mysqldata():
    # 连接到MySQL数据库
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="jingshen"
    )

    cursor = conn.cursor()

    # 查询数据
    cursor.execute("SELECT zz1 FROM test")
    rows = cursor.fetchall()

    # 关闭数据库连接
    cursor.close()
    conn.close()

    # 将数据转换为JSON格式
    data = [row[0] for row in rows]

    # 创建响应对象
    response = make_response(jsonify(data))
    response.headers['Access-Control-Allow-Origin'] = '*'  # 允许所有域名访问
    return response

def fetch_data_from_tdengine(start_time, end_time):
    conn = taos.connect(
        host="localhost",
        user="root",
        password="taosdata",
        database="log",
        port=6030
    )
    cursor = conn.cursor()
    query = f"SELECT mem FROM log.keeper_monitor_8e166bffaffd0a2f559f9e6f3d76dc26 WHERE ts >= '{start_time}' AND ts <= '{end_time}'"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@app.route('/api/tddata', methods=['GET'])
def get_td_data():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    if not start_time or not end_time:
        return jsonify({'error': 'Missing start_time or end_time'}), 400

    print(f"Received start_time: {start_time}")
    print(f"Received end_time: {end_time}")

    try:
        data = fetch_data_from_tdengine(start_time, end_time)
        return jsonify({'data': data})
    except Exception as e:
        print(f"Error: {e}")  # 输出错误信息到控制台
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
