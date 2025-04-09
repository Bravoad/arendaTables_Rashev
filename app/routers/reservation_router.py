from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.reservation import ReservationCreate, ReservationRead
from app.services.reservation_service import (
    get_all_reservations,
    create_reservation,
    delete_reservation,
    get_reservation_by_id,
)
from app.db.session import get_session

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)


@router.get("/", response_model=List[ReservationRead])
def read_reservations(db: Session = Depends(get_session)):
    """
    Возвращает список всех броней.
    """
    return get_all_reservations(db)


@router.post("/", response_model=ReservationRead, status_code=status.HTTP_201_CREATED)
def add_reservation(reservation: ReservationCreate, db: Session = Depends(get_session)):
    """
    Создает новую бронь.
    Если временной интервал пересекается с уже существующей бронью для данного столика,
    возвращается ошибка 409 Conflict.
    """
    try:
        new_reservation = create_reservation(db, reservation)
        return new_reservation
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_reservation(reservation_id: int, db: Session = Depends(get_session)):
    """
    Удаляет бронь по идентификатору.
    Если бронь не найдена, возвращается ошибка 404 Not Found.
    """
    reservation = get_reservation_by_id(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    delete_reservation(db, reservation_id)
    return
