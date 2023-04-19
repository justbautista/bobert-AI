import os
import fnmatch

def find(pattern, path):
    if "." not in pattern:
        newPattern = f"*{pattern}*"
    
    resultFiles = []
    resultDirs = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, newPattern):
                resultFiles.append(os.path.join(root, name))
        
        for name in dirs:
            if fnmatch.fnmatch(name, newPattern):
                resultDirs.append(os.path.join(root, name))

    return formatOutput(resultFiles, resultDirs)

def formatOutput(files, dirs):
    output = "This is what I found:\n\n"

    if (len(files) != 0):
        output += "Files:\n"

        for file in files:
            output += f"\t{file}\n"

    if (len(dirs) != 0):
        output += "Directories:\n"

        for dir in dirs:
            output += f"\t{dir}\n"
        
    return output