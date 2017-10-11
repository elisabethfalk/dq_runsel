#!/usr/bin/env python

#==================================================================
# 
# dqhlProcChecks.py
# E. Falk (E.Falk@sussex.ac.uk)
# 2017-05-15 
#
# Library of functions to determine the overall Pass/Fail result, 
# by processor, of the DQHL checks
# 
#==================================================================

# kAmendedMaxEventRate = 1200
kAmendedMaxEventRate = 7000  # Agreed at RS/DQ phone mtg 19/06/2017
kAmendedMaxBitFlipCount = 0
kAmendedMaxRetriggerRate = 15.0
kMinRunLength = 1800

def isPhysicsRun(data):
    physicsRun = False
    if (data):
        checks = data['checks']
        if (('dqtellieproc' not in checks) and \
            ('dqsmellieprocproc' not in checks) and \
            ('dqtriggerproc' in checks) and \
            ('dqtimeproc' in checks) and \
            ('dqrunproc' in checks) and \
            ('dqpmtproc' in checks)):
            physicsRun = True

    return physicsRun

# --- Overall DQHL Pass/Fail:

def dqhlChecksOK(data):
    passChecks = 0
    checks = data['checks']
    if ((triggerProcChecksOK(checks['dqtriggerproc']) == 1) and
        (timeProcChecksOK(checks['dqtimeproc']) == 1) and
        (runProcChecksOK(checks['dqrunproc']) == 1) and
        (pmtProcChecksOK(checks['dqpmtproc']) == 1)):
        passChecks = 1
    return passChecks

def modifDqhlChecksOK(runNumber, data):
    passChecks = 0
    checks = data['checks']
    if ((modifTriggerProcChecksOK(runNumber, checks['dqtriggerproc']) == 1) and
        (modifTimeProcChecksOK(runNumber, checks['dqtimeproc']) == 1) and
        (modifRunProcChecksOK(runNumber, checks['dqrunproc']) == 1) and
        (pmtProcChecksOK(checks['dqpmtproc']) == 1)):
        passChecks = 1
    return passChecks

# ------------------------------------------------------------------------------
# --- From dqtriggerproc: ------------------------------------------------------
# ------------------------------------------------------------------------------

def esumhTriggerRateCheckOK(triggerProc):
    passCheck = 0
    if (triggerProc['esumh_trigger_rate'] == 1):
        passCheck = 1
    return passCheck

def n100lTriggerRateCheckOK(triggerProc):
    passCheck = 0
    if (triggerProc['n100l_trigger_rate'] == 1):
        passCheck = 1
    return passCheck

def modifMissGTIDCheckOK(runNumber, triggerProc):
    passCheck = 0
    if (runNumber >= 101266): 
        if (triggerProc['triggerProcMissingGTID'] == 1): 
            passCheck = 1
    else: # If runNumber < 101266 then ignore check, which doesn't work
        passCheck = 1
    return passCheck

def missGTIDCheckOK(triggerProc):
    passCheck = 0
    if (triggerProc['triggerProcMissingGTID'] == 1):
        passCheck = 1
    return passCheck

def modifBitFlipGTIDCheckOK(triggerProc):
    passCheck = 0
    bitFlipGTIDCount = len(triggerProc['check_params']['bitflip_gtids'])
    if ((bitFlipGTIDCount <= kAmendedMaxBitFlipCount) and
        (bitFlipGTIDCount >= 0)):
        passCheck = 1
    return passCheck

def bitFlipGTIDCheckOK(triggerProc):
    passCheck = 0
    if (triggerProc['triggerProcBitFlipGTID'] == 1):
        passCheck = 1
    return passCheck

# Takes into account changes in check criteria and errors in earlier checks:
def modifTriggerProcChecksOK(runNumber, triggerProc):
    passChecks = 0
    if (n100lTriggerRateCheckOK(triggerProc) and
        esumhTriggerRateCheckOK(triggerProc) and
        modifMissGTIDCheckOK(runNumber, triggerProc) and
        modifBitFlipGTIDCheckOK(triggerProc)):
        passChecks = 1
    return passChecks

# Nominal checks: returns simple pass/fail results from DQ table, 
# whether correct or not
# Incorrect for runs < 101266
def triggerProcChecksOK(triggerProc):
    passChecks = 0
    if (n100lTriggerRateCheckOK(triggerProc) and
        esumhTriggerRateCheckOK(triggerProc) and
        missGTIDCheckOK(triggerProc) and
        bitFlipGTIDCheckOK(triggerProc)):
        passChecks = 1
    return passChecks

# ------------------------------------------------------------------------------
# --- From dqtimeproc: ---------------------------------------------------------
# ------------------------------------------------------------------------------

def modifEventRateCheckOK(timeProc):
    eventRateCheck = timeProc['event_rate']
    if (eventRateCheck == 0):
        minEventRate = timeProc['criteria']['min_event_rate']
        meanEventRate = timeProc['check_params']['mean_event_rate']
        # deltaTEventRate = timeProc['check_params']['delta_t_event_rate']
        if ((meanEventRate <= kAmendedMaxEventRate) and
            (meanEventRate >= minEventRate)):
            eventRateCheck = 1
    return eventRateCheck

def eventRateCheckOK(timeProc):
    passCheck = 0
    if (timeProc['event_rate'] == 1):
        passCheck = 1
    return passCheck

def eventSeparationCheckOK(timeProc):
    passCheck = 0
    if (timeProc['event_separation'] == 1):
        passCheck = 1
    return passCheck

def modifRetriggerCheckOK(timeProc):
    passCheck = 0
    if ((timeProc['retriggers'] == 1) or 
        (('retriggers_value' in timeProc['check_params']) and 
         (timeProc['check_params']['retriggers_value'] \
          <= kAmendedMaxRetriggerRate))):
        passCheck = 1
    return passCheck

def retriggerCheckOK(timeProc):
    passCheck = 0
    if (timeProc['retriggers'] == 1):
        passCheck = 1
    return passCheck

def runHeaderCheckOK(timeProc):
    passCheck = 0
    if (timeProc['run_header'] == 1):
        passCheck = 1
    return passCheck

def tenMhzUTComparisonCheckOK(timeProc):
    passCheck = 0
    if (timeProc['10Mhz_UT_comparrison'] == 1):
        passCheck = 1
    return passCheck

def clockForwardCheckOK(timeProc):
    passCheck = 0
    if (timeProc['clock_forward'] == 1):
        passCheck = 1
    return passCheck

# delta_t_comparison check disused as of 21 May 2017

# Takes into account changes in check criteria and errors in earlier checks:
def testTimeProcChecksOK(runNumber, timeProc):
    passChecks = 0
    if (modifEventRateCheckOK(timeProc) and
        eventSeparationCheckOK(timeProc) and
        modifRetriggerCheckOK(timeProc) and
        runHeaderCheckOK(timeProc) and
        tenMhzUTComparisonCheckOK(timeProc) and
        clockForwardCheckOK(timeProc)):
        passChecks = 1
    return passChecks

# Takes into account changes in check criteria and errors in earlier checks:
def modifTimeProcChecksOK(runNumber, timeProc):
    passChecks = 0
    if (modifEventRateCheckOK(timeProc) and
        eventSeparationCheckOK(timeProc) and
        retriggerCheckOK(timeProc) and
        runHeaderCheckOK(timeProc) and
        tenMhzUTComparisonCheckOK(timeProc) and
        clockForwardCheckOK(timeProc)):
        passChecks = 1
    return passChecks

# Nominal checks: returns simple pass/fail results from DQ table, 
# whether correct or not
# Incorrect for runs < 100600
def timeProcChecksOK(timeProc):
    passChecks = 0
    if (eventRateCheckOK(timeProc) and
        eventSeparationCheckOK(timeProc) and
        retriggerCheckOK(timeProc) and
        runHeaderCheckOK(timeProc) and
        tenMhzUTComparisonCheckOK(timeProc) and
        clockForwardCheckOK(timeProc)):
        passChecks = 1
    return passChecks

# ------------------------------------------------------------------------------
# --- From dqrunproc: ----------------------------------------------------------
# ------------------------------------------------------------------------------

def runLengthCheckOK(runProc):
    passCheck = 0
    runLength = runProc['check_params']['run_length']
    if (runLength >= kMinRunLength):
        passCheck = 1
    return passCheck

# --- From here on in source file: Need to check existing procs, plus
# --- implement individual checks
# --- Also: Edit modifEventRateCheckOK above (shouldn't check just pre-fails)

# Use this version for RS if processing v1 of runs < 100600:
def modifRunProcChecksOK(runNumber, runProc):
    passChecks = 0
    # The correct criteria mask was actually applied only as of 104697:
    if ((runNumber >= 104683) or ((runNumber < 104613) and (runNumber >= 100600))):
        passChecks = runProcChecksOK(runProc)
    # 104613-104682: The trigger mask changed, and the change wasn't reflected in the criteria mask until later:
    # Pre-ca 18 May: Ignore due to bug
    else:
        if ((runProc['run_type'] == 1) and
            # (runProc['mc_flag'] == 1) and
            # (runProc['run_length'] == 1) and        # Ca 18 May 2017: No longer used
            # (runProc['trigger'] == 1)):             # Pre-ca 18 May 2017: Ignore due to bug 
            (runProc['mc_flag'] == 1)):
            passChecks = 1
    return passChecks

# This version is fine for RS for runs 100600 onwards; if processing v1 of earlier runs,
# use modif version:
def runProcChecksOK(runProc):
    passChecks = 0
    if ((runProc['run_type'] == 1) and
        (runProc['mc_flag'] == 1) and
        # (runProc['run_length'] == 1) and            # Ca 18 May 2017: No longer used 
        (runProc['trigger'] == 1)): 
        passChecks = 1
    return passChecks

# ------------------------------------------------------------------------------
# --- From dqpmtproc: ----------------------------------------------------------
# ------------------------------------------------------------------------------

def pmtProcChecksOK(pmtProc):
    passChecks = 0
    if ((pmtProc['general_coverage'] == 1) and
        (pmtProc['crate_coverage'] == 1) and
        (pmtProc['panel_coverage'] == 1)):
        passChecks = 1
    return passChecks

