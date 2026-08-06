import ROOT
ROOT.gROOT.SetBatch(True)

import os, sys
import glob
from fnmatch import fnmatch
import optparse

import BsTauTau.nanoSkimmer.logger as log

'''
Script to check the jobs from the flattener
# FIXME : this is very naive -> fix it to check the output files and resubmit only the failed ones
'''
DEEP_CHECK = False

if __name__ == "__main__":
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('-i', '--input',      dest='input',     help='list of input datasets',    default='listSamplesMC2018.txt', type='string')
    parser.add_option('-c', '--channels',   dest='channels',  help='channel to analyze', default='emu', type='string') #FIXME: add list for channels
    parser.add_option('-y', '--year',       dest='year',      help='year to analyze', default='2018', type='string')
    parser.add_option('-t', '--tag',        dest='tag',       help='tag to analyze', default='testV0', type='string')
    parser.add_option('--filter',           dest='filter',    help='(optional) string to filter input datasets. POSIX regular expression allowed',    default='*', type='string')
    parser.add_option('--isdata',           dest='isdata',    help='flag to run on data (apply GRL and specific trigger selection)', action='store_true')
    parser.add_option('-o', '--output',     dest='output',    help='output directory where to expect job output', default='output', type='string')
    (opt, args) = parser.parse_args()

    channel = opt.channels

    # input check
    if not os.path.isfile(opt.input): 
      print('ERROR: bad input file (%s)'%opt.input)
      sys.exit(1)
    # output check
    if not os.path.isdir(opt.output): 
      print('ERROR: bad output directory (%s)'%opt.output)
      sys.exit(1)
    
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
        log.print_bold(' ---- %s ----'%(dataset.split('/')[-3]))

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
            log.print_warning(' Missing files %d (input %d, output %d)'%(n_infiles-n_outfiles, n_infiles, n_outfiles))
        elif n_outfiles > n_infiles:
            log.print_warning(' Too many files %d (input %d, output %d)'%(n_outfiles-n_infiles, n_infiles, n_outfiles))
        elif n_outfiles == n_infiles:
             log.print_success(' All files (%d) are present in output'%n_outfiles)

        # check if empty or zoombie files are present in output
        empty_files, zoombie_files = [], []
        for filename in glob.glob(outdataset):
            file = ROOT.TFile.Open(filename)
            if file.IsZombie(): zoombie_files.append(filename)
            else :
                tree = file.Get('Events')
                if tree.GetEntries()==0: empty_files.append(filename)
            file.Close()
        if len(empty_files)>0 or len(zoombie_files)>0:
            log.print_error(' %d | %d -- empty | zoombie files in output'%(len(empty_files), len(zoombie_files)))
            for filename in empty_files:
                print('\t %s'%filename)
        else:
            log.print_success(' No empty or zoombie files found in output')
            

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
