from flask import current_app
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import db, ServiceRequest
from flask_jwt_extended import jwt_required, get_jwt_identity

# 1. Поля ответа
service_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'phone': fields.String,
    'location': fields.String,
    'plants_description': fields.String,
    'status': fields.String,
    'created_at': fields.String,
}

# Парсеры без изменений
service_parser = reqparse.RequestParser()
service_parser.add_argument('phone', type=str, required=True, help="Номер телефона обязателен")
service_parser.add_argument('location', type=str, required=True, help="Локация обязательна")
service_parser.add_argument('plants_description', type=str)

status_parser = reqparse.RequestParser()
status_parser.add_argument('status', type=str, required=True,
                           choices=('pending', 'approved', 'rejected', 'in_progress', 'completed'),
                           help="Недопустимый статус")


class ServiceRequestResource(Resource):
    @jwt_required()
    @marshal_with(service_fields)
    def post(self, user_id):
        current_user_id = get_jwt_identity()
        if str(current_user_id) != str(user_id):
            abort(403, message="Запрещено создавать заявки для другого аккаунта")

        args = service_parser.parse_args()
        new_request = ServiceRequest(
            user_id=user_id,
            phone=args['phone'],
            location=args['location'],
            plants_description=args.get('plants_description'),
            status='pending'
        )

        db.session.add(new_request)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Service Request Create Error: {e}")
            abort(500, message="Не удалось сохранить заявку. Пожалуйста, попробуйте позже.")

        return new_request, 201

    @jwt_required()
    @marshal_with(service_fields)
    def patch(self, user_id, request_id):
        current_user_id = get_jwt_identity()
        if str(current_user_id) != str(user_id):
            abort(403, message="Нет прав для изменения этой заявки")

        args = status_parser.parse_args()
        request_obj = ServiceRequest.query.filter_by(id=request_id, user_id=user_id).first_or_404()

        request_obj.status = args['status']

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Service Request Update Error: {e}")
            abort(500, message="Ошибка при обновлении статуса заявки")

        return request_obj


class UserServiceList(Resource):
    @jwt_required()
    @marshal_with(service_fields)
    def get(self, user_id):
        current_user_id = get_jwt_identity()
        if str(current_user_id) != str(user_id):
            abort(403, message="Доступ запрещен к чужому списку услуг")

        requests = ServiceRequest.query.filter_by(user_id=user_id).all()
        return requests