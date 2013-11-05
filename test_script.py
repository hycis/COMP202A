
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
    
    in_main = False

    for line in f:
        
        if 'class ' + just_name in line:
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
    f.close()
    tmpfile.close()
                    
                    
def run_save(root, javafile):
    
    '''
    run and compile the temp files
    '''
    os.chdir(root)
    
    javafile = javafile.rstrip('.java') + 'tmp.java'
    
    javapath = root + '/' + javafile
    output = javapath.rstrip('.java') + '.txt'
    subprocess.check_call(['javac', javafile], stdout=subprocess.PIPE)
    p2 = Popen(['java', javafile.rstrip('.java')], stdout=subprocess.PIPE)
    out, err = p2.communicate()
    with open(output, 'w') as f:
        if out is not None:
            f.write(out)
        if err is not None:
            f.write(err)
                    
def runTest(testCases, folder):
    
    for root, dirnames, filenames in os.walk(folder):
        for file in fnmatch.filter(filenames, '*.java'):
            
            if testCases.get(file) is not None:
                try:
                    print root
                    insert_test_cases(root, file, testCases[file])
                    run_save(root, file)
                    print 'done!'
                except:
                    print sys.exc_info()[0]
                    
                    with open(root+'/errors.txt', 'w') as err:
                        err.write(str(sys.exc_info()[0]))


if __name__ == "__main__":

    testCases = {'Question1.java': '''
                 System.out.println("=TRUE=");  
                 System.out.println("HIJ" + isConsecutive("HIJ"));  
                 System.out.println("JIH" + isConsecutive("JIH"));  
                 System.out.println("123" + isConsecutive("123"));  
                 System.out.println("876" + isConsecutive("876"));  
                 System.out.println("901" + isConsecutive("901"));  
                 System.out.println("109" + isConsecutive("109"));  
                 System.out.println("=FALSE=");  
                 System.out.println("bcbc" + isConsecutive("bcbc"));  
                 System.out.println("2323" + isConsecutive("2323"));
                 ''',
                'Question2.java': '''
                System.out.println("==============");
                System.out.println("DrawMeCircle(10, 5, 5)");
                drawMeACircle(10, 5, 5);
                System.out.println("DrawMeCircle(10, 10, 5)");
                drawMeACircle(10, 10, 5);
                System.out.println("DrawMeCircle(15, 5, 5)");
                drawMeACircle(15, 5, 5);
                System.out.println("DrawMeCircle(10, 10, 10)");
                drawMeACircle(10, 10, 10);
                ''',
                'Question3.java': '''
                System.out.println("==============");
                System.out.println("DrawMeAnEllipse(10, 5, 5, 1)");
                drawMeAnEllipse(10, 5, 5, 1);
                System.out.println("DrawMeAnEllipse(10, 10, 5, 10)");
                drawMeAnEllipse(10, 10, 5, 10);
                System.out.println("DrawMeAnEllipse(15, 10, 10, 5)");
                drawMeAnEllipse(15, 10, 10, 5);
                '''
                }
    
    folder = '/Users/zhenzhou/Documents/COMP202A_Markings/Assignment_2/'
    
    # The script search through all the java files in the folder, insert test cases into main method, and save the output from the run to text file. You can then look at the output result to compare with the standard answer.
    runTest(testCases, folder)
    

 
