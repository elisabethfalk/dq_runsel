#!/usr/bin/env python

# From Mark Stringer

import couchdb
import json
import os
import DB_settings

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

    for runNum in range(firstRun, lastRun):
        outFile = "./ratdb_files/DATAQUALITY_RECORDS_%i.ratdb" % runNum

        # Donwload table if the user doesn't have it
        if not os.path.isfile(outFile):
            couchDict = getDQtable(db, runNum)
            if (couchDict != None):
                print "Creating File: %s" %outFile
                with open(outFile,"w") as fil:
                    outString = json.dumps(couchDict,fil,indent=1)
                    fil.write(outString)
            else:
                print "No DQHL table for run %i" %runNum
        else:
            print "File: %s already exists." %outFile
