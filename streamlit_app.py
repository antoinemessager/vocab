from functions import *

def traduction():
    st.session_state.i=i

def reset():
    if 'i' in st.session_state:
      del st.session_state.i
  
data=get_data('select * from ES.nouns')

if "i" not in st.session_state:
  i=np.random.choice(range(data.shape[0]))
else:
  i=st.session_state['i']

es=data['es_noun'].values[i]
fr=data['fr_noun'].values[i]
st.write(fr)

st.button('Traduction', on_click=traduction)

if "i" in st.session_state:
    st.write(es)


st.button('reset', on_click=reset)


