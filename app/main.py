from fastapi import FastAPI

from app.routers import auth, entries, snippets

import app.models as models
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='Dev Log', version='1.0.0')

app.include_router(auth.router)
app.include_router(entries.router)
app.include_router(snippets.router)
