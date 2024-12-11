import sqlite3
import os

class Database:
    def __init__(self, db_name='agenda_economica.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        );
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS materias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        );
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS apuntes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_estudiante INTEGER NOT NULL,
            id_materia INTEGER NOT NULL,
            tema TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            fecha DATE NOT NULL,
            FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id),
            FOREIGN KEY (id_materia) REFERENCES materias(id)
        );
        ''')

    def insert_initial_data(self):
        estudiantes = [
            ('Ana Martínez', 'ana.martinez@ejemplo.com'),
            ('Carlos López', 'carlos.lopez@ejemplo.com'),
            ('Lucía Gómez', 'lucia.gomez@ejemplo.com'),
            ('Pedro Sánchez', 'pedro.sanchez@ejemplo.com'),
            ('Sofía Ramírez', 'sofia.ramirez@ejemplo.com')
        ]

        materias = [
            ('Introducción a la Economía',),
            ('Matemáticas I',),
            ('Historia del Pensamiento Económico',),
            ('Microeconomía I',),
            ('Contabilidad General',),
            ('Estadística I',)
        ]

        self.cursor.executemany('INSERT OR IGNORE INTO estudiantes (nombre, email) VALUES (?, ?)', estudiantes)
        self.cursor.executemany('INSERT OR IGNORE INTO materias (nombre) VALUES (?)', materias)

        self.conn.commit()

    def get_estudiantes(self):
        self.cursor.execute('SELECT id, nombre FROM estudiantes')
        return self.cursor.fetchall()

    def get_materias(self):
        self.cursor.execute('SELECT id, nombre FROM materias')
        return self.cursor.fetchall()

    def crear_estudiante(self, nombre, email):
        self.cursor.execute('INSERT INTO estudiantes (nombre, email) VALUES (?, ?)', (nombre, email))
        self.conn.commit()

    def crear_materia(self, nombre):
        self.cursor.execute('INSERT INTO materias (nombre) VALUES (?)', (nombre,))
        self.conn.commit()

    def crear_apunte(self, id_estudiante, id_materia, tema, descripcion, fecha):
        self.cursor.execute('INSERT INTO apuntes (id_estudiante, id_materia, tema, descripcion, fecha) VALUES (?, ?, ?, ?, ?)',
                            (id_estudiante, id_materia, tema, descripcion, fecha))
        self.conn.commit()

    def get_apuntes_estudiante(self, id_estudiante, id_materia):
        self.cursor.execute('''
        SELECT a.tema, a.descripcion, a.fecha
        FROM apuntes a
        WHERE a.id_estudiante = ? AND a.id_materia = ?
        ''', (id_estudiante, id_materia))
        return self.cursor.fetchall()
