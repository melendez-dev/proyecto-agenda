import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class AppGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Agenda Económica")
        self.db = Database()
        self.db.connect()
        self.db.create_tables()
        self.db.insert_initial_data()

        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self.master)
        notebook.pack(expand=True, fill="both")

        # Pestaña para crear estudiante
        estudiante_frame = ttk.Frame(notebook)
        notebook.add(estudiante_frame, text="Crear Estudiante")
        self.create_estudiante_widgets(estudiante_frame)

        # Pestaña para crear materia
        materia_frame = ttk.Frame(notebook)
        notebook.add(materia_frame, text="Crear Materia")
        self.create_materia_widgets(materia_frame)

        # Pestaña para crear apunte
        apunte_frame = ttk.Frame(notebook)
        notebook.add(apunte_frame, text="Crear Apunte")
        self.create_apunte_widgets(apunte_frame)

        # Pestaña para listar apuntes
        listar_frame = ttk.Frame(notebook)
        notebook.add(listar_frame, text="Listar Apuntes")
        self.create_listar_widgets(listar_frame)

        # Botón para cerrar el programa
        close_button = ttk.Button(self.master, text="Cerrar Programa", command=self.close_program)
        close_button.pack(pady=10)

    def create_estudiante_widgets(self, parent):
        ttk.Label(parent, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.nombre_estudiante = ttk.Entry(parent)
        self.nombre_estudiante.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(parent, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.email_estudiante = ttk.Entry(parent)
        self.email_estudiante.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(parent, text="Crear Estudiante", command=self.crear_estudiante).grid(row=2, column=0, columnspan=2, pady=10)

    def create_materia_widgets(self, parent):
        ttk.Label(parent, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.nombre_materia = ttk.Entry(parent)
        self.nombre_materia.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(parent, text="Crear Materia", command=self.crear_materia).grid(row=1, column=0, columnspan=2, pady=10)

    def create_apunte_widgets(self, parent):
        ttk.Label(parent, text="Estudiante:").grid(row=0, column=0, padx=5, pady=5)
        self.estudiante_combobox = ttk.Combobox(parent, state="readonly")
        self.estudiante_combobox.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(parent, text="Materia:").grid(row=1, column=0, padx=5, pady=5)
        self.materia_combobox = ttk.Combobox(parent, state="readonly")
        self.materia_combobox.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(parent, text="Tema:").grid(row=2, column=0, padx=5, pady=5)
        self.tema_apunte = ttk.Entry(parent)
        self.tema_apunte.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(parent, text="Descripción:").grid(row=3, column=0, padx=5, pady=5)
        self.descripcion_apunte = tk.Text(parent, height=3, width=30)
        self.descripcion_apunte.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(parent, text="Fecha:").grid(row=4, column=0, padx=5, pady=5)
        self.fecha_apunte = ttk.Entry(parent)
        self.fecha_apunte.grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(parent, text="Crear Apunte", command=self.crear_apunte).grid(row=5, column=0, columnspan=2, pady=10)

    def create_listar_widgets(self, parent):
        ttk.Label(parent, text="Estudiante:").grid(row=0, column=0, padx=5, pady=5)
        self.estudiante_listar_combobox = ttk.Combobox(parent, state="readonly")
        self.estudiante_listar_combobox.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(parent, text="Materia:").grid(row=1, column=0, padx=5, pady=5)
        self.materia_listar_combobox = ttk.Combobox(parent, state="readonly")
        self.materia_listar_combobox.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(parent, text="Listar Apuntes", command=self.listar_apuntes).grid(row=2, column=0, columnspan=2, pady=10)

        self.apuntes_tree = ttk.Treeview(parent, columns=("Tema", "Descripción", "Fecha"), show="headings")
        self.apuntes_tree.heading("Tema", text="Tema")
        self.apuntes_tree.heading("Descripción", text="Descripción")
        self.apuntes_tree.heading("Fecha", text="Fecha")
        self.apuntes_tree.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.update_comboboxes()

    def update_comboboxes(self):
        estudiantes = self.db.get_estudiantes()
        materias = self.db.get_materias()

        self.estudiante_combobox['values'] = [f"{id} - {nombre}" for id, nombre in estudiantes]
        self.materia_combobox['values'] = [f"{id} - {nombre}" for id, nombre in materias]
        self.estudiante_listar_combobox['values'] = [f"{id} - {nombre}" for id, nombre in estudiantes]
        self.materia_listar_combobox['values'] = [f"{id} - {nombre}" for id, nombre in materias]

    def crear_estudiante(self):
        nombre = self.nombre_estudiante.get()
        email = self.email_estudiante.get()
        if nombre and email:
            self.db.crear_estudiante(nombre, email)
            messagebox.showinfo("Éxito", "Estudiante creado correctamente")
            self.nombre_estudiante.delete(0, tk.END)
            self.email_estudiante.delete(0, tk.END)
            self.update_comboboxes()
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos")

    def crear_materia(self):
        nombre = self.nombre_materia.get()
        if nombre:
            self.db.crear_materia(nombre)
            messagebox.showinfo("Éxito", "Materia creada correctamente")
            self.nombre_materia.delete(0, tk.END)
            self.update_comboboxes()
        else:
            messagebox.showerror("Error", "Por favor, ingrese el nombre de la materia")

    def crear_apunte(self):
        estudiante = self.estudiante_combobox.get()
        materia = self.materia_combobox.get()
        tema = self.tema_apunte.get()
        descripcion = self.descripcion_apunte.get("1.0", tk.END).strip()
        fecha = self.fecha_apunte.get()

        if estudiante and materia and tema and descripcion and fecha:
            id_estudiante = int(estudiante.split(" - ")[0])
            id_materia = int(materia.split(" - ")[0])
            self.db.crear_apunte(id_estudiante, id_materia, tema, descripcion, fecha)
            messagebox.showinfo("Éxito", "Apunte creado correctamente")
            self.tema_apunte.delete(0, tk.END)
            self.descripcion_apunte.delete("1.0", tk.END)
            self.fecha_apunte.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos")

    def listar_apuntes(self):
        estudiante = self.estudiante_listar_combobox.get()
        materia = self.materia_listar_combobox.get()

        if estudiante and materia:
            id_estudiante = int(estudiante.split(" - ")[0])
            id_materia = int(materia.split(" - ")[0])
            apuntes = self.db.get_apuntes_estudiante(id_estudiante, id_materia)

            self.apuntes_tree.delete(*self.apuntes_tree.get_children())
            for apunte in apuntes:
                self.apuntes_tree.insert("", tk.END, values=apunte)
        else:
            messagebox.showerror("Error", "Por favor, seleccione un estudiante y una materia")

    def close_program(self):
        self.db.close()
        self.master.destroy()