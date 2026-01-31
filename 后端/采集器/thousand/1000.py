import time
import json
import pymysql
from datetime import datetime, timedelta

# 加载配置
with open('config.json', 'r') as f:
    config = json.load(f)

db_config = config['mysql']
tasks = config['tasks']
interval = config.get('interval', 30)

def get_current_hour():
    now = datetime.now()
    return now.replace(minute=0, second=0, microsecond=0)

def run_task():
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    now_hour = get_current_hour()

    for task in tasks:
        table = task['table']
        source = task['source_field']
        target = task['target_field']

        try:
            # 查询当前整点时间的记录，并且目标字段为空
            query = f"""
                SELECT id, `{source}` FROM `{table}`
                WHERE inputtime = %s AND (`{target}` IS NULL OR `{target}` = '')
            """
            cursor.execute(query, (now_hour,))
            rows = cursor.fetchall()

            for row in rows:
                id, source_value = row
                if source_value is not None:
                    result_value = round(float(source_value) / 1000, 1)
                    update_sql = f"UPDATE `{table}` SET `{target}` = %s WHERE id = %s"
                    cursor.execute(update_sql, (result_value, id))
                    print(f"[{datetime.now()}] Updated {table}.{target} = {result_value} (ID={id})")

        except Exception as e:
            print(f"Error processing table {table}: {e}")
            continue

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    while True:
        run_task()
        time.sleep(interval)
