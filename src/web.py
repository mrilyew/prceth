from app.App import config, logger
from app.App import app as current_app
from app.Views.Web import app
from datetime import datetime
import aiohttp

current_app.cache_lists()

aiohttp.web.run_app(app,
    host=config.get("web.host"),
    port=config.get("web.port"),
)
