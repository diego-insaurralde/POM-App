import sqlite3

conn = sqlite3.connect("POM.db")
cursor = conn.cursor()
#CRIANDO A TABELA DE INÍCIO 

cursor.execute("""DROP TABLE inicio""")
cursor.execute("""DROP TABLE produtividade""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS inicio(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    meta TEXT NOT NULL,
    dias INTEGER NOT NULL,
    horas_dias INTEGER NOT NULL,
    data_inicio VARCHAR(10) NOT NULL
)
""")

#CRIANDO A TABELA QUE VAI ARMAZENAR A PRODUTIVIDADE DIÁRIA

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtividade(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    data VARCHAR(10) NOT NULL,
    minutos INTEGER NOT NULL,
    id_inicio INTEGER,
    FOREIGN KEY(id_inicio) REFERENCES inicio(id) 
)
""")
executar = False 
if executar: 
    cursor.execute("""
    INSERT INTO produtividade
    (data, minutos, id_inicio)
    VALUES ("2022-08-15", 300, 1)
        """
    )

    conn.commit()

    cursor.execute("""
    INSERT INTO produtividade
    (data, minutos, id_inicio)
    VALUES ("2022-08-16", 400, 1)
        """
    )

    conn.commit()

    cursor.execute("""
    INSERT INTO produtividade
    (data, minutos, id_inicio)
    VALUES ("2022-08-18", 500, 1)
        """
    )

    conn.commit()

    cursor.execute("""
    INSERT INTO produtividade
    (data, minutos, id_inicio)
    VALUES ("2022-08-19", 600, 1)
        """
    )

