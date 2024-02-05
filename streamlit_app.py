from functions import *

if 'user' not in st.session_state:
    user_df=get_data('select * from users')
    user_df
    user_list=['please select']+user_df.user_name.unique().tolist()+['new']
    user_name=st.selectbox('Who are you?',user_list)
    if user_name != 'please select':
      if user_name == 'new':
        new_user_name=st.text_input('Write down your name').lower()
        if new_user_name in user_list:
          st.write('Name already taken')
        elif new_user_name != '':
          st.session_state.user=new_user_name
          user_id=user_df.shape[0]+1
          st.session_state.user_id=user_id
          run(f"INSERT INTO users (user_id, user_name) VALUES ({user_id}, '{new_user_name}')")
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
          st.rerun()
      else:
        st.session_state.user=user_name
        user_id=get_data(f"select user_id from users where user_name='{user_name}'").user_id.values[0]
        st.session_state.user_id=user_id
        st.rerun()
else:
  user_name=st.session_state.user
  user_id=st.session_state.user_id
  verbose=True
  working_set_size=20
  st.session_state.known_threshold=5

  if 'df_words' not in st.session_state:
    st.write(f'Hello {user_name}!')
    st.session_state.df_words=get_data('select * from es_fr_words')#load_data(table_name='es_fr_words',verbose=verbose)
    st.session_state.df_known_words=get_data(f'select * from known_words_user_{user_id}')#load_data(table_name=f'known_words_user_{user_id}',verbose=verbose)
    st.session_state.df_history=get_data(f'select * from history_user_{user_id}')#load_data(table_name=f'history_user_{user_id}',verbose=verbose)
    st.session_state.known_words=st.session_state.df_known_words.shape[0]
    st.rerun()
  
  st.session_state.df_unknown_words=st.session_state.df_words
  if st.session_state.df_known_words.shape[0]>0:
    st.session_state.df_unknown_words=st.session_state.df_words[~st.session_state.df_words['word_id'].isin(st.session_state.df_known_words.word_id.tolist())].sort_values('word_id').reset_index(drop=True)

  if 'i' not in st.session_state: 
    st.session_state.i=np.random.choice(range(working_set_size))
    st.session_state.reveal=False

  i=int(st.session_state.i)
  word_id=st.session_state.df_unknown_words.word_id.values[i]
  st.session_state.word_id=word_id
  word_fr=st.session_state.df_unknown_words.fr_word.values[i]
  sentence_fr=st.session_state.df_unknown_words.fr_sentence.values[i]
  word_es=st.session_state.df_unknown_words.es_word.values[i]
  sentence_es=st.session_state.df_unknown_words.es_sentence.values[i]


  st.markdown("""<style>.big-font {font-size:30px;}</style>""", unsafe_allow_html=True)
  st.markdown(f"<b class='big-font'>[{word_fr}] </b><text class='big-font'>{sentence_fr}</text>", unsafe_allow_html=True)
  col1, col2, col3, col4 = st.columns(4) 
  with col1:
    st.button(label='unknown',on_click=unknown)
  with col2:
    st.button(label='known',on_click=known)
  with col3:
    st.button(label='too easy',on_click=too_easy)
  with col4:
    st.button(label='reveal',on_click=reveal)

  if st.session_state.reveal:
    st.markdown(f"<b class='big-font'>[{word_es}] </b><text class='big-font'>{sentence_es}</text>", unsafe_allow_html=True)
  else:
    st.markdown("""<style>.big-white-font {font-size:30px;color:white}</style>""", unsafe_allow_html=True)
    st.markdown(f"<b class='big-white-font'>[{word_es}] </b><text class='big-white-font'>{sentence_es}</text>", unsafe_allow_html=True)

  
  progress=int(st.session_state.known_words/4999*100)
  progress_text = f"{st.session_state.known_words} words out of 4999"
  my_bar = st.progress(progress,text=progress_text)
