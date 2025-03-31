from flask import Flask, request, jsonify, render_template, json
from resources.Globals import config, consts, ActsRepository, os, Path
from core.Api import api
from resources.Exceptions import NotPassedException, AccessDeniedException

consts["context"] = "flask"
CURRENT_FRONTEND = config.get("flask.frontend")

app = Flask(__name__, template_folder=f'web/{CURRENT_FRONTEND}', static_folder=f'web/{CURRENT_FRONTEND}/static')
app.json.ensure_ascii = False

@app.route("/", methods=["GET"])
def main_page():
    SITE_NAME = config.get("ui.name")
    CSS_FILES = []
    JS_FILES  = []

    for css_file in Path(os.path.join(consts.get("cwd"), "web", CURRENT_FRONTEND, "static", "css")).rglob('*.css'):
        CSS_FILES.append(str(css_file.name))

    for js_file in Path(os.path.join(consts.get("cwd"), "web", CURRENT_FRONTEND, "static", "js")).rglob('*.js'):
        relative_path = js_file.relative_to(os.path.join(consts.get("cwd"), "web", CURRENT_FRONTEND, "static", "js"))
        ouput_relative = str(relative_path)
        if "node_modules" in ouput_relative: #БЫДЛОКОДИНГ
            continue
        
        JS_FILES.append(ouput_relative)
    
    return render_template("index.html", site_name=SITE_NAME,__css=CSS_FILES,__js=JS_FILES)

if config.get("flask.debug") == 0:
    @app.errorhandler(Exception)
    def handle_exception(error):
        json_obj = {
            "error": {
                "exception_name": type(error).__name__,
                "message": str(error),
            }
        }

        response = jsonify(json_obj)
        response.status_code = 400
        response.mimetype = "application/json"

        return response

@app.route("/api/config.get", methods=["GET", "POST"])
def config_get():
    option = request.args.get("key")
    if option == None:
        raise NotPassedException("key was not passed")
    
    output_value = api.getOption(option)
    data = {
        "payload": {
            "key": option,
            "value": output_value,
        }
    }

    return jsonify(data)

@app.route("/api/config.set", methods=["GET", "POST"])
def config_set():
    option = request.args.get("key")
    value = request.args.get("value")
    if option == None:
        raise NotPassedException("key was not passed")
    if value == None:
        raise NotPassedException("value was not passed")
    
    api.setOption(option, value)
    data = {
        "payload": {
            "key": option,
            "value": value,
        }
    }

    return jsonify(data)

@app.route("/api/config.reset", methods=["GET", "POST"])
def config_reset():
    sure = request.args.get("sure")
    if sure != "yes":
        raise NotPassedException("you're not sure")
    
    api.resetOptions()
    data = {
        "payload": {
            "success": True,
        }
    }

    return jsonify(data)

@app.route("/api/config.getAll", methods=["GET", "POST"])
def config_get_all():
    options = api.getAllOptions()
    if consts.get("config.hidden") == 1:
        raise AccessDeniedException("config is hidden")
    
    data = {
        "payload": {
            "values": {},
        }
    }
    for option in options:
        data["payload"]["values"][option] = options[option]

    return jsonify(data)

@app.route("/api/collections.create", methods=["GET", "POST"])
def collections_new():
    new_collection = api.createCollection(params=request.args)

    data = {
        "payload": {
            "collection": new_collection.getApiStructure(),
        }
    }

    return jsonify(data)

@app.route("/api/collections.edit", methods=["GET", "POST"])
def collections_edit():
    collection = api.editCollection(params=request.args)

    data = {
        "payload": {
            "collection": collection.getApiStructure(),
        }
    }

    return jsonify(data)

@app.route("/api/collections.delete", methods=["GET", "POST", "DELETE"])
def collections_delete():
    res = api.deleteCollection(params=request.args)

    data = {
        "payload": {
            "success": res,
        }
    }

    return jsonify(data)

@app.route("/api/collections.switch", methods=["GET", "POST", "PUT"])
def collections_switch():
    api.switchCollections(params=request.args)

    data = {
        "payload": {
            "success": True,
        }
    }

    return jsonify(data)

@app.route("/api/collections.append", methods=["GET", "POST", "PUT"])
def collections_appendItem():
    api.addItemToCollection(params=request.args)

    data = {
        "payload": {
            "success": True,
        }
    }

    return jsonify(data)

@app.route("/api/collections.remove", methods=["GET", "POST", "PUT"])
def collections_removeItem():
    api.removeItemFromCollection(params=request.args)

    data = {
        "payload": {
            "success": True,
        }
    }

    return jsonify(data)

@app.route("/api/collections.get", methods=["GET"])
def collections_get():
    items, count = api.getAllCollections(request.args)

    data = {
        "payload": {
            "count": count,
            "items": [],
        }
    }

    for item in items:
        data["payload"]["items"].append(item.getApiStructure())

    return jsonify(data)

@app.route("/api/collections.getById", methods=["GET"])
def collections_getById():
    entities = api.getCollectionById(request.args)

    data = {
        "payload": {
            "items": [],
        }
    }

    for item in entities:
        data["payload"]["items"].append(item.getApiStructure())

    return jsonify(data)

@app.route("/api/entities.remove", methods=["GET", "POST", "PUT", "DELETE"])
def entities_remove():
    act = api.removeEntity(request.args)

    data = {
        "payload": {
            "success": True,
        }
    }

    return jsonify(data)

@app.route("/api/entities.edit", methods=["GET", "POST", "PUT", "DELETE"])
def entities_edit():
    __entity = api.editEntity(request.args)

    data = {
        "payload": {
            "entity": __entity.getApiStructure(),
        }
    }
    
    return jsonify(data)

@app.route("/api/entities.new", methods=["GET", "POST", "PUT", "DELETE"])
async def entities_upload():
    act = await api.uploadEntity(request.args)
    data = {}
    if type(act) == str:
        data = {
            "payload": {
                "export_dir": act,
            }
        }
    else:
        data = {
            "payload": {
                "entities": [],
            }
        }
        for _ent in act:
            data["payload"]["entities"].append(_ent.getApiStructure())
    
    return jsonify(data)

@app.route("/api/entities.getById", methods=["GET"])
async def entities_getById():
    entities = api.getEntityById(request.args)
    data = {
        "payload": {
            "entities": [],
        }
    }
    for entity in entities:
        data["payload"]["entities"].append(entity.getApiStructure())

    return jsonify(data)

@app.route("/api/entities.get", methods=["GET"])
async def entities_get():
    items, count = api.getGlobalEntities(request.args)
    data = {
        "payload": {
            "count": count,
            "items": [],
        }
    }
    
    for item in items:
        data["payload"]["items"].append(item.getApiStructure())

    return jsonify(data)

@app.route("/api/extractors.get", methods=["GET"])
async def extractors_get():
    items = api.getExtractors(request.args)
    data = {
        "payload": {
            "items": [],
        }
    }
    
    for item in items:
        data["payload"]["items"].append(item.describe())

    return jsonify(data)

@app.route("/api/acts.get", methods=["GET"])
async def acts_get():
    __show_hidden = request.args.get("show_hidden", None) != None
    __search_type = request.args.get("search_type", "all")
    acts = ActsRepository().getList(search_type=__search_type,show_hidden=__show_hidden)

    data = {
        "payload": {
            "items": [],
        }
    }
    
    for item in acts:
        data["payload"]["items"].append(item.describe())

    return jsonify(data)

@app.route("/api/acts.run", methods=["GET"])
async def acts_run():
    acts = api.runAct(request.args)
    data = {
        "payload": acts
    }

    return jsonify(data)

@app.route("/api/services.get", methods=["GET"])
async def services_get():
    items = api.getServices(request.args)
    data = {
        "payload": {
            "items": []
        }
    }

    for item in items:
        data["payload"]["items"].append(item.describe())

    return jsonify(data)

@app.route("/api/services.run", methods=["GET"])
async def services_run():
    api.runService(request.args)

    return {
        "payload": {
            "success": True
        }
    }

if __name__ == '__main__':
    app.run(host=config.get("web.host"), port=config.get("web.port"),debug=config.get("flask.debug") == 1)
