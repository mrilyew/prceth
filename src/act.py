from app.App import app
from utils.MainUtils import dump_json
from repositories.ActsRepository import ActsRepository

async def ___runAct():
    assert "i" in app.argv, "pass the name of act as --i"
    __is_print = 'silent' not in app.argv

    __act_name_input = app.argv.get("i")
    act_class = ActsRepository().getByName(plugin_name=__act_name_input)

    assert act_class != None, "act not found"

    act = act_class()

    act_response = await act.safeExecute(app.argv)

    if __is_print:
        print(dump_json(act_response, indent=4))

app.loop.run_until_complete(___runAct())
