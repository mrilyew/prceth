from resources.Globals import importlib, utils, logger, consts, os, time
from executables.services.Base import BaseService
from executables.acts.AExtractMetadata import AExtractMetadata
from executables.acts.AAdditionalMetadata import AAdditionalMetadata

def metadata_wheel(input_file):
    ___ps = dict()
    ___ps["INPUT_TYPE"] = "file"

    md = AExtractMetadata()
    RES = md.execute(i=input_file,args=___ps)

    return RES

def additional_metadata_wheel(input_file):
    ___ps = dict()
    ___ps["INPUT_TYPE"] = "file"

    md = AAdditionalMetadata()
    res = md.execute(i=input_file,args=___ps)

    return res
