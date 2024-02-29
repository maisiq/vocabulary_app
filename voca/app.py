import yaml
from pathlib import Path

from fastapi import FastAPI

app = FastAPI()

# replace auto-schema
raw_openapi_schema = yaml.safe_load((Path(__file__).parent.parent / 'oaschema.yaml').read_text())
app.openapi = lambda: raw_openapi_schema

