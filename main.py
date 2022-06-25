from fastapi import FastAPI

import tags
import items
import users
from db import SessionLocal, engine, Base
from meta import MUMU_GLOBAL_META
from mumu_exceptions import register_exception_handlers

Base.metadata.create_all(bind=engine)

app = FastAPI(**MUMU_GLOBAL_META)
app.include_router(tags.router)
app.include_router(items.router)
app.include_router(users.router)

register_exception_handlers(app)
