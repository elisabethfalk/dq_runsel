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
from downloadCouchDBFiles import createRATDBFiles
from dqhlProcChecks import isPhysicsRun
from dqhlChecksHistograms import createHistograms, fillHistograms, \
                                 drawHistograms

def dqhlChecksPlots(firstRun, lastRun):

    # Create Dictionary hist of keys(hist name) and values(hist itself):
    hist = createHistograms(firstRun, lastRun)

    nRuns = 0
    # Loop over all the saved ratdb files to produce the DQHL histograms
    for fileName in os.listdir("./ratdb_files"):
        json_data = open("./ratdb_files/"+fileName).read()
        data = json.loads(json_data)
        runNum = int(fileName[20:-6])
        if isPhysicsRun(data):
            print "Processing DQHL record for run number %i" % runNum
            nRuns += 1
            fillHistograms(runNum, data, hist)
        else:
            print "Run number %i is not a PHYSICS run" % runNum + \
                " (although DQHL record was found)"

    # Draw histograms:
    drawHistograms(firstRun, lastRun, nRuns, hist)

if __name__=="__main__":
    # Parse command line:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=int, required=True, help="First run number in your list.")
    parser.add_argument('-f', type=int, required=True, help="Last run number in your list.")
    parser.add_argument('--createratdb', dest="createRATDB",help="Save and read from existing ratdb files, instead from memory.", action='store_true')
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
        createRATDBFiles(firstRun, lastRun)

    dqhlChecksPlots(firstRun, lastRun)
    
    sys.exit(0)

