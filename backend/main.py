from fastapi import FastAPI
from core.config import settings
from db.session import engine
from scalar_fastapi import get_scalar_api_reference
from fastapi.staticfiles import StaticFiles

from apis.base import api_router
from apps.base import app_router

'''this is to create tables when i run the app, i have commented it out since am using alembic migrations'''
# from db.base import Base

# def create_tables():
#     Base.metadata.create_all(bind=engine)

def include_router(app):
    app.include_router(api_router)
    app.include_router(app_router)

def configure_staticfiles(app):
    app.mount("/static",StaticFiles(directory="static"), name="static")

def start_application():
    app = FastAPI(
        title=settings.PROJECT_TITLE, 
        version=settings.PROJECT_VERSION
    )
    include_router(app)
    configure_staticfiles(app)
    # create_tables()
    return app

app = start_application()


#Scalar api Documentation    
@app.get("/scalar",include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )