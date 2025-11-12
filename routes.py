from flask import render_template, request, jsonify, session, redirect, url_for
from models import Viaje, Encomienda, Agencia, Usuario

def init_routes(app):
    
    @app.route('/')
    def index():
        """Página principal"""
        ciudades = Viaje.obtener_ciudades()
        return render_template('index.html', ciudades=ciudades, usuario=session.get('usuario'))
    
    @app.route('/buscar-viajes', methods=['POST'])
    def buscar_viajes():
        """Buscar viajes disponibles"""
        ciudad_origen = request.form.get('ciudad_origen')
        ciudad_destino = request.form.get('ciudad_destino')
        fecha = request.form.get('fecha')
        
        viajes = Viaje.buscar_viajes(ciudad_origen, ciudad_destino, fecha)
        ciudades = Viaje.obtener_ciudades()
        
        return render_template('resultados.html', 
                             viajes=viajes, 
                             ciudades=ciudades,
                             ciudad_origen=ciudad_origen,
                             ciudad_destino=ciudad_destino,
                             fecha=fecha,
                             usuario=session.get('usuario'))
    
    # ========== RUTAS DE LOGIN ==========
    @app.route('/login')
    def login_page():
        """Página de login"""
        return render_template('login.html', usuario=session.get('usuario'))
    
    @app.route('/api/login', methods=['POST'])
    def api_login():
        """API para login"""
        data = request.get_json()
        email_dni = data.get('email_dni')
        password = data.get('password')
        rol = data.get('rol', 'Usuario')
        
        usuario = Usuario.login(email_dni, password, rol)
        if usuario:
            session['usuario'] = usuario
            return jsonify({
                'success': True,
                'usuario': usuario,
                'message': 'Login exitoso'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Credenciales incorrectas'
            }), 401
    
    @app.route('/api/registrar', methods=['POST'])
    def api_registrar():
        """API para registrar usuario"""
        data = request.get_json()
        nombre_completo = data.get('nombre_completo')
        email = data.get('email')
        telefono = data.get('telefono')
        password = data.get('password')
        
        # Verificar si el correo ya existe
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT Id_Usuario FROM Usuario WHERE Correo_Electronico = ?", (email,))
                if cursor.fetchone():
                    return jsonify({
                        'success': False,
                        'error': 'El correo ya está registrado'
                    }), 400
            except Exception as e:
                print(f"Error verificando correo: {e}")
            finally:
                conn.close()
        
        # Registrar nuevo usuario
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Usuario (Nombre_Completo, Correo_Electronico, Telefono, Contrasena_Hash, Rol)
                    VALUES (?, ?, ?, HASHBYTES('SHA2_256', ?), 'Usuario')
                """, (nombre_completo, email, telefono, password))
                conn.commit()
                
                # Obtener el usuario recién creado
                cursor.execute("SELECT Id_Usuario, Nombre_Completo, Correo_Electronico, Rol FROM Usuario WHERE Id_Usuario = SCOPE_IDENTITY()")
                usuario_data = cursor.fetchone()
                
                usuario = {
                    'id': usuario_data[0],
                    'nombre': usuario_data[1],
                    'email': usuario_data[2],
                    'rol': usuario_data[3]
                }
                
                session['usuario'] = usuario
                return jsonify({
                    'success': True,
                    'usuario': usuario,
                    'message': 'Registro exitoso'
                })
                
            except Exception as e:
                print(f"Error registrando usuario: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Error en el registro'
                }), 500
            finally:
                conn.close()
        
        return jsonify({
            'success': False,
            'error': 'Error de conexión'
        }), 500
    
    @app.route('/logout')
    def logout():
        """Cerrar sesión"""
        session.pop('usuario', None)
        return redirect(url_for('index'))
    
    # ========== APIs EXISTENTES ==========
    @app.route('/api/viajes', methods=['GET'])
    def api_viajes():
        """API para buscar viajes"""
        ciudad_origen = request.args.get('origen')
        ciudad_destino = request.args.get('destino')
        fecha = request.args.get('fecha')
        
        if not all([ciudad_origen, ciudad_destino, fecha]):
            return jsonify({'error': 'Faltan parámetros'}), 400
        
        viajes = Viaje.buscar_viajes(ciudad_origen, ciudad_destino, fecha)
        return jsonify({'viajes': viajes})
    
    @app.route('/api/rastrear', methods=['POST'])
    def api_rastrear():
        """API para rastrear encomiendas"""
        data = request.get_json()
        serie = data.get('serie')
        correlativo = data.get('correlativo')
        clave_secreta = data.get('clave_secreta')
        
        if not all([serie, correlativo, clave_secreta]):
            return jsonify({'error': 'Faltan datos de rastreo'}), 400
        
        resultado = Encomienda.rastrear_encomienda(serie, correlativo, clave_secreta)
        
        if resultado:
            return jsonify({
                'success': True,
                'encomienda': resultado
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la encomienda'
            }), 404
    
    @app.route('/api/ranking', methods=['GET'])
    def api_ranking():
        """API para obtener ranking de agencias"""
        agencias = Agencia.obtener_ranking()
        return jsonify({'agencias': agencias})