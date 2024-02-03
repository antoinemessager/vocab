from functions import *


run('drop table if exists ES.nouns')
run("""
CREATE TABLE if not exists ES.nouns (
       id integer(5) primary key not null, 
       es_noun varchar(255) not null, 
       fr_noun varchar(255) not null
)""")

file = open("Data/es_fr_nouns.txt", "r")
f=file.readlines()
i=0
text="INSERT INTO ES.nouns (id, es_noun, fr_noun) VALUES"
for l in f:
    i+=1
    if i < 1997:
        r=int(l.split('.')[0])
        fr=l.split('.')[1].split('–')[0]
        if fr[0] == ' ':
            fr=fr[1:]
        if fr[-1] == ' ':
            fr=fr[:-1]
        es=l.split('.')[1].split('–')[1][:-1]
        if es[0] == ' ':
            es=es[1:]
        if es[-1] == ' ':
            es=es[:-1]
        text+=f"  ({r}, '{es}', '{fr}'),"
run(text[:-1])
run('describe ES.nouns')
run('SELECT * from ES.nouns limit 100')


