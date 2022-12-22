# Fastapi

from fastapi import FastAPI

# Modules 

from .routes import users


app = FastAPI()


app.include_router(users.router)