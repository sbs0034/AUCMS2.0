import visa, sys, sqlite3, os, datetime
from time import time, sleep
scriptLog = open("scriptLog.txt", 'a')
key_words = {'i_var': 0, "v_var": 0, "nin_var": "", "s_var": "", "im_var =": "", "im_var=": "",
             "vm_var =": "", "vm_var=": "", "oin_var": 0, "tm_var =":""}
os_ = sys.platform
databaseMainTableFields = "(Notes TEXT, Time TEXT, Date TEXT, UserName TEXT, CriticalCurrent REAL, Current REAL, Voltage REAL, Resistance REAL, Delay REAL, Tempurature REAL, DeviceIdentifier TEXT)"
databaseMainTableFields_ = "(Notes, Time, Date, UserName, CriticalCurrent, Current, Voltage, Resistance, Delay, Tempurature, DeviceIdentifier)"
databaseSecondaryTableFields = "(VOLTAGE REAL,CURRENT REAL)"
scriptPath_ = os.path.dirname(os.path.realpath(sys.argv[0]))
scriptPath_ = str(scriptPath_)
print(scriptPath_+" script path")
if os_ == 'win32':
    scriptPath_ = scriptPath_.split("\\")
else:
    scriptPath_ = scriptPath_.split("/")
del scriptPath_[0]
del scriptPath_[-1]
scriptPath = ""
for i in (scriptPath_):
    scriptPath = scriptPath+"/"+i
UniversalDatabase = os.path.isfile(scriptPath+"/database.db")
GUI = True
DataBase = True
if UniversalDatabase == False:
    conn = sqlite3.connect("database.db")
else:
    conn = sqlite3.connect(scriptPath+"/database.db")
try:
    argVars = sys.argv[1]
    scriptLog.write("Script launched by GUI at "+str(time()) + "\n")
except:
    GUI = False
    scriptLog.write("Script launched by Terminal at "+str(time()) + "\n")
MeasuredValues = {}
def CreateDatabaseTables(chipID):
    conn.execute("CREATE TABLE "+"'"+str(chipID)+"-Resistors"+"'"+databaseMainTableFields)

 #########################################################################################################

def DeviceControl(device_file, option):
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

    def GetAddress(device_file):
        device_file = open(device_file, "r")
        file_read = device_file.readline().strip()
        while "address" not in file_read:
            file_read = device_file.readline().strip()
        read_after = file_read.index("=")
        address = (file_read[read_after + 1:])
        return address.strip()

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

    def VarrialbleChange(list_, key_words_):
        number_of_items = len(list_)
        i_ = 0
        while i_ < number_of_items:
            for i, j in key_words_.items():
                code = list_[i_]
                code = str(code)
                new_code = code.replace(str(i), str(j))
                list_[i_] = new_code.strip()
            i_ += 1
        return list_

    def FindMeasurmentVar(command_list):
        command_list_len = len(command_list)
        i = 0
        while i < command_list_len:
            if "tm_var" in command_list[i]:
                return ["tm_var", i]
            if "im_var" in command_list[i]:
                return ["im_var", i]
            if "vm_var" in command_list[i]:
                return ["vm_var", i]
            else:
                pass
            i += 1
        return "None"

    inst = visa.ResourceManager()
    # inst = visa.ResourceManager('@py')
    try:
        inst = inst.open_resource(str(GetAddress(device_file)))
    except:
        return ("Cannot connect to device")

    if option == "Setup":
        code = VarrialbleChange(GetSetupCode(device_file), key_words)
        code_steps = len(code)
        i = 0
        while i < code_steps:
            try:
                inst.write(str(code[i]).strip())
                i += 1
            except:
                return "Unable to connect to instrument"
        return "Device setup complete"

    if option == "Main":
        # print("Main")
        code = VarrialbleChange(GetMainCode(device_file), key_words)
        measurement_var = FindMeasurmentVar(GetMainCode(device_file))
        i = 0
        code_steps = len(code)
        try:
            while i < int(measurement_var[1]) and i < code_steps:
                # print("Writing code to device" + code[1][i])
                try:
                    inst.write(str(code[i]))
                    i += 1
                except:
                    return "Cannot connect to device"
        except:
            while i < code_steps:
                try:
                    inst.write(str(code[i]))
                    i += 1
                except:
                    return "Cannot connect to device"
        try:
            tester = int(measurement_var[1])
            measured_value = float(inst.query(code[i]))
        except:
            pass
        i += 1
        while i < code_steps:
            # print("Writing code to device: "+code[1][i])
            inst.write(code[i])
            i += 1
        try:
            return_this = measurement_var[0]
            return [return_this, measured_value]
        except:
            return

    if option == "Finish":
        # print("Finish")
        code = VarrialbleChange(GetFinishCode(device_file), key_words)
        code_steps = len(code)
        i = 0
        while i < code_steps:
            try:
                inst.write(str(code[i]).strip())
            except:
                return "Cannot connect to device"
            i += 1
        inst.close()
        return "Device finish complete"


def ResistorMeasurementTerminal():
    print("\n \n")
    print("*******************************************")
    print("*                                         *")
    print("*     Script for measuring resistors      *")
    print("*                                         *")
    print("*******************************************")
    print("\n \n")
    source_device = "DeviceFiles/source_device_script.txt"
    measurement_device = "DeviceFiles/measurement_device_script.txt"
    switching_device = "DeviceFiles/switching_device_script.txt"
    temp_device = "DeviceFiles/temp_device_script.txt"
    chipID = input("Input chip ID: ")
    dataFile = open("DataDump.csv", "w")
    scriptLog.write("DataDump data overwritten \n")
    delay = input("Input delay between each current step: ")
    numOfLoops = int(input("Input number of times to measure: "))
    userName = input("Input user name: ")
    notes = input("Input any notes for this measurement (leave blank if none): ")
    print("\n \n")
    print("**************************************************************************************************")
    print("Input the HIGH and LOW inputs for the switch matrix as follows.....")
    print("Input the slot number followed by a colin then the switch number Ex '1:1' ")
    print("if there are more desired inputs for HIGH, list them out in a comma sepperated list Ex 1:1,1:2")
    print("Then enter the numbers of the inputs for the LOW side of the chip input (same way as HIGH)")
    print("Then enter the devices indentirfier Ex. 'R5'(for resistor 5)")
    print("When done, just leave the HIGH and LOW input promps blank and hit ENTER")
    print("**************************************************************************************************")
    print("\n")
    switch_inputs_high = []
    switch_inputs_low = []
    deviceIdentifier = []
    currentStepsArray = []
    wantedVoltageArray = []
    _i = 0
    userInputHigh = "null"
    while(userInputHigh != ""):
        userInputHigh = input("Input HIGH: ")
        if userInputHigh != "":
            switch_inputs_high.append(userInputHigh.split(","))
        x = 0
        try:
            while x < len(switch_inputs_high[_i]):
                try:
                    switch_inputs_high[_i][x] = int(switch_inputs_high[_i][x])
                except:
                    pass
                x+=1
        except:
            pass
        userInputLow = input("Input LOW: ")
        if userInputLow != "":
            switch_inputs_low.append(userInputLow.split(","))
        x = 0
        try:
            while x < len(switch_inputs_low[_i]):
                try:
                    switch_inputs_low[_i][x] = int(switch_inputs_low[_i][x])
                except:
                    pass
                x+=1
        except:
            pass
        if userInputLow != "":
            _i+=1
        wantedVoltage_ = input("Input wanted voltage: ")
        currentSteps_ = input("Input current steps(ma): ")
        deviceIdentifier_ = input("Input device id: ")
        deviceIdentifier.append(deviceIdentifier_)
        wantedVoltageArray.append(wantedVoltage_)
        currentStepsArray.append(currentSteps_)
    print("\n \n")
    print(deviceIdentifier)
    if(DataBase == True):
        try:
            CreateDatabaseTables(chipID)
        except:
            pass
    DeviceControl(switching_device, "Setup")
    DeviceControl(source_device, "Setup")
    DeviceControl(measurement_device, "Setup")
    i = 0
    _name = str(chipID)+"-Resistors"
    dataFile.write("Voltage,Current,Resistance \n")
    while i < numOfLoops:
        t= 0
        startTime = str(time())
        while(t < len(switch_inputs_high)):
            id = deviceIdentifier[t]
            wantedVoltage = wantedVoltageArray[t]
            currentSteps = currentStepsArray[t]
            DeviceControl(switching_device, "Finish")
            x = 0
            while x < len(switch_inputs_high[t]):
                _input = switch_inputs_high[t][x]
                key_words["nin_var"] = _input.split(":")[1]
                key_words["s_var"] = _input.split(":")[0]
                DeviceControl(switching_device, "Main")
                x+=1
            v = 0
            while v < len(switch_inputs_low[t]):
                _input = switch_inputs_low[t][v]
                key_words["nin_var"] = _input.split(":")[1]
                key_words["s_var"] = _input.split(":")[0]
                DeviceControl(switching_device, "Main")
                v+=1

            t+=1
            sleep(0.25)
            key_words["i_var"] = 0
            currentToPush = 0
            databaseVoltage = ""
            databaseCurrent = ""
            databaseResistance = ""
            measureVoltage = 0
            CURSOR_UP_ONE = '\x1b[1A'
            ERASE_LINE = '\x1b[2K'
            while float(measureVoltage) <= float(wantedVoltage):
                measuredTemp = DeviceControl(temp_device, "Main")[1]
                currentToPush = currentToPush+(float(currentSteps)/1000)
                databaseCurrent = databaseCurrent+str(currentToPush)+"\n"
                key_words["i_var"] = currentToPush
                DeviceControl(source_device, "Main")
                measureVoltage = DeviceControl(measurement_device, "Main")[1]
                databaseVoltage = databaseVoltage+str(measureVoltage)+"\n"
                databaseResistance = databaseResistance+str(float(measureVoltage)/float(currentToPush))+"\n"
                dataFile.write(str(measureVoltage)+","+str(currentToPush)+","+str(float(measureVoltage)/float(currentToPush))+"\n")
                print(CURSOR_UP_ONE + ERASE_LINE+CURSOR_UP_ONE)
                print(str(id)+" --->   Current Pushed: "+str("%.8f" % currentToPush)+"   Voltage Measureed: "+str(float("%.8f" % measureVoltage))+"   Resistance: "+str("%.8f" % (((float(measureVoltage))/float(currentToPush)))/1000) +"   Tempurature: "+str(measuredTemp))
                sleep(float(delay))
                i+=1
            criticalCurrent = float(currentToPush)-(float(currentSteps)/1000)
            print("\n")
            conn.execute("INSERT INTO "+"'"+_name+"'"+databaseMainTableFields_+" VALUES("+"'"+notes+"'"+","+"'"+str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)+"'"+","+
                         "'"+str(datetime.datetime.now().year)+'-'+str(datetime.datetime.now().month)+'-'+str(datetime.datetime.now().day)+"'"+','+"'"+userName+"'"+','+str(criticalCurrent)+','+"'"+databaseCurrent+"'"+','+"'"+databaseVoltage+"'"+','+"'"+databaseResistance+"'"+","+delay+","+str(measuredTemp)+","+"'"+str(id)+"'"+")")
            conn.commit()
    DeviceControl(source_device, "Finish")
    DeviceControl(switching_device, "Finish")
    print("Done!")


if GUI == False:
    ResistorMeasurementTerminal()
