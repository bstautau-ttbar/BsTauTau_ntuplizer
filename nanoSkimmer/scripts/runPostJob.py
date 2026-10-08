import ROOT
ROOT.gROOT.SetBatch(True)

import os, sys
import glob
from fnmatch import fnmatch
import argparse

import BsTauTau.nanoSkimmer.logger as log

'''
Script to check the jobs from the flattener
# FIXME : check the output files and resubmit only the failed ones
'''
DEEP_CHECK = False
DEBUG      = False

def check_ROOTfile(filename, trees=('Runs',), hists=('autoPU',)):
    result = {
        'ok': False,
        'reason': '',
        'missing_trees': [],
        'missing_hists': [],
    }
    # empty file
    try:
        if os.path.getsize(filename) < 200:  # 200 bytes is the minimum size for a valid ROOT file
            result['reason'] = 'zero-size file'; return result
    except OSError as e:
        result['reason'] = 'cannot stat file (%s)' % e
        return result
    
    # broken
    tfile = ROOT.TFile.Open(filename)
    if not tfile or tfile.IsZombie():
        result['reason'] = 'zombie / cannot open'; return result
    
    problems = []
    if tfile.TestBit(ROOT.TFile.kRecovered):
        problems.append('file recovered (not cleanly closed)')
    if tfile.GetEND() > tfile.GetSize():
        problems.append(f'file truncated (END {tfile.GetEND()} > SIZE {tfile.GetSize()})')
    
    
    # every key must be readable
    for key in tfile.GetListOfKeys():
        if not key.ReadObj():
            problems.append(f'cannot read key {key.GetName()} ({key.GetClassName()})')
    
    for tn in trees:
        tree = tfile.Get(tn)
        if not tree or not isinstance(tree, ROOT.TTree):
            problems.append(f'missing tree {tn}')
            continue
        if tn == 'Runs' and tree.GetEntries() == 0:
            problems.append(f'empty tree {tn}')
    
    for hn in hists:
        hist = tfile.Get(hn)
        if not hist or not isinstance(hist, ROOT.TH1):
            problems.append(f'missing histogram {hn}')
            result['missing_hists'].append(hn)
    
    tfile.Close()
    result['ok'] = len(problems) == 0
    result['reason'] = ' | '.join(problems)
    return result


if __name__ == "__main__":
    usage = 'usage: %prog [options]'
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',    dest='input',    help='list of input datasets',
                        required=True, type=str)
    parser.add_argument('-c', '--channels', dest='channels', help='list of channels to analyze (e.g. emu ee mumu e mu)',
                        required=True, nargs='+', type=str)
    parser.add_argument('-y', '--year',     dest='year',     help='year to analyze',
                        default='2018', type=str)
    parser.add_argument('-t', '--tag',      dest='tag',      help='tag to analyze',
                        default='testV0', type=str)
    parser.add_argument('--filter',         dest='filter',   help='(optional) string to filter input datasets. POSIX regular expression allowed',
                        default='*', type=str)
    parser.add_argument('--isdata',         dest='isdata',   help='flag to run on data (apply GRL and specific trigger selection)',
                        action='store_true')
    parser.add_argument('-o', '--output',   dest='output',   help='output directory where to expect job output',
                        default='output', type=str)
    opt = parser.parse_args()

    channels = opt.channels
    
    # input check
    if not os.path.isfile(opt.input): 
      print('ERROR: bad input file (%s)'%opt.input)
      sys.exit(1)
    # output check
    if not os.path.isdir(opt.output): 
      print('ERROR: bad output directory (%s)'%opt.output)
      sys.exit(1)

    # summary
    tot_datasets, tot_channels, tot_goodfiles, tot_toresub = 0, 0, 0, 0
    
    # loop over input datasets
    datasets = open(opt.input).read().splitlines()
    if len(datasets)==0:
      print('ERROR: no dataset found in input file (%s)'%opt.input)
      sys.exit(1)

    output_template=os.path.join(opt.output,
                        '{channel}_{year}_{tag}',
                        '{sample_id}',
                        '{sample_full}_{channel}')
    
    for dataset in datasets:
        if '#' in dataset: continue
        if not fnmatch(dataset, opt.filter) : continue
        tot_datasets += 1
        log.print_bold(' ---- %s ----'%(dataset.split('/')[-3]))

        # loop over ttbar channels
        for channel in channels:
            log.print_bold(' >> channel: %s'%(channel))
            tot_channels += 1
            # numbre of input files
            indataset = dataset.strip()+'/*.root'
            n_infiles = len(glob.glob(indataset))
            print('\t [IN] %d files in --- %s'%(n_infiles,indataset))

            # output location
            sufix='mc' if not opt.isdata else 'data' # FIXME: better from name?
            prefix=''
            year=opt.year
            #print(dataset.split('/'))
            dataset_name = dataset.split('/')[-3]+"_"+dataset.split('/')[-1]

            outdataset = os.path.join(output_template.format(channel=channel, year=year, tag=opt.tag, sample_id=dataset_name.split('_')[0], sample_full=dataset_name),'*.root')
            n_outfiles = len(glob.glob(outdataset))
            print('\t [OUT] %d files in --- %s'%(n_outfiles, outdataset))

            if n_outfiles == 0:
                log.print_error('No output file found for dataset %s'%dataset_name)
                continue
            
            if n_outfiles < n_infiles:
                log.print_warning(' Missing %d files (input %d, output %d)'%(n_infiles-n_outfiles, n_infiles, n_outfiles))
            elif n_outfiles > n_infiles:
                log.print_warning(' Too many files %d (input %d, output %d)'%(n_outfiles-n_infiles, n_infiles, n_outfiles))
            elif n_outfiles == n_infiles:
                log.print_success(' All files (%d) are present in output'%n_outfiles)

            # check if empty or zoombie files are present in output
            bad_files = []
            for filename in glob.glob(outdataset):
                check = check_ROOTfile(filename)
                if DEBUG: print(check)
                if not check['ok']:
                    bad_files.append((filename, check['reason']))
                    # FIXME : add here a way to resubmit the job for this file
                else: tot_goodfiles += 1

            if bad_files:
                log.print_error(' %d bad file(s) in job output'%len(bad_files))
                for filename, reason in bad_files:
                    print(f'\t{filename} --> {reason}]')
                tot_toresub += len(bad_files)
            else:
                log.print_success(' All files (%d) are good in job output'%n_outfiles)
            

        # deeper check number of events in input and output files
        if not DEEP_CHECK: continue
        inchain = ROOT.TChain('Events')
        [inchain.Add(filename) for filename in glob.glob(indataset)]
        outchain = ROOT.TChain('Events')
        outchain.Add(outdataset)
        
        n_in_events = inchain.GetEntries()
        n_out_events = outchain.GetEntries()
        if n_out_events * n_in_events == 0:
            log.print_error(' No events found in input or output files (input %d, output %d)'%(n_in_events, n_out_events))
            exit(1)
        print('\t [events] output/input events %d/%d (%.2f %%)'%(n_out_events, n_in_events, 100*n_out_events/n_in_events))

    # print summary
    print('\n\n')
    log.print_bold(' ---- SUMMARY ----')
    print(' Total datasets: %d'%(tot_datasets))
    print(' Total channels: %d'%(tot_channels))
    print(' Total good files: %d'%(tot_goodfiles))
    print(' Total jobs to resubmit: %d'%(tot_toresub))
    log.print_bold(' -----------------')
