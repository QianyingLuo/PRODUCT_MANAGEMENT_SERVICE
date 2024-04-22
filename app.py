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
        frame = LabelFrame(self.ventana, text="Registrar un nuevo Producto", font=('Calibri', 16, 'bold'))
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ", font=('Calibri', 13))
        self.etiqueta_nombre.grid(row=1, column=0)

        # Entry Nombre
        self.nombre = Entry(frame, font=('Calibri', 13))
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ", font=('Calibri', 13))
        self.etiqueta_precio.grid(row=2, column=0)

        # Entry Precio
        self.precio = Entry(frame, font=('Calibri', 13))
        self.precio.grid(row=2, column=1)

        # Botón Añadir Producto
        s = ttk.Style()
        s.configure("my.TButton", font=('Calibri', 14, 'bold'))
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto", command=self.add_producto, style="my.TButton")
        #Importante: aunque add_producto es una función, no ponemos (), command ya está preparada para
        # ejecutar funciones
        self.boton_aniadir.grid(row=3, columnspan=2, sticky=W+E)

        # Mensaje informativo para el usuario
        self.mensaje = Label(text="", fg="red")
        self.mensaje.grid(row=3, column=0, columnspan=2, sticky=W+E)

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

        # Botones de editar y eliminar
        s = ttk.Style()
        s.configure("my.TButton", font=('Calibri', 14, 'bold'))
        boton_eliminar = ttk.Button(text="ELIMINAR", command=self.del_producto, style="my.TButton")
        boton_eliminar.grid(row=5, column=0, sticky=W+E)
        boton_editar = ttk.Button(text="EDITAR", command=self.edit_producto, style="my.TButton")
        boton_editar.grid(row=5, column=1, sticky=W+E)

        self.get_productos()

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):

        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

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
            query = "INSERT INTO producto VALUES(NULL, ?, ?)"
            parametros = (self.nombre.get(), self.precio.get())
            self.db_consulta(query, parametros)
            print("Datos guardados")
            self.mensaje["text"] = "Producto {} añadido con éxito".format(self.nombre.get())
            self.nombre.delete(0, END)
            self.precio.delete(0, END)
            #print(self.nombre.get())
            #print(self.precio.get())
        elif self.validacion_nombre() and self.validacion_precio() == False:
            print("El precio es obloigatorio")
            self.mensaje["text"] = "El precio es obloigatorio"
        elif self.validacion_nombre() == False and self.validacion_precio():
            print("El nombre es obloigatorio")
            self.mensaje["text"] = "El nombre es obloigatorio"
        else:
            print("El nombre y el precio son obloigatorios")
            self.mensaje["text"] = "El nombre y el precio son obloigatorios"
        self.get_productos()

    def del_producto(self):
        print("Eliminar producto")
        #print(self.tabla.item(self.tabla.selection()))
        # print(self.tabla.item(self.tabla.selection())["text"])

        self.mensaje["text"] = ""
        nombre = self.tabla.item(self.tabla.selection())["text"]
        query = "DELETE FROM producto WHERE nombre = ?"
        self.db_consulta(query, (nombre,))
        self.mensaje["text"] = "Producto {} eliminado con éxito".format(nombre)
        self.get_productos()

    def edit_producto(self):
        print("Editar producto")
        self.mensaje["text"] = ""

        old_nombre = self.tabla.item(self.tabla.selection())["text"]
        old_precio = self.tabla.item(self.tabla.selection())["values"][0]

        self.ventana_editar = Toplevel() # Crear una ventana nueva
        self.ventana_editar.title("Editar Producto")
        self.ventana_editar.resizable(1, 1)  # Habilita la redimensión
        self.ventana_editar.wm_iconbitmap("resources/icon.ico")

        titulo = Label(self.ventana_editar, text="Edición de Productos", font=("Calibri", 50, "bold"))
        titulo.grid(row=0, column=0)

        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto", font=('Calibri', 16, 'bold'))
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nombre antiguo
        self.etiqueta_nombre_antiguo = Label(frame_ep, text="Nombre antiguo: ", font=("Calibri", 13))
        self.etiqueta_nombre_antiguo.grid(row=2, column=0)
        # Entry Nombre antiguo
        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_nombre), state="readonly", font=("Calibri", 13))
        self.input_nombre_antiguo.grid(row=2, column=1)

        # Label Nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ", font=("Calibri", 13))
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)
        # Entry Nombre nuevo
        self.input_nombre_nuevo = Entry(frame_ep, font=("Calibri", 13))
        self.input_nombre_nuevo.grid(row=3, column=1)

        # Label Precio antiguo
        self.etiqueta_precio_antiguo = Label(frame_ep, text="Precio antiguo: ", font=("Calibri", 13))
        self.etiqueta_precio_antiguo.grid(row=4, column=0)
        # Entry Precio antiguo
        self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio),
                                          state="readonly", font=("Calibri", 13))
        self.input_precio_antiguo.grid(row=4, column=1)

        # Label Precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ", font=("Calibri", 13))
        self.etiqueta_precio_nuevo.grid(row=5, column=0)
        # Entry Precio nuevo
        self.input_precio_nuevo = Entry(frame_ep, font=("Calibri", 13))
        self.input_precio_nuevo.grid(row=5, column=1)

        # Botón Actualizar Producto
        ttk.Style().configure("my.TButton", font=('Calibri', 14, 'bold'))
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto", style="my.TButton", command=lambda: self.actualizar_productos(self.input_nombre_nuevo.get(),
                                                                                        self.input_nombre_antiguo.get(),
                                                                                        self.input_precio_nuevo.get(),
                                                                                        self.input_precio_antiguo.get()))
        self.boton_actualizar.grid(row=6, columnspan=2, sticky=W+E)

    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio):
        query = "UPDATE producto SET nombre = ?, precio = ? WHERE nombre = ? AND precio = ?"
        parametros = (nuevo_nombre, nuevo_precio, antiguo_nombre, antiguo_precio)
        self.db_consulta(query, parametros)
        self.ventana_editar.destroy()
        self.mensaje["text"] = "El producto {} ha sido actualizado con éxito".format(antiguo_nombre)
        self.get_productos()


if __name__ == "__main__":
    root = Tk() # un constructor que construye la ventana
    app = Producto(root)
    root.mainloop() # para mantener una ventana