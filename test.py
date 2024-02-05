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
        success bool not null,
        ts datetime primary key not null
    )""")
    run(f'drop table if exists known_words_user_{user_id}')
    run(f"""
    CREATE TABLE known_words_user_{user_id} (
        word_id integer(5) primary key not null, 
        ts datetime not null
    )""")
    run('show tables')
else:
    run('select * from history_user_1')
    run('select * from known_words_user_1')