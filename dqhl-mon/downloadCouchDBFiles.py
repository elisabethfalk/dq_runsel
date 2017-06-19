#!/usr/bin/env python

# From Mark Stringer

import couchdb
import json
import os
import DB_settings

def getCouchDBDict(server,runNumber):
    dqDB = server["data-quality"]
    data = None
    for row in dqDB.view('_design/data-quality/_view/runs'):
        if(int(row.key) == runNumber):
            runDocId = row['id']
            data = dqDB.get(runDocId)
            return data

def createRATDBFiles(db, runNum):
    if not os.path.exists("./ratdb_files"):
        os.makedirs("./ratdb_files")
    outFile = "./ratdb_files/DATAQUALITY_RECORDS_%d.ratdb" % runNum
    if not os.path.isfile(outFile):
        couchDict = getCouchDBDict(db, runNum)
        print "Creating File: %s" %outFile
        with open(outFile,"w") as fil:
            outString = json.dumps(couchDict,fil,indent=1)
            fil.write(outString)
    else:
        print "File: %s already exists." %outFile


if __name__=="__main__":
    db = couchdb.Server(DB_settings.COUCHDB_SERVER)
    # createRATDBFiles(db,"/home/mark/Documents/PHD/DQTests/TELLIEDQTest/28March2017Runs")
    createRATDBFiles(db,".")

