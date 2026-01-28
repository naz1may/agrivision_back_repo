from dotenv import load_dotenv
import os
from flask import Flask, send_from_directory, jsonify
from flask_restful import Api
from flask_cors import CORS
from models import db
from flask_jwt_extended import JWTManager


# Импорт ресурсов
from resources.user import UserRegister, UserProfile, UserHistory, UserLogin
from resources.service import ServiceRequestResource, UserServiceList
from resources.library import LibraryList, LibraryDetail, SaveToFavorites, UserFavorites
from resources.analysis import AnalysisUpload

# 1. Загрузка переменных окружения
load_dotenv()

app = Flask(__name__)
CORS(app)

# 2. Конфигурация
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'fallback-secret-key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Настройка путей
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(BASE_DIR, 'agrivision.db'))

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 3. Инициализация расширений
db.init_app(app)
api = Api(app)
jwt = JWTManager(app)  # ВАЖНО: Инициализируем JWT здесь!

# 4. Настройка JSON-ответов при проблемах с JWT
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "Срок действия токена истек", "error": "token_expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"message": "Неверный токен", "error": "invalid_token"}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"message": "Для доступа нужен токен авторизации", "error": "authorization_required"}), 401

@app.route('/')
def index():
    return jsonify({
        "status": "AgriVision API is running",
        "version": "1.0.0",
        "endpoints": "/api/register, /api/login, /api/library"
    })

# 5. Маршруты статики
@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# 6. Регистрация эндпоинтов
api.add_resource(UserRegister, '/api/register')
api.add_resource(UserLogin, '/api/login')
api.add_resource(UserProfile, '/api/user/<int:user_id>')
api.add_resource(UserHistory, '/api/user/<int:user_id>/history')
api.add_resource(AnalysisUpload, '/api/user/<int:user_id>/analyze')
api.add_resource(ServiceRequestResource, '/api/user/<int:user_id>/service-request')
api.add_resource(UserServiceList, '/api/user/<int:user_id>/services')
api.add_resource(LibraryList, '/api/library')
api.add_resource(LibraryDetail, '/api/library/<int:item_id>')
api.add_resource(SaveToFavorites, '/api/user/<int:user_id>/save/<int:item_id>')
api.add_resource(UserFavorites, '/api/user/<int:user_id>/favorites')

# 7. Глобальные обработчики ошибок (JSON вместо HTML)
@app.errorhandler(404)
def handle_404(e):
    return jsonify({"message": "Ресурс не найден", "error": "not_found"}), 404

@app.errorhandler(500)
def handle_500(e):
    return jsonify({"message": "Внутренняя ошибка сервера", "error": "server_error"}), 500

# 8. Запуск приложения
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    is_debug = os.getenv('DEBUG', 'False').lower() == 'true'
    server_port = int(os.getenv('PORT', 5000))

    app.run(
        debug=is_debug,
        host='0.0.0.0',
        port=server_port
    )