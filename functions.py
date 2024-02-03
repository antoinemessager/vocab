from config import *

def run(query):
    try:
        connection = pymysql.connect(
            charset="utf8mb4",
            connect_timeout=timeout,
            cursorclass=pymysql.cursors.DictCursor,
            db="defaultdb",
            host="vocable-vocable.a.aivencloud.com",
            password=password,
            read_timeout=timeout,
            port=27109,
            user="avnadmin",
            write_timeout=timeout,
        )
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        result=cursor.fetchall()
        if len(result) == 0:
            print("SUCCESS")
        else:
            print(pd.DataFrame(result))
        connection.close()
    except Exception as e:
        print(f'Error {e}')


def get_data(query):
    try:
        connection = pymysql.connect(
            charset="utf8mb4",
            connect_timeout=timeout,
            cursorclass=pymysql.cursors.DictCursor,
            db="defaultdb",
            host="vocable-vocable.a.aivencloud.com",
            password=password,
            read_timeout=timeout,
            port=27109,
            user="avnadmin",
            write_timeout=timeout,
        )
        cursor = connection.cursor()
        cursor.execute(query)
        result=pd.DataFrame(cursor.fetchall())
        connection.close()
        return result
    except Exception as e:
        print(f'Error {e}')