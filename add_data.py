from functions import *
from tqdm import tqdm



df=pd.read_csv('Data/english-learning.csv')
df_done=get_data('select * from es_to_en_data')
print(df_done.head(10))
df_to_do=df[df['rank'].isin(df_done.word_id)==False]
instructions='''
INSERT INTO es_to_en_data (word_id, word_es, word_en) VALUES
'''
for i in range(df_to_do.shape[0])[:1]:
    instructions+=f"({df_to_do['rank'].values[i]}, \'{df_to_do['word_es'].values[i]}\', \'{df_to_do['word_en'].values[i]}\') \n"
run(instructions)
