from fastapi import FastAPI

from src.modules.api import auth_router, machine_types_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(machine_types_router)