# Created by : Zhenzhou Wu, zhenzhou.wu@mail.mcgill.ca

# The script search through all the java files in the folder, 
# insert test cases into main method, and save the output from 
# the run to text file. You can then look at the output result 
# to compare with the standard answer. To apply this script, all
# zip folders should be unzipped

import os
import fnmatch
from subprocess import Popen
import subprocess
import re
import time
import sys

def insert_test_cases(root, file, testCase):
    
    '''
    empty the main method, insert test cases into main method, and save
    it into a temp java file.
    '''
    
    just_name = file.rstrip('.java')
    
    tmp = root + '/' + just_name + 'tmp.java'
    tmpfile = open(tmp, 'w')
    
    f = open(root+'/'+file, 'r')
    ls = []
    appearFirstTime = True
    continue_writing = True
    
    have_main = False
    in_main = False
        
    for line in f:
    
        if 'static void main' in line:
            have_main = True
            break
    
    f.seek(0)
    
    if have_main:
        for line in f:
            if 'class ' + just_name in line:
                new_line = line.replace(just_name, just_name + 'tmp')
                tmpfile.write(new_line)
                
                
            elif 'public ' + just_name in line or 'private ' + just_name in line: 
                new_line = line.replace(just_name, just_name + 'tmp')
                tmpfile.write(new_line)
            
            elif continue_writing:
                tmpfile.write(line)
                
            
            if 'static void main' in line:
                in_main = True
                continue_writing = False
            
                if '{' in line:
                    ls += [m.start() for m in re.finditer('{', line)]
                    appearFirstTime = False
                
            
            elif in_main:
                if '{' in line:            
                    if appearFirstTime:
                        ls += [m.start() for m in re.finditer('{', line)]
                        tmpfile.write('{' + '\n')
                        appearFirstTime = False
                
                    else:
                        ls += [m.start() for m in re.finditer('{', line)]
                        
                if '}' in line:
                    close_brace = [m.start() for m in re.finditer('}', line)]
                    for ele in close_brace:
                        ls.pop()
                    
            
                if len(ls) == 0:
                    tmpfile.write(testCase + '\n' + '}' + '\n')
                    in_main = False
                    continue_writing = True 
                    
    else:
    
        for line in f:
            if 'class ' + just_name in line:
                new_line = line.replace(just_name, just_name + 'tmp')
                tmpfile.write(new_line)
                
                if '{' in new_line:
                    appearFirstTime = False
                    tmpfile.write("public static void main(String[] args){" + '\n' + 
                    testCase + '\n' + '}' + '\n')
                                
            elif '{' in line and appearFirstTime:
                tmpfile.write(line)
                appearFirstTime = False
                tmpfile.write("public static void main(String[] args){" + '\n' + 
                    testCase + '\n' + '}' + '\n')
              
            elif 'public ' + just_name in line or 'private ' + just_name in line: 
                new_line = line.replace(just_name, just_name + 'tmp')
                tmpfile.write(new_line)
                          
            else:
                tmpfile.write(line)
                    
           
    
    f.close()
    tmpfile.close()
                    
                    
def run_save(root, javafile):
    
    '''
    run and compile the temp java files and save to output text files
    '''
    os.chdir(root)
    
    javapath = root + '/' + javafile
    output = javapath.rstrip('.java') + '_output.txt'
    with open(output, 'w') as f:
    
        subprocess.check_call(['javac', javafile], stdout=f, stderr=f)
    
        print "compiled successfully"

        Popen(['java', javafile.rstrip('.java')], stdout=f, stderr=f)

        print "run successfully"
        
                    
def runTest(testCases, folder):
    
    for root, dirnames, filenames in os.walk(folder):
        for file in fnmatch.filter(filenames, '*.java'):
            
            if testCases.get(file) is not None:

                try:
                    print 'processing: ', file, ' == ', root.split('/')[-1]

                    if testCases[file] is not "":
                        insert_test_cases(root, file, testCases[file])
                        run_save(root, file.rstrip('.java') + 'tmp.java')
                    else:
                        run_save(root, file)

                    print 'process done!', file, ' == ', root.split('/')[-1]
                except:
                    print 'complete with errors'


if __name__ == "__main__":

    testCases = {'Agent.java': '''
                    Agent a = new Agent();
                    System.out.println("getCityNow: " + a.getCityNow());
                    System.out.println("getCityBorn: " + a.getCityBorn());
                    System.out.println("getName: " + a.getName());
                    System.out.println("getGender: " + a.getGender());
                    System.out.println("getMajor: " + a.getMajor());
                    System.out.println("getBirthday: " + a.getBirthday());
                    a.sayHello();
                    a.sayCityBorn();
                    a.howOldAreYou();
                    a.sayGender();
                    a.sayCityNow();
                    a.sayMajor();
                    '''
                    }
                
#     folder = '/Users/Hycis/Documents/COMP202A/'
    folder = '/Users/Hycis/Documents/COMP202A/Assignment%204%20Download%20Dec%2013%2C%202013%201012%20AM-2/James Bodzay - Dec 8, 2013 247 PM - Assignment 4-James Bodzay'
    runTest(testCases, folder)
    


 
