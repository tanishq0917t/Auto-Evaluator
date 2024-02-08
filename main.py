import subprocess
import os
import json

def loadData():
    with open('data.json','r') as dataFile:
        a=json.load(dataFile)
        directory=a['directory']
        files=a['files']
        return (directory,files)

directory,files=loadData()
print(directory)
print(files)

mainResult={}

def list_zip_files(directory):
    return [file for file in os.listdir(directory) if file.endswith(".zip")]

def list_cpp_files(directory):
    return [file for file in os.listdir(directory) if file.endswith(".cpp")]

def list_c_files(directory):
    return [file for file in os.listdir(directory) if file.endswith(".c")]

def list_py_files(directory):
    return [file for file in os.listdir(directory) if file.endswith(".py")]

def compileCPP(files):
    count=0
    for i in files:
        fileName=i[0:-4]
        with open(f'error_{fileName}.txt','w') as errorFile:
            subprocess.run(["g++",i,"-o",f"{fileName}.out"],stderr=errorFile)
        if len(open(f'error_{fileName}.txt','r').read())>0:
            print(f"Error while compiling code for {i}")
            subprocess.run(["rm",f"error_{fileName}.txt"])
        else:
            print(f"Successfully compiled {i}")
            #print(f'{directory}/input_{fileName}.txt')
            with open(f'{directory}/input_{fileName}.txt','r') as inputFile:
                with open(f'output_{fileName}_code.txt','w') as codeOutputFile:                
                    subprocess.run([f"./{fileName}.out"],stdin=inputFile,stdout=codeOutputFile)
            actualOutput=open(f'{directory}/output_{fileName}.txt','r').read().strip()
            currentOutput=open(f'output_{fileName}_code.txt','r').read().strip()
            subprocess.run(["rm",f"output_{fileName}_code.txt"])
            subprocess.run(["rm",f"{fileName}.out"])
            #print(actualOutput)
            #print(currentOutput)
            if actualOutput==currentOutput:
                print(f"Output Matches for {i}")
                count+=1
            else:
                print(f"Output doesn't matches for {i}")
    return count


        

def compileC(files):
    count=0
    for i in files:
        fileName=i[0:-2]
        with open(f'error_{fileName}.txt','w') as errorFile:
            subprocess.run(["gcc",i,"-o",f"{fileName}.out"],stderr=errorFile)
        if len(open(f'error_{fileName}.txt','r').read())>0:
            print(f"Error while compiling code for {i}")
            subprocess.run(["rm",f"error_{fileName}.txt"])
        else:
            print(f"Successfully compiled {i}")
            # print(f'{directory}/input_{fileName}.txt')
            with open(f'{directory}/input_{fileName}.txt','r') as inputFile:
                with open(f'output_{fileName}_code.txt','w') as codeOutputFile:                
                    subprocess.run([f"./{fileName}.out"],stdin=inputFile,stdout=codeOutputFile)
            actualOutput=open(f'{directory}/output_{fileName}.txt','r').read().strip()
            currentOutput=open(f'output_{fileName}_code.txt','r').read().strip()
            subprocess.run(["rm",f"output_{fileName}_code.txt"])
            subprocess.run(["rm",f"{fileName}.out"])
            #print(actualOutput)
            #print(currentOutput)
            if actualOutput==currentOutput:
                print(f"Output Matches for {i}")
                count+=1
            else:
                print(f"Output doesn't matches for {i}")
    return count

def compilePy(files):
    count=0
    for i in files:
        fileName=i[0:-3]
        with open(f'error_{fileName}.txt','w') as errorFile:
            with open(f'{directory}/input_{fileName}.txt','r') as inputFile:
                with open(f'output_{fileName}_code.txt','w') as codeOutputFile:
                    subprocess.run(["python3",i],stderr=errorFile,stdin=inputFile,stdout=codeOutputFile)
        if os.stat(f'error_{fileName}.txt').st_size!=0:
            print("Error")
        else:
            actualOutput=open(f'{directory}/output_{fileName}.txt','r').read().strip()
            currentOutput=open(f'output_{fileName}_code.txt','r').read().strip()
            subprocess.run(["rm",f"output_{fileName}_code.txt"])
            if actualOutput==currentOutput:
                print(f"Output Matches for {i}")
                count+=1
            else:
                print(f"Output doesn't matches for {i}")
    return count


def printAll():
    print(list_cpp_files("."))
    print(list_c_files("."))
    print(list_py_files("."))

def compileAll():
    a=compileCPP(list_cpp_files("."))
    b=compileC(list_c_files("."))
    c=compilePy(list_py_files("."))
    return a+b+c






lst=list_zip_files(".")
print(lst)
for i in lst:
    subprocess.run(["unzip",i])
    subprocess.run(["rm","-r",i])

#print(lst[0][0:-4])
for i in lst:
    os.chdir(i[0:-4])
    subprocess.run(["pwd"])
    #printAll()
    mainResult[i[0:-4]]=compileAll()
    #subprocess.run(["ls"])
    os.chdir("../")

print(mainResult)
