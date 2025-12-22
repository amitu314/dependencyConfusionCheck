import os
import re
import requests
from pathlib import Path
from git import Repo


def pypiCheck(packageName):
   pypiURL = f'https://pypi.org/pypi/{packageName}/json'
   try:
       response =  requests.get(pypiURL,timeout=5)
       if response.status_code == 200:
           return True
       else:
           return False
   except Exception as e:
       print(f"Error checking PyPI for {packageName}: {e}")
       return False




def checkDependencyConfusion(reqFilePath):
   print(f"""Checking dependency confusion in file: {reqFilePath}
         """)
   package = set()
   try:
       with open(reqFilePath, 'r', encoding='utf-8', errors='ignore') as reqFile:
           lines = reqFile.readlines()
           #print(lines)
           for pkgV in lines:
               pkgVal = pkgV.strip()
               if pkgVal and not pkgVal.startswith('#') and not pkgVal.startswith('--') and not pkgVal.startswith('-e') and not pkgVal.startswith('-') :
                       if ';' in pkgVal:
                           pkgVal = pkgVal.split(';')[0]
                       if '[' in pkgVal:
                           pkgVal = pkgVal.split('[')[0]
                       
                       if pkgVal.startswith(('git+', 'http:', 'https:', '.', '/')):
                               if 'egg=' in pkgVal:
                                   val = re.search(r'egg=([A-Za-z0-9_.-]+)', pkgVal)
                                   if val:
                                       pkgVal= val.group(1)
                               
                       pkgVal = pkgVal.lstrip('\ufeff').strip()
                       justPkgName = pkgVal.split('===')[0].split('==')[0].split('~=')[0].split('!=')[0].split('>=')[0].split('<=')[0].split('>')[0].split('<')[0].strip()
                       normalizePkgName = re.sub(r"[-_.]+", "-", justPkgName).lower().strip()
                       #print(f"{normalizePkgName}|{reqFilePath}")
                       
                       
                       
                       if not os.path.exists("notDependencyConfusionUniqPackage.txt"):
                           with open("notDependencyConfusionUniqPackage.txt", "a", encoding="utf-8"):
                               pass

    
                       with open('notDependencyConfusionUniqPackage.txt', 'r', encoding='utf-8', errors='ignore') as depReadFile:
                           depReadFileContent = depReadFile.read().splitlines()
                       if normalizePkgName not in depReadFileContent:
                           #print(f"Checking package: {normalizePkgName}")
                           pypiCheckResult = pypiCheck(normalizePkgName)
                           if pypiCheckResult:
                               #print(f"Package {normalizePkgName} exists on PyPI.")
                               with open('notDependencyConfusionUniqPackage.txt', 'a', encoding='utf-8', errors='ignore') as depWriteFile:
                                   depWriteFile.write(f"{normalizePkgName}\n")
                           else:
                               print(f"Potential Dependency Confusion package found: {normalizePkgName} in file {reqFilePath}")
                               with open('potentialDependencyConfusionPackage.txt', 'a', encoding='utf-8', errors='ignore') as potentialdepFile:
                                   potentialdepFile.write(f"{normalizePkgName}\n")
                       
                        

   except Exception as e:
       print(f"Error reading {reqFilePath}: {e}")
       return 

if __name__ == "__main__":
   repoPath = './<path/to/your/repo>/'
   #repoPath = Path('<path_to_your_repository_in_windows>')
   #requireRePattern = r'(.+|^)requirements\.txt$'
   requireRePattern = r'(.+|^)requirements\.txt$|^requirements(?:-[A-Za-z0-9_.-]+)?\.txt$'
   #with open ('dependencyConfusion.txt', 'w',encoding='utf-8', errors='ignore') as credFile:
   for root, dirs, files in os.walk(repoPath):
       #print(f"Checking directory: {root}| Dir {dirs}| Files: {files}")
       for file in files:
           match = re.findall(requireRePattern, file)
           if match:
               reqFilePath = os.path.join(root, file)
               checkDependencyConfusion(reqFilePath)
