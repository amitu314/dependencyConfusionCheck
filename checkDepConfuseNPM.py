import os
import re
import requests
from pathlib import Path
from git import Repo
import json

def npmCheck(packageName):

   pypiURL = f'https://registry.npmjs.org/{packageName}'

   try:

       response =  requests.get(pypiURL,timeout=5)

       if response.status_code == 200:

           return True

       else:

           return False

   except Exception as e:

       print(f"Error checking NPM for {packageName}: {e}")

       return False



def checkDependencyConfusionNPM(reqFilePath):

   print(f"""Checking dependency confusion in file: {reqFilePath}

         """)

   package = set()

   npmPackages = {}

   try:

       with open(reqFilePath, 'r', encoding='utf-8', errors='ignore') as reqFile:

           linesData = json.load(reqFile)

           npmPackages.update(linesData.get('devDependencies',{}))

           npmPackages.update(linesData.get('dependencies',{}))

           #print(npmPackages)

          

           for pkgV in npmPackages.keys():

               normalizePkgName = re.sub(r"[-_]+", "-", pkgV).lower().strip()

               npmCheckResult = npmCheck(normalizePkgName)

               if not npmCheckResult:

                   print(f"Potential Dependency Confusion package found: {normalizePkgName} in file {reqFilePath}")

                   with open('potentialDependencyConfusionPackageNPM.txt', 'a', encoding='utf-8', errors='ignore') as potentialdepFile:

                       potentialdepFile.write(f"{normalizePkgName} | {reqFilePath}\n")

               else:

                    with open('notDependencyConfusionUniqPackageNPM.txt', 'a', encoding='utf-8', errors='ignore') as depWriteFile:

                                   depWriteFile.write(f"{normalizePkgName}\n")



   except Exception as e:

       print(f"Error reading {reqFilePath}: {e}")

       return



if __name__ == "__main__":

   repoPath = './<your/path/to/repo>/'

   #repoPath = Path('<path_to_your_repository_in_windows>')

   requireRePatternNPM = r'(^package.json$)'

   #with open ('dependencyConfusion.txt', 'w',encoding='utf-8', errors='ignore') as credFile:

   for root, dirs, files in os.walk(repoPath):

       #print(f"Checking directory: {root}| Dir {dirs}| Files: {files}")

       for file in files:

           matchNPM = re.findall(requireRePatternNPM, file)

           if matchNPM:

               reqFilePath = os.path.join(root, file)

               checkDependencyConfusionNPM(reqFilePath)


