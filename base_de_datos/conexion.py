import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="cursoplatzi"
)

cursor = conexion.cursor()

cursor.execute("SELECT * FROM employees")
resultados = cursor.fetchall()
for fila in resultados:
    print(fila)