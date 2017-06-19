#!/user/bin/env python

#==================================================================
# 
# dqhlChecksPlots.py
#
# E. Falk (E.Falk@sussex.ac.uk)
# 2017-05-28
#
# Produces histograms of the various DQHL checks, and of some of
# the parameters monitored by DQHL
# 
#==================================================================

import argparse
import sys
import ROOT
import couchdb
import DB_settings
from downloadCouchDBFiles import getCouchDBDict
from downloadCouchDBFiles import createRATDBFiles
from dqhlProcChecks import *
from dqhlChecksHistograms import createHistograms, fillHistograms, \
                                 drawHistograms

def processRun(runNumber, data, hist):
    # Fill histograms:
    fillHistograms(runNumber, data, hist)

    return

def dqhlChecksPlots(firstRun, lastRun):

    # Create Histograms:
    hist = createHistograms(firstRun, lastRun)

    # Open database(s):                                                         
    db = couchdb.Server(DB_settings.COUCHDB_SERVER)

    # Loop over run range to extract stats and fill list(s)/histogram(s):
    nRuns = 0
    for runNumber in range(firstRun, lastRun+1):
        # Download DQ ratdb table:
        data = getCouchDBDict(db, runNumber)
        # print "data: ", data
        if (data is not None):
            if isPhysicsRun(data):
                print "Processing DQHL record for run number %i" % runNumber
                processRun(runNumber, data, hist)
                nRuns += 1
            else:
                print "Run number %i is not a PHYSICS run" % runNumber + \
                      " (although DQHL record was found)"
        else:
            print "No DQHL record found for run number %i" % runNumber

    # Draw histograms:
    c1 = drawHistograms(firstRun, lastRun, nRuns, hist)

    return c1


if __name__=="__main__":
    # Parse command line:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=int, required=True, help="First run number in your list.")
    parser.add_argument('-f', type=int, required=True, help="Last run number in your list.")
    parser.add_argument('--createratdb', dest="createRATDB",help="Save and read from existing ratdb files, instead from memory", action='store_true')
    args = parser.parse_args()

    firstRun = args.i
    lastRun = args.f

    # Check that first run <= last run
    if lastRun < firstRun:
        print "Invalid run range: first run must precede, " \
               "or be equal to, last run"
        sys.exit(1)

    print "Running dqhlChecksPlots for run range %i-%i" % (firstRun, lastRun)

    # Check if user wants to save ratdb files
    if (args.createRATDB):
        db = couchdb.Server(DB_settings.COUCHDB_SERVER)
        for runNumber in range(firstRun, lastRun+1):
            createRATDBFiles(db, runNumber)

    
    sys.exit(0)

