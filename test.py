from functions import *

df=get_data('select * from history_user_2')
df=df.groupby('word_id').tail(1)
print(df)
