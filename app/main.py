from fastapi import FastAPI
from app.routers import table_router, reservation_router
from app.config import settings

app = FastAPI()
print("Settings:")
print(f"POSTGRES_PORT={settings.POSTGRES_PORT}")
print(f"APP_PORT={settings.APP_PORT}")
print(f"DEBUG={settings.DEBUG}")
app.include_router(table_router.router)
app.include_router(reservation_router.router)
