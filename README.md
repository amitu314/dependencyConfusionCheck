This scripts helps you identify dependency confusion in your Project. Currently, this supports Python and Javascript/TypeScript. 

*Note: This is version 1 of the script and may need some fine tuning.*

# how to run

- First, run the cloneRepo script or manually clone the repo you want to scan [Note: You will have to change the repo['language'] based on what language you want to use this for.
- For Python Dependency Confusion, Go to the cloned folder and then run `checkDepConfusion.py`
- For JS/TS Dependency Confusion, Go to the cloned folder and then run `checkDepConfusionNPM.py`


# Prerequisite

- You will need Github token

# Output

- Based on what Check you ran (checDepConfusion.py OR checkDepConfusionNPM.py) this will create a `potentialDependencyConfusionPackage.txt` file with the potential  Python Dependency Confusion OR `potentialDependencyConfusionPackageNPM.txt` file with the potential  JS/TS Dependency Confusion
