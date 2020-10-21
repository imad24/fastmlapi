# -*- coding: utf-8 -*-
"""This file contains the global settings of the package
Make sure you set the following environement variables:
        APPPATH: the absolute path to the application folder
"""
import os
import sys
import logging
import json
from dotenv import find_dotenv, load_dotenv
import datetime



#Setting the app directory
app_dir= None
logging_level = logging.INFO
globalConfigFile = None
userConfigFile = None

options = {}

def init():

        load_dotenv(find_dotenv())

        global app_dir

        global globalConfigFile
        global userConfigFile
        global options

        app_dir = os.path.normpath(os.getenv("APPPATH"))
        globalConfigFile = os.path.join(app_dir,'config.json')

        with open(globalConfigFile, mode="r", encoding="utf-8") as cfg:
                options = json.load(cfg)


        if "log_level" in options:
                _set_logging_level(options["log_level"])

def get_logger(name):
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_fmt)

    logger = logging.getLogger(name)

    # clean any set logger
    if (logger.hasHandlers()):
        logger.handlers.clear()

    logger.setLevel(logging.DEBUG)
     
    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging_level)
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
 
    now = datetime.datetime.now()
    # create error file handler and set level to error
    log_file_name = "error_%s.log"%(now.strftime("%d_%m_%Y"))
    handler = logging.FileHandler(os.path.join(app_dir, log_file_name),"a", encoding=None, delay="true")
    handler.setLevel(logging.ERROR)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
 
    # create debug file handler and set level to debug
    log_file_name = "app_%s.log"%(now.strftime("%d_%m_%Y"))
    handler = logging.FileHandler(os.path.join(app_dir, log_file_name),"a")
    handler.setLevel(logging_level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
    
def load_json_file(filename):
        # ignore .json extension if provided
        base_filename = str(filename).split(".")[0]
        #get current directory (configuration)
        dirpath = os.path.dirname(os.path.realpath(__file__))
        #build the full path to the local json file
        full_filepath = os.path.join(dirpath, base_filename + ".json")
        with open(full_filepath) as filecontent:
                data = json.load(filecontent)
                return data     


    
def _set_logging_level(verbose):
        global logging_level
        levels= {
        "DEBUG":logging.DEBUG,
        "INFO":logging.INFO,
        "WARNING":logging.WARNING,
        "ERROR":logging.ERROR,
        "CRITICAL":logging.CRITICAL,
        "FATAL":logging.FATAL
        }
        alias = { 0:"DEBUG", 1:"INFO",2:"WARNING", 3:"ERROR", 4:"CRITICAL", 5:"FATAL"}
        if verbose in levels: 
                logging_level = levels[verbose]
        elif verbose in range(len(levels)):
                logging_level = levels[alias[verbose]]

def get_option(key, default=None):
        return options.get(key, default)

def set_options(options):
    with open(userConfigFile, 'w') as cfg:
        json.dump(options, cfg)


#init configuration
init()