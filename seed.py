from app import app
from models import db, LibraryItem

with app.app_context():
    # Проверим, нет ли уже такой статьи, чтобы не дублировать
    if not LibraryItem.query.filter_by(id=1).first():
        item1 = LibraryItem(
            title="Фитофтороз",
            description="Опасная болезнь томатов",
            content="Фитофтороз — это грибковое заболевание..."
        )
        db.session.add(item1)
        db.session.commit()
        print("Библиотека наполнена!")
    else:
        print("Статья с ID 1 уже существует.")