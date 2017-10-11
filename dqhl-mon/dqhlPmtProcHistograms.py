#!/user/bin/env python

#==================================================================
# 
# dqhlPmtProcHistograms.py
#
# E. Falk (E.Falk@sussex.ac.uk)
# 2017-05-28
#
# Produces histograms of the DQPmtProcessor DQHL checks, and of 
# some of the parameters monitored by DQHL
# 
#==================================================================

import ROOT
from dqhlProcChecks import *

#-- Create histograms ---------------------------------------------

def createGeneralCoverageHistogram(firstRun, lastRun):
    histTitle = "DQHL Overall PMT coverage for Physics runs %i-%i" % (firstRun, lastRun)
    nBins = lastRun - firstRun + 1
    hGeneralCov = ROOT.TH1D("hDQHLGeneralCoverage", histTitle, nBins, firstRun-0.5, lastRun+0.5)
    hGeneralCov.GetYaxis().SetTitle("Overall detector coverage (%)")
    hGeneralCov.GetXaxis().SetTitle("Run number")
    hGeneralCov.SetMarkerStyle(7) # 8 = kFullDotLarge
    hGeneralCov.SetMarkerColor(4)

    return hGeneralCov

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

def createPmtProcHistograms(firstRun, lastRun, hist):
    hist['hGeneralCov'] = createGeneralCoverageHistogram(firstRun, lastRun)
    hist['hCrateCov'] = createCrateCoverageHistogram(firstRun, lastRun) # 100%, with 50% in crate
    hist['hPanelCov'] = createPanelCoverageHistogram(firstRun, lastRun) # 80%
    # Runs with no of crates failing coverage may be best listed (certainly for crates -- but maybe wait until cut has been modified)
    # No of panels failing coverage could be plotted

    return hist

#-- Fill histograms -----------------------------------------------

def fillPmtProcHistograms(runNumber, pmtProc, hist):
    hist['hGeneralCov'].Fill(runNumber, pmtProc['check_params']['overall_detector_coverage'])
    hist['hCrateCov'].Fill(runNumber, pmtProc['check_params']['crates_coverage_percentage'])
    hist['hPanelCov'].Fill(runNumber, pmtProc['check_params']['percentage_of_panels_passing_coverage'])

    return

#-- Draw histograms -----------------------------------------------

def drawPmtProcHistograms(c1, firstRun, lastRun, hist):
    ROOT.gPad.SetLogy(0)
    hist['hGeneralCov'].Draw("P")
    c1.Print(("DQHL_general_coverage_%i-%i.png" % (firstRun, lastRun)))
    # Should have a line on it, where the numerical value comes from general_cov_thresh' ... genCovLine = TLine(firstRun-0.5, 70, lastRun+0.5, 70)
    hist['hCrateCov'].Draw("P")
    c1.Print(("DQHL_crate_coverage_%i-%i.png" % (firstRun, lastRun)))
    hist['hPanelCov'].Draw("P")
    c1.Print(("DQHL_panel_coverage_%i-%i.png" % (firstRun, lastRun)))

    return c1
