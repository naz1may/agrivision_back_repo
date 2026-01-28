from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from translations import MESSAGES
from flask import request, current_app  # Добавили current_app для логирования
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'role': fields.String,
    'phone': fields.String,
    'location': fields.String,
    'created_at': fields.String
}

# Парсеры без изменений
user_parser = reqparse.RequestParser()
user_parser.add_argument('name', type=str, required=True, help="Имя обязательно")
user_parser.add_argument('email', type=str, required=True, help="Email обязателен")
user_parser.add_argument('password', type=str, required=True, help="Пароль обязателен")
user_parser.add_argument('phone', type=str)
user_parser.add_argument('location', type=str)

update_parser = reqparse.RequestParser()
update_parser.add_argument('name', type=str)
update_parser.add_argument('phone', type=str)
update_parser.add_argument('location', type=str)

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True)
login_parser.add_argument('password', type=str, required=True)


class UserRegister(Resource):
    @marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()
        if User.query.filter_by(email=args['email']).first():
            abort(400, message="Пользователь с таким email уже существует")

        hashed_pw = generate_password_hash(args['password'], method='pbkdf2:sha256')
        new_user = User(name=args['name'], email=args['email'], password_hash=hashed_pw,
                        phone=args.get('phone'), location=args.get('location'))

        db.session.add(new_user)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Registration Error: {e}")
            abort(500, message="Ошибка при создании пользователя в базе данных")

        return new_user, 201


class UserLogin(Resource):
    def post(self):
        args = login_parser.parse_args()
        user = User.query.filter_by(email=args['email']).first()
        if user and check_password_hash(user.password_hash, args['password']):
            access_token = create_access_token(identity=str(user.id))
            return {
                "access_token": access_token,
                "user_id": user.id,
                "name": user.name,
                "role": user.role
            }, 200
        abort(401, message="Неверный email или пароль")


class UserProfile(Resource):
    @jwt_required()
    @marshal_with(user_fields)
    def get(self, user_id):
        current_user_id = get_jwt_identity()
        if str(current_user_id) != str(user_id):
            abort(403, message="Нет доступа к чужому профилю")
        return User.query.get_or_404(user_id)

    @jwt_required()
    @marshal_with(user_fields)
    def patch(self, user_id):
        current_user_id = get_jwt_identity()
        if str(current_user_id) != str(user_id):
            abort(403, message="Нельзя редактировать чужой профиль")

        args = update_parser.parse_args()
        user = User.query.get_or_404(user_id)

        if args['name']: user.name = args['name']
        if args['phone']: user.phone = args['phone']
        if args['location']: user.location = args['location']

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Profile Update Error: {e}")
            abort(500, message="Не удалось обновить данные профиля")

        return user


class UserHistory(Resource):
    @jwt_required()
    def get(self, user_id):
        current_user_id = get_jwt_identity()
        if str(current_user_id) != str(user_id):
            abort(403, message="Доступ запрещен: нельзя смотреть чужую историю")

        lang = request.headers.get('Accept-Language', 'ru')
        if lang not in ['ru', 'en']: lang = 'ru'

        user = User.query.get_or_404(user_id)
        base_url = request.host_url.rstrip('/')
        results = []

        sorted_analyses = sorted(user.analyses, key=lambda x: x.created_at, reverse=True)

        for analysis in sorted_analyses:
            res = analysis.result
            img = analysis.images[0] if analysis.images else None
            if res:
                translation = MESSAGES.get(res.label, MESSAGES.get("unknown", MESSAGES["healthy"]))[lang]
                results.append({
                    "id": analysis.id,
                    "date": analysis.created_at.strftime("%Y-%m-%d %H:%M"),
                    "status_text": translation["status"],
                    "diagnosis_text": translation["diagnosis"],
                    "confidence": f"{res.confidence * 100:.2f}%",
                    "image_url": f"{base_url}/{img.image_url}" if img else None,
                    "label": res.label,
                    "symptom_description": translation["symptom"],
                    "recommendation": translation["rec"]
                })
        return results, 200