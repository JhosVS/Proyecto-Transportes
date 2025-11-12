from flask import render_template, request, jsonify, session, redirect, url_for
from models import Viaje, Encomienda, Agencia, Usuario
from datetime import datetime, timedelta

def init_routes(app):
    
    @app.route('/')
    def index():
        """Página principal"""
        ciudades = Viaje.obtener_ciudades()
        
        # Configurar fecha por defecto (mañana)
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        return render_template('index.html', ciudades=ciudades, tomorrow=tomorrow)
    
    @app.route('/buscar-viajes', methods=['POST'])
    def buscar_viajes():
        """Buscar viajes disponibles"""
        ciudad_origen = request.form.get('ciudad_origen')
        ciudad_destino = request.form.get('ciudad_destino')
        fecha = request.form.get('fecha')
        
        # Buscar viajes en la base de datos
        viajes = Viaje.buscar_viajes(ciudad_origen, ciudad_destino, fecha)
        ciudades = Viaje.obtener_ciudades()
        
        return render_template('resultados.html', 
                             viajes=viajes, 
                             ciudades=ciudades,
                             ciudad_origen=ciudad_origen,
                             ciudad_destino=ciudad_destino,
                             fecha=fecha)
    
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
                'usuario': usuario
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Credenciales incorrectas'
            }), 401
    
    @app.route('/api/logout', methods=['POST'])
    def api_logout():
        """API para logout"""
        session.pop('usuario', None)
        return jsonify({'success': True})
    
    @app.route('/api/register', methods=['POST'])
    def api_register():
        """API para registro de usuarios"""
        data = request.get_json()
        
        nombre = data.get('nombre')
        email = data.get('email')
        telefono = data.get('telefono')
        password = data.get('password')
        
        if not all([nombre, email, password]):
            return jsonify({
                'success': False,
                'error': 'Faltan campos obligatorios'
            }), 400
        
        # Aquí puedes implementar el registro usando el SP_RegistrarUsuario
        # Por ahora retornamos éxito simulado
        return jsonify({
            'success': True,
            'message': 'Usuario registrado exitosamente'
        })
    
    @app.route('/perfil')
    def perfil():
        """Página de perfil de usuario"""
        if 'usuario' not in session:
            return redirect('/')
        
        return render_template('perfil.html', usuario=session['usuario'])
    
    @app.route('/mis-viajes')
    def mis_viajes():
        """Página de viajes del usuario"""
        if 'usuario' not in session:
            return redirect('/')
        
        # Aquí puedes agregar la lógica para obtener los viajes del usuario
        return render_template('mis_viajes.html', usuario=session['usuario'])
    
    # Ruta para servir el favicon (evita error 404)
    @app.route('/favicon.ico')
    def favicon():
        return '', 204
    
    # Manejo de errores
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500