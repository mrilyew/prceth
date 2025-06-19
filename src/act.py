from app.Views.CLI import cli
from app.App import app

app.loop.run_until_complete(cli.act())
