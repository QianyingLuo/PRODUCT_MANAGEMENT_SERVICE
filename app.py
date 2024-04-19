from tkinter import ttk
from tkinter import *
import sqlite3

class Producto:

    db ="database/productos.db"

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Productos")
        self.ventana.resizable(1,1) # Habilita la redimensión
        self.ventana.wm_iconbitmap("resources/icon.ico")

        # Creación del contenedor
        frame = LabelFrame(self.ventana, text="Registrar un nuevo Producto")
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ")
        self.etiqueta_nombre.grid(row=1, column=0)

        # Entry Nombre
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ")
        self.etiqueta_precio.grid(row=2, column=0)

        # Entry Precio
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1)

        # Botón Añadir Producto
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto", command=self.add_producto)
        #Importante: aunque add_producto es una función, no ponemos (), command ya está preparada para
        # ejecutar funciones
        self.boton_aniadir.grid(row=3, columnspan=2, sticky=W+E)

        # Tabla de Productos
        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Calibri', 11))  # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea',
                    {'sticky': 'nswe'})])  # Eliminamos los bordes

        # Estructura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=2, style="mystyle.Treeview")
        self.tabla.grid(row=4, column=0, columnspan=2)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)  # Encabezado 0
        self.tabla.heading('#1', text='Precio', anchor=CENTER)  # Encabezado 1

        self.get_productos()

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):
        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros = self.db_consulta(query)
        #print(registros)

        for fila in registros:
            print(fila)
            self.tabla.insert("", 0, text=fila[1], values=fila[2])
            #0 significa empezar desde arriba de la tabla, para la primera columna siempre es text, a partir de la segunda es values

    def validacion_nombre(self):
        return len(self.nombre.get()) != 0

    def validacion_precio(self):
        return len(self.precio.get()) != 0

    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio():
            print(self.nombre.get())
            print(self.precio.get())
        elif self.validacion_nombre() and self.validacion_precio() == False:
            print("El precio es obloigatorio")
        elif self.validacion_nombre() == False and self.validacion_precio():
            print("El nombre es obloigatorio")
        else:
            print("El nombre y el precio son obloigatorios")


if __name__ == "__main__":
    root = Tk() # un constructor que construye la ventana
    app = Producto(root)
    root.mainloop() # para mantener una ventana