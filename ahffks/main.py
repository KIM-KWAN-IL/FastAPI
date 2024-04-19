import pymysql
from fastapi import FastAPI


import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gpt_001 import gpt_test





app = FastAPI()

# 데이터베이스 연결 설정
def get_db_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='5451',
        db='gcumall',
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.get("/")
def read_items():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # SQL 쿼리 실행
            sql = "SELECT * FROM board"
            cursor.execute(sql)

            # 결과 가져오기
            result = cursor.fetchall()
            return result
    finally:
        # 데이터베이스 연결 종료
        connection.close()
        

@app.get("/gpt")
def chat():
    return gpt_test.result.content