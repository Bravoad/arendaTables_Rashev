from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Создаем engine для подключения к базе данных
engine = create_engine(
    settings.database_url,
    echo=settings.DEBUG,  # Если DEBUG=True, выводим SQL-запросы в лог
    pool_pre_ping=True  # Проверка подключения перед использованием
)

# Фабрика сессий для создания объектов сессий БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для декларативных моделей
Base = declarative_base()


def get_session():
    """
    Функция-зависимость для FastAPI, предоставляющая сессию SQLAlchemy.
    Использование в маршрутах:

        from fastapi import Depends
        from app.db.session import get_session

        @app.get("/endpoint")
        def endpoint(db: Session = Depends(get_session)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
