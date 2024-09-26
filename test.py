from functions import *
from tqdm import tqdm

instruction=f"""
    CREATE TABLE es_to_en_history_user_1 (
        word_id integer(5) not null, 
        box_level integer(5) not null,
        ts datetime not null,
        PRIMARY KEY(word_id, ts)
    )"""

df=pd.read_csv('Data/english-learning.csv')
df['rank']=df.index.astype(int)+1
df.to_csv('Data/english-learning.csv',index=False,header=True)



