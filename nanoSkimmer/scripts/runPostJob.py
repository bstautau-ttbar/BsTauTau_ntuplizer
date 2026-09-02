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

def check_ROOTfile(filename, trees=('Runs',), hists=('autoPU',)):
    result = {
        'zero_size': False,
        'zombie': False,
        'missing_trees': [],
        'empty_trees': [],
        'missing_hists': [],
        'ok': False,
        'reason': '',
    }
    # empty file
    try:
        size = os.path.getsize(filename)
    except OSError as e:
        result['reason'] = 'cannot stat file (%s)' % e
        return result
    if size < 1000:
        result['zero_size'] = True
        result['reason'] = 'zero-size file'
        return result
    # zombie
    tfile = ROOT.TFile.Open(filename)
    if tfile is None:
        result['zombie'] = True
        result['reason'] = 'TFile.Open returned null'
        return result
    if tfile.IsZombie():
        result['zombie'] = True
        result['reason'] = 'zombie file'
        tfile.Close()
        return result
    # no entries in Runs
    for treename in trees:
        tree = tfile.Get(treename)
        if not tree or not isinstance(tree, ROOT.TTree):
            result['missing_trees'].append(treename)
            continue
        if tree.GetEntries() == 0:
            result['empty_trees'].append(treename)
    tfile.Close()
    for histname in hists:
        obj = tfile.Get(histname)
        if not obj or not isinstance(obj, ROOT.TH1):
            result['missing_hists'].append(histname)
    tfile.Close()
    
    if result['missing_trees'] or result['empty_trees']:
        parts = []
        if result['missing_trees']:
            parts.append('missing tree(s) %s' % result['missing_trees'])
        if result['empty_trees']:
            parts.append('empty tree(s) %s' % result['empty_trees'])
        if result['missing_hists']:
            parts.append('missing hist(s) %s' % result['missing_hists'])
        result['reason'] = ', '.join(parts)
        return result
 
    result['ok'] = True
    return result


if __name__ == "__main__":
    usage = 'usage: %prog [options]'
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',    dest='input',    help='list of input datasets',
                        default='listSamplesMC2018.txt', type=str)
    parser.add_argument('-c', '--channels', dest='channels', help='list of channels to analyze (e.g. emu ee mumu e mu)',
                        default=['emu'], nargs='+', type=str)
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
                exit(1)
            
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
                if not check['ok']:
                    bad_files.append((filename, check['reason']))
                    # FIXME : add here a way to resubmit the job for this file

            if bad_files:
                log.print_error(' %d bad file(s) in job output'%len(bad_files))
                for filename, reason in bad_files:
                    print('\t %s  [%s]'%(filename, reason))
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
