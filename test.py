from functions import *
from tqdm import tqdm

data=pd.read_csv('Data/english-learning.csv')
for i in tqdm(range(data.shape[0])):
    id=data['rank'].values[i]
    es=data.word_es.values[i]
    en=data.word_en.values[i]

    instruction=f"""
    INSERT INTO es_to_en_data (word_id, word_es, word_en) 
    VALUES ({id}, '{es}', '{en}');
    """
instruction="select * from es_to_en_data"
df=run(instruction)
print(df)


