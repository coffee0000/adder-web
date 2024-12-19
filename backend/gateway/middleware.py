import httpx
from logging import getLogger
from starlette.types import ASGIApp
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import APIRouter, Request
from starlette.middleware.base import BaseHTTPMiddleware
from backend.gateway.auth_router import introspect_token, OAUTH2_URL_USERINFO

logger = getLogger(__name__)
router = APIRouter()

class HttpMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: ASGIApp):
        if request.url.path not in ["/oauth2/login", "/oauth2/callback", "/oauth2/logout"]:
                access_token = request.cookies.get("access_token") or request.headers.get("access_token")
                user_agent = request.headers.get('User-Agent', '')
                if not access_token :
                    next_url = request.url.path
                    return RedirectResponse(url=f"/oauth2/login?next={next_url}")
                else:
                    # トークンの有効性の検証
                    introspect_resp = introspect_token(access_token)
                    introspect_json = introspect_resp.json()
                    if not introspect_json["active"]:
                        logger.error(introspect_resp.json())
                        # curlコマンドでAPIにアクセスすると、トークンが無効であるというエラーメッセージが直接返されます。
                        if 'curl' in user_agent:
                            return JSONResponse(status_code=401, content={"error": "Token is invalid"})
                        # ウェブページのリクエスト時に、トークンが無効な場合は、直接ログイン画面にリダイレクトされ、再ログインが求められます。
                        next_url = request.url.path
                        return RedirectResponse(url=f"/oauth2/login?next={next_url}")
                    else:
                        logger.info(introspect_resp.json())
                        async with httpx.AsyncClient() as client:
                                userinfo_response = await client.get(
                                    OAUTH2_URL_USERINFO,
                                    headers={"Authorization": f"Bearer {access_token}"},
                                )
                                userinfo = userinfo_response.json()
                                request.state.current_user = userinfo
        response = await call_next(request)
        return response