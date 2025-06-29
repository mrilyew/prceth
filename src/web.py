from app.Views.Web import fl_app
from app.App import config

if __name__ == '__main__':
    fl_app.run(host=config.get("web.host"), port=config.get("web.port"),debug=config.get("web.debug") == True)
