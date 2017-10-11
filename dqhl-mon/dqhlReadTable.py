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

def processRun(runNumber):

    # Open DQHL ratdb file:
    fileName = "DATAQUALITY_RECORDS_%s.ratdb" % runNumber
    tableFile = open(fileName, "r")
    # Check whether file exists...!!

    # Write DQHL table, in JSON format, to file:
    print "Reading DQHL record for run number %i from file" % runNumber
    data = json.load(tableFile)

    # Close DQHL ratdb file:
    tableFile.close()

    return data

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
        # data = getCouchDBDict(db, runNumber)
        data = processRun(runNumber)
        if (data is not None):
            if isPhysicsRun(data):
                # print "Processing DQHL record for run number %i" % runNumber
                # print "data: ", data
                print
                print "type:        ", data['type']
                print "run_range:   ", data['run_range']
                print "timestamp:   ", data['timestamp']
                print "comment:     ", data['comment']
                print "version:     ", data['version']
                print "pass:        ", data['pass']
                print "production:  ", data['production']
                print "index:       ", data['index']
                print "_id:         ", data['_id']
                print "_rev:        ", data['_rev']

                checks = data['checks']
                print "checks:      "
                print "    status_mask:  ", checks['status_mask']
                print "    applied_mask: ", checks['applied_mask']

                triggerProc = checks['dqtriggerproc']
                print "    dqtriggerproc:"
                print "        n100l_trigger_rate:    ", triggerProc['n100l_trigger_rate']
                print "        esumh_trigger_rate:    ", triggerProc['esumh_trigger_rate']
                print "        triggerProcMissingGTID:", triggerProc['triggerProcMissingGTID']
                print "        triggerProcBitFlipGTID:", triggerProc['triggerProcBitFlipGTID']
                check_params = triggerProc['check_params']
                print "        check_params:          "
                print "            n100l_trigger_rate:    ", check_params['n100l_trigger_rate']
                print "            esumh_trigger_rate:    ", check_params['esumh_trigger_rate']
                print "            orphans_count:         ", check_params['orphans_count']
                print "            no of bitflip_gtids:   ", len(check_params['bitflip_gtids'])
                print "            no of missing_gtids:   ", len(check_params['missing_gtids'])
                criteria = triggerProc['criteria']
                print "        criteria:              "
                print "            min_nhit100l_rate:     ", criteria['min_nhit100l_rate']
                print "            min_esum_hi_rate:      ", criteria['min_esum_hi_rate']
                print "            max_num_missing_gtids: ", criteria['max_num_missing_gtids']
                print "            max_num_bitflip_gtids: ", criteria['max_num_bitflip_gtids']

                timeProc = checks['dqtimeproc']
                print "    dqtimeproc:   "
                print "        event_rate:            ", timeProc['event_rate']
                print "        event_separation:      ", timeProc['event_separation']
                print "        retriggers:            ", timeProc['retriggers']
                print "        run_header:            ", timeProc['run_header']
                print "        10Mhz_UT_comparrison:  ", timeProc['10Mhz_UT_comparrison']
                print "        clock_forward:         ", timeProc['clock_forward']
                check_params = timeProc['check_params']
                print "        check_params:          "
                print "            mean_event_rate:             ", check_params['mean_event_rate']
                print "            delta_t_event_rate:          ", check_params['delta_t_event_rate']
                print "            event_rate_agreement:        ", check_params['event_rate_agreement']
                print "            num_UT_10MhzClock_comp_fails:", check_params['num_UT_10MhzClock_comp_fails']
                if ('retriggers_value' in check_params):
                    print "            retriggers_value:            ", check_params['retriggers_value']
                # print "            non_coincident_count_10_delta_ts:      ", check_params['non_coincident_count_10_delta_ts']
                # print "            non_coincident_universal_time_delta_ts:", check_params['non_coincident_universal_time_delta_ts']
                # print "            coincident_offsets:                    ", check_params['coincident_offsets']
                # print "            count_10_offset:                       ", check_params['count_10_offset']
                # print "            universal_time_offsets:                ", check_params['universal_time_offsets']
                criteria = timeProc['criteria']
                print "        criteria:              "
                print "            min_event_rate:              ", criteria['min_event_rate']
                print "            max_event_rate:              ", criteria['max_event_rate']
                print "            event_separation_thresh:     ", criteria['event_separation_thresh']
                print "            retriggers_thresh:           ", criteria['retriggers_thresh']
                print "            run_header_thresh:           ", criteria['run_header_thresh']
                print "            clock_forward_thresh:        ", criteria['clock_forward_thresh']

                runProc = checks['dqrunproc']
                print "    dqrunproc:    "
                print "        run_type:              ", runProc['run_type']
                print "        mc_flag:               ", runProc['mc_flag']
                print "        trigger:               ", runProc['trigger']
                check_params = runProc['check_params']
                print "        check_params:          "
                print "            mean_nhit:                ", check_params['mean_nhit']
                print "            universal_time_run_length:", check_params['universal_time_run_length']
                print "            count_10_run_length:      ", check_params['count_10_run_length']
                print "            count_50_run_length:      ", check_params['count_50_run_length']
                print "            run_length:               ", check_params['run_length']
                print "            run_length_source:        ", check_params['run_length_source']
                criteria = runProc['criteria']
                print "        criteria:              "
                print "            mc_flag_criteria:         ", criteria['mc_flag_criteria']
                print "            trigger_check_thresh:     ", criteria['trigger_check_thresh']
                print "            trigger_check_criteria:   ", format(criteria['trigger_check_criteria'], '#010x')
                # print "            min_run_length:           ", criteria['min_run_length']

                pmtProc = checks['dqpmtproc']
                print "    dqpmtproc:    "
                print "        general_coverage:      ", pmtProc['general_coverage']
                print "        crate_coverage:        ", pmtProc['crate_coverage']
                print "        panel_coverage:        ", pmtProc['panel_coverage']
                check_params = pmtProc['check_params']
                print "        check_params:          "
                print "            overall_detector_coverage:            ", check_params['overall_detector_coverage']
                print "            crates_failing_coverage:              ", check_params['crates_failing_coverage']
                print "            crates_coverage_percentage:           ", check_params['crates_coverage_percentage']
                print "            number_of_panels_failing_coverage:    ", check_params['number_of_panels_failing_coverage']
                print "            percentage_of_panels_passing_coverage:", check_params['percentage_of_panels_passing_coverage']
                criteria = pmtProc['criteria']
                print "        criteria:              "
                print "            general_cov_thresh:                   ", criteria['general_cov_thresh']
                print "            crate_cov_thresh:                     ", criteria['crate_cov_thresh']
                print "            in_crate_cov_thresh:                  ", criteria['in_crate_cov_thresh']
                print "            panel_cov_thresh:                     ", criteria['panel_cov_thresh']
                print

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

