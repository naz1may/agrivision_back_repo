from app import app
from models import db, User

with app.app_context():
    # Находим пользователя с ID 1 (твоя первая регистрация)
    user = User.query.get(1)
    if user:
        user.role = 'admin'
        db.session.commit()
        print(f"Пользователь {user.name} теперь админ!")
    else:
        print("Пользователь не найден.")