import operator
import time
import traceback
import threading
import platform
import os
import win32api
import win32file
import json
import sys
import random
import i18n
import yt_dlp
import shutil
import requests
import mimetypes
import importlib
from resources.exceptions import ApiException
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from urllib.parse import urlparse
from urllib.parse import urlencode
from pathlib import Path
from playhouse.shortcuts import model_to_dict
from datetime import datetime
from functools import reduce
from resources.consts import consts
from core.settings import settings
from localization.locale import _
from core.logger import logger
from core.file_manager import file_manager 
from core.utils import utils
from db.db import db, Collection, Entity, Relation, Stat
from plugins import load_plugins
