from resources.Globals import importlib, utils, logger, consts, os, time
from executables.services.Base import BaseService
from executables.acts.Metadata.ExtractMetadata import ExtractMetadata
from executables.acts.Metadata.AdditionalMetadata import AdditionalMetadata

def metadata_wheel(input_file):
    ___ps = dict()
    ___ps["INPUT_TYPE"] = "file"

    md = ExtractMetadata()
    RES = md.execute(i=input_file,args=___ps)

    return RES

def additional_metadata_wheel(input_file):
    ___ps = dict()
    ___ps["INPUT_TYPE"] = "file"

    md = AdditionalMetadata()
    res = md.execute(i=input_file,args=___ps)

    return res
