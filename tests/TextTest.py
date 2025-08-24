import os, sys

correct_path = os.path.join(os.path.dirname(os.getcwd()), 'src')
os.chdir(correct_path)
sys.path.append(correct_path)

from app.Views.CLI import cli
from app.App import app

app.argv = {
    'i': 'Executables.RepresentationsExtract',
    'representation': 'Abstract.Text',
    'text': '123456',
}

app.loop.run_until_complete(cli.act())
