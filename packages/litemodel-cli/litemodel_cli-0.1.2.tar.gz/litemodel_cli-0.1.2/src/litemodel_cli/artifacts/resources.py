from databases import Database
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from app import settings
from app.jinja_filters import my_filter

# This file is mainly used to avoid circular imports

# Database Resource
database = Database(settings.DATABASE_URL)

# Templates resource (add custom filters here)
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)
templates.env.filters["my_filter"] = my_filter

# Admin Templates resource (can also add filters here)
admin_templates = Jinja2Templates(directory=settings.ADMIN_TEMPLATES_DIR)

# Static files
static = StaticFiles(directory=settings.STATIC_DIR)
images = StaticFiles(directory=settings.IMAGE_DIR)
