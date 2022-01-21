from os.path import exists
import json

def check_exists(PATH):
    return exists(PATH)

def create_file(PATH):
    open(PATH, "x")

def dump_content(PATH, js_obj):
    temp_file = open(PATH, "w")
    json.dump(js_obj, temp_file)
    temp_file.close()

def get_content(PATH):
    #Open the .json file
    jsonfile = open(PATH,"r")
    #Converts json oject to a python list
    js_obj = json.load(jsonfile)
    jsonfile.close() #close the .json file
    return js_obj


