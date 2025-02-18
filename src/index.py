import os
from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from .database.db import connect_to_mongo, close_mongo_connection
from .controller.enterprise_controller import router as enterprise_router
from .controller.login_controller import router as login_router
from .auth.auth import Auth
app = FastAPI()
auth = Auth()

load_dotenv()

origins = [
    os.getenv('CORS_ORIGINS')
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"], dependencies=[Depends(validate_token)])

app.include_router(enterprise_router, prefix='/api/v1/enterprise', tags=['enterprise'], dependencies=[Depends(auth.get_current_user)])
app.include_router(login_router, prefix='/api/v1/login', tags=['login'])