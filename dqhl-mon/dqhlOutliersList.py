#!/user/bin/env python

#==================================================================
# 
# dqhlOutliersList.py
#
# E. Falk (E.Falk@sussex.ac.uk)
# 2017-05-17 
#
# Produces an ascii file list with the outliers showing up in
# various DQHL parameters, one table row entry per run number
# 
#==================================================================

import argparse
import sys
import couchdb
import DB_settings
from downloadCouchDBFiles import getCouchDBDict
from dqhlProcChecks import *

# Outlier thresholds:
# esumhTriggerRateThreshold = 20
esumhTriggerRateThreshold = 30
n100lTriggerRateThreshold = 100
# orphansCountThreshold = 100
orphansCountThreshold = 1000
# meanNhitThreshold = 10
meanNhitThreshold = 20
bitFlipThreshold = 0

minEventRate = 300
maxEventRate = 2000

def isOutlierNhit(runProc):
    outlier = False
    if (runProc['check_params']['mean_nhit'] > meanNhitThreshold):
        outlier = True
    return outlier

def isOutlierEsumhTriggerRate(triggerProc):
    outlier = False
    if (triggerProc['check_params']['esumh_trigger_rate'] > \
        esumhTriggerRateThreshold):
        outlier = True
    return outlier

def isOutlierN100lTriggerRate(triggerProc):
    outlier = False
    if (triggerProc['check_params']['n100l_trigger_rate'] > \
        n100lTriggerRateThreshold):
        outlier = True
    return outlier

def isOutlierOrphansCount(triggerProc):
    outlier = False
    if (triggerProc['check_params']['orphans_count'] > \
        orphansCountThreshold):
        outlier = True
    return outlier

def isOutlierBitFlipCount(triggerProc):
    outlier = False
    if (len(triggerProc['check_params']['bitflip_gtids']) > \
        bitFlipThreshold):
        outlier = True
    return outlier

def isOutlierMeanEventRate(timeProc):
    outlier = False
    if ((timeProc['check_params']['mean_event_rate'] < minEventRate) or \
        (timeProc['check_params']['mean_event_rate'] > maxEventRate)):
        outlier = True
    return outlier

def initOutliersListFile(firstRun, lastRun):

    # Open outliers list file:
    outliersListFileName = "outliers_%s-%s.txt" % (firstRun, lastRun)
    outliersListFile = open(outliersListFileName, "w")

    # Print list header:
    outliersListFile.write("\n")
    outliersListFile.write("Run no | Length | DQHL P/F |                              Outlier\n")
    outliersListFile.write("-------------------------------------------------------" + \
                           "--------------------------------------------------------\n")
    outliersListFile.write("       |        |   TTRP   | Mean nhit | ESUMH rate | N100L rate |" + \
                           " Orphan count | BitFlip count | Mean ev rate\n")
    outliersListFile.write("       |  (s)   |  (modif) |   > %2i    |    > %2i    |   > %3i    |" % \
                           (meanNhitThreshold, esumhTriggerRateThreshold, \
                            n100lTriggerRateThreshold) + \
                           "    > %4i    |      > %1i      |   < %3i or \n" % \
                           (orphansCountThreshold, bitFlipThreshold, minEventRate))
    outliersListFile.write("       |        |          |           |            |            |" + \
                           "              |               |    > %4i\n" % \
                           (maxEventRate))
    outliersListFile.write("-------------------------------------------------------" + \
                           "--------------------------------------------------------\n")

    return outliersListFile

def processRun(runNumber, data, outliersListFile):

    # Unpack validity range and results:
    run_range = data['run_range']
    checks = data['checks']

    # Unpack results from the four DQ procs:
    triggerProc = checks['dqtriggerproc']
    timeProc = checks['dqtimeproc']
    runProc = checks['dqrunproc']
    pmtProc = checks['dqpmtproc']
    runLength = runProc['check_params']['run_length']
    runPass = ' '
    if runLength < 1800:
        runPass = '!'

    # Print outliers list:
    if (isOutlierNhit(runProc) or \
        isOutlierEsumhTriggerRate(triggerProc) or \
        isOutlierN100lTriggerRate(triggerProc) or \
        isOutlierOrphansCount(triggerProc) or \
        isOutlierBitFlipCount(triggerProc)):
        outliersListFile.write("%s | " % runNumber)
        outliersListFile.write(" %4.0f%s | " % (runLength, runPass))
        outliersListFile.write("  %i%i%i%i   | " % \
                               (modifTriggerProcChecksOK(runNumber, triggerProc), \
                                modifTimeProcChecksOK(runNumber, timeProc), \
                                modifRunProcChecksOK(runNumber, runProc), 
                                pmtProcChecksOK(pmtProc)))
        if isOutlierNhit(runProc):
            outliersListFile.write("%9.2f | " % \
            runProc['check_params']['mean_nhit'])
        else:
            outliersListFile.write("          | ")
        if isOutlierEsumhTriggerRate(triggerProc):
            outliersListFile.write("%10.2f | " % \
            triggerProc['check_params']['esumh_trigger_rate'])
        else:
            outliersListFile.write("           | ")
        if isOutlierN100lTriggerRate(triggerProc):
            outliersListFile.write("%10.2f | " % \
            triggerProc['check_params']['n100l_trigger_rate'])
        else:
            outliersListFile.write("           | ")
        if isOutlierOrphansCount(triggerProc):
            outliersListFile.write("%12i | " % \
            triggerProc['check_params']['orphans_count'])
        else:
            outliersListFile.write("             | ")
        if isOutlierBitFlipCount(triggerProc):
            outliersListFile.write("%13i | " % \
            len(triggerProc['check_params']['bitflip_gtids']))
        else: 
            outliersListFile.write("              | ")
        if isOutlierMeanEventRate(timeProc):
            outliersListFile.write("%12i" % \
            timeProc['check_params']['mean_event_rate'])
        else: 
            outliersListFile.write("             ")
        outliersListFile.write("\n")

    return

def dqhlOutliersList(firstRun, lastRun):

    # Open and initiate outliers-list file:
    outliersListFile = initOutliersListFile(firstRun, lastRun)

    # Open database(s):
    db = couchdb.Server(DB_settings.COUCHDB_SERVER)

    # Loop over run range to extract stats and fill list(s)/histogram(s):
    nRuns = 0
    for runNumber in range(firstRun, lastRun+1):
        # if ((i % 10 == 0) and (i != 0)):
        if ((runNumber % 100 == 0) and (nRuns != 0)):
            outliersListFile.write("- - - -|- - - - | - - - - -|- - - - - -|" + \
                                   "- - - - - - | - - - - - -|" + \
                                   "- - - - - - - | - - - - - - - | - - - - - - -\n")

        # Download DQ ratdb table:
        data = getCouchDBDict(db, runNumber)
        if (data is not None):
            # print "data: ", data
            if isPhysicsRun(data):
                print "Processing DQHL record for run number %i" % runNumber
                processRun(runNumber, data, outliersListFile)
                nRuns += 1
            else:
                print "Run number %i is not a PHYSICS run" % runNumber + \
                      " (although DQHL record was found)"
        else:
            print "No DQHL record found for run number %i" % runNumber

    # Close outliers-list file:
    outliersListFile.close()

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

    print "Running dqhlOutliersList for run range %i-%i" % (firstRun, lastRun)
    dqhlOutliersList(firstRun, lastRun)
    sys.exit(0)

