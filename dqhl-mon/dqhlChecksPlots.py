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
import json
import os
from downloadCouchDBFiles import downloadRATDBtables
from dqhlProcChecks import *
from dqhlChecksHistograms import createHistograms, fillHistograms, \
                                 drawHistograms

def processRun(runNumber, data, hist):
    # Fill histograms
    fillHistograms(runNumber, data, hist)

    return

def dqhlChecksPlots(firstRun, lastRun, dataDir, downloadRATDB):
    # If true download missing ratdb DQHL tables
    if ( downloadRATDB ):
        downloadRATDBtables(firstRun, lastRun, dataDir)
        
    # Create Dictionary hist of keys(hist name) and values(hist itself):
    hist = createHistograms(firstRun, lastRun)

    nRuns = 0
    # Loop over all the saved ratdb files to produce the DQHL histograms
    for runNum in range(firstRun, lastRun+1):
        fileName = os.path.join(dataDir, "DATAQUALITY_RECORDS_%i.ratdb" % runNum)
        try:
            json_data = open(fileName).read()
            data = json.loads(json_data)
            if isPhysicsRun(data):
                print "Processing DQHL record for run number %i" % runNum
                processRun(runNum, data, hist)
                nRuns += 1
            else:
                print "Run number %i is not a PHYSICS run" % runNum + \
                    " (although DQHL record was found)"
        except IOError:
            print "No RATDB file for run %i " %runNum
            continue
    # Draw histograms:
    drawHistograms(firstRun, lastRun, nRuns, hist)

    return

if __name__=="__main__":
    # Parse command line:
    parser = argparse.ArgumentParser()
    parser.add_argument('run_range', help="FIRSTRUN-LASTRUN", type=str)
    parser.add_argument('--download', dest="downloadRATDB",help="Download RATDB tables to a directory.", action='store_true')
    parser.add_argument('-d', '--dir', dest="dataDir", help="Directory (including path) of ratdb files.", type=str, required=True)
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
        print "Invalid run range: first run must precede or be equal to, last run"
        sys.exit(1)

    print "Running dqhlChecksPlots for run range %i-%i" % (firstRun, lastRun)

    dqhlChecksPlots(firstRun, lastRun, args.dataDir, args.downloadRATDB)

    sys.exit(0)

