import sqlite3
import matplotlib.pyplot as plt
from datetime import date

class Crud:

    def insert(self, meta='', dias='', horas_dias='', produtividade=False, data="", minutos="", id_inicio=""):        
        if produtividade:
            data = date.today()
            comando = f'INSERT INTO produtividade (data, minutos, id_inicio) VALUES ("{data}", {minutos}, {id_inicio})'
        else:
            data_inicio = date.today()
            comando = f'INSERT INTO inicio (meta,dias,horas_dias,data_inicio) VALUES ("{meta}",{dias},{horas_dias}, "{data_inicio}")'

        self.cursor.execute(comando)
        self.conn.commit() 

    def read(self, produtividade=False):

        if produtividade:
            self.comando_mostrar = f'SELECT * FROM produtividade'
            self.cursor.execute(self.comando_mostrar)
            self.resultado = self.cursor.fetchall()

            if not self.resultado:
                return [1, '', 1]
            else:
                indice, data, minutos, *desc = self.resultado[-1]  
                return indice, data, minutos

        else:
            self.comando_mostrar = f'SELECT * FROM inicio'
            self.cursor.execute(self.comando_mostrar)
            self.resultado = self.cursor.fetchall()
            if not self.resultado:
                return None
            
            else:
                indice, meta, dias, horas_dias, data_inicio = self.resultado[-1]  
                return indice, meta, dias, horas_dias, data_inicio




    def conectar(self):
        self.conn = sqlite3.connect("POM.db")
        self.cursor = self.conn.cursor()  
    def close(self):
        self.conn.close()
    


class Grafico:
    def __init__(self):        
        conn = sqlite3.connect("POM.db")
        cursor = conn.cursor()
        comando_mostrar = f'SELECT data FROM produtividade'
        cursor.execute(comando_mostrar)

        self.resultado1 = cursor.fetchall()
        self.resultado1 = [x[0] for x in self.resultado1]
        
        comando_mostrar = f'SELECT minutos FROM produtividade'
        cursor.execute(comando_mostrar)

        self.resultado2 = cursor.fetchall()
        self.resultado2 = [x[0] for x in self.resultado2]

        cursor.close()
        conn.close()

        #if False in map(lambda x: True if x//60>=1 else False, self.resultado2):
            #pass
        #else:
            #self.resultado2 = list(map(lambda x: f"{x//60}:{int(x%60)}", self.resultado2))
           # print(self.resultado2)

    def plotar(self):        
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(self.resultado1, self.resultado2)
        ax.set_xlabel("Dias")
        ax.set_ylabel("Tempo")
        ax.set_title("Produtividade")
        fig.savefig("grafico")



