from flask import current_app
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import db, User, LibraryItem, UserSavedItem
from flask_jwt_extended import jwt_required, get_jwt_identity

# 1. Описание полей для ответов API
library_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'content': fields.String,
    'created_at': fields.String
}

library_parser = reqparse.RequestParser()
library_parser.add_argument('title', type=str, required=True, help="Заголовок обязателен")
library_parser.add_argument('description', type=str)
library_parser.add_argument('content', type=str, required=True, help="Контент обязателен")


class LibraryList(Resource):
    @marshal_with(library_fields)
    def get(self):
        """Получить все статьи (доступно всем без токена)"""
        return LibraryItem.query.all()

    @jwt_required()
    @marshal_with(library_fields)
    def post(self):
        """Создать статью (только для админов)"""
        current_user_id = get_jwt_identity()
        admin = User.query.get_or_404(current_user_id)

        if admin.role != 'admin':
            abort(403, message="Доступ запрещен: только админы могут добавлять статьи")

        args = library_parser.parse_args()
        new_item = LibraryItem(
            title=args['title'],
            description=args['description'],
            content=args['content']
        )
        db.session.add(new_item)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Library Post Error: {e}")
            abort(500, message="Не удалось сохранить статью в библиотеку")

        return new_item, 201


class LibraryDetail(Resource):
    @marshal_with(library_fields)
    def get(self, item_id):
        """Просмотр одной конкретной статьи (доступно всем)"""
        return LibraryItem.query.get_or_404(item_id)


class SaveToFavorites(Resource):
    @jwt_required()
    def post(self, user_id, item_id):
        """Добавить статью в избранное"""
        current_user_id = get_jwt_identity()
        if str(current_user_id) != str(user_id):
            abort(403, message="Нельзя изменять чужое избранное")

        existing = UserSavedItem.query.filter_by(user_id=user_id, library_item_id=item_id).first()
        if existing:
            return {"message": "Уже в избранном"}, 400

        saved_item = UserSavedItem(user_id=user_id, library_item_id=item_id)
        db.session.add(saved_item)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Save to Favorites Error: {e}")
            abort(500, message="Ошибка при сохранении в избранное")

        return {"message": "Статья сохранена в профиль"}, 201

    @jwt_required()
    def delete(self, user_id, item_id):
        """Удалить из избранного"""
        current_user_id = get_jwt_identity()
        if str(current_user_id) != str(user_id):
            abort(403, message="Нельзя изменять чужое избранное")

        item = UserSavedItem.query.filter_by(user_id=user_id, library_item_id=item_id).first_or_404()
        db.session.delete(item)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Delete from Favorites Error: {e}")
            abort(500, message="Ошибка при удалении из избранного")

        return {"message": "Статья удалена из избранного"}, 200


class UserFavorites(Resource):
    @jwt_required()
    @marshal_with(library_fields)
    def get(self, user_id):
        """Список всех избранных статей пользователя"""
        current_user_id = get_jwt_identity()
        if str(current_user_id) != str(user_id):
            abort(403, message="Доступ запрещен к чужому избранному")

        user_saved = UserSavedItem.query.filter_by(user_id=user_id).all()
        return [saved.library_item for saved in user_saved]