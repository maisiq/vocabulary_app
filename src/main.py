from pathlib import Path
from contextlib import asynccontextmanager
import yaml

from fastapi import FastAPI


from .config.db_config import Base, engine
from .words.routes.words import router as words_router
from .words.routes.vocabulary import router as vocabulary_router
# from .auth.router import router as login_router


@asynccontextmanager
async def lifespan(app: FastAPI):
     yield


app = FastAPI()
app.include_router(words_router)
app.include_router(vocabulary_router)
# app.include_router(login_router)

# replace auto-schema
# raw_openapi_schema = yaml.safe_load((Path(__file__).parent.parent / 'oaschema.yaml').read_text())
# app.openapi = lambda: raw_openapi_schema

