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

def reveal():
    st.session_state.reveal=True

def unknown():
    st.session_state.reveal=False
    del st.session_state.i
    ts=datetime.datetime.now()
    run(f"INSERT INTO history_user_{st.session_state.user_id} (word_id, success, ts) VALUES ({st.session_state.word_id}, False, '{ts}')")
    new_df=pd.DataFrame({
      'word_id':[st.session_state.word_id],
      'success':[False],
      'ts':[ts]
    })
    st.session_state.df_history=pd.concat([st.session_state.df_history,new_df]).copy()

def known():
    st.session_state.reveal=False
    del st.session_state.i
    ts=datetime.datetime.now()
    run(f"INSERT INTO history_user_{st.session_state.user_id} (word_id, success, ts) VALUES ({st.session_state.word_id}, True, '{ts}')")
    new_df=pd.DataFrame({
      'word_id':[st.session_state.word_id],
      'success':[True],
      'ts':[ts]
    })
    st.session_state.df_history=pd.concat([st.session_state.df_history,new_df]).copy()
    df=st.session_state.df_history
    if df[df.word_id==st.session_state.word_id].success.sum()>=st.session_state.known_threshold:
      run(f"INSERT INTO known_words_user_{st.session_state.user_id} (word_id, ts) VALUES ({st.session_state.word_id},'{ts}')")
      new_df=pd.DataFrame({
        'word_id':[st.session_state.word_id],
        'ts':[ts]
      })
      st.session_state.df_known_words=pd.concat([st.session_state.df_known_words,new_df]).copy()
      st.session_state.known_words+=1


def too_easy():
    st.session_state.reveal=False
    del st.session_state.i
    ts=datetime.datetime.now()
    run(f"INSERT INTO history_user_{st.session_state.user_id} (word_id, success, ts) VALUES ({st.session_state.word_id}, True, '{ts}')")
    new_df=pd.DataFrame({
      'word_id':[st.session_state.word_id],
      'success':[True],
      'ts':[ts]
    })
    st.session_state.df_history=pd.concat([st.session_state.df_history,new_df]).copy()
    run(f"INSERT INTO known_words_user_{st.session_state.user_id} (word_id, ts) VALUES ({st.session_state.word_id},'{ts}')")
    new_df=pd.DataFrame({
      'word_id':[st.session_state.word_id],
      'ts':[ts]
    })
    st.session_state.df_known_words=pd.concat([st.session_state.df_known_words,new_df]).copy()
    st.session_state.known_words+=1