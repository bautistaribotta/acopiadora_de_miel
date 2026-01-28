
from model.conexion_db import abrir_conexion

def inspect():
    try:
        with abrir_conexion() as (cursor, conexion):
            cursor.execute("SELECT * FROM operaciones LIMIT 1")
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                for i, col in enumerate(columns):
                    print(f"{i}: {col}")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    inspect()
