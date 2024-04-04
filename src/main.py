from pathlib import Path
from contextlib import asynccontextmanager
import yaml
import os

from fastapi import FastAPI

from .config.db_config import Base
from .words.routes.words import router as words_router
from .words.routes.vocabulary import router as vocabulary_router
from .config.db_config import sessionmanager
# from .auth.router import router as login_router


def init_app(init_db=True):
     lifespan = None

     if init_db:
          sessionmanager.init(os.environ.get('MYSQLDB_URI', None))

          @asynccontextmanager
          async def lifespan(app: FastAPI):
               yield
               if sessionmanager._engine is not None:
                    await sessionmanager.close()

     app = FastAPI(title="FastAPI server", lifespan=lifespan)


     app.include_router(words_router)
     app.include_router(vocabulary_router)
     # app.include_router(login_router)

     return app


# replace auto-schema
# raw_openapi_schema = yaml.safe_load((Path(__file__).parent.parent / 'oaschema.yaml').read_text())
# app.openapi = lambda: raw_openapi_schema

