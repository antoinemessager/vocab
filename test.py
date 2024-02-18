from functions import *

reset=False
if reset:
    run('drop table if exists users')
    run("""
    CREATE TABLE users (
        user_id integer(5) primary key not null, 
        user_name varchar(255) not null
    )""")
    run("INSERT INTO users (user_id, user_name) VALUES (1, 'antoine')")
    user_id=1
    run(f'drop table if exists history_user_{user_id}')
    run(f"""
    CREATE TABLE history_user_{user_id} (
        word_id integer(5) not null, 
        box_level integer(5) not null,
        ts datetime not null,
        PRIMARY KEY(word_id, ts)
    )""")
    run('show tables')
else:
    df=get_data('select * from history_user_2')
    df=df.groupby('word_id').tail(1)
    print(df)
    df['box_level']=df['box_level'].replace({7:5,6:4,5:4,4:3,3:2})
    df['ts']=datetime.datetime.utcnow()
    print(df)
    append_dataframe_to_mysql(df, 'history_user_2')
"""
1: au hasard parmi tous les elements (max 20 éléments nouveaux)
2: au moins 2min
3: au moins 5min
4: au moins 1j
5: au moins 3j
6: au moins 1s
7: au moins 1mois
8: succès
"""