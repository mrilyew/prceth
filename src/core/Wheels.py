from resources.Globals import importlib, utils, logger, consts, os, time
from executables.services.Base import BaseService
from executables.acts.AExtractMetadata import AExtractMetadata
from executables.acts.AAdditionalMetadata import AAdditionalMetadata

def metadata_wheel(i):
    ___ps = dict()
    ___ps["type"] = "arr"

    md = AExtractMetadata()
    RES = md.execute(i=i,args=___ps)

    return RES

def additional_metadata_wheel(i):
    ___ps = dict()
    ___ps["type"] = "arr"

    md = AAdditionalMetadata()
    __F = md.parseMainInput(main_input=i)
    res = md.execute(i=__F,args=___ps)

    return res
