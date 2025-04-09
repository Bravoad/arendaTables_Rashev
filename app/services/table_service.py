from sqlalchemy.orm import Session
from app.models.table import Table
from app.schemas.table import TableCreate


def get_all_tables(db: Session):
    """
    Возвращает список всех столиков.
    """
    return db.query(Table).all()


def get_table_by_id(db: Session, table_id: int):
    """
    Возвращает столик по его идентификатору.
    """
    return db.query(Table).filter(Table.id == table_id).first()


def create_table(db: Session, table_in: TableCreate):
    """
    Создаёт новый столик и сохраняет его в БД.
    Перед сохранением проверяет уникальность имени.
    """
    # Проверяем наличие столика с таким именем
    existing_table = db.query(Table).filter(Table.name == table_in.name).first()
    if existing_table:
        raise ValueError("Table with this name already exists")

    new_table = Table(**table_in.dict())
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return new_table


def delete_table(db: Session, table_id: int):
    """
    Удаляет столик по идентификатору.
    Если столик не найден, возвращается None.
    """
    table = get_table_by_id(db, table_id)
    if not table:
        return None

    db.delete(table)
    db.commit()
    return table
