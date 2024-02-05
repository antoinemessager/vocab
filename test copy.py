from functions import *

df=pd.read_csv('Data/5000_words_es_fr.csv')
df_source=pd.read_csv('Data/5000_words_es.csv')
df_missing=pd.merge(
    df,
    df_source.rename(columns={'word':'es_word'}),
    on=['rank','es_word'],
    how='right'
)
df=df_missing[df_missing.fr_word.isna()][['rank','es_word','sentence']].copy()
df.to_csv('Data/missing.csv',header=True,index=False)