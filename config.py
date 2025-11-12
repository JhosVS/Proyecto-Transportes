import pyodbc

class Config:
    # Configuración de la base de datos SQL Server con Windows Authentication
    SERVER = 'localhost'  # o tu servidor de SQL Server (ej: 'localhost\\SQLEXPRESS')
    DATABASE = 'PascoTravel1'
    DRIVER = '{ODBC Driver 17 for SQL Server}'  # Driver más común
    
    # Cadena de conexión para Windows Authentication
    CONNECTION_STRING = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'
    
    # Configuración Flask
    SECRET_KEY = 'tu_clave_secreta_aqui_muy_segura_123'
    DEBUG = True

def get_db_connection():
    """Establece conexión con la base de datos usando Windows Authentication"""
    try:
        conn = pyodbc.connect(Config.CONNECTION_STRING)
        print("✅ Conexión a SQL Server exitosa (Windows Authentication)")
        return conn
    except pyodbc.InterfaceError as e:
        print(f"❌ Error de interfaz ODBC: {e}")
        print("💡 Verifica que el driver ODBC esté instalado")
    except pyodbc.OperationalError as e:
        print(f"❌ Error operacional: {e}")
        print("💡 Verifica que el servidor SQL esté ejecutándose")
    except pyodbc.Error as e:
        print(f"❌ Error de conexión a la base de datos: {e}")
        print("💡 Verifica:")
        print("   - Que el servidor SQL esté ejecutándose")
        print("   - Que la base de datos 'PascoTravel1' exista")
        print("   - Que tengas permisos de acceso")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    
    return None