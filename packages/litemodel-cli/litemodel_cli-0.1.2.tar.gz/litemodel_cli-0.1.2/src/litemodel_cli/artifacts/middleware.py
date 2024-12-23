from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette_login.login_manager import LoginManager
from starlette_login.middleware import AuthenticationMiddleware
from starlette_login.backends import SessionAuthBackend
from litemodel_starlette.utils import get_by_admin_user_id
from app import settings

login_manager = LoginManager(redirect_to='login', secret_key='secret')


login_manager.set_user_loader(get_by_admin_user_id)


if settings.DEBUG:
    middleware = [
        Middleware(SessionMiddleware, secret_key="soemthing!realy!@secret"),
        Middleware(GZipMiddleware),
        Middleware(
            AuthenticationMiddleware,
            backend=SessionAuthBackend(login_manager),
            login_manager=login_manager,
            allow_websocket=False,
        ),
        Middleware(CORSMiddleware, allow_origins=["*"]),
    ]
else:
    middleware = [
        Middleware(HTTPSRedirectMiddleware),
        Middleware(SessionMiddleware, secret_key="soemthing!realy!@secret"),
        Middleware(GZipMiddleware),
        Middleware(
            AuthenticationMiddleware,
            backend=SessionAuthBackend(login_manager),
            login_manager=login_manager,
            allow_websocket=False,
        ),
        Middleware(CORSMiddleware, allow_origins=["*"]),
    ]
