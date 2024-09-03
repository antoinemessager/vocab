from functions import *

df=run(
    """CREATE TABLE verb_es_fr AS (
        verb_id integer(5), 
        verb_fr varchar(255),
        verb_es varchar(255),
        present varchar(255),
        futur varchar(255),
        passe varchar(255),
        conditionnel varchar(255),
        PRIMARY KEY (verb_id, verb_fr)
    );
    """)
print(df)
