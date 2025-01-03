from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers

from app.modassembly.authentication.endpoints.login_api import router
app.include_router(router)
from app.modassembly.authentication.endpoints.login_api import router
app.include_router(router)
from app.inventory.endpoints.add_item import router
app.include_router(router)
from app.inventory.endpoints.place_order import router
app.include_router(router)

# Database

from app.modassembly.database.get_session import Base, engine
Base.metadata.create_all(engine)
