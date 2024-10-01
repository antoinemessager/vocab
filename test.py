from functions import *
from tqdm import tqdm

instructions='''
CREATE TABLE fr_to_es_users (
    user_id INT PRIMARY KEY,
    user_name VARCHAR(100)
);'''

instructions='''
INSERT INTO fr_to_es_users (user_id, user_name) VALUES
(1, 'Sophie')
'''

run(f"""
CREATE TABLE fr_to_es_history_user_1 (
    word_id integer(5) not null, 
    box_level integer(5) not null,
    ts datetime not null,
    PRIMARY KEY(word_id, ts)
)"""
)

