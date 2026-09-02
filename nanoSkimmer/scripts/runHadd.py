import os, sys
import glob
import optparse
import ROOT
ROOT.gROOT.SetBatch(True)
# my imports
import BsTauTau.nanoSkimmer.logger as log 
from .runPostJob import check_ROOTfile

'''
(!!!) with haddnano.py you can hadd no more than 1k files
'''

def main():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--inputDir", dest="inputDir", help="input directory")
    parser.add_option("-o", "--outputFile", dest="outputFile", help="output .root file")
    parser.add_option("-d", "--dryrun", dest="dryrun", action="store_true", default=False, help="print hadd command without executing it")
    parser.add_option("-f", "--force", dest="force", action="store_true", default=False, help="force overwrite of output file if it already exists")
    (options, args) = parser.parse_args()

    # input location and #directories
    inputDir    = options.inputDir
    paths = glob.glob("%s" % inputDir)
    directories = [d for d in paths if os.path.isdir(d)]
    log.print_info(" %d directories in %s" % (len(directories), inputDir))
    
    # output location
    outputFile = options.outputFile
    outputDir  = os.path.dirname(outputFile)
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
        log.print_info(" created output directory %s" % outputDir)
    if os.path.exists(outputFile):
        log.print_warning(" output file %s already exists, exiting" % outputFile)
        if options.force:
            log.print_warning(" force option enabled, overwriting %s" % outputFile)
            os.remove(outputFile)
        else:
            sys.exit(1)
    
    # loop over directories and hadd
    log.print_info(" hadd'ing files in %d directories" % len(directories)) 
    tmp_outputFiles = []
    for i, thisDir in enumerate(directories):
        print("\t> %s" % thisDir)
        inFiles     = "%s/*.root" % thisDir
        nFiles      = len(glob.glob(inFiles))
        if nFiles == 0:
            log.print_warning(" NO .root files found in %s, exiting" % thisDir)
            sys.exit(1)
        thisOutputFile = outputFile.replace(".root", "_%d.root" % i)
    
        # hadd command
        print("\t\thadding %d files --> %s" % (nFiles, thisOutputFile))
        cmd = "python3 $CMSSW_BASE/src/BsTauTau/nanoSkimmer/scripts/haddnano.py %s %s" % (thisOutputFile, inFiles)
        log.print_exe(cmd)
        if not options.dryrun: os.system(cmd)
        thisCheck = check_ROOTfile(thisOutputFile)
        # check output
        if not thisCheck["ok"] :
            log.print_error(" intermediate output file %s is not valid, exiting" % thisOutputFile)
            sys.exit(1)
        tmp_outputFiles.append(thisOutputFile)

    # final hadd
    if len(tmp_outputFiles) == 1:
        log.print_info("\tonly 1 file, renaming %s --> %s" % (tmp_outputFiles[0], outputFile))
        if not options.dryrun: os.rename(tmp_outputFiles[0], outputFile)     
    else:
        log.print_info("\thadding %d files --> %s" % (len(tmp_outputFiles), outputFile))
        for f in tmp_outputFiles:
            if not os.path.exists(f) and not options.dryrun:
                log.print_error(" intermediate output file %s not found, exiting" % f)
                sys.exit(1)
        #cmd = "python $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/haddnano.py %s %s" % (outputFile, " ".join(tmp_outputFiles))
        cmd = "python3 $CMSSW_BASE/src/BsTauTau/nanoSkimmer/scripts/haddnano.py %s %s" % (outputFile, " ".join(tmp_outputFiles))
        log.print_exe(cmd)
        if options.dryrun: return 0
        
        os.system(cmd)
        if not os.path.exists(outputFile):
            log.print_error(" final output file %s not found, exiting" % outputFile)
            return 1
        
        file = ROOT.TFile.Open(outputFile)
        if file.IsZombie():
            log.print_error(" final output file %s is zombie, exiting" % outputFile)
            return 1
        else :
            tree = file.Get('Runs')
            if tree.GetEntries()==0: 
                log.print_error(" final output file %s is empty, exiting" % outputFile)
                return 1
        file.Close()
        # remove intermediate files
        rmcmd = "rm -f %s" % " ".join(tmp_outputFiles)
        log.print_exe(rmcmd)
        os.system(rmcmd)
    if os.path.exists(outputFile):
        log.print_success(" final output: %s" % outputFile)

if __name__ == "__main__":
    sys.exit(main())
