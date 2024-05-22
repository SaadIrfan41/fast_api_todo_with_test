
from fastapi import FastAPI
from api.router.main import api_router 



app = FastAPI(
    
    docs_url="/api/v1/docs", openapi_url="/api/v1/openapi.json")

app.include_router(api_router, prefix="/api/v1")


