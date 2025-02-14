from fastapi import APIRouter, HTTPException, Path, Body, Depends
from fastapi.responses import JSONResponse, StreamingResponse

router = APIRouter()

@router.get("/", response_model=dict)
async def root():
    return {"message": "Hello World"}