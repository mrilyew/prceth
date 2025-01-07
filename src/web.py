from flask import Flask, request, jsonify, render_template
from resources.globals import config, consts

app = Flask(__name__, template_folder='web', static_folder='web/static')

@app.route("/", methods=["GET"])
def main_page():
    return render_template("index.html", site_name=config.get("ui.name"), langs=["ru", "qqx"])

@app.route("/api/{method_name}", methods=["GET", "POST"])
def api_request(method_name):
    pass

if __name__ == '__main__':
    app.run(host=config.get("net.host"), port=config.get("net.port"),debug=config.get("flask.debug") == 1)
