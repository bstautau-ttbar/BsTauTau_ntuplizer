#!/usr/bin/env python
import os
import sys
import optparse
from fnmatch import fnmatch
import shutil
import random
import glob
# my imports
import BsTauTau.nanoSkimmer.EraConfig as eracfg
import BsTauTau.nanoSkimmer.logger as log 


def buildCondorFile(opt,FarmDirectory, infodict):

  """ builds the condor file to submit the ntuplizer """

  cmssw=os.environ['CMSSW_BASE']
  OpSysAndVer = str(os.system('cat /etc/redhat-release')) 
  rand='{:03d}'.format(random.randint(0,123456))
  jobname   = infodict.get('name', 'job_'+rand)

  #condor submission file
  condorFile='%s/condor_generator_%s.sub'%(FarmDirectory,jobname)
  log.print_addition('Writes: %s'%condorFile)
  
  with open (condorFile,'w') as condor:

    condor.write(
      '''
executable = {0}/worker_{1}.sh
output     = {0}/output_{1}.out
error      = {0}/output_{1}.err
log        = {0}/output_{1}.log
+JobBatchName = "{1}"
+JobFlavour = "tomorrow"
+AccountingGroup = "group_u_CMST3.all"
+SingularityImage = "/cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/el8:x86_64"
should_transfer_files = YES
transfer_input_files = {2}

'''.format(
        FarmDirectory, 
        jobname,
        os.environ['X509_USER_PROXY']
      )
    )

    # one job per file
    file_list = infodict.get('files', [])
    if not file_list:
      log.print_error('file list empty') #FIXME skip the condor submission if filelist is empty
    for file in file_list:
      infile = infodict.get('prefix', '')+file 
      condor.write('arguments = %s %s %s %s\n'%(infile, infodict.get('analysis', ''),infodict.get('output', ''),infodict.get('filter', '')))
      condor.write('queue 1\n') #FIXME: remove multiple que statement
  
  # worker script to execute
  workerFile='%s/worker_%s.sh'%(FarmDirectory, jobname)
  with open(workerFile,'w') as worker:
    worker.write('#!/bin/bash\n')
    worker.write('startMsg="Job started on "`date`\n')
    worker.write('echo $startMsg\n')
    #worker.write('export HOME=%s\n'%os.environ['HOME']) #otherwise, 'dasgoclient' won't work on condor
    worker.write('source /cvmfs/cms.cern.ch/cmsset_default.sh\n')
    worker.write('export X509_USER_PROXY=%s\n'%os.environ['X509_USER_PROXY'])
    worker.write('########### INPUT SETTINGS ###########\n')
    worker.write('input=${1}\n')
    worker.write('channel=${2}\n')
    worker.write('output=${3}\n')
    worker.write('filter=${@:4}\n')
    worker.write('filename=`echo ${1} | rev | cut -d"/" -f1 | rev | cut -d"." -f1`\n')
    worker.write('######################################\n')
    worker.write('echo "worker_%s.sh arguments:"\n'%(jobname))
    worker.write('echo input="$input"\necho channel="$channel"\necho output="$output"\necho filter="$filter"\n')
    worker.write('######################################\n')
    worker.write('WORKDIR=/tmp/%s/${filename}; mkdir -pv $WORKDIR\n'%os.environ['USER'])
    worker.write('echo "Working directory is ${WORKDIR}"\n')
    worker.write('cd %s\n'%cmssw)
    worker.write('eval `scram r -sh`\n')
    worker.write('cd ${WORKDIR}\n')
    worker.write('echo "INFO: Run ntuplizer"\n')
    worker.write('echo "python3 $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py \\\\"\n')
    worker.write('echo "$filename ${input}  \\\\"\n')
    worker.write('echo "--bi $CMSSW_BASE/src/BsTauTau/nanoSkimmer/scripts/keep_in.txt   \\\\"\n')
    worker.write('echo "--bo $CMSSW_BASE/src/BsTauTau/nanoSkimmer/scripts/keep_out.txt  \\\\"\n')
    worker.write('echo "${filter} -I BsTauTau.nanoSkimmer.Flattener_analysis ${channel} "\n')
    worker.write('python3 $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py \\\n')
    worker.write('$filename ${input}  \\\n')
    worker.write('--bi $CMSSW_BASE/src/BsTauTau/nanoSkimmer/scripts/keep_in.txt   \\\n')
    worker.write('--bo $CMSSW_BASE/src/BsTauTau/nanoSkimmer/scripts/keep_out.txt  \\\n')
    worker.write('${filter} -I BsTauTau.nanoSkimmer.Flattener_analysis ${channel} \n')
    worker.write('echo cp ${filename}/${filename}_Skim.root ${output}/${filename}_Skim.root\n')
    worker.write('cp ${filename}/${filename}_Skim.root ${output}/\n')
    worker.write('\necho clean output\ncd ../\nrm -rf ${WORKDIR}\n')
    worker.write('echo ls; ls -l $PWD\n')
    worker.write('echo $startMsg\n')
    worker.write('echo job finished on `date`\n')
  
  os.system('chmod u+x %s'%(workerFile))

  return condorFile


def split_input(opt, FarmDirectory):
  """ split the submission by samples """

  condorfiles = []
  
  datasets = open(opt.input).read().splitlines()
  if len(datasets) == 0:
    log.print_error(' Input file {} is empty!'.format(opt.input))
    sys.exit(1)
  
  # -- loop on datasets --
  for dataset in datasets:
    if "#" in dataset or len(dataset)<2: continue
    if not fnmatch(dataset, opt.filter) : continue
    log.print_info('Processing %s'%(dataset))
    
    sufix=''
    prefix=''
    year=opt.year
    print(dataset.split('/'))
    if 'NanoAODv9' in dataset or 'NanoAODAPVv9' in dataset: # data from DAS
      dataset_name = '_'.join(dataset.split('/')[1:3])
      year=dataset.split('UL')[1][:4]
      if 'UL1' in dataset:
        year="20"+str(dataset.split('UL')[1][:2])
      sufix='data'
      cmd='dasgoclient --query=\"file dataset={} status=*\"'.format(dataset)
      file_list=os.popen(cmd).read().split()
      prefix='root://cms-xrd-global.cern.ch/'
    elif 'eos' in dataset.split('/'):
      sufix='mc' 
      dataset_name = dataset.split('/')[-3]+"_"+dataset.split('/')[-1]
    
    if "SingleMu" in dataset_name or "doublemu" in dataset_name or "muonEG" in dataset_name or "egamma" in dataset_name:
      sufix='data'
    
    file_list = glob.glob(dataset+'/*.root')
    print('\tdataset | suffix | year | #files: {0} | {1} | {2} | {3}'.format(dataset_name,sufix,year, len(file_list)))
    
    if len(file_list) == 0:
      log.print_error('found invalid dataset "{}" stop the code'.format(dataset))
      sys.exit(1)

    channels=['ee', 'mumu', 'e', 'mu']#['emu'] #FIXME
    yearmodified=year
    if "preVFP" in dataset and year=="2016" and (sufix=="mc" or sufix=="sig"):
        yearmodified="2016pre"
    if "preVFP" not in dataset and year=="2016" and (sufix=="mc" or sufix=="sig"):
        yearmodified="2016post"

      
    #prepare output
    output=opt.output+'/'+dataset_name
    # -- loop on channels --
    for channel in channels:
      
      output_full=output+"_"+channel
      os.system('mkdir -p {}'.format(output_full))
      
      # apply filter to data: trigger and GRL
      if opt.isdata:
        filter=eracfg.ANALYSISCUT['data'][year][channel]
      else:
        filter=eracfg.ANALYSISCUT['mc'][year][channel]
      print ("\t ({0}) filter : {1} ".format(year, filter))
      

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
      
      #for file in file_list: # FIXME : bypassed for the moment
      #  outfile='%s/%s'%(output_full,os.path.basename(file).replace('.root','_Skim.root'))
      #  if os.path.isfile(outfile) and not opt.force: continue

      #  #condor.write('arguments = %s %s %s %s\n'%(prefix+file,'analysis_'+channel+sufix+yearmodified,output_full,filter))
      #  #condor.write('queue 1\n')

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
    parser.add_option('--filter',     dest='filter',    help='(optional) string to filter input datasets. POSIX regular expression allowed',    default='*', type='string')
    parser.add_option('--isdata',           dest='isdata',    help='flag to run on data (apply GRL and specific trigger selection)', action='store_true')
    parser.add_option('-y', '--year',       dest='year',      help='data-taking year to process',    default='2018', type='string')
    parser.add_option('-t', '--tag',        dest='tag',       help='tag for your task | not affecting the output ntuple structure', default='')
    parser.add_option('-o', '--out',        dest='output',    help='output directory',          default='/eos/cms/store/group/phys_bphys/cbasile/BsTauTau-ttbar/test2018/', type='string') #EDIT THIS
    parser.add_option('-f', '--force',      dest='force',     help='force resubmission',        action='store_true')
    parser.add_option('-s', '--submit',     dest='submit',    help='submit jobs',               action='store_true')
    (opt, args) = parser.parse_args()
     
    if not os.path.isfile(opt.input): 
      print('ERROR: bad input file (%s)'%opt.input)
      sys.exit(1)
	
    #prepare directory with scripts
    jobtag = '_'.join([
      opt.year,
      opt.tag,
    ])
    FarmDirectory = os.path.join(os.environ['PWD'], "FarmLocalNtuple_{}".format(jobtag))
    if not os.path.exists(FarmDirectory):  os.system('mkdir -vp '+FarmDirectory)
    print('\n')
    log.print_info(' IMPORTANT MESSAGE - RUN THE FOLLOWING SEQUENCE:')
    print('\tvoms-proxy-init --voms cms --valid 72:00 --out %s/myproxy509\n'%FarmDirectory)
    os.environ['X509_USER_PROXY']='%s/myproxy509'%FarmDirectory

    condorfiles = split_input(opt,FarmDirectory)
    print('\n----------------------')
    log.print_success('')
    # handle job submission within the Singularity
    # FIXME: handle the submitter.sh
    if opt.submit:
      log.print_info('Prepare `submitter.sh` to submit the jobs with condor_submit')
      with open('submitter.sh','w') as submitter:
        submitter.write('#!/bin/bash\n')
        for condor_script in condorfiles: 
          log.print_exe('condor_submit {}\n'.format(condor_script), logger=submitter)
          #if opt.submit:
            #submitter.write('condor_submit {}\n'.format(condor_script))
            #os.system('condor_submit {}'.format(condor_script))
        submitter.write('echo "DONE | all jobs submitted"\n')
    else: 
      print('Just print commands')
      for condor_script in condorfiles: 
        log.print_exe('condor_submit {}\n'.format(condor_script))
		

if __name__ == "__main__":
    sys.exit(main())
