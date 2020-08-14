#import tkinter
import sqlite3
from tkinter import *

class BaseDeDatos:

    def __init__(self):

        self.conexion = sqlite3.connect("database.db")
        self.cursor = self.conexion.cursor()
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
        self.conexion.close()

    def insertar(self, nombre, apellido, password, direccion, comentarios):
        comando = "INSERT INTO PRODUCTOS VALUES(NULL,'{}','{}','{}','{}','{}')".format(nombre, password, apellido, direccion, comentarios)
        self.cursor.execute(comando)
        self.conexion.commit()

    def leer(self, id):
        comando = "SELECT * FROM PRODUCTOS WHERE ID='{}'".format(id)
        self.cursor.execute(comando)
        return self.cursor.fetchall()

    def actualizar(self, id, nombre, apellido, password, direccion, comentarios):
        coma = 0
        comando = "UPDATE PRODUCTOS SET"
        if nombre:
            comando = comando + " NOMBRE_USUARIO = '{}'".format(nombre)
            coma = 1
        if password:
            if coma:
                comando = comando + ","
            comando = comando + " PASSWORD = '{}'".format(password)
            coma = 1
        if apellido:
            if coma:
                comando = comando + ","
            comando = comando + " APELLIDO = '{}'".format(apellido)
            coma = 1
        if direccion:
            if coma:
                comando = comando + ","
            comando = comando + " DIRECCION = '{}'".format(direccion)
            coma = 1
        if comentarios:
            if coma:
                comando = comando + ","
            comando = comando + " COMENTARIOS = '{}'".format(comentarios)
        comando = comando + " WHERE ID = '{}'".format(id)
        self.cursor.execute(comando)
        self.conexion.commit()       

    def borrar(self, id):
        comando = "DELETE FROM PRODUCTOS WHERE ID = '{}'".format(id)
        self.cursor.execute(comando)
        self.conexion.commit()

db = BaseDeDatos()
# #db.insertar("Fabian","Toledo","","","")
# print(db.leer(1))
# db.actualizar("1","Fabian","Toledo","password","Necochea 1256","Comentarios varios")
# # db.borrar(1)
# print(db.leer(1))
main = Tk('Fabian','nombrebase','Aplicación CRUD')

frame1 = Frame(main)
frame1.grid(row=0, column=0)

nombre_entry = Entry(frame1)
nombre_entry.grid(row=0, column=1, padx=10, pady=10)
nombre_label = Label(frame1, text='Nombre:')
nombre_label.grid(row=0, column=0, padx=10, pady=10)

apellido_entry = Entry(frame1)
apellido_entry.grid(row=1, column=1, padx=10, pady=10)
apellido_label = Label(frame1, text='Apellido:')
apellido_label.grid(row=1, column=0, padx=10, pady=10)

pass_entry = Entry(frame1)
pass_entry.grid(row=2, column=1, padx=10, pady=10)
pass_entry.config(show='*')
pass_label = Label(frame1, text='Password:')
pass_label.grid(row=2, column=0, padx=10, pady=10)

direccion_entry = Entry(frame1)
direccion_entry.grid(row=3, column=1, padx=10, pady=10)
direccion_label = Label(frame1, text='Dirección:')
direccion_label.grid(row=3, column=0, padx=10, pady=10)

comentarios_entry = Text(frame1, width=20, height=6)
comentarios_entry.grid(row=4, column=1, padx=10, pady=10)
scrollV = Scrollbar(frame1, command=comentarios_entry.yview)
scrollV.grid(row=4, column=2, sticky='nsew')
comentarios_entry.config(yscrollcommand=scrollV.set)
comentarios_label = Label(frame1, text='Comentarios:')
comentarios_label.grid(row=4, column=0, padx=10, pady=10)

frame2 = Frame(main)
frame2.grid(row=1, column=0)

botonCrear = Button(frame2, text='Crear')
botonCrear.grid(row=0, column=0, padx=10, pady=10)

botonLeer = Button(frame2, text='Leer')
botonLeer.grid(row=0, column=1, padx=10, pady=10)

botonActualizar = Button(frame2, text='Actualizar')
botonActualizar.grid(row=0, column=2, padx=10, pady=10)

botonBorrar = Button(frame2, text='Borrar')
botonBorrar.grid(row=0, column=3, padx=10, pady=10)

main.mainloop()
