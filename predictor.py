import os
import shutil
from predict import analyze


class PlantPredictor:
    @staticmethod
    def predict(image_path):
        # 1. Создаем временную папку для ИИ, если её нет
        temp_ai_dir = 'temp_ai_analysis'
        if os.path.exists(temp_ai_dir):
            shutil.rmtree(temp_ai_dir)  # Очищаем старое
        os.makedirs(temp_ai_dir)

        # 2. Копируем туда наше загруженное фото
        filename = os.path.basename(image_path)
        temp_image_path = os.path.join(temp_ai_dir, filename)
        shutil.copy(image_path, temp_image_path)

        try:
            # 3. Передаем ПАПКУ функции коллеги
            results = analyze(temp_ai_dir)

            if not results:
                return {"label": "unknown", "confidence": 0.0, "visual_status": "error"}

            return results[0]
        finally:
            # 4. Удаляем временную папку после анализа
            if os.path.exists(temp_ai_dir):
                shutil.rmtree(temp_ai_dir)