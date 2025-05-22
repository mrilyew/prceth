from resources.Globals import utils, loop, ActsRepository
from resources.DbPrefetch import prefetch__db

prefetch__db()

args = utils.parse_args()

async def runAct():
    assert "i" in args, "i not passed"

    __act_name = args.get("i")
    __act_res = ActsRepository().getByName(act_name=__act_name)
    assert __act_res != None, "act not found"

    OUT_ACT = __act_res()
    OUT_ACT.setArgs(args)

    ACT_F = await OUT_ACT.execute(args=args)

    print({"results": ACT_F})

loop.run_until_complete(runAct())
