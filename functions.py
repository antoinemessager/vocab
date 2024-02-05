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

@st.cache_data 
def load_data(table_name,verbose=False):
    t0=datetime.datetime.utcnow()
    df = get_data(f'select * from {table_name}')
    t1=datetime.datetime.utcnow()  
    dt=(t1-t0).seconds+(t1-t0).microseconds/1e6
    if verbose:
        st.write(f"[timing][{get_str_time()}] loading {table_name} {dt:.2f}s elapsed")
    return df


def get_str_time(date=''):
    '''
    if no date given, it returns the current utc date rounded to the second
    otherwise, it outputs the rounded date
    '''
    if date == '':
        date=datetime.datetime.now()
    date=pd.to_datetime(date)
    return date.strftime("%Y-%m-%d %H:%M:%S")

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
        'word_id':[st.session_state.ord_id],
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