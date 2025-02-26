from resources.Globals import importlib, utils, logger, consts, os, time
from executables.services.Base import BaseService
from executables.acts.AExtractMetadata import AExtractMetadata
from executables.acts.AAdditionalMetadata import AAdditionalMetadata

def metadata_wheel(input_file):
    ps = dict()
    ps["type"] = "arr"
    ps["input_file"] = input_file

    md = AExtractMetadata()
    res = md.execute(args=ps)

    return res

def additional_metadata_wheel(input_file):
    ps = dict()
    ps["type"] = "arr"
    ps["input_file"] = input_file

    md = AAdditionalMetadata()
    res = md.execute(args=ps)

    return res
