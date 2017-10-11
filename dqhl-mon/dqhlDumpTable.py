#!/user/bin/env python

#==================================================================
# 
# dqhlDumpTable.py
#
# E. Falk (E.Falk@sussex.ac.uk)
# 2017-06-06 
#
# Fetches DQHL tables from CouchDB and prints them to file,
# one file per run, file name DATAQUALITY_RECORDS_NNNNNN.ratdb
# 
#==================================================================

import argparse
import sys
import os
import json
import couchdb
import DB_settings
from downloadCouchDBFiles import getCouchDBDict
from dqhlProcChecks import isPhysicsRun

def processRun(runNumber, data):

    # Open DQHL ratdb file:
    fileName = "DATAQUALITY_RECORDS_%s.ratdb" % runNumber
    tableFile = open(fileName, "w")

    # Write DQHL table, in JSON format, to file:
    print "Writing DQHL record for run number %i to file" % runNumber
    json.dump(data, tableFile)

    # Close DQHL ratdb file:
    tableFile.close()

    return

def dqhlDumpTable(firstRun, lastRun, dir):

    # Change to output directory:
    homeDir = os.getcwd()
    if not os.path.exists(dir):
        os.mkdir(dir)
    if not os.path.isdir(dir):
        print "Invalid directory name:", dir
        sys.exit(1)
    os.chdir(dir)

    # Open database(s):
    db = couchdb.Server(DB_settings.COUCHDB_SERVER)

    # Loop over run range to retrieve and dump DQHL tables:
    nRuns = 0
    for runNumber in range(firstRun, lastRun+1):

        # Download DQ ratdb table:
        data = getCouchDBDict(db, runNumber)
        if (data is not None):
            if isPhysicsRun(data):
                # print "data: ", data
                # print "Processing DQHL record for run number %i" % runNumber
                processRun(runNumber, data)
                nRuns += 1
            else:
                print "Run number %i is not a PHYSICS run" % runNumber + \
                      " (although DQHL record was found)"
        else:
            print "No DQHL record found for run number %i" % runNumber

    # Change back to home directory of script:
    os.chdir(homeDir)

    return


if __name__=="__main__":
    # Parse command line:
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="dir", help="directory", type=str, \
                        default=".")
    parser.add_argument('run_range', help="FIRSTRUN-LASTRUN", type=str)
    args = parser.parse_args()
    runs = args.run_range.split("-")
    parseOK = False
    if (len(runs) >= 1):
        if runs[0].isdigit():
            firstRun = int(runs[0])
            if len(runs) == 2:
                if runs[1].isdigit():
                    lastRun = int(runs[1])
                    parseOK = True
            elif len(runs) == 1:
                lastRun = firstRun
                parseOK = True
    if not parseOK:
        print parser.print_help()
        sys.exit(1)

    # Check that first run <= last run
    if lastRun < firstRun:
        print "Invalid run range: first run must precede, " \
               "or be equal to, last run"
        sys.exit(1)

    print "Running dqhlDumpTable for run range %i-%i" % (firstRun, lastRun)
    dqhlDumpTable(firstRun, lastRun, args.dir)
    sys.exit(0)

