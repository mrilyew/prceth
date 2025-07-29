from app.Views.Web import make_app
from tornado.ioloop import IOLoop
from app.App import config, logger
from datetime import datetime
import tornado
import asyncio

app = make_app()
app.listen(port=config.get("web.port"),address=config.get("web.host"))

logger.log(message=f"Started tornado server", kind=logger.KIND_MESSAGE, section=logger.SECTION_WEB)

IOLoop.current().start()
