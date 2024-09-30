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
run(instructions)

