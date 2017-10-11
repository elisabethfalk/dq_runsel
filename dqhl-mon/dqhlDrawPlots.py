#!/user/bin/env python

#==================================================================
# 
# dqhlDrawPlots.py
#
# E. Falk (E.Falk@sussex.ac.uk)
# 2017-09-11
#
# Draws histograms of the various DQHL checks that have previously
# been saved to file
# 
#==================================================================

import argparse
import sys
import os
import ROOT

def processRun(runNumber, data, hist):

     # Fill histograms:
     # fillHistograms(runNumber, data, hist)

    return

def dqhlDrawPlots(firstRun, lastRun, dir):

    # Change to output directory:
    homeDir = os.getcwd()
    if not os.path.exists(dir):
        os.mkdir(dir)
    if not os.path.isdir(dir):
        print "Invalid directory name:", dir
        sys.exit(1)
    os.chdir(dir)

    # Open histogram:
    filename = "dqhlHistos_%s_%s.root" % (firstRun, lastRun)
    f = ROOT.TFile.Open(("dqhlHistos_%s_%s.root" % (firstRun, lastRun)), 'read')

    # Create canvas:
    c1 = ROOT.TCanvas("canvas", "", 800, 500)

    # Plot DQHL pass/fail stats:
    h0 = f.Get("hPassStats;1")
    # h0.SetTitle("Physics runs failing Retrigger cut (run range %i-%i)" % (firstRun, lastRun))
    h0.SetLineWidth(2)
    h0.SetStats(False)
    h0.Draw()
    c1.SaveAs("PassFailModif.pdf")

    # Plot all runs failing retrigger cut:
    h0 = f.Get("hRetrig")
    h0.SetTitle("Physics runs failing Retrigger cut (run range %i-%i)" % (firstRun, lastRun))
    h0.SetMarkerStyle(7) # Medium dot
    h0.SetMarkerColor(4) # Blue
    h0.SetStats(False)
    h0.Draw('p')
    c1.SaveAs("RetriggersAllByRun.pdf")

    # Plot all runs failing retrigger and passing all other cuts:
    h0 = f.Get("hRetrigPassAllOth")
    h0.SetTitle("Physics runs failing Retrigger cut (run range %i-%i)" % (firstRun, lastRun))
    h0.SetMarkerStyle(7) # Medium dot
    h0.SetMarkerColor(2) # Red
    h0.SetStats(False)
    h0.Draw('p')
    c1.SaveAs("RetriggersPassAllOthByRun.pdf")

    # Plot distribution of all retriggers:
    h1 = f.Get("hRetrigDistr")
    h1.SetTitle("Physics runs failing Retrigger cut (run range %i-%i)" % (firstRun, lastRun))
    h1.SetLineColor(4) # Blue
    h1.SetLineWidth(2)
    h1.SetStats(False)
    h1.Draw()
    l1 = ROOT.TLegend(0.35, 0.85, 0.90, 0.90)
    # l1.SetHeader("Physics runs failing Retrigger cut")
    l1.AddEntry(h1, ("%i runs in total" % h1.GetEntries()), 'l')
    l1.Draw()
    c1.SaveAs("RetriggersAll.pdf")

    # Plot distribution of retriggers passing DQHL + run length cuts:
    h2 = f.Get("hRetrigPassDqhlRunLenDistr")
    h2.SetLineColor(8) # Dark green
    h2.SetLineWidth(2)
    h2.SetStats(False)
    h2.Draw("same")
    l2 = ROOT.TLegend(0.35, 0.80, 0.90, 0.90)
    # l2.SetHeader("Physics runs failing Retrigger cut")
    l2.AddEntry(h1, ("%i runs in total" % h1.GetEntries()), 'l')
    l2.AddEntry(h2, ("%i of which pass high-level + run-length DQ cuts" % h2.GetEntries()), 'l')
    l2.Draw()
    c1.SaveAs("RetriggersPassDQHL+RL.pdf")

    # Plot distribution of retriggers passing all other DQ cuts:
    h3 = f.Get("hRetrigPassAllOthDistr")
    # h3.SetLineColor(3) # Green
    h3.SetLineColor(2) # Red
    h3.SetLineWidth(2)
    h3.SetStats(False)
    h3.Draw("same")
    l3 = ROOT.TLegend(0.35, 0.75, 0.90, 0.90)
    # l3.SetHeader("Physics runs failing Retrigger cut")
    l3.AddEntry(h1, ("%i runs in total" % h1.GetEntries()), 'l')
    l3.AddEntry(h2, ("%i of which pass high-level + run-length DQ cuts" % h2.GetEntries()), 'l')
    l3.AddEntry(h3, ("%i* of which pass all other DQ cuts (*preliminary)" % h3.GetEntries()), 'l')
    l3.Draw()
    c1.SaveAs("RetriggersPassAllOther.pdf")

    f.Close()

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

    print "Running dqhlDrawPlots for run range %i-%i" % (firstRun, lastRun)
    c1 = dqhlDrawPlots(firstRun, lastRun, args.dir)

    sys.exit(0)

