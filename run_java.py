import os.path,subprocess
from subprocess import STDOUT,PIPE
import glob
from zipfile import ZipFile
import subprocess
#import pexpect

def compile_java2(java_file):
    subprocess.check_output(['javac', java_file])

def execute_java2(java_file, stdin):
    #import pdb
    #pdb.set_trace()
    java_class, ext = os.path.splitext(java_file)
    cmd = ['java', java_class]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    # for str in stdin:
    #     print str
    #import pdb
    #pdb.set_trace()
    print "finished writing"
    #proc.stdin.flush()
    for line in iter(proc.stdout.readline, ''):
        proc.stdin.write("123")
        print line
    #proc.stdin.close()
    #proc.stdin.write("456")
    #proc.stdin.flush()
    #print proc.stdout.readline()
    #proc.stdin.close()
    
    #proc.stdout.close()
    #stdout1, stderr1 = proc.communicate("123")
    #stdout2, stderr2 = proc.communicate("456")
    
    #print ('This was "' + stdout1 + '"')
    #print (out1)

#compile_java('Hi.java')
#execute_java2('Hi.java', "123")

import sys
import os.path,subprocess

def compile_java(java_file):
    subprocess.check_call(['javac', java_file])

def execute_java(java_file):
    java_class,ext = os.path.splitext(java_file)
    cmd = ['java', java_class]
    return subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

def run_java(java_file):
    compile_java(java_file)
    process = execute_java(java_file)
    #for i in range(10):
    process.stdin.write("123")
    #out = process.wait()
    #line = process.stdout.read()
    #print line


def unzip(path):
    
    #output = open('grading.txt', 'w')
    
    folders = glob.glob(path+'/Assignment*')
    for folder in folders:
        zipfiles = glob.glob(folder + '/*.zip')
        for zipfile in zipfiles:
            #print zipfile
            #output.write(zipfile)
            
            myzip = ZipFile(zipfile)
            myzip.extractall(path=zipfile.rstrip('.zip'))
            #import pdb
            #pdb.set_trace()
            file_list = myzip.namelist()
            #if 'MathTrick.java' in file_list:
             #   out = myzip.extract('MathTrick.java')
                
            
            
            #print file_list
            myzip.close()
                

import sys
import os.path,subprocess

def compile_java3(java_file):
    subprocess.check_call(['javac', java_file])

def execute_java3(java_file):
    java_class,ext = os.path.splitext(java_file)
    cmd = ['java', java_class]
    return subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

def run_java3(java_file):
    compile_java(java_file)
    process = execute_java(java_file)
    for i in range(10):
        process.stdin.write(str(i) + "\n")

def run_Hi():
    pexpect.spawn("javac Hi.java")
    child = pexpect.spawn("java Hi")
    child.expect("")
    child.send("123")
    child.send("456")
    #child.echo()
    print child.readline()


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

if __name__ == '__main__':
    #question1()
    #execute_java2("Hi.java")
    #run_Hi()
    #("Hi.java")
    import argparse
    parser = argparse.ArgumentParser(description='assignment folder path')
    parser.add_argument('-p', '--path')
    args = parser.parse_args()
    print args
    #unzip(args.path)
    compilefiles(args.path)
    