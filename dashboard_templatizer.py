'''
Created on Feb 26, 2018

@author: kpolakala
'''
import json
import collections
import pprint
import sys
import os

db_map = {
  "Attrition_Detail_Data_File_RL_PL": {
    "from": {
      "id": "0Fb0M000000AyrqSAC",
      "label": "Attrition_Detail_Data_File_RL_PL",
      "name": "Attrition_Detail_Data_File_RL_PL",
      "url": "/services/data/v42.0/wave/datasets/0Fb0M000000AyrqSAC"
    },
    "to": {
      "id": "0Fb0t0000008RhXCAU",
      "name": "Attrition_Detail_Data_File_RL_PL",
      "label": "Attrition_Detail_Data_File_RL_PL",
      "url": "/services/data/v42.0/wave/datasets/0Fb0t0000008RhXCAU"
    }
  },
  "POC_DATA_FY18_CSG_RL_SL_PL_Metric_Scorecard": {
    "from": {
      "id": "0Fb0M000000TOvJSAW",
      "label": "FY18 CSG RL/SL/PL Metric Scorecard",
      "name": "POC_DATA_FY18_CSG_RL_SL_PL_Metric_Scorecard",
      "url": "/services/data/v42.0/wave/datasets/0Fb0M000000TOvJSAW"
    },
    "to": {
      "id": "0Fb0t0000008RhWCAU",
      "name": "FY18_CSG_RL_SL_PL_Metric_Scorecard",
      "label": "FY18_CSG_RL_SL_PL_Metric_Scorecard",
      "url": "/services/data/v42.0/wave/datasets/0Fb0t0000008RhWCAU"
    }
  },
  "EWS_Growth_Detail_Data_File_RL_and_PL_Combined": {
    "from": {
      "id": "0Fb0M000000Az1gSAC",
      "label": "EWS_Growth_Detail_Data_File_RL and PL Combined",
      "name": "EWS_Growth_Detail_Data_File_RL_and_PL_Combined",
      "url": "/services/data/v42.0/wave/datasets/0Fb0M000000Az1gSAC"
    },
    "to": {
      "id": "0Fb0t0000008RhSCAU",
      "name": "EWS_Growth_Detail_Data_File_RL_PL",
      "label": "EWS_Growth_Detail_Data_File_RL_PL",
      "url": "/services/data/v42.0/wave/datasets/0Fb0t0000008RhSCAU"
    }
  },
  "Qualified_Oppty_Detail_Data_File_RL": {
    "from": {
      "id": "0Fb0M000000Az0OSAS",
      "label": "Qualified_Oppty_Detail_Data_File_RL",
      "name": "Qualified_Oppty_Detail_Data_File_RL",
      "url": "/services/data/v42.0/wave/datasets/0Fb0M000000Az0OSAS"
    },
    "to": {
      "id": "0Fb0t0000008RhUCAU",
      "name": "Qualified_Oppty_Detail_Data_File_RL",
      "label": "Qualified_Oppty_Detail_Data_File_RL",
      "url": "/services/data/v42.0/wave/datasets/0Fb0t0000008RhUCAU"
    }
  },
  "Cloud_Services_Bookings_Detail_Data_File_RL": {
    "from": {
      "id": "0Fb0M000000AyyhSAC",
      "label": "Cloud_Services_Bookings_Detail_Data_File_RL",
      "name": "Cloud_Services_Bookings_Detail_Data_File_RL",
      "url": "/services/data/v42.0/wave/datasets/0Fb0M000000AyyhSAC"
    },
    "to": {
      "id": "0Fb0t0000008RhTCAU",
      "name": "Cloud_Services_Bookings_Detail_Data_File_RL",
      "label": "Cloud_Services_Bookings_Detail_Data_File_RL",
      "url": "/services/data/v42.0/wave/datasets/0Fb0t0000008RhTCAU"
    }
  }
}

locations = [
    "state","dataSourceLinks","Array","fields","dataSourceName",
    "steps","STEP_NAME","datasets","OR","query",
    ]
DB_JSON = "/Users/kpolakala/csg/CSGScorecards/04 Detail Pages/CSG Scorecard -- Attrition Scorecard Details.json"
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
if __name__ == '__main__':
    fllist = get_filelist("/Users/kpolakala/csg/CSGScorecards/03 Team View Page")
    pprint.pprint(fllist)
    
    for db_fl in fllist: 
        db = load_json_from_file(db_fl,object_pairs_hook=None)
        db = templatize_datasourcelinks(db)
        db = templatize_stepsdatasets(db)
        db = templatize_stepsquery(db)
        db = templatize_stepsquerypigql(db)
        db = templatize_datasets(db)
        dump_json_to_file(db_fl+"temp", db)
    sys.exit()
