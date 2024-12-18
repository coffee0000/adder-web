
import os
import httpx
import requests
from jose import JWTError
from logging import getLogger
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import APIRouter, HTTPException, Response, status, Request

logger = getLogger(__name__)
router = APIRouter()

# 環境変数
APP_BASE_URL = os.environ.get("SERVER_BASE_URL", "")
APP_REDIRECT_URL = f"{APP_BASE_URL}/oauth2/callback" 

KEYCLOAK_BASE_URL = os.environ.get("KEYCLOAK_BASE_URL", "")
KEYCLOAK_REALM_NAME = os.environ.get("KEYCLOAK_REALM_NAME", "") 
KEYCLOAK_CLIENT_ID = os.environ.get("KEYCLOAK_CLIENT_ID", "")
KEYCLOAK_CLIENT_SECRET = os.environ.get("KEYCLOAK_CLIENT_SECRET", "")

OAUTH2_URL_AUTH = f"{KEYCLOAK_BASE_URL}/realms/{KEYCLOAK_REALM_NAME}/protocol/openid-connect/auth"
OAUTH2_URL_TOKEN = f"{KEYCLOAK_BASE_URL}/realms/{KEYCLOAK_REALM_NAME}/protocol/openid-connect/token"
OAUTH2_URL_USERINFO = f"{KEYCLOAK_BASE_URL}/realms/{KEYCLOAK_REALM_NAME}/protocol/openid-connect/userinfo"
OAUTH2_URL_LOGOUT = f"{KEYCLOAK_BASE_URL}/realms/{KEYCLOAK_REALM_NAME}/protocol/openid-connect/logout"
OAUTH2_URL_INTROSPECTION = f"{KEYCLOAK_BASE_URL}/realms/{KEYCLOAK_REALM_NAME}/protocol/openid-connect/token/introspect"


@router.get("/login")
async def login(request: Request):
    state = request.query_params.get("next", "/")  
    login_url = OAUTH2_URL_AUTH
    params = {
        "response_type": "code",
        "client_id": KEYCLOAK_CLIENT_ID,
        "redirect_uri": APP_REDIRECT_URL,
        "scope": "openid",
        "state": state
    }
    redirect_url = f"{login_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    
    return RedirectResponse(url=redirect_url)


@router.get("/callback")
async def callback(code: str, request: Request):
    state = request.query_params.get("state", "/")  
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            OAUTH2_URL_TOKEN,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": APP_REDIRECT_URL,
                "client_id": KEYCLOAK_CLIENT_ID,
                "client_secret": KEYCLOAK_CLIENT_SECRET,
            },
        )
    
    try:
        token_response_json = token_response.json()
        
        if token_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token exchange failed.",
            )
        response = __create_homepage_response(token_response_json, homepage_url=state)
        return response
    except (IndexError, JWTError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Could not validate credentials", 
            headers={"WWW-Authenticate": "Bearer"}
        )


# ユーザーメッセージ取得
@router.get("/userinfo")
async def get_userinfo(request: Request):
    userinfo = request.state.current_user
    result = {"userinfo": userinfo}
    return JSONResponse(status_code = 200, content = result)
    

# ログアウト処理
@router.get("/logout")
async def logout(request: Request, response: Response):
    id_token = request.cookies.get("id_token") or request.headers.get("id_token")
    response.delete_cookie(key="access_token")
    request.state.current_user = None

    logout_url = f"{OAUTH2_URL_LOGOUT}?id_token_hint={id_token}&post_logout_redirect_uri={APP_BASE_URL}/oauth2/login"
    return RedirectResponse(url=logout_url)


 # コールバック
def __create_homepage_response(token_response_json, homepage_url):
    response = RedirectResponse(url=homepage_url, status_code=302)
    response.set_cookie(key="access_token", value=token_response_json["access_token"])
    response.set_cookie(key="id_token", value=token_response_json["id_token"])
    return response


 # トークンの有効性の検証
def introspect_token(token: str):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'token': token,
        'client_id': KEYCLOAK_CLIENT_ID,
        'client_secret': KEYCLOAK_CLIENT_SECRET
    }
    try:
        response = requests.post(OAUTH2_URL_INTROSPECTION, data=data, headers=headers)

        if response.status_code == 200:
            return response
        else:
            logger.error(f"Error: {response.status_code}")
            logger.error(response.text)
            return response
    except requests.RequestException as e:
        logger.exception("トークンの有効性の検証に失敗しました。")
