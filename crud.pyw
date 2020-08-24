#import tkinter
import sqlite3
from tkinter import *
from tkinter import messagebox
import pbkdf2, os, base64

class BaseDeDatos:

    def __init__(self, nombre_archivo):

        self.conexion = sqlite3.connect(nombre_archivo)
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
            # print("Se creó la tabla")
        except sqlite3.OperationalError:
            pass
            # print("La tabla ya existe")

    def __del__(self):
        self.conexion.close()
        # print("Me muero...")

    def insertar(self, nombre, apellido, password, direccion, comentarios):
        comando = "INSERT INTO PRODUCTOS VALUES(NULL,'{}','{}','{}','{}','{}')".format(nombre, password, apellido, direccion, comentarios)
        self.cursor.execute(comando)
        self.conexion.commit()

    def leer(self, id):
        comando = "SELECT * FROM PRODUCTOS WHERE ID='{}'".format(id)
        self.cursor.execute(comando)
        return self.cursor.fetchone()

    def leer_prox(self, id):
        last = self.getLast()
        for i in range(id+1,last[0]+1):
            prox = self.leer(i)
            if not prox:            
                continue
            else:
                return prox

    def leer_ant(self, id):
       
        for i in range(id-1,0,-1):
            prox = self.leer(i)
            if not prox:            
                continue
            else:
                return prox

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
            coma = 1
        if not coma:
            return
        comando = comando + " WHERE ID = '{}'".format(id)
        self.cursor.execute(comando)
        self.conexion.commit()       

    def borrar(self, id):
        comando = "DELETE FROM PRODUCTOS WHERE ID = '{}'".format(id)
        self.cursor.execute(comando)
        self.conexion.commit()

    def getLast(self):
        comando = "SELECT * FROM PRODUCTOS ORDER BY ID DESC LIMIT 1"
        self.cursor.execute(comando)
        return self.cursor.fetchone()

    def buscarPorNombre(self, nombre):
        comando = "SELECT * FROM PRODUCTOS WHERE NOMBRE_USUARIO LIKE '%{}%' COLLATE NOCASE ORDER BY ID ASC".format(nombre)
        self.cursor.execute(comando)
        return self.cursor.fetchall() 

    def buscarPorApellido(self, apellido):
        comando = "SELECT * FROM PRODUCTOS WHERE APELLIDO LIKE '%{}%' COLLATE NOCASE ORDER BY ID ASC".format(apellido)
        self.cursor.execute(comando)
        return self.cursor.fetchall()

    def buscarPorDireccion(self, direccion):
        comando = "SELECT * FROM PRODUCTOS WHERE DIRECCION LIKE '%{}%' COLLATE NOCASE ORDER BY ID ASC".format(direccion)
        self.cursor.execute(comando)
        return self.cursor.fetchall()

    def buscarAny(self, any):
        comando = '''SELECT * FROM PRODUCTOS WHERE 
            NOMBRE_USUARIO LIKE '%{0}%' COLLATE NOCASE OR
            APELLIDO LIKE '%{0}%' COLLATE NOCASE OR 
            DIRECCION LIKE '%{0}%' COLLATE NOCASE OR
            COMENTARIOS LIKE '%{0}%' COLLATE NOCASE
            ORDER BY ID ASC'''.format(any)
        self.cursor.execute(comando)
        return self.cursor.fetchall()

salt = b'\x8c\xbe\x8e*\xdd\xbe\xbf\\\xb7{\x1e2m\xc3\xae\x16\xef\x90\xaa{\x90!\xb4`\t\xee\x8a!\x90\xb0\\\x14'

# Se conecta a la base de datos y se crea un archivo nuevo si es necesario
db = BaseDeDatos("database.db")

main = Tk()
main.title("Aplicación CRUD")


ult_busqueda_nombre=""
ult_busqueda_apellido=""
ult_busqueda_direccion=""
ult_busqueda_comentario=""
ult_busqueda_any=""
datos_nombre_iter : iter
datos_apellido_iter : iter
datos_direccion_iter : iter
datos_any_iter : iter

frame1 = Frame(main)
frame1.grid(row=0, column=0)

data_any = StringVar()
data_id = IntVar(value=1)
data_nombre = StringVar()
data_apellido = StringVar()
data_pass = StringVar()
data_direccion = StringVar()


any_entry = Entry(frame1, textvariable=data_any)
any_entry.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
any_label = Label(frame1, text='Buscar:')
any_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

id_entry = Entry(frame1, textvariable=data_id)
id_entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
id_label = Label(frame1, text='ID:')
id_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

nombre_entry = Entry(frame1, textvariable=data_nombre)
nombre_entry.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
nombre_label = Label(frame1, text='Nombre:')
nombre_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

apellido_entry = Entry(frame1, textvariable=data_apellido)
apellido_entry.grid(row=3, column=1, padx=10, pady=10, sticky='nsew')
apellido_label = Label(frame1, text='Apellido:')
apellido_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

pass_entry = Entry(frame1, textvariable=data_pass)
pass_entry.grid(row=4, column=1, padx=10, pady=10, sticky='nsew')
pass_entry.config(show='*')
pass_label = Label(frame1, text='Password:')
pass_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

direccion_entry = Entry(frame1, textvariable=data_direccion)
direccion_entry.grid(row=5, column=1, padx=10, pady=10, sticky='nsew')
direccion_label = Label(frame1, text='Dirección:')
direccion_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")

comentarios_text = Text(frame1, width=20, height=6)
comentarios_text.grid(row=6, column=1, padx=10, pady=10)
scrollV = Scrollbar(frame1, command=comentarios_text.yview)
scrollV.grid(row=6, column=2, sticky='nsew')
comentarios_text.config(yscrollcommand=scrollV.set)
comentarios_label = Label(frame1, text='Comentarios:')
comentarios_label.grid(row=6, column=0, padx=10, pady=10, sticky="e")
comentarios_text.delete('0.0', END)

frame2 = Frame(main)
frame2.grid(row=1, column=0)

def generar_password(password):
    return str(base64.standard_b64encode(pbkdf2.PBKDF2(password, salt).read(32)),'utf-8')

def actualizarCampos(dato):
    ids, nombre, password, apellido, direccion, comentario = dato
    data_id.set(ids)
    data_nombre.set(nombre)
    data_apellido.set(apellido)
    data_pass.set("")
    data_direccion.set(direccion)
    comentarios_text.delete('1.0', END)
    comentarios_text.insert('1.0', comentario)

def comandoCrear():
    password = generar_password(data_pass.get())
    comm = comentarios_text.get('1.0', 'end-1c')
    db.insertar(data_nombre.get(), data_apellido.get(), password, data_direccion.get(), comm)
    actualizarCampos(db.getLast())


def comandoLeer():
    dato = db.leer(data_id.get())
    if dato:
        actualizarCampos(dato)
    else:
        messagebox.showinfo("Leer", "El ID {} no existe".format(data_id.get()))

def comandoActualizar():
    password = ""
    if data_pass.get():
        password = generar_password(data_pass.get())

    dato = db.leer(data_id.get())
    if dato:
        db.actualizar(data_id.get(),data_nombre.get(),data_apellido.get(),password,data_direccion.get(),comentarios_text.get('1.0', 'end-1c'))
    else:
        messagebox.showinfo("Leer", "El ID {} no existe".format(data_id.get()))

def comandoBorrar():  
    dato = db.leer(data_id.get())
    if dato:
        ids, nombre, password, apellido, direccion, comentario = dato
        ans = messagebox.askyesno("Borrar",
        "¿Está seguro que desea borrar los siguientes datos?:\n"
        "Nombre: {}\n"
        "Apellido: {}\n"
        "Dirección: {}".format(nombre,apellido,direccion))
        if ans == True:
            db.borrar(data_id.get())
            messagebox.showinfo("Borrar", "El ID {} ha sido borrado con éxito".format(data_id.get()))
            comandoClearFields()
    else:
        messagebox.showinfo("Borrar", "El ID {} no existe".format(data_id.get()))

def comandoClearFields():
    # data_id.set(1)
    data_nombre.set("")
    data_apellido.set("")
    data_pass.set("")
    data_direccion.set("")
    comentarios_text.delete('1.0', END)

def comandoProximo():
    dato = db.leer_prox(data_id.get())
    if dato:
        actualizarCampos(dato)
    else:
        messagebox.showinfo("Leer Próximo", "Se ha alcanzado el final de la lista")

def comandoAnterior():
    dato = db.leer_ant(data_id.get())
    if dato:
        actualizarCampos(dato)
    else:
        messagebox.showinfo("Leer Próximo", "Se ha alcanzado el final de la lista")

def comandoBuscarAny():
    global ult_busqueda_any
    global datos_any_iter
    any = data_any.get()
    if not any: return
    
    if (ult_busqueda_any != any):
        ult_busqueda_any = any
        # datos = db.buscarPorNombre(any)
        # datos.extend(db.buscarPorApellido(any))
        # datos.extend(db.buscarPorDireccion(any))
        datos = db.buscarAny(any)
        datos_any_iter = iter(datos)
        if not datos:
            messagebox.showinfo("Busqueda", "No se encontró el nombre")
            ult_busqueda_any=""
            return

    try:
        actualizarCampos(datos_any_iter.__next__())     

    except StopIteration:
        messagebox.showinfo("Busqueda", "Se ha alcanzado el final de la lista")
        ult_busqueda_any=""

def comandoBuscarNombre():
    global ult_busqueda_nombre
    global datos_nombre_iter
    nombre = data_nombre.get()
    if not nombre: return
    
    if (ult_busqueda_nombre != nombre):
        ult_busqueda_nombre = nombre
        datos = db.buscarPorNombre(nombre)
        datos_nombre_iter = iter(datos)
        if not datos:
            messagebox.showinfo("Busqueda", "No se encontró el nombre")
            ult_busqueda_nombre=""
            return

    try:
        actualizarCampos(datos_nombre_iter.__next__())     

    except StopIteration:
        messagebox.showinfo("Busqueda", "Se ha alcanzado el final de la lista")
        ult_busqueda_nombre=""

 
def comandoBuscarApellido():
    global ult_busqueda_apellido
    global datos_apellido_iter
    apellido = data_apellido.get()
    if not apellido: return
    
    if (ult_busqueda_apellido != apellido):
        ult_busqueda_apellido = apellido
        datos = db.buscarPorApellido(apellido)
        datos_apellido_iter = iter(datos)
        if not datos:
            messagebox.showinfo("Busqueda", "No se encontró el apellido")
            ult_busqueda_apellido=""
            return

    try:
        actualizarCampos(datos_apellido_iter.__next__())     

    except StopIteration:
        messagebox.showinfo("Busqueda", "Se ha alcanzado el final de la lista")
        ult_busqueda_apellido=""

def comandoVerificarPass():
    pass_to_check = generar_password(data_pass.get())
    if data_id.get():
        dato = db.leer(data_id.get())
        if dato:
            ids, nombre, password, apellido, direccion, comentario = dato
            if password == pass_to_check:
                messagebox.showinfo("Password Correcto", "Ganaste!!")
            else:
                messagebox.showerror("Password Incorrecto", "Verifique los datos ingresados")

botonCrear = Button(frame2, text='Crear', command=comandoCrear)
botonCrear.grid(row=0, column=0, padx=10, pady=10)

botonLeer = Button(frame2, text='Leer', command=comandoLeer)
botonLeer.grid(row=0, column=1, padx=10, pady=10)

botonActualizar = Button(frame2, text='Actualizar', command=comandoActualizar)
botonActualizar.grid(row=0, column=2, padx=10, pady=10)

botonBorrar = Button(frame2, text='Borrar', command=comandoBorrar)
botonBorrar.grid(row=0, column=3, padx=10, pady=10)

botonClearFields = Button(frame2, text='Limpiar Campos', command=comandoClearFields)
botonClearFields.grid(row=0, column=4, padx=10, pady=10)

botonBuscarAny = Button(frame1, text='Buscar', command=comandoBuscarAny)
botonBuscarAny.grid(row=0, column=3, columnspan=2, padx=10, pady=10)

botonProximo = Button(frame1, text='>', command=comandoProximo)
botonProximo.grid(row=1, column=4, padx=10, pady=10)

botonAnterior = Button(frame1, text='<', command=comandoAnterior)
botonAnterior.grid(row=1, column=3, padx=10, pady=10)

# botonBuscarPorNombre = Button(frame1, text='Buscar', command=comandoBuscarNombre)
# botonBuscarPorNombre.grid(row=2, column=3, padx=10, pady=10)

# botonBuscarPorApellido = Button(frame1, text='Buscar', command=comandoBuscarApellido)
# botonBuscarPorApellido.grid(row=3, column=3, padx=10, pady=10)

botonVerificarPass = Button(frame1, text='Check', command=comandoVerificarPass)
botonVerificarPass.grid(row=4, column=3, columnspan=2, padx=10, pady=10)


def comandoAbout():
    messagebox.showinfo("About","Práctica de python")

def comandoOpenFile():
    pass

#Menús
menubar = Menu(main)
def hello():
    print ("hello!")
# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
# filemenu.add_command(label="Conectar", command=comandoOpenFile)
# filemenu.add_command(label="Save", command=hello)
# filemenu.add_separator()
filemenu.add_command(label="Salir", command=main.destroy)
menubar.add_cascade(label="Archivo", menu=filemenu)

# create more pulldown menus
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Borrar campos", command=comandoClearFields)
# editmenu.add_command(label="Copy", command=hello)
# editmenu.add_command(label="Paste", command=hello)
menubar.add_cascade(label="Editar", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=comandoAbout)
menubar.add_cascade(label="Ayuda", menu=helpmenu)

# display the menu
main.config(menu=menubar)


main.mainloop()
