from config import get_db_connection

class Viaje:
    """Modelo para manejar los viajes"""
    
    @staticmethod
    def buscar_viajes(ciudad_origen, ciudad_destino, fecha):
        """Busca viajes según criterios"""
        conn = get_db_connection()
        if not conn:
            return []
            
        try:
            cursor = conn.cursor()
            
            # Llamar al stored procedure SP_BuscarViajes
            cursor.execute("EXEC SP_BuscarViajes @p_CiudadOrigen=?, @p_CiudadDestino=?, @p_Fecha=?", 
                         (ciudad_origen, ciudad_destino, fecha))
            
            # Obtener resultados
            viajes = []
            columns = [column[0] for column in cursor.description]
            
            for row in cursor.fetchall():
                viaje = dict(zip(columns, row))
                viajes.append(viaje)
                
            return viajes
            
        except Exception as e:
            print(f"Error buscando viajes: {e}")
            return []
        finally:
            conn.close()
    
    @staticmethod
    def obtener_ciudades():
        """Obtiene todas las ciudades disponibles"""
        conn = get_db_connection()
        if not conn:
            return []
            
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Id_Ciudad, Nombre_Ciudad FROM Ciudad ORDER BY Nombre_Ciudad")
            
            ciudades = []
            for row in cursor.fetchall():
                ciudades.append({
                    'id': row[0],
                    'nombre': row[1]
                })
                
            return ciudades
            
        except Exception as e:
            print(f"Error obteniendo ciudades: {e}")
            return []
        finally:
            conn.close()

class Encomienda:
    """Modelo para manejar encomiendas"""
    
    @staticmethod
    def rastrear_encomienda(serie, correlativo, clave_secreta):
        """Rastrea una encomienda"""
        conn = get_db_connection()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor()
            cursor.execute("EXEC SP_RastrearEncomienda @p_Serie=?, @p_Correlativo=?, @p_ClaveSecreta=?", 
                         (serie, correlativo, clave_secreta))
            
            # Obtener información principal
            encomienda = cursor.fetchone()
            if not encomienda:
                return None
            
            # Obtener timeline
            cursor.nextset()
            timeline_data = []
            columns = [column[0] for column in cursor.description]
            
            for row in cursor.fetchall():
                item = dict(zip(columns, row))
                timeline_data.append(item)
            
            return {
                'id': encomienda[0],
                'serie': encomienda[1],
                'correlativo': encomienda[2],
                'origen': encomienda[3],
                'destino': encomienda[4],
                'estado_actual': encomienda[5],
                'timeline': timeline_data
            }
            
        except Exception as e:
            print(f"Error rastreando encomienda: {e}")
            return None
        finally:
            conn.close()

class Agencia:
    """Modelo para manejar agencias"""
    
    @staticmethod
    def obtener_ranking():
        """Obtiene el ranking de agencias"""
        conn = get_db_connection()
        if not conn:
            return []
            
        try:
            cursor = conn.cursor()
            cursor.execute("EXEC SP_ObtenerRankingAgencias @p_Limit=10")
            
            agencias = []
            columns = [column[0] for column in cursor.description]
            
            for row in cursor.fetchall():
                agencia = dict(zip(columns, row))
                agencias.append(agencia)
                
            return agencias
            
        except Exception as e:
            print(f"Error obteniendo ranking: {e}")
            return []
        finally:
            conn.close()

class Usuario:
    """Modelo para manejar usuarios"""
    
    @staticmethod
    def login(email_dni, password, rol='Usuario'):
        """Autentica un usuario"""
        conn = get_db_connection()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor()
            cursor.execute("EXEC SP_LoginUsuario @p_EmailDNI=?, @p_Password=?, @p_Rol=?", 
                         (email_dni, password, rol))
            
            usuario = cursor.fetchone()
            if usuario:
                return {
                    'id': usuario[0],
                    'nombre': usuario[1],
                    'rol': usuario[2]
                }
            return None
            
        except Exception as e:
            print(f"Error en login: {e}")
            return None
        finally:
            conn.close()

class Usuario:
    """Modelo para manejar usuarios"""
    
    @staticmethod
    def login(email_dni, password, rol='Usuario'):
        """Autentica un usuario"""
        conn = get_db_connection()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor()
            cursor.execute("EXEC SP_LoginUsuario @p_EmailDNI=?, @p_Password=?, @p_Rol=?", 
                         (email_dni, password, rol))
            
            usuario = cursor.fetchone()
            if usuario:
                return {
                    'id': usuario[0],
                    'nombre': usuario[1],
                    'rol': usuario[2]
                }
            return None
            
        except Exception as e:
            print(f"Error en login: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def registrar(nombre_completo, email, telefono, password):
        """Registra un nuevo usuario"""
        conn = get_db_connection()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor()
            
            # Verificar si el correo ya existe
            cursor.execute("SELECT Id_Usuario FROM Usuario WHERE Correo_Electronico = ?", (email,))
            if cursor.fetchone():
                return {'error': 'El correo ya está registrado'}
            
            # Insertar nuevo usuario
            cursor.execute("""
                INSERT INTO Usuario (Nombre_Completo, Correo_Electronico, Telefono, Contrasena_Hash, Rol)
                VALUES (?, ?, ?, HASHBYTES('SHA2_256', ?), 'Usuario')
            """, (nombre_completo, email, telefono, password))
            conn.commit()
            
            # Obtener el usuario recién creado
            cursor.execute("SELECT Id_Usuario, Nombre_Completo, Correo_Electronico, Rol FROM Usuario WHERE Correo_Electronico = ?", (email,))
            usuario_data = cursor.fetchone()
            
            return {
                'id': usuario_data[0],
                'nombre': usuario_data[1],
                'email': usuario_data[2],
                'rol': usuario_data[3]
            }
            
        except Exception as e:
            print(f"Error registrando usuario: {e}")
            return {'error': 'Error en el registro'}
        finally:
            conn.close()