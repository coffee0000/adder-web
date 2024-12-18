
from fastapi import APIRouter, HTTPException, Request
from logging import getLogger

from fastapi.responses import JSONResponse
import backend.utils

logger = getLogger(__name__)
router = APIRouter()

@router.get("/hello")
async def hello(request: Request):
    userinfo = request.state.current_user
    return {"message": f"Hello GET, {userinfo.get('preferred_username', 'unknown')}"}


@router.get("/userinfo")
async def hello(request: Request):
    userinfo = request.state.current_user
    return userinfo


@router.post("/hello")
async def hello(request: Request):
    userinfo = request.state.current_user
    return {"message": f"Hello POST, {userinfo.get('preferred_username', 'unknown')}"}


@router.post("/calculate")
async def calculate(request: Request):
    try:
        data = await request.json()
        num1 = data.get("num1")
        num2 = data.get("num2")

        if num1 is None or num2 is None:
            raise HTTPException(status_code=400, detail="Both 'num1' and 'num2' are required.")

        if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
            raise HTTPException(status_code=400, detail="'num1' and 'num2' must be numbers.")

        result = num1 + num2

        return JSONResponse(content={"result": result}, status_code=200)

    except Exception as e:
        return JSONResponse(
            content={"error": f"An error occurred: {str(e)}"},
            status_code=500,
        )