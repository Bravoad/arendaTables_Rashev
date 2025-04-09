from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.table import TableCreate, TableRead
from app.services.table_service import get_all_tables, create_table, delete_table, get_table_by_id
from app.db.session import get_session

router = APIRouter(
    prefix="/tables",
    tags=["Tables"]
)


@router.get("/", response_model=List[TableRead])
def read_tables(db: Session = Depends(get_session)):
    """
    Возвращает список всех столиков.
    """
    return get_all_tables(db)


@router.post("/", response_model=TableRead, status_code=status.HTTP_201_CREATED)
def add_table(table: TableCreate, db: Session = Depends(get_session)):
    """
    Создает новый столик. В случае, если столик с таким именем уже существует,
    возвращается ошибка 409 Conflict.
    """
    try:
        new_table = create_table(db, table)
        return new_table
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_table(table_id: int, db: Session = Depends(get_session)):
    """
    Удаляет столик по идентификатору.
    Если столик не найден, возвращается ошибка 404 Not Found.
    """
    table = get_table_by_id(db, table_id)
    if not table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
    delete_table(db, table_id)
    return
