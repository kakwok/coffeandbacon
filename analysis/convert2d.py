import ROOT
import re
import numpy as np

fin = ROOT.TFile.Open("templates.root")
fout = ROOT.TFile.Open("hist_1DZbb_pt_scalesmear.root", "recreate")

hists1d = {}
for k in fin.GetListOfKeys():
    hists1d[k.GetName()] = fin.Get(k.GetName())

binre = re.compile('_bin\d')
msd = np.linspace(40., 201, 24)
pt = np.array([450., 500, 550, 600, 675, 800, 1200])


rename = {
    'trigweight': 'trigger',
    'pileupweight': 'Pu',
    'mutrigweight': 'mutrigger',
    'muidweight': 'muid',
    'muisoweight': 'muiso',
    'matchedUp': 'matched',
    'matchedDown': 'unmatched',
}

fout.cd()
hists2d = {}
for hname in set(binre.sub('', k) for k in hists1d.keys()):
    hnamerhalph = hname
    for k,v in rename.items():
        hnamerhalph = hnamerhalph.replace(k, v)
    hist = ROOT.TH2D(hnamerhalph, ";msd;pt;counts", len(msd)-1, msd, len(pt)-1, pt)
    for ipt in range(len(pt)-1):
        hptname = hname+'_bin%d' % ipt
        if hptname not in hists1d:
            continue
        h1d = hists1d[hptname]
        for imsd in range(len(msd)-1):
            hist.SetBinContent(imsd+1, ipt+1, h1d.GetBinContent(imsd+1))
            hist.SetBinError(imsd+1, ipt+1, h1d.GetBinError(imsd+1))
    hists2d[hnamerhalph] = hist

map(ROOT.TH2D.Write, hists2d.values())
fout.Write()
