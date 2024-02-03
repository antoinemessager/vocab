from config import *

def query(text):
    try:
        cursor = connection.cursor()
        cursor.execute(text)
        result=cursor.fetchall()
        if len(result) == 0:
            print("SUCCESS")
        else:
            print(pd.DataFrame(result))
    except Exception as e:
        print(f'Error {e}')
        