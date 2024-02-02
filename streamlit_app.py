import mysql.connector

# Définir les informations de connexion à la base de données
config = {
    'user': 'if0_35903117',
    'password': 'CaSSeTTe8963',
    'host': 'sql113.byetcluster.com',
    'database': 'if0_35903117_vocable',
    'raise_on_warnings': True
}
print(config)
# Créer une connexion à la base de données
try:
    connection = mysql.connector.connect(**config)

    if connection.is_connected():
        print("Connexion réussie à la base de données")

        # Créer un objet curseur pour exécuter des requêtes SQL
        cursor = connection.cursor()

        # Spécifier la table que vous souhaitez interroger
        table_name = 'nouns'

        # Exécuter une requête SQL pour récupérer la première ligne de la table
        query = f"SELECT * FROM {table_name} LIMIT 1"
        cursor.execute(query)

        # Récupérer la première ligne et l'imprimer
        first_row = cursor.fetchone()
        print("Première ligne de la table:")
        print(first_row)

except mysql.connector.Error as err:
    print(f"Erreur: {err}")

finally:
    # Fermer le curseur et la connexion, même en cas d'erreur
    if 'cursor' in locals() and cursor is not None:
        cursor.close()
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connexion à la base de données fermée")
