#/usr/bin/env python

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

def createRATDBFiles(db,imagedir):
    folders = os.listdir(imagedir)
    for fold in folders:
        if not "TELLIE_DQ_IMAGES" in fold:
            continue
        runNum = int(fold.split("_")[-1])
        couchDict = getCouchDBDict(db,runNum)
        outFile = os.path.join(imagedir,fold)
        outFile = os.path.join(outFile,"DATAQUALITY_RECORDS_%d_p1.ratdb" % runNum)
        print "Creating File: %s" % outFile
        with open(outFile,"w") as fil:
            outString = json.dumps(couchDict,fil,indent=0)
            fil.write(outString)


if __name__=="__main__":
    db = couchdb.Server(DB_settings.COUCHDB_SERVER)
    # createRATDBFiles(db,"/home/mark/Documents/PHD/DQTests/TELLIEDQTest/28March2017Runs")
    createRATDBFiles(db,".")

