from starlette.applications import Starlette
from server.routes import routes
from server.middleware import middleware, login_manager
from server.event_handlers import on_shutdown, on_startup


# manager your starlette application here

app = Starlette(routes=routes, middleware=middleware, on_startup=on_startup, on_shutdown=on_shutdown)
app.state.login_manager = login_manager