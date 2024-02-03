from functions import *
  
data=get_data('select * from ES.nouns')

if "i" not in st.session_state:
  i=np.random.choice(range(data.shape[0]))
else:
  i=st.session_state['i']

es=data['es_noun'].values[i]
fr=data['fr_noun'].values[i]
st.write(fr)

def traduction():
    st.session_state.i=i

st.button('Traduction', on_click=traduction)

if "i" in st.session_state:
    st.write(es)

def reset():
    del st.session_state.i
st.button('reset', on_click=reset)


