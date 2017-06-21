#!/usr/bin/env python

# From Mark Stringer

import couchdb
import json
import os
import DB_settings
from dqhlProcChecks import isPhysicsRun

def getDQtable(server,runNumber):
    dqDB = server["data-quality"]
    data = None
    for row in dqDB.view('_design/data-quality/_view/runs'):
        if(int(row.key) == runNumber):
            runDocId = row['id']
            data = dqDB.get(runDocId)
            return data

def createRATDBFiles(firstRun, lastRun):
    # Connect to couchdb
    db = couchdb.Server(DB_settings.COUCHDB_SERVER)
    if not os.path.exists("./ratdb_files"):
        os.makedirs("./ratdb_files")

    for runNum in range(firstRun, lastRun+1):
        outFile = "./ratdb_files/DATAQUALITY_RECORDS_%i.ratdb" % runNum

        # Donwload table if the user doesn't have it and is a physics run
        if not os.path.isfile(outFile):
            couchDict = getDQtable(db, runNum)
            if (couchDict != None):
                if isPhysicsRun(couchDict):
                    print "Creating File: %s" %outFile
                    with open(outFile,"w") as fil:
                        outString = json.dumps(couchDict,fil,indent=1)
                        fil.write(outString)
                else:
                    print "Run number %i is not a PHYSICS run" % runNum + \
                        " (although DQHL record was found)"
            else:
                print "No DQHL table for run %i" %runNum
        else:
            print "File: %s already exists." %outFile
