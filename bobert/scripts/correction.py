import json

def correct(prevInput, currInput, jsonFile):
    currInputArray = currInput.split()
    newTag = currInputArray[-1]
    foundTag = False
    output = ""

    try:
        with open(jsonFile, "r") as file:
            data = json.load(file)
    except:
        return "JSON file was not found"
    
    for intent in data["intents"]:
        if intent["tag"] == newTag:
            intent["patterns"].append(prevInput)
            foundTag = True
            break
    
    if foundTag:
        with open(jsonFile, "w") as file:
            json.dump(data, file)
            output = f"Okay, I will remember that, '{prevInput}', is a {newTag}"
    else:
        output = f"'{newTag}' tag doesn't exist"
    
    return output

print(correct("hello", "hi weathertoday", "temp.json"))
    
    
    
