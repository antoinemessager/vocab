from functions import *
from tqdm import tqdm

df=pd.read_csv('Data/data.csv')
instructions="""CREATE TABLE IF NOT EXISTS fr_to_es_data (
    word_id INT AUTO_INCREMENT PRIMARY KEY,
    word_fr VARCHAR(255) NOT NULL,
    word_es VARCHAR(255) NOT NULL
);
"""
run(instructions)
df_done=get_data('select * from fr_to_es_data')
if df_done.shape[0]>0:
    df_to_do=df[df['rank'].isin(df_done.word_id)==False]
else:
    df_to_do=df
print(df_to_do.shape[0])
instructions='''
INSERT INTO fr_to_es_data (word_id, word_fr, word_es) VALUES
'''
nb=min(200,df_to_do.shape[0])
for i in range(df_to_do.shape[0])[:nb-1]:
    instructions+=f"({df_to_do['rank'].values[i]}, \'{df_to_do['word_fr'].values[i]}\', \'{df_to_do['word_es'].values[i]}\'),  \n "
instructions+=f"({df_to_do['rank'].values[nb-1]}, \'{df_to_do['word_fr'].values[nb-1]}\', \'{df_to_do['word_es'].values[nb-1]}\')  \n "
run(instructions)
