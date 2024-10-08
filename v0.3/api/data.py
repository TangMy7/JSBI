from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import taos
import logging

app = Flask(__name__)
CORS(app)  # 启用跨域请求

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 全局变量来保存数据库连接
conn = None

def init_db_connection() -> None:
    """初始化数据库连接"""
    global conn
    try:
        conn = taos.connect(
            host="localhost",
            user="root",
            password="taosdata",
            database="jinshen",
            port=6030
        )
        logger.info("Database connection established")
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}")

def get_latest_value(table_name: str) -> float:
    """获取指定表的最新 fvalue 值"""
    try:
        if conn:
            cursor = conn.cursor()
            
            query = f"SELECT fvalue FROM jinshen.{table_name} ORDER BY ts DESC LIMIT 1;"
            logger.info(f"Executing query: {query}")
            cursor.execute(query)
            query_res = cursor.fetchall()
            result = query_res[0][0] if query_res else None
            logger.info(f"Query result: {result}")
            
            cursor.close()
            
            return round(float(result), 1) if result is not None else None
        else:
            logger.warning("No database connection available")
            return None

    except Exception as e:
        logger.error(f"Error: {e}")
        return None

@app.route("/get_value/<element_id>", methods=["GET"])
def get_value(element_id: str) -> jsonify:
    """API 路由: 获取指定元素 ID 的最新值"""
    value = get_latest_value(element_id)
    return jsonify({"id": element_id, "value": value})

if __name__ == "__main__":
    init_db_connection()
    app.run(debug=True, host='0.0.0.0', port=5000)
