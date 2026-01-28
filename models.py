from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# 1. ПОЛЬЗОВАТЕЛЬ
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), default='user') # user / admin
    phone = db.Column(db.String(20), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Связи
    analyses = db.relationship('Analysis', backref='user', lazy=True)
    service_requests = db.relationship('ServiceRequest', backref='user', lazy=True)
    saved_items = db.relationship('UserSavedItem', backref='user', lazy=True)

# 2. АНАЛИЗ (Сессия)
class Analysis(db.Model):
    __tablename__ = 'analyses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='processing') # processing/completed/failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Связи
    images = db.relationship('AnalysisImage', backref='analysis', lazy=True)
    result = db.relationship('AnalysisResult', backref='analysis', uselist=False)
    reports = db.relationship('Report', backref='analysis', lazy=True)

# 3. ИЗОБРАЖЕНИЕ
class AnalysisImage(db.Model):
    __tablename__ = 'analysis_images'
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('analyses.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

# 4. РЕЗУЛЬТАТ ИИ
class AnalysisResult(db.Model):
    __tablename__ = 'analysis_results'
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('analyses.id'), nullable=False)

    # Данные от ИИ
    visual_status = db.Column(db.String(50))  # healthy / diseased
    label = db.Column(db.String(100))  # scab, rust, complex и т.д.
    confidence = db.Column(db.Float)  # 0.91
    symptom_description = db.Column(db.String(500))

    # Статичная рекомендация (подтягиваем на бэкенде)
    recommendation = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# 5. ОТЧЕТ
class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('analyses.id'), nullable=False)
    report_url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 6. ЗАЯВКА НА СЕРВИС
class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    plants_description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending') # pending/approved/rejected/in_progress/completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 7. БИБЛИОТЕКА (Статьи)
class LibraryItem(db.Model):
    __tablename__ = 'library_items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 8. ИЗБРАННОЕ
class UserSavedItem(db.Model):
    __tablename__ = 'user_saved_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    library_item_id = db.Column(db.Integer, db.ForeignKey('library_items.id'), nullable=False)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)