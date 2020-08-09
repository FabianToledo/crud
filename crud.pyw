import tkinter
import sqlite3
from tkinter import tix

class BaseDeDatos:

    def __init__(self):

        self.db = sqlite3.connect("database.db")
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute('''
                CREATE TABLE PRODUCTOS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOMBRE_USUARIO VARCHAR(50),
                PASSWORD VARCHAR(50),
                APELLIDO VARCHAR(10),
                DIRECCION VARCHAR(50),
                COMENTARIOS VARCHAR(100))
            ''')
            print("Se creó la tabla")
        except sqlite3.OperationalError:
            print("La tabla ya existe")

    def __del__(self):
        self.db.close()

    def insertar(self, nombre, apellido, password, direccion, comentarios):
        comando = "INSERT INTO PRODUCTOS VALUES(NULL,'{}','{}','{}','{}','{}')".format(nombre, password, apellido, direccion, comentarios)
        self.cursor.execute(comando)
        self.db.commit()



db = BaseDeDatos()


