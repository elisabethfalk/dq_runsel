#!/user/bin/env python

#==================================================================
# 
# dqhlChecksHistograms.py
#
# E. Falk (E.Falk@sussex.ac.uk)
# 2017-05-28
#
# Produces histograms of the various DQHL checks, and of some of
# the parameters monitored by DQHL
# 
#==================================================================

import ROOT
from dqhlProcChecks import *

dqhlChecks = ['n100l_trigger_rate', 'esumh_trigger_rate', \
              'triggerProcMissingGTID', 'triggerProcBitFlipGTID', \
              'event_rate', 'event_separation', 'retriggers', \
#               'event_rate', 'event_separation', \
              'run_header', '10Mhz_UT_comparison', 'clock_forward', \
              'run_type', 'mc_flag', 'trigger', \
              'general_coverage', 'crate_coverage', 'panel_coverage']

#-- Create histograms ---------------------------------------------

#-- Overall Pass/Fails: -----

def createPassFailStatsHistogram(firstRun, lastRun):
    histTitle = "DQHL Pass/Fail stats for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = len(dqhlChecks)
    hStats = ROOT.TH1D("hPassStats", histTitle, nBins, -0.5, nBins-0.5)
    # hStats.GetXaxis().SetTitle("DQHL check")
    hStats.GetYaxis().SetTitle("Pass fraction")
    hStats.GetXaxis().SetBinLabel(dqhlChecks.index('n100l_trigger_rate')+1, 'n100l_trigger_rate')
    hStats.GetXaxis().SetBinLabel(dqhlChecks.index('esumh_trigger_rate')+1, 'esumh_trigger_rate')
    hStats.GetXaxis().SetBinLabel(dqhlChecks.index('triggerProcMissingGTID')+1, 'triggerProcMissingGTID')
    hStats.GetXaxis().SetBinLabel(dqhlChecks.index('triggerProcBitFlipGTID')+1, 'triggerProcBitFlipGTID')
    hStats.GetXaxis().SetBinLabel(dqhlChecks.index('event_rate')+1, 'event_rate')
    hStats.GetXaxis().SetBinLabel(dqhlChecks.index('event_separation')+1, 'event_separation')
    hStats.GetXaxis().SetBinLabel(dqhlChecks.index('retriggers')+1, 'retriggers')
    hStats.GetXaxis().SetBinLabel(dqhlChecks.index('run_header')+1, 'run_header')
    hStats.GetXaxis().SetBinLabel(dqhlChecks.index('10Mhz_UT_comparison')+1, '10Mhz_UT_comparison')
    hStats.GetXaxis().SetBinLabel(dqhlChecks.index('clock_forward')+1, 'clock_forward')
    # hStats.GetXaxis().SetBinLabel(dqhlChecks.index('delta_t_comparison')+1, 'delta_t_comparison')
    hStats.GetXaxis().SetBinLabel(dqhlChecks.index('run_type')+1, 'run_type')
    hStats.GetXaxis().SetBinLabel(dqhlChecks.index('mc_flag')+1, 'mc_flag')
    # hStats.GetXaxis().SetBinLabel(dqhlChecks.index('run_length')+1, 'run_length')
    hStats.GetXaxis().SetBinLabel(dqhlChecks.index('trigger')+1, 'trigger')
    hStats.GetXaxis().SetBinLabel(dqhlChecks.index('general_coverage')+1, 'general_coverage')
    hStats.GetXaxis().SetBinLabel(dqhlChecks.index('crate_coverage')+1, 'crate_coverage')
    hStats.GetXaxis().SetBinLabel(dqhlChecks.index('panel_coverage')+1, 'panel_coverage')

    return hStats

#-- From DQTriggerProc: -----

def createEsumhRateHistogram(firstRun, lastRun):
    histTitle = "DQHL ESUMH trigger rate for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hEsumhRate = ROOT.TH1D("hDQHLEsumhRate", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hEsumhRate.GetYaxis().SetTitle("ESUMH trigger rate (Hz)")
    hEsumhRate.GetXaxis().SetTitle("Run number")
    hEsumhRate.SetMarkerStyle(7) # 7 = kFullDotMedium
    hEsumhRate.SetMarkerColor(4)

    return hEsumhRate

def createN100lRateHistogram(firstRun, lastRun):
    histTitle = "DQHL N100L trigger rate for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hN100lRate = ROOT.TH1D("hDQHLN100lRate", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hN100lRate.GetYaxis().SetTitle("N100L trigger rate (Hz)")
    hN100lRate.GetXaxis().SetTitle("Run number")
    hN100lRate.SetMarkerStyle(7) # 7 = kFullDotMedium
    hN100lRate.SetMarkerColor(4)

    return hN100lRate

def createOrphansCountHistogram(firstRun, lastRun):
    histTitle = "DQHL Number of orphans for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hOrphans = ROOT.TH1D("hDQHLOrphans", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hOrphans.GetYaxis().SetTitle("Number of orphans")
    hOrphans.GetXaxis().SetTitle("Run number")
    hOrphans.SetMarkerStyle(7) # 7 = kFullDotMedium
    hOrphans.SetMarkerColor(4)

    return hOrphans

def createMissingGTIDHistogram(firstRun, lastRun):
    histTitle = "DQHL Number of missing GTIDs for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hMissGTIDs = ROOT.TH1D("hDQHLMissGTIDs", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hMissGTIDs.GetYaxis().SetTitle("Number of missing GTIDs")
    hMissGTIDs.GetXaxis().SetTitle("Run number")
    hMissGTIDs.SetMarkerStyle(7) # 7 = kFullDotMedium
    hMissGTIDs.SetMarkerColor(4)

    return hMissGTIDs

def createBitFlipGTIDHistogram(firstRun, lastRun):
    histTitle = "DQHL Number of bitflip GTIDs for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hBitFlipGTIDs = ROOT.TH1D("hDQHLBitFlipGTIDs", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hBitFlipGTIDs.GetYaxis().SetTitle("Number of bitflip GTIDs")
    hBitFlipGTIDs.GetXaxis().SetTitle("Run number")
    hBitFlipGTIDs.SetMarkerStyle(7) # 7 = kFullDotMedium
    hBitFlipGTIDs.SetMarkerColor(4)

    return hBitFlipGTIDs

#-- From DQTimeProc: -----

def createAverageEventRateHistogram(firstRun, lastRun):
    histTitle = "DQHL Event rate (average) for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hAvgEvRate = ROOT.TH1D("hDQHLAvgEvRate", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hAvgEvRate.GetYaxis().SetTitle("Event rate (Hz)")
    hAvgEvRate.GetXaxis().SetTitle("Run number")
    hAvgEvRate.SetMarkerStyle(7) # 7 = kFullDotMedium
    hAvgEvRate.SetMarkerColor(4)

    return hAvgEvRate

def createDeltaTEventRateHistogram(firstRun, lastRun):
    histTitle = "DQHL Event rate (delta T) for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hDelTEvRate = ROOT.TH1D("hDQHLDeltaTEvRate", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hDelTEvRate.GetYaxis().SetTitle("Event rate (Hz)")
    hDelTEvRate.GetXaxis().SetTitle("Run number")
    hDelTEvRate.SetMarkerStyle(7) # 7 = kFullDotMedium
    hDelTEvRate.SetMarkerColor(2)

    return hDelTEvRate

def createEventRateAgreementHistogram(firstRun, lastRun):
    histTitle = "DQHL Event rate agreement for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hEvRateAgr = ROOT.TH1D("hDQHLEvRateAgreement", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hEvRateAgr.GetYaxis().SetTitle("Event rate agreement (Hz)")
    hEvRateAgr.GetXaxis().SetTitle("Run number")
    hEvRateAgr.SetMarkerStyle(7) # 7 = kFullDotMedium
    hEvRateAgr.SetMarkerColor(4)

    return hEvRateAgr

def createRetriggerPercentageHistogram(firstRun, lastRun):
    histTitle = "DQHL Retriggers as percentage of total number of events for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hRetrigPercentage = ROOT.TH1D("hRetrig", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hRetrigPercentage.GetYaxis().SetTitle("Percentage")
    hRetrigPercentage.GetXaxis().SetTitle("Run number")
    hRetrigPercentage.SetMarkerStyle(7) # 7 = kFullDotMedium
    hRetrigPercentage.SetMarkerColor(2)

    return hRetrigPercentage

def createRetriggerPercentageDistributionHistogram(firstRun, lastRun):
    histTitle = "DQHL Retriggers as percentage of total number of events for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = 101
    hRetrigPercentageDistribution = ROOT.TH1D("hRetrigDistr", histTitle, nBins, -0.5, 100.5)
    hRetrigPercentageDistribution.GetYaxis().SetTitle("No of runs")
    hRetrigPercentageDistribution.GetXaxis().SetTitle("Percentage")
    hRetrigPercentageDistribution.SetMarkerColor(2)

    return hRetrigPercentageDistribution

def createRetriggerPercentagePassDqhlHistogram(firstRun, lastRun):
    histTitle = "DQHL Retriggers as percentage of total number of events for Physics runs %i-%i that pass all other DQHL cuts" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hRetrigPercentagePassDqhl = ROOT.TH1D("hRetrigPassDqhl", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hRetrigPercentagePassDqhl.GetYaxis().SetTitle("Percentage")
    hRetrigPercentagePassDqhl.GetXaxis().SetTitle("Run number")
    hRetrigPercentagePassDqhl.SetMarkerStyle(7) # 7 = kFullDotMedium
    hRetrigPercentagePassDqhl.SetMarkerColor(2)

    return hRetrigPercentagePassDqhl

def createRetriggerPercentagePassDqhlDistributionHistogram(firstRun, lastRun):
    histTitle = "DQHL Retriggers as percentage of total number of events for Physics runs %i-%i that pass all other DQHL cuts" % (firstRun, lastRun)
    nBins = 101
    hRetrigPercentagePassDqhlDistribution = ROOT.TH1D("hRetrigPassDqhlDistr", histTitle, nBins, -0.5, 100.5)
    hRetrigPercentagePassDqhlDistribution.GetYaxis().SetTitle("No of runs")
    hRetrigPercentagePassDqhlDistribution.GetXaxis().SetTitle("Percentage")
    hRetrigPercentagePassDqhlDistribution.SetMarkerColor(2)

    return hRetrigPercentagePassDqhlDistribution

def createRetriggerPercentagePassDqhlAndRunLengthHistogram(firstRun, lastRun):
    histTitle = "DQHL Retriggers as percentage of total number of events for Physics runs %i-%i that pass all other DQHL cuts + run length" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hRetrigPercentagePassDqhlAndRunLength = ROOT.TH1D("hRetrigPassDqhlRunLen", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hRetrigPercentagePassDqhlAndRunLength.GetYaxis().SetTitle("Percentage")
    hRetrigPercentagePassDqhlAndRunLength.GetXaxis().SetTitle("Run number")
    hRetrigPercentagePassDqhlAndRunLength.SetMarkerStyle(7) # 7 = kFullDotMedium
    hRetrigPercentagePassDqhlAndRunLength.SetMarkerColor(2)

    return hRetrigPercentagePassDqhlAndRunLength

def createRetriggerPercentagePassDqhlAndRunLengthDistributionHistogram(firstRun, lastRun):
    histTitle = "DQHL Retriggers as percentage of total number of events for Physics runs %i-%i that pass all other DQHL cuts + run length" % (firstRun, lastRun)
    nBins = 101
    hRetrigPercentagePassDqhlAndRunLengthDistribution = ROOT.TH1D("hRetrigPassDqhlRunLenDistr", histTitle, nBins, -0.5, 100.5)
    hRetrigPercentagePassDqhlAndRunLengthDistribution.GetYaxis().SetTitle("No of runs")
    hRetrigPercentagePassDqhlAndRunLengthDistribution.GetXaxis().SetTitle("Percentage")
    hRetrigPercentagePassDqhlAndRunLengthDistribution.SetMarkerColor(2)

    return hRetrigPercentagePassDqhlAndRunLengthDistribution

def createRetriggerPercentagePassAllExceptRetriggerHistogram(firstRun, lastRun):
    histTitle = "DQHL Retriggers as percentage of total number of events for Physics runs %i-%i that pass all other RS cuts" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hRetrigPercentagePassAllExceptRetrigger = ROOT.TH1D("hRetrigPassAllOth", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hRetrigPercentagePassAllExceptRetrigger.GetYaxis().SetTitle("Percentage")
    hRetrigPercentagePassAllExceptRetrigger.GetXaxis().SetTitle("Run number")
    hRetrigPercentagePassAllExceptRetrigger.SetMarkerStyle(7) # 7 = kFullDotMedium
    hRetrigPercentagePassAllExceptRetrigger.SetMarkerColor(2)

    return hRetrigPercentagePassAllExceptRetrigger

def createRetriggerPercentagePassAllExceptRetriggerDistributionHistogram(firstRun, lastRun):
    histTitle = "DQHL Retriggers as percentage of total number of events for Physics runs %i-%i that pass all other RS cuts" % (firstRun, lastRun)
    nBins = 101
    hRetrigPercentagePassAllExceptRetriggerDistribution = ROOT.TH1D("hRetrigPassAllOthDistr", histTitle, nBins, -0.5, 100.5)
    hRetrigPercentagePassAllExceptRetriggerDistribution.GetYaxis().SetTitle("No of runs")
    hRetrigPercentagePassAllExceptRetriggerDistribution.GetXaxis().SetTitle("Percentage")
    hRetrigPercentagePassAllExceptRetriggerDistribution.SetMarkerColor(2)

    return hRetrigPercentagePassAllExceptRetriggerDistribution

#-- From DQRunProc: -----

def createMeanNhitsHistogram(firstRun, lastRun):
    histTitle = "DQHL Mean NHits Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hMeanNhits = ROOT.TH1D("hDQHLMeanNhits", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hMeanNhits.GetYaxis().SetTitle("Mean NHits")
    hMeanNhits.GetXaxis().SetTitle("Run number")
    hMeanNhits.SetMarkerStyle(7) # 7 = kFullDotMedium
    hMeanNhits.SetMarkerColor(4)

    return hMeanNhits

#-- From DQPmtProc: -----

def createGeneralCoverageHistogram(firstRun, lastRun):
    histTitle = "DQHL Overall PMT coverage for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hGeneralCov = ROOT.TH1D("hDQHLGeneralCoverage", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hGeneralCov.GetYaxis().SetTitle("Overall detector coverage (%)")
    hGeneralCov.GetXaxis().SetTitle("Run number")
    hGeneralCov.SetMarkerStyle(7) # 7 = kFullDotMedium
    hGeneralCov.SetMarkerColor(4)

    return hGeneralCov

def createCrateCoverageHistogram(firstRun, lastRun):
    histTitle = "DQHL Crate coverage for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hCrateCov = ROOT.TH1D("hDQHLCrateCoverage", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hCrateCov.GetYaxis().SetTitle("Crate coverage (%)")
    hCrateCov.GetXaxis().SetTitle("Run number")
    hCrateCov.SetMarkerStyle(7) # 7 = kFullDotMedium
    hCrateCov.SetMarkerColor(2)

    return hCrateCov

def createPanelCoverageHistogram(firstRun, lastRun):
    histTitle = "DQHL Panel coverage for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hPanelCov = ROOT.TH1D("hDQHLPanelCoverage", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hPanelCov.GetYaxis().SetTitle("Panel coverage (%)")
    hPanelCov.GetXaxis().SetTitle("Run number")
    hPanelCov.SetMarkerStyle(7) # 7 = kFullDotMedium
    hPanelCov.SetMarkerColor(8)

    return hPanelCov

def createNumPanelFailsHistogram(firstRun, lastRun):
    histTitle = "DQHL Number of panels failing coverage for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hPanelFails = ROOT.TH1D("hDQHLNumPanelFails", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hPanelFails.GetYaxis().SetTitle("Number of panels")
    hPanelFails.GetXaxis().SetTitle("Run number")
    hPanelFails.SetMarkerStyle(7) # 7 = kFullDotMedium
    hPanelFails.SetMarkerColor(8)

    return hPanelFails

#-- Create all histograms and store in a list/dict ----------------

def createHistograms(firstRun, lastRun):
    hist = {}
#    ROOT.gStyle.SetOptStat(0)

    # Overall Pass/Fail histogram(s):
    hist['hStats'] = createPassFailStatsHistogram(firstRun, lastRun)
    hist['hStatsModif'] = createPassFailStatsHistogram(firstRun, lastRun)

    # From Trigger proc:
    # *** Done ***
    # Pass/fails: esumh_trigger_rate, n100l_trigger_rate, triggerProcMissingGTID, triggerProcBitFlipGTID, 
    # check_params: *esumh_trigger_rate, *n100l_trigger_rate, 
    #               *missing_gtids (list), *bitflip_gtids (list), *orphans_count (list)
    # criteria: min_esum_hi_rate (5), min_nhit100l_rate (5), 
    #           max_num_missing_gtids (20 --> 0), max_num_bitflip_gtids (20 --> 0)
    hist['hEsumhRate'] = createEsumhRateHistogram(firstRun, lastRun)
    hist['hN100lRate'] = createN100lRateHistogram(firstRun, lastRun)
    hist['hOrphans'] = createOrphansCountHistogram(firstRun, lastRun)
    hist['hMissGTIDs'] = createMissingGTIDHistogram(firstRun, lastRun)
    hist['hBitFlipGTIDs'] = createBitFlipGTIDHistogram(firstRun, lastRun)

    # From TimeProc:
    # Pass/fails: event_rate, event_separation, retriggers, 
    #             10Mhz_UT_comparrison, delta_t_comparison, clock_forward, run_header 
    # check_params: *event_rate_agreement, -num_UT_10MhzClock_comp_fails, *mean_event_rate, *delta_t_event_rate
    #               --- The following are added if the check is failed: ---
    #               run_header (first event time), clock_forward_value, event_separation_value, retriggers_value,
    #               min_event_rate (= criterion), max_event_rate (= criterion)
    #               --- The following were present before run 101265: ---
    #               count_10_offset, non_coincident_count_10_delta_ts, non_coincident_universal_time_delta_ts, 
    #               coincident_offsets, universal_time_offsets
    # criteria: retriggers_thresh (10), run_header_thresh (1000000000), 
    #           min_event_rate (5), max_event_rate (1000), clock_forward_thresh (99), event_separation_thresh (1)
    hist['hAvgEvRate'] = createAverageEventRateHistogram(firstRun, lastRun)
    hist['hDelTEvRate'] = createDeltaTEventRateHistogram(firstRun, lastRun)
    hist['hEvRateAgr'] = createEventRateAgreementHistogram(firstRun, lastRun)
#    hist['hRetrigRate'] = createRunHeaderFailsHistogram(firstRun, lastRun) # First event time in ns
#    hist['hRetrigRate'] = createClockForwardFailsHistogram(firstRun, lastRun)
#    hist['hRetrigRate'] = createEventSeparationFailsHistogram(firstRun, lastRun)
    hist['hRetrigPercentage'] = createRetriggerPercentageHistogram(firstRun, lastRun)
    hist['hRetrigPercentageDistribution'] = createRetriggerPercentageDistributionHistogram(firstRun, lastRun)
    hist['hRetrigPercentagePassDqhl'] = createRetriggerPercentagePassDqhlHistogram(firstRun, lastRun) 
    hist['hRetrigPercentagePassDqhlDistribution'] = createRetriggerPercentagePassDqhlDistributionHistogram(firstRun, lastRun)
    hist['hRetrigPercentagePassDqhlAndRunLength'] = createRetriggerPercentagePassDqhlAndRunLengthHistogram(firstRun, lastRun)
    hist['hRetrigPercentagePassDqhlAndRunLengthDistribution'] = createRetriggerPercentagePassDqhlAndRunLengthDistributionHistogram(firstRun, lastRun)
    hist['hRetrigPercentagePassAllExceptRetrigger'] = createRetriggerPercentagePassAllExceptRetriggerHistogram(firstRun, lastRun)
    hist['hRetrigPercentagePassAllExceptRetriggerDistribution'] = createRetriggerPercentagePassAllExceptRetriggerDistributionHistogram(firstRun, lastRun)
    # Clock comparison fails are best listed

    # From RunProc:
    # Pass/fails: run_type, mc_flag, run_length, trigger
    # check_params: universal_time_run_length, count_50_run_length, count_10_run_length, 
    #               *mean_nhit, run_length, run_length_source (count_10)
    # criteria: trigger_check_thresh (90), mc_flag_criteria (0), trigger_check_criteria (26326), 
    #           min_run_length (1800) 
    hist['hMeanNhits'] = createMeanNhitsHistogram(firstRun, lastRun)
    # Run type, MC flag and trigger mask probably best counted, and runs & values listed
    # Could check agreement between the different run length calculations

    # From PMT proc:
    # *** Plots done; one parameter to list ***
    # Pass/fails: general_coverage, crate_coverage, panel_coverage
    # check_params: *overall_detector_coverage, crates_failing_coverage, *crates_coverage_percentage, 
    #               *number_of_panels_failing_coverage, *percentage_of_panels_passing_coverage, 
    # criteria: general_cov_thresh (70), panel_cov_thresh (80), crate_cov_thresh (100), in_crate_cov_thresh (50)
    hist['hGeneralCov'] = createGeneralCoverageHistogram(firstRun, lastRun) # 70%
    hist['hCrateCov'] = createCrateCoverageHistogram(firstRun, lastRun) # 100%, with 50% in crate
    hist['hPanelCov'] = createPanelCoverageHistogram(firstRun, lastRun) # 80%
    hist['hPanelFails'] = createNumPanelFailsHistogram(firstRun, lastRun)
    # Runs with no of crates failing coverage may be best listed 

    return hist

#-- Fill histograms -----------------------------------------------

def fillHistograms(runNumber, data, hist):
    # Unpack validity range and results:
    run_range = data['run_range']
    checks = data['checks']

    # Unpack results from the four DQ procs:
    triggerProc = checks['dqtriggerproc']
    timeProc = checks['dqtimeproc']
    runProc = checks['dqrunproc']
    pmtProc = checks['dqpmtproc']

    # Get pass results by processor:
    triggerProcOK = triggerProcChecksOK(triggerProc)
    modifTriggerProcOK = modifTriggerProcChecksOK(runNumber, triggerProc)
    timeProcOK = timeProcChecksOK(timeProc)
    modifTimeProcOK = modifTimeProcChecksOK(runNumber, timeProc)
    runProcOK = runProcChecksOK(runProc)
    modifRunProcOK = modifRunProcChecksOK(runNumber, runProc)
    pmtProcOK = pmtProcChecksOK(pmtProc)

    # Fill Pass/Fail histograms: 
    hStats = hist['hStats']
    hStatsModif = hist['hStatsModif']
    if (triggerProc['n100l_trigger_rate']):
        hStats.Fill(dqhlChecks.index('n100l_trigger_rate'))
        hStatsModif.Fill(dqhlChecks.index('n100l_trigger_rate'))
    if (triggerProc['esumh_trigger_rate']):
        hStats.Fill(dqhlChecks.index('esumh_trigger_rate'))
        hStatsModif.Fill(dqhlChecks.index('esumh_trigger_rate'))
    if (triggerProc['triggerProcMissingGTID']):
        hStats.Fill(dqhlChecks.index('triggerProcMissingGTID'))
    if (runNumber >= 101266):
        if (triggerProc['triggerProcMissingGTID']):
            hStatsModif.Fill(dqhlChecks.index('triggerProcMissingGTID'))
    else:
        hStatsModif.Fill(dqhlChecks.index('triggerProcMissingGTID'))
    if (triggerProc['triggerProcBitFlipGTID']):
        hStats.Fill(dqhlChecks.index('triggerProcBitFlipGTID'))
    if (modifBitFlipGTIDCheckOK(triggerProc)):
        hStatsModif.Fill(dqhlChecks.index('triggerProcBitFlipGTID'))
    if (timeProc['event_rate']):
        hStats.Fill(dqhlChecks.index('event_rate'))
    if (modifEventRateCheckOK(timeProc)):
        hStatsModif.Fill(dqhlChecks.index('event_rate'))
    if (timeProc['event_separation']):
        hStats.Fill(dqhlChecks.index('event_separation'))
        hStatsModif.Fill(dqhlChecks.index('event_separation'))
    if (timeProc['retriggers']):
        hStats.Fill(dqhlChecks.index('retriggers'))
        hStatsModif.Fill(dqhlChecks.index('retriggers'))
    if (timeProc['run_header']):
        hStats.Fill(dqhlChecks.index('run_header'))
        hStatsModif.Fill(dqhlChecks.index('run_header'))
    if (timeProc['10Mhz_UT_comparrison']):
        hStats.Fill(dqhlChecks.index('10Mhz_UT_comparison'))
        hStatsModif.Fill(dqhlChecks.index('10Mhz_UT_comparison'))
    if (timeProc['clock_forward']):
        hStats.Fill(dqhlChecks.index('clock_forward'))
        hStatsModif.Fill(dqhlChecks.index('clock_forward'))
    # if (timeProc['delta_t_comparison']):     # No longer used
    #     hStats.Fill(dqhlChecks.index('delta_t_comparison'))
    if (runProc['run_type']):
        hStats.Fill(dqhlChecks.index('run_type'))
        hStatsModif.Fill(dqhlChecks.index('run_type'))
    if (runProc['mc_flag']):
        hStats.Fill(dqhlChecks.index('mc_flag'))
        hStatsModif.Fill(dqhlChecks.index('mc_flag'))
    # if (runProc['run_length']):              # No longer used
    #     hStats.Fill(dqhlChecks.index('run_length'))
    if (runProc['trigger']): 
        hStats.Fill(dqhlChecks.index('trigger'))
    if (runNumber >= 100600):
        if (runProc['trigger']):
            hStatsModif.Fill(dqhlChecks.index('trigger'))
    else:
        hStatsModif.Fill(dqhlChecks.index('trigger'))
    if (pmtProc['general_coverage']):
        hStats.Fill(dqhlChecks.index('general_coverage'))
        hStatsModif.Fill(dqhlChecks.index('general_coverage'))
    if (pmtProc['crate_coverage']):
        hStats.Fill(dqhlChecks.index('crate_coverage'))
        hStatsModif.Fill(dqhlChecks.index('crate_coverage'))
    if (pmtProc['panel_coverage']):
        hStats.Fill(dqhlChecks.index('panel_coverage'))
        hStatsModif.Fill(dqhlChecks.index('panel_coverage'))

    # Fill Trigger Processor histograms: 
    hist['hEsumhRate'].Fill(runNumber, triggerProc['check_params']['esumh_trigger_rate'])
    hist['hN100lRate'].Fill(runNumber, triggerProc['check_params']['n100l_trigger_rate'])
    hist['hOrphans'].Fill(runNumber, triggerProc['check_params']['orphans_count'])
    hist['hMissGTIDs'].Fill(runNumber, len(triggerProc['check_params']['missing_gtids']))
    hist['hBitFlipGTIDs'].Fill(runNumber, len(triggerProc['check_params']['bitflip_gtids']))

    # Fill Time Processor histograms: 
    hist['hAvgEvRate'].Fill(runNumber, timeProc['check_params']['mean_event_rate'])
    hist['hDelTEvRate'].Fill(runNumber, timeProc['check_params']['delta_t_event_rate'])
    hist['hEvRateAgr'].Fill(runNumber, abs(timeProc['check_params']['event_rate_agreement']))
    retrigFailOtherRSCuts = [100696, 100926, 100974, 100985, 101020, 101024, 101027, 101183, 101473, 101493, \
                             101494, 102059, 102072, 102094, 102109, 102111, 102347, 104413, 104441, 104478, \
                             104495, 104496, 104497, 104500, 104501, 104642]
    if ('retriggers_value' in timeProc['check_params']):
        hist['hRetrigPercentage'].Fill(runNumber, timeProc['check_params']['retriggers_value'])
        hist['hRetrigPercentageDistribution'].Fill(timeProc['check_params']['retriggers_value'])
        if (modifTriggerProcOK and modifRunProcOK and pmtProcOK and \
            modifEventRateCheckOK and timeProc['event_separation'] and timeProc['run_header'] and \
            timeProc['10Mhz_UT_comparrison'] and timeProc['clock_forward']):
            hist['hRetrigPercentagePassDqhl'].Fill(runNumber, timeProc['check_params']['retriggers_value'])
            hist['hRetrigPercentagePassDqhlDistribution'].Fill(timeProc['check_params']['retriggers_value'])
            if (runProc['check_params']['run_length'] > 1800):
                hist['hRetrigPercentagePassDqhlAndRunLength'].Fill(runNumber, timeProc['check_params']['retriggers_value'])
                hist['hRetrigPercentagePassDqhlAndRunLengthDistribution'].Fill(timeProc['check_params']['retriggers_value'])
                if (runNumber not in retrigFailOtherRSCuts):
                    hist['hRetrigPercentagePassAllExceptRetrigger'].Fill(runNumber, timeProc['check_params']['retriggers_value'])
                    hist['hRetrigPercentagePassAllExceptRetriggerDistribution'].Fill(timeProc['check_params']['retriggers_value'])
    
    # Fill Run Processor histograms: 
    hist['hMeanNhits'].Fill(runNumber, runProc['check_params']['mean_nhit'])

    # Fill PMT Processor histograms:
    hist['hGeneralCov'].Fill(runNumber, pmtProc['check_params']['overall_detector_coverage'])
    hist['hCrateCov'].Fill(runNumber, pmtProc['check_params']['crates_coverage_percentage'])
    hist['hPanelCov'].Fill(runNumber, pmtProc['check_params']['percentage_of_panels_passing_coverage'])
    hist['hPanelFails'].Fill(runNumber, pmtProc['check_params']['number_of_panels_failing_coverage'])

    return

#-- Write histograms to file --------------------------------------
def writeHistograms(firstRun, lastRun, nRuns, hist):
    filename = "dqhlHistos_%s_%s.root" % (firstRun, lastRun)
    f = ROOT.TFile(filename, 'recreate')
    for key in hist:
        hist[key].Write()
    f.Close()

    return

#-- Draw histograms -----------------------------------------------

def drawHistograms(firstRun, lastRun, nRuns, hist):
    # Scale histogram to get fractional pass rates:
    # print "No of physics runs with DQHL data processed: %i" % nRuns
    if (nRuns > 0):
        hist['hStats'].Scale(1./nRuns)
        hist['hStatsModif'].Scale(1./nRuns)

    # Create canvas and draw histograms
    ROOT.gROOT.SetBatch(ROOT.kTRUE)
    c1 = ROOT.TCanvas()

    # Pass/Fail histogram: 
    ROOT.gPad.SetLogy(0)
    hist['hStats'].Draw()
    hist['hStats'].SetMaximum(1.1)
    hist['hStats'].SetMinimum(0.0)
    c1.Print(("DQHL_pass_fail_stats_%i-%i.png" % (firstRun, lastRun)))
    ROOT.gPad.SetLogy(0)
    hist['hStatsModif'].Draw()
    hist['hStatsModif'].SetMaximum(1.1)
    hist['hStatsModif'].SetMinimum(0.0)
    c1.Print(("DQHL_pass_fail_stats_modif_%i-%i.png" % (firstRun, lastRun)))

    # From Trigger Processor: ----------
    # ESUMH rate:
    ROOT.gPad.SetLogy()
    hist['hEsumhRate'].Draw("P")
    c1.Print(("DQHL_esumh_trigger_rate_log_%i-%i.png" % (firstRun, lastRun)))
    ROOT.gPad.SetLogy(0)
    hist['hEsumhRate'].Draw("P")
    hist['hEsumhRate'].SetMaximum(100.)
    c1.Print(("DQHL_esumh_trigger_rate_lin_%i-%i.png" % (firstRun, lastRun)))

    # N100L rate:
    ROOT.gPad.SetLogy()
    hist['hN100lRate'].Draw("P")
    c1.Print(("DQHL_n100l_trigger_rate_log_%i-%i.png" % (firstRun, lastRun)))
    ROOT.gPad.SetLogy(0)
    hist['hN100lRate'].Draw("P")
    hist['hN100lRate'].SetMaximum(300.)
    c1.Print(("DQHL_n100l_trigger_rate_lin_%i-%i.png" % (firstRun, lastRun)))

    # Orphans:
    ROOT.gPad.SetLogy()
    hist['hOrphans'].Draw("P")
    c1.Print(("DQHL_orphans_count_%i-%i.png" % (firstRun, lastRun)))

    # Missing GTIDs:
    ROOT.gPad.SetLogy()
    hist['hMissGTIDs'].Draw("P")
    c1.Print(("DQHL_missing_gtids_log_%i-%i.png" % (firstRun, lastRun)))
    ROOT.gPad.SetLogy(0)
    hist['hMissGTIDs'].Draw("P")
    c1.Print(("DQHL_missing_gtids_lin_%i-%i.png" % (firstRun, lastRun)))

    # BitFlip GTIDs:
    ROOT.gPad.SetLogy()
    hist['hBitFlipGTIDs'].Draw("P")
    c1.Print(("DQHL_bitflip_gtids_log_%i-%i.png" % (firstRun, lastRun)))
    ROOT.gPad.SetLogy(0)
    hist['hBitFlipGTIDs'].Draw("P")
    c1.Print(("DQHL_bitflip_gtids_lin_%i-%i.png" % (firstRun, lastRun)))

    # From Time Processor: ---------- 
    # Average event rate:
    ROOT.gPad.SetLogy()
    hist['hAvgEvRate'].Draw("P")
    c1.Print(("DQHL_avg_event_rate_log_%i-%i.png" % (firstRun, lastRun)))
    ROOT.gPad.SetLogy(0)
    hist['hAvgEvRate'].Draw("P")
    hist['hAvgEvRate'].SetMaximum(3000.)
    c1.Print(("DQHL_avg_event_rate_lin_%i-%i.png" % (firstRun, lastRun)))

    # Delta T event rate:
    ROOT.gPad.SetLogy()
    hist['hDelTEvRate'].Draw("P")
    c1.Print(("DQHL_delta_t_event_rate_log_%i-%i.png" % (firstRun, lastRun)))
    ROOT.gPad.SetLogy(0)
    hist['hDelTEvRate'].Draw("P")
    hist['hDelTEvRate'].SetMaximum(3000.)
    c1.Print(("DQHL_delta_t_event_rate_lin_%i-%i.png" % (firstRun, lastRun)))

    # Event rate agreement:
    ROOT.gPad.SetLogy()
    hist['hEvRateAgr'].Draw("P")
    c1.Print(("DQHL_event_rate_agreement_log_%i-%i.png" % (firstRun, lastRun)))
    ROOT.gPad.SetLogy(0)
    hist['hEvRateAgr'].Draw("P")
    hist['hEvRateAgr'].SetMaximum(10.)
    c1.Print(("DQHL_event_rate_agreement_lin_%i-%i.png" % (firstRun, lastRun)))

    # Retrigger percentage:
    ROOT.gPad.SetLogy()
    hist['hRetrigPercentage'].Draw("P")
    c1.Print(("DQHL_retrigger_percentage_log_%i-%i.png" % (firstRun, lastRun)))
    ROOT.gPad.SetLogy(0)
    hist['hRetrigPercentage'].Draw("P")
    hist['hRetrigPercentage'].SetMaximum(100.)
    c1.Print(("DQHL_retrigger_percentage_lin_%i-%i.png" % (firstRun, lastRun)))

    # Retrigger percentage distribution:
    ROOT.gPad.SetLogy(0)
    hist['hRetrigPercentageDistribution'].Draw()
    c1.Print(("DQHL_retrigger_percentage_distribution_lin_%i-%i.png" % (firstRun, lastRun)))

    # Retrigger percentage for runs passing all other DQHL cuts:
    ROOT.gPad.SetLogy()
    hist['hRetrigPercentagePassDqhl'].Draw("P")
    c1.Print(("DQHL_retrigger_percentage_pass_dqhl_log_%i-%i.png" % (firstRun, lastRun)))
    ROOT.gPad.SetLogy(0)
    hist['hRetrigPercentagePassDqhl'].Draw("P")
    hist['hRetrigPercentagePassDqhl'].SetMaximum(100.)
    c1.Print(("DQHL_retrigger_percentage_pass_dqhl_lin_%i-%i.png" % (firstRun, lastRun)))

    # Retrigger percentage distribution for runs passing all other DQHL cuts:
    ROOT.gPad.SetLogy(0)
    hist['hRetrigPercentagePassDqhlDistribution'].Draw()
    c1.Print(("DQHL_retrigger_percentage_pass_dqhl_distribution_lin_%i-%i.png" % (firstRun, lastRun)))

    # Retrigger percentage for runs passing all other DQHL cuts as well as run length:
    ROOT.gPad.SetLogy()
    hist['hRetrigPercentagePassDqhlAndRunLength'].Draw("P")
    c1.Print(("DQHL_retrigger_percentage_pass_dqhl_and_runlength_log_%i-%i.png" % (firstRun, lastRun)))
    ROOT.gPad.SetLogy(0)
    hist['hRetrigPercentagePassDqhlAndRunLength'].Draw("P")
    hist['hRetrigPercentagePassDqhlAndRunLength'].SetMaximum(100.)
    c1.Print(("DQHL_retrigger_percentage_pass_dqhl_and_runlength_lin_%i-%i.png" % (firstRun, lastRun)))

    # Retrigger percentage distribution for runs passing all other DQHL cuts as well as run length:
    ROOT.gPad.SetLogy(0)
    hist['hRetrigPercentagePassDqhlAndRunLengthDistribution'].Draw()
    c1.Print(("DQHL_retrigger_percentage_pass_dqhl_and_runlength_distribution_lin_%i-%i.png" % (firstRun, lastRun)))

    # Retrigger percentage for runs passing all other RS cuts:
    ROOT.gPad.SetLogy()
    hist['hRetrigPercentagePassAllExceptRetrigger'].Draw("P")
    c1.Print(("DQHL_retrigger_percentage_pass_all_except_retrigger_log_%i-%i.png" % (firstRun, lastRun)))
    ROOT.gPad.SetLogy(0)
    hist['hRetrigPercentagePassAllExceptRetrigger'].Draw("P")
    hist['hRetrigPercentagePassAllExceptRetrigger'].SetMaximum(100.)
    c1.Print(("DQHL_retrigger_percentage_pass_all_except_retrigger_lin_%i-%i.png" % (firstRun, lastRun)))

    # Retrigger percentage distribution for runs passing all other RS cuts:
    ROOT.gPad.SetLogy(0)
    hist['hRetrigPercentagePassAllExceptRetriggerDistribution'].Draw()
    c1.Print(("DQHL_retrigger_percentage_pass_all_except_retrigger_distribution_lin_%i-%i.png" % (firstRun, lastRun)))

    # Retrigger percentage and average event rate:
    ROOT.gPad.SetLogy(0)
    hist['hAvgEvRate'].Draw("P")
    hist['hAvgEvRate'].SetMaximum(3000.)
    hist['hRetrigPercentage'].Draw("P same")
    hist['hRetrigPercentage'].SetMaximum(100.)
    c1.Print(("DQHL_retrigger_percentage_and_mean_event_rate_lin_%i-%i.png" % (firstRun, lastRun)))

    # From Run Processor: ----------
    # Mean Nhits:
    ROOT.gPad.SetLogy()
    hist['hMeanNhits'].Draw("P")
    c1.Print(("DQHL_mean_nhit_log_%i-%i.png" % (firstRun, lastRun)))
    ROOT.gPad.SetLogy(0)
    hist['hMeanNhits'].Draw("P")
    hist['hMeanNhits'].SetMaximum(50.)
    c1.Print(("DQHL_mean_nhit_lin_%i-%i.png" % (firstRun, lastRun)))

    # From PMT Processor: ----------
    # General, crate and panel coverage: 
    ROOT.gPad.SetLogy(0)
    hist['hGeneralCov'].Draw("P")
    c1.Print(("DQHL_general_coverage_%i-%i.png" % (firstRun, lastRun)))
    hist['hCrateCov'].Draw("P")
    c1.Print(("DQHL_crate_coverage_%i-%i.png" % (firstRun, lastRun)))
    hist['hPanelCov'].Draw("P")
    c1.Print(("DQHL_panel_coverage_%i-%i.png" % (firstRun, lastRun)))

    # No of panels failing coverage:
    ROOT.gPad.SetLogy()
    hist['hPanelFails'].Draw("P")
    c1.Print(("DQHL_num_panel_fails_log_%i-%i.png" % (firstRun, lastRun)))
    ROOT.gPad.SetLogy(0)
    hist['hPanelFails'].Draw("P")
    c1.Print(("DQHL_num_panel_fails_lin_%i-%i.png" % (firstRun, lastRun)))

    return c1
