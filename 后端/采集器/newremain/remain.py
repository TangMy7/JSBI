import os
import time
import requests
import configparser
from datetime import datetime, timedelta, timezone

import configparser

import mysql.connector
from mysql.connector import pooling
import json
from datetime import datetime


def load_mysql_config(config_file):
    """从配置文件加载MySQL配置"""
    config = configparser.ConfigParser()
    with open(config_file, 'r', encoding='utf-8') as file:
        config.read_file(file)
    return {
        "host": config['MySQL']['Host'].strip(),
        "user": config['MySQL']['User'].strip(),
        "password": config['MySQL']['Password'].strip(),
        "database": config['MySQL']['Database'].strip(),
    }


config_file = 'config.cfg'  # 配置文件路径

# 从配置文件加载MySQL配置
dbconfig = load_mysql_config(config_file)

# 使用配置文件中的信息创建连接池
connection_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **dbconfig)


def get_connection():
    """从连接池获取连接"""
    return connection_pool.get_connection()


def insert_data_to_mysql(table_name, data):
    """将数据插入到 MySQL 表中"""
    conn = get_connection()
    cursor = conn.cursor()

    # 获取表的字段
    fields = get_table_fields(conn, cursor, table_name)
    fields = fields[1:]
    field_table_map = field_map[table_name]
    field_dict = map_data_to_fields(data, field_table_map)
    # 构建插入查询
    insert_query, insert_values = build_insert_query(table_name, fields, field_dict)

    try:
        # 执行插入查询
        cursor.execute(insert_query, insert_values)
        # 提交事务
        conn.commit()
        print("数据插入成功！")
        return True  # 插入成功返回 True
    except mysql.connector.Error as err:
        # print(f"插入数据时出错: {err}")
        conn.rollback()  # 回滚事务
        return False
    finally:
        # 关闭连接
        cursor.close()
        conn.close()


def select_child_table_name():
    try:
        # 从连接池获取连接
        conn = connection_pool.get_connection()
        cursor = conn.cursor()

        # 查询超表的所有子表名称
        cursor.execute(
            "select name from jingshen_td_childtable_name where parent_name = 'meters';")  # 将TABLES改成 mysql中对应的表名

        # 获取所有结果并生成列表
        child_table_names = [row[0] for row in cursor.fetchall()]

        return child_table_names

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

    finally:
        # 确保游标和连接被关闭
        cursor.close()
        conn.close()


def load_field_map(filename):
    """加载字段映射，支持一对多映射"""
    with open(filename, 'r') as f:
        base_map = json.load(f)

    # 处理一对多映射
    expanded_map = {}
    for table_name, field_mappings in base_map.items():
        expanded_map[table_name] = {}
        for td_field, mysql_fields in field_mappings.items():
            if isinstance(mysql_fields, str):
                # 单个映射
                expanded_map[table_name][td_field] = [mysql_fields]
            elif isinstance(mysql_fields, list):
                # 多个映射
                expanded_map[table_name][td_field] = mysql_fields
            else:
                expanded_map[table_name][td_field] = [mysql_fields]
    return expanded_map


def get_table_fields(conn, cursor, table_name):
    """获取指定表的字段名"""
    # 查询表字段
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    fields = [row[0] for row in cursor.fetchall()]
    return fields


def build_insert_query(table_name, field_names, field_dict):
    """构建完整的 INSERT 语句"""
    # 过滤出存在于 field_dict 中的字段
    valid_field_names = [field for field in field_names if field in field_dict]

    # 构建字段字符串和占位符字符串
    fields_str = ", ".join([f"`{field}`" for field in valid_field_names])
    placeholders_str = ", ".join(["%s"] * len(valid_field_names))

    insert_query = f"INSERT INTO {table_name} ({fields_str}) VALUES ({placeholders_str})"

    # 返回完整的插入查询和对应的值
    return insert_query, tuple(field_dict[field] for field in valid_field_names)


def map_data_to_fields(data, field_map):
    """将数据与映射的字段对应起来，支持一对多映射"""
    mapped_values_dict = {
        'inputTime': None,
        'submitTime': None,
    }
    flag = True
    submitTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 遍历数据列表
    for entry in data:
        value = entry[0]  # 获取数据值
        timestamp = entry[1]  # 获取时间戳
        map_key = entry[2]  # 获取映射键

        if flag:
            mapped_values_dict["inputTime"] = timestamp[:-1]
            mapped_values_dict["submitTime"] = submitTime
            flag = False

        # 获取对应的字段名（可能是单个字段名或字段名列表）
        field_names = field_map.get(map_key, [])
        if not isinstance(field_names, list):
            field_names = [field_names]

        # 为每个映射的字段都设置值
        for field_name in field_names:
            if field_name:
                # 判断是否是可以转换成 float 的数值，并保留两位小数
                try:
                    float_value = float(value)
                    formatted_value = round(float_value, 1)  # 保留一位小数
                    mapped_values_dict[field_name] = formatted_value
                except (ValueError, TypeError):
                    # 如果不能转换成 float，例如是 '--' 或 None，就原样保留
                    mapped_values_dict[field_name] = value

    return mapped_values_dict


"""获取字段对应的值"""
field_map = load_field_map("field_map.json")


def find_outer_key_by_inner_key(target_key):
    """
    target_key: 要查找的内层键
    返回包含该键的所有表名列表
    """
    data_dict = load_field_map("field_map.json")
    table_names = []
    for outer_key, inner_dict in data_dict.items():
        if target_key in inner_dict:
            table_names.append(outer_key)
    return table_names


def load_config(config_file):
    """从配置文件加载TD数据库的URL和DATABASE"""
    config = configparser.ConfigParser()
    # 添加encoding='utf-8'
    with open(config_file, 'r', encoding='utf-8') as file:
        config.read_file(file)
    return config['DEFAULT']['Url'], config['DEFAULT']['DATABASE']


def format_query_body(sql_query):
    """格式化SQL查询语句的body"""
    return f"{sql_query}"


def post_to_server(sql_query, url):
    """发送POST请求到TDengine服务器"""
    headers = {
        "Authorization": "Basic cm9vdDp0YW9zZGF0YQ==",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=format_query_body(sql_query), headers=headers)
    return response


def process_response(response):
    """处理从服务器返回的查询结果"""
    if response.status_code == 200:
        try:
            # 将响应内容转为字典，假设TDengine返回JSON格式
            data = response.json()
            return data
        except ValueError:
            print("Error: Response content is not valid JSON")
            return None
    else:
        print(f"Request failed with status code: {response.status_code}")
        return None


def get_table_data(data):
    classified_data = {}

    for value in data:
        if value:
            target_key = value[2]
            # 获取所有包含该键的表名
            table_names = find_outer_key_by_inner_key(value[2])

            # 对每个表名都添加数据
            for table_name in table_names:
                if table_name not in classified_data:
                    classified_data[table_name] = []
                classified_data[table_name].append(value)

    return classified_data


def main():
    try:
        config_file = 'config.cfg'  # 配置文件路径

        # 加载URL配置
        url, td_databse_name = load_config(config_file)
        print(f"URL Loaded from config: {url}")

        while True:
            # 获取当前UTC时间
            now = datetime.now(timezone.utc)

            # 向下取整到最近的整点
            rounded_to_hour = now.replace(minute=0, second=0, microsecond=0)

            # 将取整后的时间加上8个小时
            future_time = rounded_to_hour + timedelta(hours=8)

            # 格式化时间字符串
            formatted_time = future_time.strftime('%Y-%m-%dT%H:%M:00.000Z')
            print(f"查询时间点: {formatted_time}")

            query_res_list = []
            child_table_name_list = select_child_table_name()  # 获取所有子表表名
            print(f"获取到的子表列表: {child_table_name_list}")  # 添加调试信息
            for child_table_name in child_table_name_list:
                tquery = (
                    f'select fvalue,ts ,"{child_table_name}" As name from {td_databse_name}.{child_table_name} where ts =\"{formatted_time}"')
                print(f"执行查询: {tquery}")  # 添加调试信息

                # response = post_to_server(tquery, url)  # 修改这里，从query改为tquery
                # response_json = process_response(response)
                # query_res_list.append(response_json["data"][0])
                response = post_to_server(tquery, url)
                response_json = process_response(response)
                # 检查响应内容是否有效，避免访问空列表
                if response_json and "data" in response_json and isinstance(response_json["data"], list) and len(response_json["data"]) > 0:
                 query_res_list.append(response_json["data"][0])
                else:
                    print(f"子表 {child_table_name} 返回的数据为空或格式错误，跳过。响应内容：{response_json}")
            # 发送SQL查询请求
            try:
                # 处理响应结果，保存到字典
                # data_dict = process_response(response)
                if len(query_res_list) > 0:
                    print("Query result saved to dictionary:")
                    # 获取分类后的数据
                    classified_data = get_table_data(query_res_list)
                    # 将数据插入到 MySQL
                    for table_name, entries in classified_data.items():
                        try:
                            insert_res = insert_data_to_mysql(table_name, entries)
                            if insert_res:
                                print(f"数据成功插入到表 {table_name}。")
                            else:
                                print(f"数据插入到表 {table_name} 失败。")
                        except Exception as e:
                            print(f"插入数据时发生异常: {e}，表名: {table_name}")
                else:
                    print("No data returned or failed to process the response.")

            except Exception as e:
                print(f"Error posting query to server: {e}")

            time.sleep(30)  # 每隔30秒执行一次查询

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
