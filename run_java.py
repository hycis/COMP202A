import os.path,subprocess
from subprocess import STDOUT,PIPE
import glob
from zipfile import ZipFile
import subprocess

import sys
import os.path,subprocess

def unzip(path):    
    folders = glob.glob(path+'/Assignment*')
    for folder in folders:
        zipfiles = glob.glob(folder + '/*.zip')
        for zipfile in zipfiles:
            myzip = ZipFile(zipfile)
            myzip.extractall(path=zipfile.rstrip('.zip'))
            file_list = myzip.namelist()
            myzip.close()
    print 'unzip completed'
                


def compilefiles(path):
    
    folders = glob.glob(path+'/Assignment*')
    
    for folder in folders:
        subfolders = glob.glob(folder + '/*') 
        for subfolder in subfolders:
            print 'compile:', subfolder
            if os.path.isdir(subfolder):
                javafiles = glob.glob(subfolder + '/*.java')
                #print javafiles
                #lst = ['javac'] + javafiles
                #print 'hahahah====', lst
                subprocess.Popen(['javac']+ javafiles)
    print 'compile completed'

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description='assignment folder path')
    parser.add_argument('-p', '--path')
    args = parser.parse_args()
    print args
    unzip(args.path)
#   compilefiles(args.path)
    