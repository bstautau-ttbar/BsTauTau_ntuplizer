#!/usr/bin/env python
import os, sys
import optparse
from fnmatch import fnmatch
import datetime
import random
import glob
# my imports
import BsTauTau.nanoSkimmer.EraConfig as eracfg
import BsTauTau.nanoSkimmer.logger as log 


def buildCondorFile(opt,FarmDirectory, infodict):

  """ builds the condor file to submit the ntuplizer """

  cmssw=os.environ['CMSSW_BASE']
  rand='{:03d}'.format(random.randint(0,123456))
  jobname   = infodict.get('name', 'job_'+rand)

# ---- condor submission file -----
  condorFile=os.path.join(FarmDirectory, f'condorsub_{jobname}.sub')
  print(f"\t> {os.path.basename(condorFile)}")
  
  with open (condorFile,'w') as condor:

    condor.write(
      '''
executable = {0}/worker_{1}.sh

output     = {0}/output/{1}.out
error      = {0}/output/{1}.err
log        = {0}/log/{1}.log

should_transfer_files = YES
when_to_transfer_output = ON_EXIT_OR_EVICT
use_x509userproxy = true

+JobBatchName = "{1}"
+JobFlavour = "tomorrow"
+AccountingGroup = "group_u_CMST3.all"
+SingularityImage = "/cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/el8:x86_64"

'''.format(
        FarmDirectory, 
        jobname,
        #os.environ['X509_USER_PROXY']
      )
    )

    # one job per file, submitted via a single inline queue list
    file_list = infodict.get('files', [])
    if not file_list:
      log.print_error('file list empty') #FIXME skip the condor submission if filelist is empty
    prefix = infodict.get('prefix', '')
    condor.write('arguments = $(infile) %s %s %s\n\n'%(infodict.get('analysis', ''),infodict.get('output', ''),infodict.get('filter', '')))
    condor.write('queue infile in (\n')
    for file in file_list:
      condor.write('  %s%s\n'%(prefix, file))
    condor.write(')\n')
  
# ---- worker script to execute -----
  workerFile='%s/worker_%s.sh'%(FarmDirectory, jobname)
  with open(workerFile,'w') as worker:
    worker.write('''#!/bin/bash
echo ------- START JOB :  `date`
source /cvmfs/cms.cern.ch/cmsset_default.sh

# ---------------- INPUT
input=${{1}}
channel=${{2}}
output=${{3}}
filter=${{@:4}}
filename=`echo ${{1}} | rev | cut -d"/" -f1 | rev | cut -d"." -f1`


echo "worker_{1}.sh arguments:"
echo input="$input"
echo channel="$channel"
echo output="$output"
echo filter="$filter"
# ----------------

WORKDIR=/tmp/{2}/${{filename}}; mkdir -pv $WORKDIR
echo "Working directory is ${{WORKDIR}}"
cd {0}
eval `scram r -sh`
cd ${{WORKDIR}}

echo "INFO: Run ntuplizer"
echo "python3 $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py \\\\"
echo "$filename ${{input}}  \\\\"
echo "--bi $CMSSW_BASE/src/BsTauTau/nanoSkimmer/scripts/keep_in.txt   \\\\"
echo "--bo $CMSSW_BASE/src/BsTauTau/nanoSkimmer/scripts/keep_out.txt  \\\\"
echo "${{filter}} -I BsTauTau.nanoSkimmer.Flattener_analysis ${{channel}} "

python3 $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py $filename ${{input}} --bi $CMSSW_BASE/src/BsTauTau/nanoSkimmer/scripts/keep_in.txt --bo $CMSSW_BASE/src/BsTauTau/nanoSkimmer/scripts/keep_out.txt  ${{filter}} -I BsTauTau.nanoSkimmer.Flattener_analysis ${{channel}}

echo cp ${{filename}}/${{filename}}_Skim.root ${{output}}/${{filename}}_Skim.root
cp ${{filename}}/${{filename}}_Skim.root ${{output}}/

echo clean output
cd ../
rm -rf ${{WORKDIR}}
echo ls; ls -l $PWD
echo $startMsg
echo ------- END JOB :  `date`
'''.format(cmssw, jobname, os.environ['USER']))

  os.system('chmod u+x %s'%(workerFile))

  return condorFile


def split_input(opt, FarmDirectory):
  """ split the submission by samples """

  condorfiles = []
  
  datasets = open(opt.input).read().splitlines()
  if len(datasets) == 0:
    log.print_error(' Input file {} is empty!'.format(opt.input))
    sys.exit(1)
  
  #prepare output
  output_template=os.path.join(opt.output,
                        '{channel}_{year}_{tag}',
                        '{sample_id}',
                        '{sample_full}_{channel}')
  
  # -- loop on datasets --
  for dataset in datasets:
    if "#" in dataset or len(dataset)<2: continue
    if not fnmatch(dataset, opt.filter) : continue
    log.print_addition(f'{dataset}')
    
    sufix='mc' if not opt.isdata else 'data' # FIXME: better from name?
    prefix=''
    year=opt.year
    #print(dataset.split('/'))
    dataset_name = dataset.split('/')[-3]+"_"+dataset.split('/')[-1]
    
    file_list = glob.glob(dataset+'/*.root')
    max_files = min(opt.nfiles, len(file_list)) if opt.nfiles>0 else len(file_list)
    file_list = file_list[:max_files]
    log.print_info(f' dataset | suffix | year | #files: {dataset_name} | {sufix} | {year} | {len(file_list)}')
    
    if len(file_list) == 0:
      log.print_error('found invalid dataset "{}" stop the code'.format(dataset))
      sys.exit(1)

    channels=['ee','emu','mumu','e','mu']
    yearmodified=year
    if "preVFP" in dataset and year=="2016" and (sufix=="mc" or sufix=="sig"):
        yearmodified="2016pre"
    if "preVFP" not in dataset and year=="2016" and (sufix=="mc" or sufix=="sig"):
        yearmodified="2016post"
      
    
    # -- loop on channels --
    for channel in channels:
     
      output_full=output_template.format(channel=channel, year=year, tag=opt.tag, sample_id=dataset_name.split('_')[0], sample_full=dataset_name)
      os.makedirs(output_full, exist_ok=True)
      print(f'[OUT] {output_full}')
      
      # apply filter to data: trigger and GRL
      if opt.isdata:
        filter=eracfg.ANALYSISCUT['data'][year][channel]
      else:
        filter=eracfg.ANALYSISCUT['mc'][year][channel]
      print (f"\t({year} | {channel}) FILTER : {filter} ")

      sample_dict ={
        'name'      : '_'.join([dataset_name, channel]),
        'prefix'    : prefix,
        'files'     : file_list,
        'analysis'  : 'analysis_'+channel+sufix+yearmodified,
        'output'    : output_full,
        'filter'    : filter,
      }
      this_condor = buildCondorFile(
        opt,
        FarmDirectory,
        sample_dict 
      )
      if os.path.exists(this_condor): condorfiles.append(this_condor)

  return condorfiles



def main():
  # FIXME:
  # -- split the production by sample

  if not os.environ.get('CMSSW_BASE'):
    print('ERROR: CMSSW not set')
    sys.exit(0)

  cmssw=os.environ['CMSSW_BASE']

  #configuration
  usage = 'usage: %prog [options]'
  parser = optparse.OptionParser(usage)
  parser.add_option('-i', '--input',      dest='input',     help='list of input datasets',    default='listSamplesMC2018.txt', type='string')
  parser.add_option('--filter',           dest='filter',    help='(optional) string to filter input datasets. POSIX regular expression allowed',    default='*', type='string')
  parser.add_option('--isdata',           dest='isdata',    help='flag to run on data (apply GRL and specific trigger selection)', action='store_true')
  parser.add_option('-y', '--year',       dest='year',      help='data-taking year to process',    default='2018', type='string')
  parser.add_option('-t', '--tag',        dest='tag',       help='tag for your task used also in the output folder', default=None)
  parser.add_option('-o', '--out',        dest='output',    help='output directory',          default='/eos/cms/store/group/phys_bphys/cbasile/BsTauTau-ttbar/test2018/', type='string') #EDIT THIS
  parser.add_option('-n', '--nfiles',     dest='nfiles',    help='MAX number of files to process', default=-1, type='int')
  parser.add_option('-f', '--force',      dest='force',     help='force resubmission',        action='store_true')
  parser.add_option('-s', '--submit',     dest='submit',    help='submit jobs',               action='store_true')
  (opt, args) = parser.parse_args()
    
  if not os.path.isfile(opt.input): 
    print('ERROR: bad input file (%s)'%opt.input)
    sys.exit(1)

  #prepare directory with scripts
  jobtag = '_'.join(filter(None, [
    opt.year,
    opt.tag,
    datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
  ]))
  FarmDirectory = os.path.join(os.environ['PWD'], "FarmLocalNtuple_{}".format(jobtag))
  os.makedirs(FarmDirectory, exist_ok=True)
  os.makedirs(os.path.join(FarmDirectory, 'output'), exist_ok=True)
  os.makedirs(os.path.join(FarmDirectory, 'log'), exist_ok=True)
  log.print_info('Created farm directory: {}'.format(FarmDirectory))

  print('\n >>> INPUTS <<<')
  condorfiles = split_input(opt, FarmDirectory)
  print('\n----------------------\n')

  # submitter script to submit all the jobs
  log.print_success('Prepare `submitter.sh` to submit the jobs')
  with open('submitter.sh','w') as submitter:
    submitter.write('#!/bin/bash\n')
    for condor_script in condorfiles: 
      log.print_exe('condor_submit {}'.format(os.path.relpath(condor_script)), logger=submitter)
    submitter.write('echo "DONE | all jobs submitted"\n')

  print('\n----------------------')
  command = 'chmod u+x submitter.sh'
  log.print_exe(command)
  os.system(command)
  cmdtosubmit =  './submitter.sh'

  if not opt.submit:
    log.print_info(f'DRYRUN: to submit the jobs, run: {cmdtosubmit}')
  else:
    log.print_info(f'Submitting the jobs with: {cmdtosubmit}')
    os.system(cmdtosubmit) 

  return 0
      
		

if __name__ == "__main__":
  
  sys.exit(main())
