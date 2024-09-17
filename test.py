from functions import *
from tqdm import tqdm

instruction="""
INSERT INTO es_to_en_users (user_id, user_name) 
VALUES (1, 'Antoine');
"""
df=run(instruction)
print(df)


