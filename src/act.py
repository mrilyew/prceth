from resources.Globals import utils, loop, ActsRepository, utils
from resources.DbPrefetch import prefetch__db

prefetch__db()

args = utils.parse_args()

async def runAct():
    assert "i" in args, "pass the name of act as --i"

    __act_name = args.get("i")
    __act_res = ActsRepository().getByName(act_name=__act_name)

    assert __act_res != None, "act not found"

    out_act = __act_res()
    out_act.setArgs(args)

    ACT_F = await out_act.execute(args=args)

    print(utils.dump_json(ACT_F, indent=4))

loop.run_until_complete(runAct())
