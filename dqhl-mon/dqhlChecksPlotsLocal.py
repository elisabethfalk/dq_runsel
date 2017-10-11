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
import os
import json
import couchdb
import ROOT
import DB_settings
from downloadCouchDBFiles import getCouchDBDict
from dqhlProcChecks import *
from dqhlChecksHistograms import createHistograms, fillHistograms, \
                                 drawHistograms, writeHistograms

def processRun(runNumber, data, hist):

     # Fill histograms:
    fillHistograms(runNumber, data, hist)

    return

def printRuns(runList, listTitle, printRunNo = True, printParam = True):

    # List run numbers, associated parameter, or both, for supplied list of runs:
    print "\n%s:" % listTitle
    if (printRunNo and printParam): # List run no and parameter
        for run in runList:
            print "%6i, %13.10f" % (run[0], run[1])
    elif printRunNo: # List run no only
        for run in runList:
            print "%6i" % run[0]
    else: # List parameter only
        for run in runList:
            print "%13.10f" % run[1]
    print "\n"

    return

def printMissBitFlipGTIDRecoveryCandidates(runList, listTitle, printRunNo = True, printParams = True):

    # List run numbers, associated parameters, or both, for supplied list of runs:
    print "\n%s:" % listTitle
    if (printRunNo and printParams): # List run no and parameters
        for run in runList:
            print "%6i, %6i, %6i, %6i" % (run[0], run[1], run[2], run[3])
    elif printRunNo: # List run no only
        for run in runList:
            print "%6i" % run[0]
    else: # List parameters only
        for run in runList:
            print "%6i" % run[3]
    print "\n"

    return

def dqhlChecksPlots(firstRun, lastRun, dir):

    # Change to output directory:
    homeDir = os.getcwd()
    if not os.path.exists(dir):
        os.mkdir(dir)
    if not os.path.isdir(dir):
        print "Invalid directory name:", dir
        sys.exit(1)
    os.chdir(dir)

    # Create Histograms:
    hist = createHistograms(firstRun, lastRun)

    # Open database(s):
    # if True:
    # else:
        # db = couchdb.Server(DB_settings.COUCHDB_SERVER)

    # Loop over run range to extract stats and fill list(s)/histogram(s):
    nRuns = 0
    nDqhlPass = 0
    nRetriggerFail = 0
    nRetriggerFailDqhlPass = 0
    nRetriggerFailDqhlPassRunLengthPass = 0
    retriggerRecoveryCandidates = []
    nMissGTIDFail = 0
    nBitFlipGTIDFail = 0
    nMissBitFlipGTIDFail = 0
    nMissBitFlipGTIDFailDqhlPass = 0
    nMissBitFlipGTIDFailDqhlPassRunLengthPass = 0
    missBitFlipGTIDRecoveryCandidates = []
    missBitFlipGTIDRecoveryCandidatesRelaxedRetrigger = []
    for runNumber in range(firstRun, lastRun+1):
        # Download DQ ratdb table:
        data = None
        if True: 
            fileName = "DATAQUALITY_RECORDS_%s.ratdb" % runNumber
            if os.path.exists(fileName):
                tableFile = open(fileName, "r")
                # Check whether file exists...!!
                data = json.load(tableFile)
        else:
            data = getCouchDBDict(db, runNumber)
        # print "data: ", data
        if (data is not None):
            if isPhysicsRun(data):
                print "Processing DQHL record for run number %i" % runNumber
                processRun(runNumber, data, hist)
                nRuns += 1

                timeProc = data['checks']['dqtimeproc']
                triggerProc = data['checks']['dqtriggerproc']
                runProc = data['checks']['dqrunproc']
                pmtProc = data['checks']['dqpmtproc']

                if (modifDqhlChecksOK(runNumber, data)):
                        nDqhlPass += 1

                if (not retriggerCheckOK(timeProc)):
                    nRetriggerFail += 1
                if (not modifMissGTIDCheckOK(runNumber, triggerProc)):
                        nMissGTIDFail +=1
                if (not modifBitFlipGTIDCheckOK(triggerProc)):
                        nBitFlipGTIDFail +=1
                if ((not modifMissGTIDCheckOK(runNumber, triggerProc)) or \
                    (not modifBitFlipGTIDCheckOK(triggerProc))):
                        nMissBitFlipGTIDFail +=1

                if (modifTriggerProcChecksOK(runNumber, triggerProc) and
                    modifRunProcChecksOK(runNumber, runProc) and
                    pmtProcChecksOK(pmtProc)):
                    if (not modifTimeProcChecksOK(runNumber, timeProc)):
                        if (modifEventRateCheckOK(timeProc) and
                            eventSeparationCheckOK(timeProc) and
                            runHeaderCheckOK(timeProc) and
                            tenMhzUTComparisonCheckOK(timeProc) and
                            clockForwardCheckOK(timeProc)):
                            if (not retriggerCheckOK(timeProc)):
                                nRetriggerFailDqhlPass += 1
                                if (runLengthCheckOK(runProc)):
                                    nRetriggerFailDqhlPassRunLengthPass +=1
                                    retriggerRecoveryCandidates.append([runNumber, \
                                                                        timeProc['check_params']['retriggers_value']])

                # if (modifTimeProcChecksOK(runNumber, timeProc) and
                if (testTimeProcChecksOK(runNumber, timeProc) and
                    modifRunProcChecksOK(runNumber, runProc) and
                    pmtProcChecksOK(pmtProc)):
                    if (not modifTriggerProcChecksOK(runNumber, triggerProc)):
                        if (n100lTriggerRateCheckOK(triggerProc) and
                            esumhTriggerRateCheckOK(triggerProc)):
                            if ((not modifMissGTIDCheckOK(runNumber, triggerProc)) or \
                                (not modifBitFlipGTIDCheckOK(triggerProc))):
                                nMissBitFlipGTIDFailDqhlPass +=1
                                if (runLengthCheckOK(runProc)):
                                    nMissBitFlipGTIDFailDqhlPassRunLengthPass +=1
                                    missBitFlipGTIDRecoveryCandidates.append([runNumber, \
                                                                              triggerProc['check_params']['orphans_count'], 
                                                                              len(triggerProc['check_params']['missing_gtids']), 
                                                                              len(triggerProc['check_params']['bitflip_gtids'])])
                                    if (not modifTimeProcChecksOK(runNumber, timeProc)):
                                        missBitFlipGTIDRecoveryCandidatesRelaxedRetrigger.append([runNumber])

            else:
                print "Run number %i is not a PHYSICS run" % runNumber + \
                      " (although DQHL record was found)"
        else:
            print "No DQHL record found for run number %i" % runNumber

    # Change back to home directory of script:
    os.chdir(homeDir)

    # Write histograms to file; draw them to .png canvasses:
    c1 = drawHistograms(firstRun, lastRun, nRuns, hist)
    writeHistograms(firstRun, lastRun, nRuns, hist)

    # Print stats of runs failing Retrigger, Miss GTID and BitFlip checks:
    print "\n"
    print "No of physics runs with DQHL data processed: %i" % nRuns
    print "No of physics runs that pass all DQHL criteria: %i" % nDqhlPass
    print "No of physics runs that fail retrigger criterion: %i" % nRetriggerFail
    print "No of physics runs that fail retrigger criterion and pass the other DQHL criteria: %i" % \
          nRetriggerFailDqhlPass
    print "No of physics runs that fail retrigger criterion and pass the other DQHL criteria + run length: %i" % \
          nRetriggerFailDqhlPassRunLengthPass
    print "No of physics runs that fail missing GTID criterion: %i" % nMissGTIDFail
    print "No of physics runs that fail bitflip GTID criterion: %i" % nBitFlipGTIDFail
    print "No of physics runs that fail at least one of missing and bitflip GTID criteria: %i" % nMissBitFlipGTIDFail
    print "No of physics runs that fail at least one of missing and bitflip GTID criteria and pass the other DQHL criteria: %i" % \
          nMissBitFlipGTIDFailDqhlPass
    print "No of physics runs that fail at least one of missing and bitflip GTID criteria and pass the other DQHL criteria + run length: %i" % \
          nMissBitFlipGTIDFailDqhlPassRunLengthPass

    # print missBitFlipGTIDRecoveryCandidates

    # Print list of runs that failed retrigger cut:
    printRuns(retriggerRecoveryCandidates, "Retrigger recovery candidates", 
              printRunNo = True, printParam = True)

    # Print list of runs that failed miss or bitflip GTID cut:
    # printMissBitFlipGTIDRecoveryCandidates(missBitFlipGTIDRecoveryCandidates, "Missing/BitFlip GTID recovery candidates", 
    #     printRunNo = False, printParams = True)

    # Print list of runs that failed miss or bitflip GTID cut and are recovered Retrigger failures:
    # printRuns(missBitFlipGTIDRecoveryCandidatesRelaxedRetrigger, "Missing/BitFlip GTID recovery candidates that are recovered Retrigger failures", 
    #          printRunNo = True, printParam = False)

    return c1


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

    print "Running dqhlChecksPlots for run range %i-%i" % (firstRun, lastRun)
    c1 = dqhlChecksPlots(firstRun, lastRun, args.dir)

    sys.exit(0)

