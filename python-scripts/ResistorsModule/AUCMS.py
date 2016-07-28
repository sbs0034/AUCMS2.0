# External libraries needed
import visa, sqlite3, sys, os
# Keywords for the parsing function to look for in the device script files
deviceVar = {'currentToSource': 0, "voltageToSource": 0, "inputToClose": "", "inputSlot": "", "currentMeasured =": "", "currentMeasured=": "",
             "voltageMeasured =": "", "voltageMeasured=": "", "inputToOpen": 0, "tempuratureMeasured =":""}
# Connects to an existing database or creates one if it does not exist
operatingSystem = sys.platform
rawScriptPath = os.path.dirname(os.path.realpath(sys.argv[0]))
rawScriptPath = str(rawScriptPath)
print(rawScriptPath+" script path")
if operatingSystem == 'win32':
    rawScriptPath = rawScriptPath.split("\\")
else:
    rawScriptPath = rawScriptPath.split("/")
del rawScriptPath[0]
scriptPath = ""
for i in (rawScriptPath):
    scriptPath = scriptPath+"/"+i
UniversalDatabase = os.path.isfile(scriptPath+"/database.db")
conn = sqlite3.connect(scriptPath+"/database.db")

# Function to create GUI componets
def CreateUiComponet(componetFeatures):
    componet = ""
    # Gets the classes and IDs of the componet, if there was none speciefied it sets them to an empty string
    try:
        classes = componetFeatures["class"]
    except Exception:
        classes = ""
    try:
        ids = componetFeatures["id"]
    except Exception:
        ids = ""
    try:
        onClick = componetFeatures["ifPressed"]
    except Exception:
        onClick = ""
    if componetFeatures["type"] == "button":
        componet+='<button class="btn btn-raised btn-success '+classes+'" onclick="'+onClick+'">'+componetFeatures["label"]+"</button>"
    if componetFeatures["type"] == 'textInput':
        componet+='<div class="form-group label-floating"><label for="'+ids+'" class="control-label" style="font-weight: 600">'+componetFeatures["label"]+'</label><input type="text" class="form-control scriptInput'+classes+'" id="'+ids+'"></div>'
    if componetFeatures["type"] == "textArea":
        componet+='<div class="form-group label-floating"><label for="'+ids+'" class="control-label" style="font-weight: 600">'+componetFeatures["label"]+'</label><textarea class="form-control scriptInput '+classes+'" id="'+ids+'"></textarea></div>'
    if componetFeatures["type"] == "rawHTML":
        componet+=componetFeatures["html"]
    if componetFeatures['type'] == 'graph':
        componet+="<div id='dataGraph'></div>"
    if componetFeatures["type"] == "table":
        componet+='<table class="table" id="'+componetFeatures["id"]+'>'
        for rows in componetFeatures["rows"]:
            componet+='<tr class="tableRow">'
            for columns in rows:
                componet+="<td>"
                componet+=columns
                componet+='</td>'
            componet+='</tr>'
        # componet+="</table>"
    return(componet)

# Creates javascript
def CreateJS(js):
    script=""
    script+='<script>'
    script+=js
    script+="</script>"
    print(script)

# Function for creating a new database table
def CreateDatabaseTable(tableName, tableFields):
    conn.execute("CREATE TABLE "+"'"+str(tableName)+"'"+tableFields)
    conn.commit()

# Function for reading device code files and sending commands to them
def DeviceControl(device_file, option):

    # Finds the instruments address in the device_file
    def GetAddress(device_file):
        device_file = open(device_file, "r")
        file_read = device_file.readline().strip()
        while "address" not in file_read:
            file_read = device_file.readline().strip()
        read_after = file_read.index("=")
        address = (file_read[read_after + 1:])
        return address.strip()

    # Chages the variable in the device script file with what it is set to
    def VarrialbleChange(deviceCode):
        for line in range(len(deviceCode)):
            # Replaces the varriable in the device script with the varriable's definition set by the code
            for origVar, varDef in deviceVar.items():
                code = deviceCode[line]
                code = str(code)
                new_code = code.replace(str(origVar), str(varDef))
                deviceCode[line] = new_code.strip()
        return deviceCode

    # Finds any varraibles that will need to be returned by the instrument
    def FindMeasurmentVar(deviceCode):
        command_list_len = len(deviceCode)
        for line in range(len(deviceCode)):
            if "tempuratureMeasured" in deviceCode[line]:
                return ["tempuratureMeasured", line]
            if "currentMeasured" in deviceCode[line]:
                return ["currentMeasured", line]
            if "voltageMeasured" in deviceCode[line]:
                return ["voltageMeasured", line]
            else:
                pass
        return False

    # Finds the setup cdoe for the device
    def GetSetupCode(device_file):
        file = open(device_file, "r")
        file_read = file.readline().rstrip()
        while file_read != "setup code begin":
            file_read = file.readline().rstrip()
        file_read = file.readline().rstrip()
        setup_code_list = []
        while file_read != "setup code end":
            if file_read == "":
                pass
            else:
                setup_code_list.append(file_read)
            file_read = file.readline().rstrip()
        return setup_code_list

    # Gets the main code for the device
    def GetMainCode(device_file):
        file = open(device_file, "r")
        file_read = file.readline().strip()
        while file_read != "main code begin":
            file_read = file.readline().strip()
        file_read = file.readline().strip()
        main_code_list = []
        while file_read != "main code end":
            if file_read == "":
                pass
            else:
                main_code_list.append(file_read)
            file_read = file.readline().strip()
        return main_code_list

    # Gets the finishing code for the device
    def GetFinishCode(device_file):
        file = open(device_file, "r")
        file_read = file.readline().strip()
        while file_read != "finish code begin":
            file_read = file.readline().strip()
        file_read = file.readline().strip()
        finish_code_list = []
        while file_read != "finish code end":
            if file_read == "":
                pass
            else:
                finish_code_list.append(file_read)
            file_read = file.readline().strip()
        return finish_code_list

    # Attempts to connect to the instrument
    inst = visa.ResourceManager()
    # inst = visa.ResourceManager('@py')
    try:
        inst = inst.open_resource(str(GetAddress(device_file)))
    except:
        return ("Cannot connect to device")
    # Runs the setup code for the device
    if option == "Setup":
        code = VarrialbleChange(GetSetupCode(device_file))
        code_steps = len(code)
        for i in range(code_steps):
            try:
                inst.write(str(code[i]).strip())
            except:
                return False
        return True

    if option == "Main":
        code = VarrialbleChange(GetMainCode(device_file))
        measurement_var = FindMeasurmentVar(GetMainCode(device_file))
        i = 0
        code_steps = len(code)
        try:
            while i < int(measurement_var[1]) and i < code_steps:
                try:
                    inst.write(str(code[i]))
                    i += 1
                except:
                    return False
        except:
            while i < code_steps:
                try:
                    inst.write(str(code[i]))
                    i += 1
                except:
                    return False
        try:
            tester = int(measurement_var[1])
            measured_value = float(inst.query(code[i]))
        except:
            pass
        i += 1
        while i < code_steps:
            inst.write(code[i])
            i += 1
        try:
            return_this = measurement_var[0]
            return [return_this, measured_value]
        except:
            return

    # Runs finish code
    if option == "Finish":
        code = VarrialbleChange(GetFinishCode(device_file))
        code_steps = len(code)
        i = 0
        while i < code_steps:
            try:
                inst.write(str(code[i]).strip())
            except:
                return False
            i += 1
        inst.close()
        return True
