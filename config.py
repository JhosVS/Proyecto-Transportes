import pyodbc

class Config:
    # Configuración de la base de datos SQL Server
    SERVER = 'localhost'  # o tu servidor de SQL Server
    DATABASE = 'PascoTravel1'
    DRIVER = '{ODBC Driver 17 for SQL Server}'  # Ajusta según tu driver
    
    # Cadena de conexión
    CONNECTION_STRING = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'
    
    # Configuración Flask
    SECRET_KEY = 'tu_clave_secreta_aqui'
    DEBUG = True

def get_db_connection():
    """Establece conexión con la base de datos"""
    try:
        conn = pyodbc.connect(Config.CONNECTION_STRING)
        return conn
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return None