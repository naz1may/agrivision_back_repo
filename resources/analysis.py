import os
import uuid
from flask import request, current_app
from flask_restful import Resource, abort
from werkzeug.utils import secure_filename
from models import db, Analysis, AnalysisImage, AnalysisResult
from translations import MESSAGES
from flask_jwt_extended import jwt_required, get_jwt_identity
from predictor import PlantPredictor

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class AnalysisUpload(Resource):
    @jwt_required()
    def post(self, user_id):
        current_user_id = get_jwt_identity()
        if str(current_user_id) != str(user_id):
            abort(403, message="Доступ запрещен: нельзя проводить анализ для другого аккаунта")

        lang = request.headers.get('Accept-Language', 'ru')
        if lang not in ['ru', 'en']: lang = 'ru'

        if 'file' not in request.files:
            abort(400, message="Файл не найден")

        file = request.files['file']
        if file.filename == '':
            abort(400, message="Файл не выбран")

        if not allowed_file(file.filename):
            abort(400, message="Разрешены только png, jpg, jpeg")

        # 1. Сохранение файла
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        relative_path = os.path.join('static/uploads', filename).replace("\\", "/")
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(full_path)

        # 2. Логика БД и ИИ с защитой от сбоев
        try:
            # Предварительное создание записи анализа
            new_analysis = Analysis(user_id=user_id, status='completed')
            db.session.add(new_analysis)
            db.session.flush()

            new_image = AnalysisImage(analysis_id=new_analysis.id, image_url=relative_path)
            db.session.add(new_image)

            # --- ВНЕДРЕННЫЙ БЛОК ИИ ---
            # Вызываем предсказание (теперь через обертку predictor.py)
            prediction = PlantPredictor.predict(full_path)

            # Безопасно извлекаем данные с дефолтными значениями
            ai_label = prediction.get("label", "unknown")
            ai_confidence = float(prediction.get("confidence", 0.0))
            visual_status = prediction.get("visual_status", "healthy")

            # Подтягиваем перевод из словаря MESSAGES
            # Если ИИ выдал метку, которой нет в словаре, берем "unknown"
            translation_data = MESSAGES.get(ai_label, MESSAGES.get("unknown"))
            translation = translation_data[lang]
            # --------------------------

            new_result = AnalysisResult(
                analysis_id=new_analysis.id,
                visual_status=visual_status,
                label=ai_label,
                confidence=ai_confidence,
                symptom_description=translation.get("symptom", ""),
                recommendation=translation.get("rec", "")
            )
            db.session.add(new_result)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            if os.path.exists(full_path):
                os.remove(full_path)
            current_app.logger.error(f"Analysis Integration Error: {e}")
            abort(500, message=f"Техническая ошибка при анализе: {str(e)}")

        # 3. Формирование ответа
        base_url = request.host_url.rstrip('/')
        full_image_url = f"{base_url}/{relative_path}"

        return {
            "message": "Analysis completed" if lang == 'en' else "Анализ успешно завершен",
            "analysis_id": new_analysis.id,
            "visual_status": visual_status,
            "label": ai_label,
            "confidence": f"{ai_confidence * 100:.2f}%",
            "status_text": translation.get("status", ""),
            "diagnosis_text": translation.get("diagnosis", ""),
            "symptom_description": translation.get("symptom", ""),
            "recommendation": translation.get("rec", ""),
            "image_url": full_image_url,
            "created_at": new_analysis.created_at.strftime("%Y-%m-%d %H:%M")
        }, 201