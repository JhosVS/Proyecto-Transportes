from flask import Flask
from config import Config
from routes import init_routes

def create_app():
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar rutas
    init_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("=" * 50)
    print("🚀 Servidor PascoTransport iniciado")
    print("📍 Disponible en: http://localhost:5000")
    print("🔗 Windows Authentication activada")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)