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
              'run_header', '10Mhz_UT_comparison', 'clock_forward', \
              'run_type', 'mc_flag', 'trigger', \
              'general_coverage', 'crate_coverage', 'panel_coverage']

#-- Create histograms ---------------------------------------------

#-- Overall Pass/Fails: -----

def createPassFailStatsHistogram(firstRun, lastRun):
    histTitle = "DQHL Pass/Fail stats for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = len(dqhlChecks)
    hStats = ROOT.TH1D("hDQHLPassStats", histTitle, nBins, -0.5, nBins-0.5)
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
    hEsumhRate.GetYaxis().SetTitle("ESUMH trigger rate")
    hEsumhRate.GetXaxis().SetTitle("Run number")
    hEsumhRate.SetMarkerStyle(7) # 8 = kFullDotLarge
    hEsumhRate.SetMarkerColor(4)

    return hEsumhRate

def createN100lRateHistogram(firstRun, lastRun):
    histTitle = "DQHL N100L trigger rate for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hN100lRate = ROOT.TH1D("hDQHLN100lRate", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hN100lRate.GetYaxis().SetTitle("N100L trigger rate")
    hN100lRate.GetXaxis().SetTitle("Run number")
    hN100lRate.SetMarkerStyle(7) # 8 = kFullDotLarge
    hN100lRate.SetMarkerColor(4)

    return hN100lRate

def createOrphansCountHistogram(firstRun, lastRun):
    histTitle = "DQHL Number of orphans for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hOrphans = ROOT.TH1D("hDQHLOrphans", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hOrphans.GetYaxis().SetTitle("Number of orphans")
    hOrphans.GetXaxis().SetTitle("Run number")
    hOrphans.SetMarkerStyle(7) # 8 = kFullDotLarge
    hOrphans.SetMarkerColor(4)

    return hOrphans

def createBitFlipGTIDHistogram(firstRun, lastRun):
    histTitle = "DQHL Number of bitflip GTIDs for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hBitFlipGTIDs = ROOT.TH1D("hDQHLBitFlipGTIDs", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hBitFlipGTIDs.GetYaxis().SetTitle("Number of bitflip GTIDs")
    hBitFlipGTIDs.GetXaxis().SetTitle("Run number")
    hBitFlipGTIDs.SetMarkerStyle(7) # 8 = kFullDotLarge
    hBitFlipGTIDs.SetMarkerColor(4)

    return hBitFlipGTIDs

#-- From DQTimeProc: -----

def createAverageEventRateHistogram(firstRun, lastRun):
    histTitle = "DQHL Event rate (average) for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hAvgEvRate = ROOT.TH1D("hDQHLAvgEvRate", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hAvgEvRate.GetYaxis().SetTitle("Event rate, average (Hz)")
    hAvgEvRate.GetXaxis().SetTitle("Run number")
    hAvgEvRate.SetMarkerStyle(7) # 8 = kFullDotLarge
    hAvgEvRate.SetMarkerColor(2)

    return hAvgEvRate

def createDeltaTEventRateHistogram(firstRun, lastRun):
    histTitle = "DQHL Event rate for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hDelTEvRate = ROOT.TH1D("hDQHLDeltaTEvRate", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hDelTEvRate.GetYaxis().SetTitle("Event rate (Hz)")
    hDelTEvRate.GetXaxis().SetTitle("Run number")
    hDelTEvRate.SetMarkerStyle(7) # 8 = kFullDotLarge
    hDelTEvRate.SetMarkerColor(4)

    return hDelTEvRate

#-- From DQRunProc: -----

def createMeanNhitsHistogram(firstRun, lastRun):
    histTitle = "DQHL Mean NHits Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hMeanNhits = ROOT.TH1D("hDQHLMeanNhits", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hMeanNhits.GetYaxis().SetTitle("Mean NHits")
    hMeanNhits.GetXaxis().SetTitle("Run number")
    hMeanNhits.SetMarkerStyle(7) # 8 = kFullDotLarge
    hMeanNhits.SetMarkerColor(4)

    return hMeanNhits

#-- From DQPmtProc: -----

def createGeneralCoverageHistogram(firstRun, lastRun):
    histTitle = "DQHL Overall PMT coverage for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hGeneralCov = ROOT.TH1D("hDQHLGeneralCoverage", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hGeneralCov.GetYaxis().SetTitle("Overall detector coverage (%)")
    hGeneralCov.GetXaxis().SetTitle("Run number")
    hGeneralCov.SetMarkerStyle(7) # 8 = kFullDotLarge
    hGeneralCov.SetMarkerColor(4)

    return hGeneralCov

def createGeneralCovThreshHistogram(firstRun, lastRun):
    histTitle = "DQHL Overall PMT coverage threshold for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hGeneralCovThresh = ROOT.TH1D("hDQHLGeneralCoverageCriterion", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hGeneralCovThresh.GetYaxis().SetTitle("Overall detector coverage threshold (percent)")
    hGeneralCovThresh.GetXaxis().SetTitle("Run number")
    # hGeneralCovThresh.SetMarkerStyle(8) # 8 = kFullDotLarge

    return hGeneralCovThresh

def createCrateCoverageHistogram(firstRun, lastRun):
    histTitle = "DQHL Crate coverage for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hCrateCov = ROOT.TH1D("hDQHLCrateCoverage", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hCrateCov.GetYaxis().SetTitle("Crate coverage (%)")
    hCrateCov.GetXaxis().SetTitle("Run number")
    hCrateCov.SetMarkerStyle(7) # 8 = kFullDotLarge
    hCrateCov.SetMarkerColor(2)

    return hCrateCov

def createPanelCoverageHistogram(firstRun, lastRun):
    histTitle = "DQHL Panel coverage for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hCrateCov = ROOT.TH1D("hDQHLPanelCoverage", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hCrateCov.GetYaxis().SetTitle("Panel coverage (%)")
    hCrateCov.GetXaxis().SetTitle("Run number")
    hCrateCov.SetMarkerStyle(7) # 8 = kFullDotLarge
    hCrateCov.SetMarkerColor(8)

    return hCrateCov

#-- Create all histograms and store in a list/dict ----------------

def createHistograms(firstRun, lastRun):
    hist = {}
    ROOT.gStyle.SetOptStat(0)

    # Overall Pass/Fail histogram(s):
    hist['hStats'] = createPassFailStatsHistogram(firstRun, lastRun)

    # From Trigger proc:
    # Pass/fails: esumh_trigger_rate, n100l_trigger_rate, triggerProcMissingGTID, triggerProcBitFlipGTID, 
    # check_params: *esumh_trigger_rate, *n100l_trigger_rate, missing_gtids, *bitflip_gtids (list), *orphans_count (list)
    # criteria: min_esum_hi_rate (5), min_nhit100l_rate (5), max_num_missing_gtids (20 --> 0), max_num_bitflip_gtids (20 --> 0)
    hist['hEsumhRate'] = createEsumhRateHistogram(firstRun, lastRun)
    hist['hN100lRate'] = createN100lRateHistogram(firstRun, lastRun)
    hist['hOrphans'] = createOrphansCountHistogram(firstRun, lastRun)
    # Missing GTIDs and bit flips probably best counted, and runs & values listed
    hist['hBitFlipGTIDs'] = createBitFlipGTIDHistogram(firstRun, lastRun)

    # From TimeProc:
    # Pass/fails: event_rate, event_separation, retriggers, 10Mhz_UT_comparrison, delta_t_comparison, clock_forward, run_header 
    # check_params: count_10_offset, non_coincident_count_10_delta_ts, non_coincident_universal_time_delta_ts, *delta_t_event_rate, coincident_offsets,
    #               num_UT_10MhzClock_comp_fails, *mean_event_rate, event_rate_agreement, universal_time_offsets
    # criteria: retriggers_thresh (10), run_header_thresh (1000000000), min_event_rate (5), max_event_rate (1000), clock_forward_thresh (99), event_separation_thresh (1)
    hist['hAvgEvRate'] = createAverageEventRateHistogram(firstRun, lastRun)
    hist['hDelTEvRate'] = createDeltaTEventRateHistogram(firstRun, lastRun)
    # Lots to do here...

    # From RunProc:
    # Pass/fails: run_type, mc_flag, run_length, trigger
    # check_params: universal_time_run_length, count_50_run_length, count_10_run_length, *mean_nhit, run_length, run_length_source (count_10)
    # criteria: trigger_check_thresh (90), mc_flag_criteria (0), trigger_check_criteria (26326), min_run_length (1800) 
    hist['hMeanNhits'] = createMeanNhitsHistogram(firstRun, lastRun)
    # Run type, MC flag and trigger mask probably best counted, and runs & values listed
    # Could check agreement between the different run length calculations

    # From PMT proc:
    # Pass/fails: general_coverage, crate_coverage, panel_coverage
    # check_params: *overall_detector_coverage, crates_failing_coverage, *crates_coverage_percentage, 
    #               number_of_panels_failing_coverage, *percentage_of_panels_passing_coverage, 
    # criteria: general_cov_thresh (70), panel_cov_thresh (80), crate_cov_thresh (100), in_crate_cov_thresh (50)
    hist['hGeneralCov'] = createGeneralCoverageHistogram(firstRun, lastRun)
    hist['hGeneralCovThresh'] = createGeneralCovThreshHistogram(firstRun, lastRun) # 70%
    hist['hCrateCov'] = createCrateCoverageHistogram(firstRun, lastRun) # 100%, with 50% in crate
    hist['hPanelCov'] = createPanelCoverageHistogram(firstRun, lastRun) # 80%
    # Runs with no of crates failing coverage may be best listed (certainly for crates -- but maybe wait until cut has been modified)
    # No of panels failing coverage could be plotted

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

    # Fill Pass/Fail histogram: 
    hStats = hist['hStats']
    if (triggerProc['n100l_trigger_rate']):
        hStats.Fill(dqhlChecks.index('n100l_trigger_rate'))
    if (triggerProc['esumh_trigger_rate']):
        hStats.Fill(dqhlChecks.index('esumh_trigger_rate'))
    if (triggerProc['triggerProcMissingGTID']):
        hStats.Fill(dqhlChecks.index('triggerProcMissingGTID'))
    if (triggerProc['triggerProcBitFlipGTID']):
        hStats.Fill(dqhlChecks.index('triggerProcBitFlipGTID'))
    if (timeProc['event_rate']):
        hStats.Fill(dqhlChecks.index('event_rate'))
    if (timeProc['event_separation']):
        hStats.Fill(dqhlChecks.index('event_separation'))
    if (timeProc['retriggers']):
        hStats.Fill(dqhlChecks.index('retriggers'))
    if (timeProc['run_header']):
        hStats.Fill(dqhlChecks.index('run_header'))
    if (timeProc['10Mhz_UT_comparrison']):
        hStats.Fill(dqhlChecks.index('10Mhz_UT_comparison'))
    if (timeProc['clock_forward']):
        hStats.Fill(dqhlChecks.index('clock_forward'))
    # if (timeProc['delta_t_comparison']):     # No longer used
    #     hStats.Fill(dqhlChecks.index('delta_t_comparison'))
    if (runProc['run_type']):
        hStats.Fill(dqhlChecks.index('run_type'))
    if (runProc['mc_flag']):
        hStats.Fill(dqhlChecks.index('mc_flag'))
    # if (runProc['run_length']):              # No longer used
    #     hStats.Fill(dqhlChecks.index('run_length'))
    if (runProc['trigger']): 
        hStats.Fill(dqhlChecks.index('trigger'))
    if (pmtProc['general_coverage']):
        hStats.Fill(dqhlChecks.index('general_coverage'))
    if (pmtProc['crate_coverage']):
        hStats.Fill(dqhlChecks.index('crate_coverage'))
    if (pmtProc['panel_coverage']):
        hStats.Fill(dqhlChecks.index('panel_coverage'))

    # Fill Trigger Processor histograms: 
    hist['hEsumhRate'].Fill(runNumber, triggerProc['check_params']['esumh_trigger_rate'])
    hist['hN100lRate'].Fill(runNumber, triggerProc['check_params']['n100l_trigger_rate'])
    hist['hOrphans'].Fill(runNumber, triggerProc['check_params']['orphans_count'])
    hist['hBitFlipGTIDs'].Fill(runNumber, len(triggerProc['check_params']['bitflip_gtids']))

    # Fill Time Processor histograms: 
    hist['hAvgEvRate'].Fill(runNumber, timeProc['check_params']['mean_event_rate'])
    hist['hDelTEvRate'].Fill(runNumber, timeProc['check_params']['delta_t_event_rate'])

    # Fill Run Processor histograms: 
    hist['hMeanNhits'].Fill(runNumber, runProc['check_params']['mean_nhit'])

    # Fill PMT Processor histograms:
    hist['hGeneralCov'].Fill(runNumber, pmtProc['check_params']['overall_detector_coverage'])
    hist['hGeneralCovThresh'].Fill(runNumber, pmtProc['criteria']['general_cov_thresh'])
    hist['hCrateCov'].Fill(runNumber, pmtProc['check_params']['crates_coverage_percentage'])
    hist['hPanelCov'].Fill(runNumber, pmtProc['check_params']['percentage_of_panels_passing_coverage'])

    return

#-- Draw histograms -----------------------------------------------

def drawHistograms(firstRun, lastRun, nRuns, hist):
    # Scale histogram to get fractional pass rates:
    print "No of physics runs with DQHL data processed: ", nRuns
    hist['hStats'].Scale(1./nRuns)

    # Create canvas and draw histogram
    ROOT.gROOT.SetBatch(ROOT.kTRUE)
    c1 = ROOT.TCanvas()

    hist['hStats'].Draw()
    c1.Print(("DQHL_pass_fail_stats_%i-%i.png" % (firstRun, lastRun)))

    # From Trigger Processor: 
    hist['hEsumhRate'].Draw("P")
    c1.Print(("DQHL_esumh_trigger_rate_%i-%i.png" % (firstRun, lastRun)))

    hist['hN100lRate'].Draw("P")
    c1.Print(("DQHL_n100l_trigger_rate_%i-%i.png" % (firstRun, lastRun)))

    ROOT.gPad.SetLogy()
    hist['hOrphans'].Draw("P")
    c1.Print(("DQHL_orphans_count_%i-%i.png" % (firstRun, lastRun)))

    ROOT.gPad.SetLogy(0)
    hist['hBitFlipGTIDs'].Draw("P")
    c1.Print(("DQHL_bitflip_gtids_%i-%i.png" % (firstRun, lastRun)))

    # From Time Processor: 
    ROOT.gPad.SetLogy()
    hist['hAvgEvRate'].Draw("P")
    c1.Print(("DQHL_avg_event_rate_%i-%i.png" % (firstRun, lastRun)))

    ROOT.gPad.SetLogy(0)
    hist['hDelTEvRate'].Draw("P")
    hist['hDelTEvRate'].SetMaximum(3000.)
    c1.Print(("DQHL_avg_event_rate_lin_%i-%i.png" % (firstRun, lastRun)))

    ROOT.gPad.SetLogy()
    hist['hDelTEvRate'].Draw("P")
    c1.Print(("DQHL_delta_t_event_rate_%i-%i.png" % (firstRun, lastRun)))

    ROOT.gPad.SetLogy(0)
    hist['hDelTEvRate'].Draw("P")
    hist['hDelTEvRate'].SetMaximum(3000.)
    c1.Print(("DQHL_delta_t_event_rate_lin_%i-%i.png" % (firstRun, lastRun)))

    ROOT.gPad.SetLogy()
    hist['hAvgEvRate'].SetTitle(("DQHL Event rate for Physics runs %i-%i" % (firstRun, lastRun)))
    hist['hAvgEvRate'].GetYaxis().SetTitle("Event rate (Hz)")
    hist['hAvgEvRate'].Draw("P")
    hist['hDelTEvRate'].Draw("P same")
    c1.Print(("DQHL_event_rate_avg_and_delta_t_%i-%i.png" % (firstRun, lastRun)))
    hist['hAvgEvRate'].SetTitle(("DQHL Event rate (average) for Physics runs %i-%i" % (firstRun, lastRun)))
    hist['hAvgEvRate'].GetYaxis().SetTitle("Event rate, average (Hz)")

    # From Run Processor: 
    ROOT.gPad.SetLogy(0)
    hist['hMeanNhits'].Draw("P")
    c1.Print(("DQHL_mean_nhit_%i-%i.png" % (firstRun, lastRun)))

    # From PMT Processor: 
    ROOT.gPad.SetLogy(0)
    hist['hGeneralCov'].Draw("P")
    c1.Print(("DQHL_general_coverage_%i-%i.png" % (firstRun, lastRun)))
    hist['hCrateCov'].Draw("P")
    c1.Print(("DQHL_crate_coverage_%i-%i.png" % (firstRun, lastRun)))
    hist['hPanelCov'].Draw("P")
    c1.Print(("DQHL_panel_coverage_%i-%i.png" % (firstRun, lastRun)))

    return c1
