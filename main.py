from tkinter import *
from tkinter.messagebox import *
import sqlite3
from tkinter import ttk
import re

# ##############################################
# VALIDACIONES
# ##############################################

def validar_nombre(nombre):
    patron = "^[A-Za-záéíóúÁÉÍÓÚñÑ ]{2,20}$"
    return re.match(patron, nombre) is not None

def validar_telefono(telefono):
    patron_telefono = r'^[\+]?[0-9\s\-\(\)]{7,20}$'
    return re.match(patron_telefono, telefono) is not None

def validar_email(email):
    patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron_email, email) is not None

# ##############################################
# MODELO
# ##############################################

def conexion():
    con = sqlite3.connect("mibase.db")
    return con

def crear_tabla():
    con = conexion()
    cursor = con.cursor()
    
    # Primero eliminamos la tabla si existe (para evitar conflictos)
    try:
        cursor.execute("DROP TABLE IF EXISTS contactos")
    except:
        pass
    
    # Creamos la tabla con la estructura correcta
    sql = """CREATE TABLE contactos
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             nombre varchar(20) NOT NULL,
             apellido varchar(20),
             telefono varchar(20),
             email varchar(50))
    """
    cursor.execute(sql)
    con.commit()
    con.close()
    print("Tabla creada correctamente")

def inicializar_base_datos():
    try:
        crear_tabla()
        print("Base de datos inicializada correctamente")
    except Exception as e:
        print("Error al crear la tabla:", e)

def alta(nombre, apellido, telefono, email, tree):
    # Validaciones
    if not nombre or not apellido or not telefono or not email:
        showerror("Error", "Todos los campos son obligatorios")
        return

    if not validar_nombre(nombre):
        showerror("Error", "Nombre inválido. Solo letras y espacios (2-20 caracteres)")
        return

    if not validar_telefono(telefono):
        showerror("Error", "Teléfono inválido. Use solo números, espacios, guiones, +")
        return

    if not validar_email(email):
        showerror("Error", "Email inválido")
        return

    try:
        con = conexion()
        cursor = con.cursor()
        data = (nombre, apellido, telefono, email)
        sql = "INSERT INTO contactos(nombre, apellido, telefono, email) VALUES(?, ?, ?, ?)"
        cursor.execute(sql, data)
        con.commit()
        con.close()
        print("Contacto agendado")
        actualizar_treeview(tree)
        showinfo("Éxito", "Contacto agregado correctamente")
        # Limpiar campos después de agregar
        limpiar_campos()
    except Exception as e:
        showerror("Error", f"Error al insertar: {e}")

def borrar(tree):
    valor = tree.selection()
    if not valor:
        showwarning("Advertencia", "Seleccione un elemento para borrar")
        return

    item = tree.item(valor)
    mi_id = item['text']

    try:
        con = conexion()
        cursor = con.cursor()
        data = (mi_id,)
        sql = "DELETE FROM contactos WHERE id = ?"
        cursor.execute(sql, data)
        con.commit()
        con.close()
        tree.delete(valor)
        print("Contacto eliminado")
        showinfo("Éxito", "Contacto eliminado correctamente")
    except Exception as e:
        showerror("Error", f"Error al borrar: {e}")

def actualizar_treeview(mitreview):
    # Limpiar Treeview
    for item in mitreview.get_children():
        mitreview.delete(item)

    try:
        con = conexion()
        cursor = con.cursor()
        # Consulta segura
        sql = "SELECT id, nombre, apellido, telefono, email FROM contactos ORDER BY id ASC"
        cursor.execute(sql)
        resultado = cursor.fetchall()
        
        for fila in resultado:
            if len(fila) >= 5:
                mitreview.insert("", "end", text=fila[0], values=(fila[1], fila[2], fila[3], fila[4]))
        con.close()
    except Exception as e:
        showerror("Error", f"Error al actualizar vista: {e}")

def limpiar_campos():
    a_val.set("")
    b_val.set("")
    c_val.set("")  
    d_val.set("")

# ##############################################
# VISTA
# ##############################################

root = Tk()
root.title("Agenda de Contactos")

# Inicializar base de datos
inicializar_base_datos()

# Título
titulo = Label(root, text="Ingrese sus datos", bg="DarkOrchid3", fg="thistle1", height=1, width=60)
titulo.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky=W+E)

# Etiquetas
Label(root, text="NOMBRE").grid(row=1, column=0, sticky=W)
Label(root, text="APELLIDO").grid(row=2, column=0, sticky=W)
Label(root, text="TELEFONO").grid(row=3, column=0, sticky=W)
Label(root, text="EMAIL").grid(row=4, column=0, sticky=W)

# Variables
a_val = StringVar()
b_val = StringVar()
c_val = StringVar()
d_val = StringVar()
w_ancho = 20

# Entradas
Entry(root, textvariable=a_val, width=w_ancho).grid(row=1, column=1)
Entry(root, textvariable=b_val, width=w_ancho).grid(row=2, column=1)
Entry(root, textvariable=c_val, width=w_ancho).grid(row=3, column=1)
Entry(root, textvariable=d_val, width=w_ancho).grid(row=4, column=1)

# Treeview
tree = ttk.Treeview(root)
tree["columns"] = ("col1", "col2", "col3", "col4")
tree.column("#0", width=50, minwidth=50, anchor=W)
tree.column("col1", width=150, minwidth=100)
tree.column("col2", width=150, minwidth=100)
tree.column("col3", width=120, minwidth=100)
tree.column("col4", width=200, minwidth=150)
tree.heading("#0", text="ID")
tree.heading("col1", text="NOMBRE")
tree.heading("col2", text="APELLIDO")
tree.heading("col3", text="TELEFONO")
tree.heading("col4", text="EMAIL")
tree.grid(row=10, column=0, columnspan=4, pady=10)

# Botones
Button(root, text="Alta", command=lambda: alta(a_val.get(), b_val.get(), c_val.get(), d_val.get(), tree)).grid(row=6, column=1, pady=5)
Button(root, text="Consultar", command=lambda: print("Consultar")).grid(row=7, column=1, pady=5)
Button(root, text="Borrar", command=lambda: borrar(tree)).grid(row=8, column=1, pady=5)
Button(root, text="Limpiar", command=limpiar_campos).grid(row=9, column=1, pady=5)

# Inicializar Treeview
actualizar_treeview(tree)

root.mainloop()