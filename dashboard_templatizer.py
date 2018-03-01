'''
Created on Feb 26, 2018

@author: kpolakala
'''
import json
import collections
import pprint
import sys
import os
from __builtin__ import str
CONFIG_FILE="scorecards_config.json"

def load_json_from_file(filename, object_pairs_hook=collections.OrderedDict):
    fl = open(filename, "r")
#     fl_json = json.load(fl, object_pairs_hook=object_pairs_hook)
    fl_json = json.load(fl, object_pairs_hook=object_pairs_hook)
    fl.close()
    return fl_json

def dump_json_to_file(filename,json_obj,sort_keys=False):
    fl = open(filename, "w")
    json.dump(json_obj, fl, indent=2)
    fl.close()
def get_filelist(directory):
    fllist = []
    for fl in os.listdir(directory):
        if os.path.isdir(os.path.join(directory,fl)):
            fls = get_filelist(os.path.join(directory,fl))
            for fl_1 in fls:
                fllist.append(fl_1)
        if str(fl).endswith(".json") and str(fl).find("xmd")<0 and os.stat(os.path.join(directory,fl)).st_size > 0:
            fllist.append(os.path.join(directory,fl))
    return fllist
    
def templatize_datasourcelinks(db):
    for dsrc in db["state"]["dataSourceLinks"]:
        for fld in dsrc["fields"]:
            print fld["dataSourceName"]
            if db_map.has_key(fld["dataSourceName"]):
                fld["dataSourceName"] = db_map[fld["dataSourceName"]]["to"]["name"]
            else:
                print fld["dataSourceName"], "is not MAPPED..."
    return db  

def templatize_stepsdatasets(db):
    for step in db["state"]["steps"].keys():
        if db["state"]["steps"][step].has_key("datasets"):
            for i in range(len(db["state"]["steps"][step]["datasets"])):
                if db_map.has_key(db["state"]["steps"][step]["datasets"][i]["name"]):
                    db["state"]["steps"][step]["datasets"][i] = db_map[db["state"]["steps"][step]["datasets"][i]["name"]]["to"]
                else:
                    print db["state"]["steps"][step]["datasets"][i]["name"], "is not MAPPED..."
    return db  

def templatize_stepsquery(db):
    for k in range(len(db["state"]["steps"].keys())):
        step = db["state"]["steps"].keys()[k]
        if db["state"]["steps"][step].has_key("query"):
            if type(db["state"]["steps"][step]["query"]) is unicode or type(db["state"]["steps"][step]["query"]) is str:
                qry =  db["state"]["steps"][step]["query"]
                qry = str(qry).split(";")
                for i in range(len(qry)):
                    stm = qry[i]
                    if str(stm).find("load ") >=0:
                        lds = str(stm).split("load ")
                        edg = str(lds[1]).lstrip().lstrip('"').rstrip().rstrip('"')
                        if db_map.has_key(edg):
                            lds[1] = str(lds[1]).replace(edg, db_map[edg]["to"]["name"])
                        else:
                            print edg, "is not MAPPED..."
                        qry[i] = "load ".join(lds)
                db["state"]["steps"][step]["query"] = ";".join(qry)
#                 pprint.pprint(qry)
    return db  
def templatize_stepsquerypigql(db):
    for k in range(len(db["state"]["steps"].keys())):
        step = db["state"]["steps"].keys()[k]
        if db["state"]["steps"][step].has_key("query"):
            if type(db["state"]["steps"][step]["query"]) is str or type(db["state"]["steps"][step]["query"]) is unicode:
                continue
            if db["state"]["steps"][step]["query"].has_key("pigql"):
                if type(db["state"]["steps"][step]["query"]["pigql"]) is unicode or type(db["state"]["steps"][step]["query"]["pigql"]) is str:
                    qry =  db["state"]["steps"][step]["query"]["pigql"]
                    qry = str(qry).split(";")
                    for i in range(len(qry)):
                        stm = qry[i]
                        if str(stm).find("load ") >=0:
                            lds = str(stm).split("load ")
                            edg = str(lds[1]).lstrip().lstrip('"').rstrip().rstrip('"')
                            if db_map.has_key(edg):
                                lds[1] = str(lds[1]).replace(edg, db_map[edg]["to"]["name"])
                            else:
                                print edg, "is not MAPPED..."
                            qry[i] = "load ".join(lds)
                    db["state"]["steps"][step]["query"]["pigql"] = ";".join(qry)
#                 pprint.pprint(qry)
    return db  

def templatize_datasets(db):
    datasets = []
    for ds in db["datasets"]:
        if db_map.has_key(ds["name"]):
            datasets.append(db_map[ds["name"]]["to"])
        else:
            print ds["name"], "is not MAPPED..."
    db["datasets"] = datasets
    return db
def templatize_images(db):
    for i in range(len(db["state"]["gridLayouts"])):
        gl = db["state"]["gridLayouts"][i]
        if gl["style"].has_key("image"):
            if db_image_map.has_key(gl["style"]["image"]["name"]):
                gl["style"]["image"]["name"] = db_image_map[gl["style"]["image"]["name"]]
#             pprint.pprint(gl["style"]["image"]["name"])
    return db
def templatize_links(db):
    for wname in db["state"]["widgets"].keys():
        widget = db["state"]["widgets"][wname]
        if widget["type"] == "link":
            if widget["parameters"]["destinationType"] == "dashboard":
                if widget["parameters"].has_key("destinationLink"):
                    print widget["parameters"]["destinationLink"]["name"]
                    if db_links_map.has_key(widget["parameters"]["destinationLink"]["name"]):
                        widget["parameters"]["destinationLink"]["name"] = db_links_map[widget["parameters"]["destinationLink"]["name"]] 
        
    return db

if __name__ == '__main__':
    db_config = load_json_from_file(CONFIG_FILE)
    db_map = db_config["db_datasets_map"]
    db_links_map = db_config["db_links_map"]
    db_image_map = db_config["db_image_map"]
    
    src_dir = db_config["SRC_DIR"]
    dst_dir = db_config["DST_DIR"]
    db_fls = db_config["dashboards"]
    
#     fllist = get_filelist("/Users/kpolakala/csg/CSGScorecards/03 Team View Page")
    fllist = {}
    for db_fl in db_fls:
        fllist[os.path.join(src_dir,db_fl)] = os.path.join(dst_dir,db_fl)
    pprint.pprint(fllist)
    
    for db_fl in fllist.keys():
        print db_fl 
        db = load_json_from_file(db_fl)
        db = templatize_datasourcelinks(db)
        db = templatize_stepsdatasets(db)
        db = templatize_stepsquery(db)
        db = templatize_stepsquerypigql(db)
        db = templatize_datasets(db)
        db = templatize_images(db)
        db = templatize_links(db)
        ddir = os.path.dirname(fllist[db_fl])
        if os.path.exists(ddir) == False:
            os.makedirs(ddir)
        dump_json_to_file(fllist[db_fl], db)
    sys.exit()
