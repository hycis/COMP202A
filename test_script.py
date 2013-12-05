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
    
    tmpfile.write("import java.util.Arrays;")
    
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
                            
            else:
                tmpfile.write(line)
                    
           
    
    f.close()
    tmpfile.close()
                    
                    
def run_save(root, javafile):
    
    '''
    run and compile the temp java files and save to output text files
    '''
    os.chdir(root)
    
#     javafile = javafile.rstrip('.java') + 'tmp.java'
    
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
                    print 'processing: ', file, ' == ', root.split('/')[-1]
                    if testCases[file] is not "":
                        insert_test_cases(root, file, testCases[file])
                        run_save(root, file.rstrip('.java') + 'tmp.java')
                    else:
                        run_save(root, file)
                    print 'process done!', file, ' == ', root.split('/')[-1]
                except:
                    print sys.exc_info()[0]
                    with open(root+'/errors.txt', 'w') as err:
                        err.write(str(sys.exc_info()[0]))


if __name__ == "__main__":

    testCases = {'ArrayUtilities.java': '''
                    int[] arr = {8, 35, 23, 53, 1, 3, 100, 432, 10, 0};
                    int[] sorted = {0, 1, 3, 8, 35, 47, 54, 57, 89, 90};
                    System.out.println("boolean linearSearch(int[] array, int target)");
                    System.out.println("TRUE");
                    System.out.println(linearSearch(arr, 0));
                    System.out.println(linearSearch(arr, 432));
                    System.out.println(linearSearch(arr, 53));
                    System.out.println("FALSE");  
                    System.out.println(linearSearch(arr, 2));
                    System.out.println(linearSearch(arr, 500));
                    System.out.println(linearSearch(arr, -1));

                    System.out.println("boolean binarySearch(int[] array, int target)");
                    System.out.println("TRUE");
                    System.out.println(binarySearch(sorted, 0));
                    System.out.println(binarySearch(sorted, 35));
                    System.out.println(binarySearch(sorted, 90));
                    System.out.println("FALSE");  
                    System.out.println(binarySearch(sorted, 2));
                    System.out.println(binarySearch(sorted, 500));
                    System.out.println(binarySearch(sorted, -1));

                    System.out.println("void sort(int[] array)");
                    System.out.println("original array" + Arrays.toString(arr));
                    sort(arr);
                    System.out.println("sorted array" + Arrays.toString(arr));

                    System.out.println("int[] copy(int[] array)");
                    int [] copied = copy(arr);
                    System.out.println("copied array" + Arrays.toString(copied));  



                    System.out.println("int[] generateRandom(int 5)"); 
                    System.out.println(Arrays.toString(generateRandom(5)));
                    ''',
                    'StopWatch.java':'''
                    StopWatchtmp watch = new StopWatchtmp();
                    watch.start();
                    for (int i = 0; i < 100; i++)
                    {
                    System.out.println(i);
                    }
                    watch.stop();
                    System.out.println("It took " + watch.getTimeNano() + " nanoseconds to complete that task");
                    '''
                    }
                
    folder = '/Users/Hycis/Documents/comp202/'
  
    runTest(testCases, folder)
    


 
