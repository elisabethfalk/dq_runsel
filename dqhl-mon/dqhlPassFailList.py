#!/user/bin/env python

#==================================================================
# 
# dqhlPassFailList.py
#
# E. Falk (E.Falk@sussex.ac.uk)
# 2017-05-15 
#
# Produces an ascii file list with the Pass/Fail results of all
# the DQHL checks, one row entry per run number
# 
#==================================================================

import argparse
import sys
import couchdb
import DB_settings
from downloadCouchDBFiles import getCouchDBDict
from dqhlProcChecks import *

def initRunlistFile(firstRun, lastRun):
    # Open runlist file:
    runlistFileName = "runlist_%s-%s.txt" % (firstRun, lastRun)
    runlistFile = open(runlistFileName, "w")

    # Print list header:
    runlistFile.write("\n")
    runlistFile.write("Run no |   By processor   |" + \
                      "    Trigger Processor    |" + \
                      "                 Time Processor                 |" + \
                      "       Run Processor       |   PMT Processor\n")
    runlistFile.write("---------------------------" + \
                      "--------------------------" + \
                      "--------------------------------------------------" + \
                      "-----------------------------------------------\n")
    runlistFile.write("       | TTRP    | TTRP   |" + \
                      " N100L ESUMH Miss BitFlp |" + \
                      " Event GT in  Re-   1st ev 10 MHz  Event Event  |" + \
                      " Physics Monte Run    Trig | Ov'all Crate Panel\n")
    runlistFile.write("       | (modif) | (orig) |"+ \
                      " rate  rate  GTID GTID   |" + \
                      " rate  oth ev trigs time   UT comp order sep UT |" + \
                      " run     Carlo length mask | covg   covg  covg\n")
    runlistFile.write("---------------------------" + \
                      "--------------------------" + \
                      "--------------------------------------------------" + \
                      "-----------------------------------------------\n")

    return runlistFile

def processRun(runNumber, data, runlistFile):
    # Unpack validity range and results:
    run_range = data['run_range']
    checks = data['checks']

    # Unpack results from the four DQ procs:
    triggerProc = checks['dqtriggerproc']
    timeProc = checks['dqtimeproc']
    runProc = checks['dqrunproc']
    pmtProc = checks['dqpmtproc']

    # Print run results list:
    runlistFile.write("%s | %i%i%i%i    | %i%i%i%i   |" % \
           (str(runNumber), \
           modifTriggerProcChecksOK(triggerProc), \
           modifTimeProcChecksOK(timeProc), \
           modifRunProcChecksOK(runProc), pmtProcChecksOK(pmtProc), \
           triggerProcChecksOK(triggerProc), timeProcChecksOK(timeProc), \
           runProcChecksOK(runProc), pmtProcChecksOK(pmtProc)) + \
                      " %i     %i     %i    %i      |" % \
           (triggerProc['n100l_trigger_rate'], \
           triggerProc['esumh_trigger_rate'], \
           triggerProc['triggerProcMissingGTID'], 
           triggerProc['triggerProcBitFlipGTID']) + \
                      " %i     %i      %i     %i     " % \
           (timeProc['event_rate'], timeProc['event_separation'], \
           timeProc['retriggers'], timeProc['run_header']) + \
                      " %i       %i     %i      |" % \
           (timeProc['10Mhz_UT_comparrison'], timeProc['clock_forward'], \
           timeProc['delta_t_comparison']) + \
                      " %i       %i     %i      %i    | %i      %i     %i\n" % \
           (runProc['run_type'], runProc['mc_flag'], \
           runProc['run_length'], runProc['trigger'], \
           pmtProc['general_coverage'], pmtProc['crate_coverage'], \
           pmtProc['panel_coverage']))

    return

def dqhlPassFailList(firstRun, lastRun):

    # Open and initiate run-list file:
    runlistFile = initRunlistFile(firstRun, lastRun)

    # Loop over run range to print stats and fill histogram:
    i = 0
    for runNumber in range(firstRun, lastRun+1):
        # if ((i % 10 == 0) and (i != 0)):
        if ((runNumber % 10 == 0) and (i != 0)):
            runlistFile.write("- - - -|- - - - -|- - - - |" + \
                              " - - - - - - - - - - - - |" + \
                              " - - - - - - - - - - - - - "
                              "- - - - - - - - - - -|" + \
                              "- - - - - - - - - - - - - -|- - - - - - - - - -\n")

        # Download DQ ratdb table:
        db = couchdb.Server(DB_settings.COUCHDB_SERVER)
        data = getCouchDBDict(db, runNumber)
        # print "data: ", data
        if (data != None):
            print "Processing DQHL record for run number %i" % runNumber
            processRun(runNumber, data, runlistFile)
            i += 1

    return


if __name__=="__main__":
    # Parse command line:
    parser = argparse.ArgumentParser()
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

    print "Running dqhlPassFailList for run range %i-%i" % (firstRun, lastRun)
    dqhlPassFailList(firstRun, lastRun)
    sys.exit(0)

