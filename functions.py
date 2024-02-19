from config import *

def run(query):
    try:
        connection = pymysql.connect(
            charset="utf8mb4",
            connect_timeout=timeout,
            cursorclass=pymysql.cursors.DictCursor,
            db="defaultdb",
            host="vocable-vocable.a.aivencloud.com",
            password=password,
            read_timeout=timeout,
            port=27109,
            user="avnadmin",
            write_timeout=timeout,
        )
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        result=cursor.fetchall()
        if len(result) == 0:
            print("SUCCESS")
        else:
            print(pd.DataFrame(result))
        connection.close()
    except Exception as e:
        print(f'Error {e}')

def get_data(query):
    try:
        connection = pymysql.connect(
            charset="utf8mb4",
            connect_timeout=timeout,
            cursorclass=pymysql.cursors.DictCursor,
            db="defaultdb",
            host="vocable-vocable.a.aivencloud.com",
            password=password,
            read_timeout=timeout,
            port=27109,
            user="avnadmin",
            write_timeout=timeout,
        )
        cursor = connection.cursor()
        cursor.execute(query)
        result=pd.DataFrame(cursor.fetchall())
        connection.close()
        return result
    except Exception as e:
        print(f'Error {e}')

def append_dataframe_to_mysql(dataframe, table_name):
    # Établir la connexion à la base de données MySQL
    connection = pymysql.connect(
          charset="utf8mb4",
          connect_timeout=timeout,
          cursorclass=pymysql.cursors.DictCursor,
          db="defaultdb",
          host="vocable-vocable.a.aivencloud.com",
          password=password,
          read_timeout=timeout,
          port=27109,
          user="avnadmin",
          write_timeout=timeout,
      )
    # Créer un curseur pour exécuter les requêtes SQL
    cursor = connection.cursor()

    # Convertir les types de données du DataFrame en types compatibles avec MySQL
    dataframe = dataframe.map(lambda x: str(x) if pd.notna(x) else None)

    # Générer la requête SQL d'insertion
    columns = ', '.join(dataframe.columns)
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES "
    try:
        insert_query+="('"+"', '".join(dataframe.values[0])+"')"
        for i in range(1,dataframe.shape[0]):
            insert_query+=", ('"+"', '".join(dataframe.values[i])+"')"
        print(insert_query)
        cursor.execute(insert_query)
        
        # Valider les modifications et fermer la connexion
        connection.commit()
        print(f"Les données ont été insérées avec succès dans la table {table_name}")

    except Exception as e:
        # En cas d'erreur, annuler les modifications et afficher l'erreur
        connection.rollback()
        print(f"Erreur lors de l'insertion des données : {e}")

    finally:
        # Fermer le curseur et la connexion
        cursor.close()
        connection.close()

def do_update(box_level):
    ts=datetime.datetime.utcnow()
    new_df=pd.DataFrame({
      'word_id':[st.session_state.word_id],
      'box_level':[box_level],
      'ts':[ts]
    })
    st.session_state.to_append={
        'table_name':f'history_user_{st.session_state.user_id}',
        'df':new_df
    }
    st.session_state.df_box=pd.concat([st.session_state.df_box,new_df]).copy()
    del st.session_state.word_id
    st.session_state.reveal=False
    #run(f"INSERT INTO history_user_{st.session_state.user_id} (word_id, box_level, ts) VALUES ({st.session_state.word_id}, '{box_level}', '{ts}')")

def reveal():
    st.session_state.reveal=True

def unknown():
    box_level=1
    do_update(box_level)


def known():
    box_level=st.session_state.box_level+1
    do_update(box_level)


def too_easy():
    box_level=max(5,st.session_state.box_level+1)
    do_update(box_level)