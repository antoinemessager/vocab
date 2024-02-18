from functions import *

st_theme = st_javascript("""window.getComputedStyle(window.parent.document.getElementsByClassName("stApp")[0]).getPropertyValue("color-scheme")""")

if 'user' not in st.session_state:
    user_df=get_data('select * from users')
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
              box_level integer(5) not null,
              ts datetime not null,
              PRIMARY KEY(word_id, ts)
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
  working_set_size=20
  st.session_state.number_box=5
  dict_level_to_dt_sec={0:0,1:30,2:600,3:3600*24,4:3600*24*7,5:3600*24*30}

  if 'df_words' not in st.session_state:
    st.write(f'Hello {user_name}! Loading data...')
    st.session_state.df_words=get_data('select * from es_fr_words')
    st.session_state.df_box=get_data(f'select * from history_user_{user_id}')
    st.rerun()

  df_words=st.session_state.df_words.copy()
  df_box=st.session_state.df_box.copy()
  df_current_box=pd.DataFrame({'word_id':[],'box_level':[],'ts':[]})
  if df_box.shape[0]>0:
    df_current_box=df_box.sort_values('ts').groupby('word_id').tail(1).reset_index(drop=True)
  if 'word_id' not in st.session_state: 

    nb_level_0=(df_current_box.box_level<=1).sum()
    if nb_level_0<=working_set_size:
      new_word_id=df_words[~df_words.word_id.isin(df_current_box.word_id.tolist())].sort_values('word_id').head(working_set_size-nb_level_0).word_id.tolist()
      df_new_box=pd.DataFrame({
        'word_id':new_word_id,
        'box_level':[0]*len(new_word_id),
        'ts':[datetime.datetime.utcnow()]*len(new_word_id),
      })
      df_box=pd.concat([df_box,df_new_box])
      df_current_box=df_box.sort_values('ts').groupby('word_id').tail(1).reset_index(drop=True)
      st.session_state.df_box=df_box.copy()
      append_dataframe_to_mysql(df_new_box,f'history_user_{user_id}')

    df_current_box['dt']=df_current_box['box_level'].map(dict_level_to_dt_sec)
    df_current_box['min_ts']=pd.to_datetime(pd.to_datetime(df_current_box['ts']).astype(int).div(1e9)+df_current_box['dt'],unit='s')
    df_unknown=df_current_box[df_current_box.min_ts<=pd.to_datetime(datetime.datetime.utcnow())]

  
    st.session_state.reveal=False
    word_id=int(df_unknown.word_id.sample(1).values[0])
    st.session_state.word_id=word_id
    st.session_state.box_level=df_unknown[df_unknown.word_id==word_id].box_level.values[0]

  
  word_id=st.session_state.word_id
  word_fr=df_words[df_words.word_id==word_id].fr_word.values[0]
  sentence_fr=df_words[df_words.word_id==word_id].fr_sentence.values[0]
  word_es=df_words[df_words.word_id==word_id].es_word.values[0]
  sentence_es=df_words[df_words.word_id==word_id].es_sentence.values[0]

  st.markdown("""<style>.big-font {font-size:30px;}</style>""", unsafe_allow_html=True)
  st.markdown(f"<b class='big-font'>[{word_fr}] </b><text class='big-font'>{sentence_fr}</text>", unsafe_allow_html=True)
  
  col1, col2 = st.columns(2) 
  with col1:
    st.write('''<style>
    [data-testid="column"] {
        width: calc(33.3333% - 1rem) !important;
        flex: 1 1 calc(33.3333% - 1rem) !important;
        min-width: calc(33% - 1rem) !important;
    }
    </style>''', unsafe_allow_html=True)
    st.button(label='unknown',on_click=unknown)
    st.button(label='too easy',on_click=too_easy)
  with col2:
    st.write('''<style>
    [data-testid="column"] {
        width: calc(33.3333% - 1rem) !important;
        flex: 1 1 calc(33.3333% - 1rem) !important;
        min-width: calc(33% - 1rem) !important;
    }
    </style>''', unsafe_allow_html=True)
    st.button(label='known',on_click=known)
    st.button(label='reveal',on_click=reveal)
    
  if st.session_state.reveal:
    st.markdown(f"<b class='big-font'>[{word_es}] </b><text class='big-font'>{sentence_es}</text>", unsafe_allow_html=True)
  else:
    if st_theme == 'light':
      st.markdown("""<style>.big-white-font {font-size:30px;color:white}</style>""", unsafe_allow_html=True)
    if st_theme == 'dark':
      st.markdown("""<style>.big-white-font {font-size:30px;color:#0e1117}</style>""", unsafe_allow_html=True)
    st.markdown(f"<b class='big-white-font'>[{word_es}] </b><text class='big-white-font'>{sentence_es}</text>", unsafe_allow_html=True)


  nb_word_learning=df_current_box.box_level.sum()/6
  progress=np.round(nb_word_learning/4999*100,1)
  progress_text = f"learned {nb_word_learning:.1f} words out of 4999"
  my_bar = st.progress(progress,text=progress_text)

  