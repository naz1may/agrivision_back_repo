import random
from translations import MESSAGES


class PlantPredictor:
    @staticmethod
    def predict(image_path):
        """
        Имитация работы нейросети.
        В будущем здесь будет загрузка модели (TensorFlow/PyTorch)
        и классификация изображения по пути image_path.
        """
        # Список возможных диагнозов из твоих MESSAGES
        possible_labels = [
            "healthy", "scab", "scab frog_eye_leaf_spot",
            "scab frog_eye_leaf_spot complex", "rust",
            "rust frog_eye_leaf_spot", "rust complex",
            "frog_eye_leaf_spot", "frog_eye_leaf_spot complex",
            "powdery_mildew", "powdery_mildew complex", "complex"
        ]

        # Имитируем случайный выбор диагноза и уверенность ИИ
        label = random.choice(possible_labels)
        confidence = round(random.uniform(0.85, 0.99), 4)

        # Определяем технический статус
        visual_status = "healthy" if label == "healthy" else "diseased"

        return {
            "label": label,
            "confidence": confidence,
            "visual_status": visual_status
        }