from AUCMS import *
import json
labelDivB = "<div class='mdl-textfield mdl-js-textfield mdl-textfield--floating-label'>"
databaseMainTableFields = "(Notes TEXT, Time TEXT, Date TEXT, UserName TEXT, CriticalCurrent REAL, Current REAL, Voltage REAL, Resistance REAL, Delay REAL, DeviceIdentifier TEXT,  Tempurature REAL, CurrentLimit REAL, VoltageLimit REAL, ForcedCurrentType TEXT)"
databaseMainTableFields_ = "(Notes, Time, Date, UserName, CriticalCurrent, Current, Voltage, Resistance, Delay, DeviceIdentifier, Tempurature, CurrentLimit, VoltageLimit, ForcedCurrentType)"
def ViaTerminal():
    print("\n \n")
    print("*******************************************")
    print("*                                         *")
    print("*     Script for measuring resistors      *")
    print("*                                         *")
    print("*******************************************")
    print("\n \n")
    chipID = input("Input chip ID: ")
    _name = str(chipID)+"-Resistors"
    try:
        CreateDatabaseTables(_name, databaseMainTableFields)
        conn.commit()
    except:
        pass
    print("1. Sweep current")
    print("2. Constant current")
    measurementType = input("Choose measurement type: ")
    dataFile = open("DataDump.csv", "w")
    scriptLog.write("DataDump data overwritten \n")
    delay = input("Input delay between each current step: ")
    numOfLoops = int(input("Input number of times to measure: "))
    userName = input("Input user name: ")
    notes = input("Input any notes for this measurement (leave blank if none): ")
    if measurementType == "1":
        measurementType = "Sweep"
    else:
        measurementType = "Constant"
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
    wantedCurrentArray = []
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
        wantedVoltage_ = input("Input voltage limit: ")
        if(measurementType == "Sweep"):
            currentSteps_ = input("Input current steps(ma): ")
            wantedCurrent_ = input("Current limit: ")
        else:
            currentSteps_ = input("Enter current to force(ma): ")
            wantedCurrent_ = currentSteps_
        deviceIdentifier_ = input("Input device id: ")
        deviceIdentifier.append(deviceIdentifier_)
        wantedVoltageArray.append(wantedVoltage_)
        wantedCurrentArray.append(wantedCurrent_)
        currentStepsArray.append(currentSteps_)
    MakeMeasurement("Terminal",userName,notes,_name,deviceIdentifier,measurementType,switch_inputs_high,switch_inputs_low,currentStepsArray,wantedCurrentArray,wantedVoltageArray)
def ViaGUI(arguments):
    if arguments[1] == "buildGUI":
        guiFill = ""

        print("<h2>Resistor Module</h>")
        print('<div class="form-group label-floating"><label for="chipID" class="control-label" style="font-weight: 600">Chip ID</label><input type="text" class="form-control scriptInput" id="chipID"></div><br>')
        print('<div class="form-group label-floating"><label for="userName" class="control-label" style="font-weight: 600">User Name</label><input type="text" class="form-control scriptInput" id="userName"></div><br>')
        print('<div class="form-group label-floating"><label for="notes" class="control-label" style="font-weight: 600">Measurement Notes</label><textarea class="form-control scriptInput" id="notes"></textarea></div><br>')
        print("<table id='deviceTable' class='table'>")
        print("")
        guiFill=guiFill+("<tr class='tableRow'>")
        guiFill=guiFill+('<td><div class="form-group label-floating"><label style="font-weight: 600" for="deviceID" class="control-label">Device ID</label><input type="text" class="form-control deviceID" id="deviceID"></div></td>')
        guiFill=guiFill+('<td><div class="form-group label-floating"><label style="font-weight: 600" for="inputHigh" class="control-label">Input High</label><input type="text" class="form-control inputHigh" id="inputHigh"></div></td>')
        guiFill=guiFill+('<td><div class="form-group label-floating"><label style="font-weight: 600" for="inputLow" class="control-label">Input Low</label><input type="text" class="form-control inputLow" id="inputLow"></div></td>')
        guiFill=guiFill+('<td><div class="form-group label-floating"><label style="font-weight: 600" for="currentSteps" class="control-label">Current Steps</label><input type="text" class="form-control currentSteps" id="currentSteps"></div></td>')
        guiFill=guiFill+('<td><div class="form-group label-floating"><label style="font-weight: 600" for="currentLimit" class="control-label">Current Limit</label><input type="text" class="form-control currentLimit" id="currentLimit"></div></td>')
        guiFill=guiFill+('<td><div class="form-group label-floating"><label style="font-weight: 600" for="voltageLimit" class="control-label">Voltage Limit</label><input type="text" class="form-control voltageLimit" id="voltageLimit"></div></td>')
        guiFill=guiFill+("</tr>")
        print(guiFill)
        print("<br><button class='btn btn-raised btn-warning' class='addDevice' onclick='AddDevice()'>Add Device</button><br><br>")

    if arguments[1] == "measureDevice":
        measurementType = "Sweep"
        i = 2
        newArguments = []
        while(i < len(arguments)):
            newArguments.append(arguments[i].split("@"))
            i+=1
        argumentDict = {}
        i=0
        while(i < len(newArguments)):
            argumentDict[newArguments[i][0]]=newArguments[i][1]
            i+=1
        notes = argumentDict["notes"]
        switch_inputs_high = argumentDict["inputHigh"].split(",")
        deviceIdentifier = argumentDict["deviceID"].split(",")
        wantedCurrentArray = argumentDict["currentLimit"].split(",")
        wantedVoltageArray = argumentDict["voltageLimit"].split(",")
        currentStepsArray = argumentDict["currentSteps"].split(",")
        switch_inputs_low = argumentDict["inputLow"].split(",")
        DeviceControl(switching_device, "Setup")
        DeviceControl(source_device, "Setup")
        DeviceControl(measurement_device, "Setup")
        _name = argumentDict["chipID"]+"-Resistors"
        userName = argumentDict["userName"]
        MakeMeasurement("GUI",userName,notes,_name,deviceIdentifier,measurementType,switch_inputs_high,switch_inputs_low,currentStepsArray,wantedCurrentArray,wantedVoltageArray)
def MakeMeasurement(userInteraction,userName,notes,_name,deviceIdentifier,measurementType,switch_inputs_high,switch_inputs_low,currentStepsArray,wantedCurrentArray,wantedVoltageArray):
    DeviceControl(switching_device, "Setup")
    DeviceControl(source_device, "Setup")
    DeviceControl(measurement_device, "Setup")
    try:
        CreateDatabaseTables(_name, databaseMainTableFields)
        conn.commit()
    except:
        pass
    delay = 0
    i = 0
    i_ = 0
    numOfLoops = 1
    print("Got to this point")
    while i_ < numOfLoops:
        t= 0
        i_ +=1
        startTime = str(time())
        while(t < len(switch_inputs_high)):
            id = deviceIdentifier[t]
            if(wantedCurrentArray[t] == ""):
                wantedCurrent = float("inf")
            else:
                wantedCurrent = wantedCurrentArray[t]
            wantedVoltage = wantedVoltageArray[t]
            currentSteps = currentStepsArray[t]
            DeviceControl(switching_device, "Finish")
            x = 0
            while x < len(switch_inputs_high[t]):
                _input = switch_inputs_high[t]
                key_words["nin_var"] = _input.split(":")[1]
                key_words["s_var"] = _input.split(":")[0]
                DeviceControl(switching_device, "Main")
                x+=1
            v = 0
            while v < len(switch_inputs_low[t]):
                _input = switch_inputs_low[t]
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
            while float(measureVoltage) <= float(wantedVoltage) and float(wantedCurrent) >= float(currentToPush):
                measuredTemp = DeviceControl(temp_device, "Main")[1]
                currentToPush = currentToPush+(float(currentSteps)/1000)
                databaseCurrent = databaseCurrent+str(currentToPush)+"\n"
                key_words["i_var"] = currentToPush
                DeviceControl(source_device, "Main")
                measureVoltage = DeviceControl(measurement_device, "Main")[1]
                databaseVoltage = databaseVoltage+str(measureVoltage)+"\n"
                databaseResistance = databaseResistance+str(float(measureVoltage)/float(currentToPush))+"\n"
                # dataFile.write(str(measureVoltage)+","+str(currentToPush)+","+str(float(measureVoltage)/float(currentToPush))+"\n")
                if(userInteraction == "Terminal"):
                    print(CURSOR_UP_ONE + ERASE_LINE+CURSOR_UP_ONE)
                print(str(id)+" --->   Current Pushed: "+str("%.8f" % currentToPush)+"   Voltage Measureed: "+str(float("%.8f" % measureVoltage))+"   Resistance: "+str("%.8f" % ((float(measureVoltage)/(float(currentToPush))))) +"   Tempurature: "+str(measuredTemp))
                sleep(float(delay))
                i+=1
            criticalCurrent = float(currentToPush)-(float(currentSteps)/1000)
            conn.execute("INSERT INTO "+"'"+_name+"'"+databaseMainTableFields_+" VALUES("+"'"+notes+"'"+","+"'"+str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)+"'"+","+
                         "'"+str(datetime.datetime.now().year)+'-'+str(datetime.datetime.now().month)+'-'+str(datetime.datetime.now().day)+"'"+','+"'"+userName+"'"+','+str(criticalCurrent)+','+"'"+databaseCurrent+"'"+','+"'"+databaseVoltage+"'"+','+"'"+databaseResistance+"'"+","+str(delay)+","+"'"+str(id)+"'"+","+str(measuredTemp)+","+"'"+str(wantedCurrent)+"'"+","+"'"+str(wantedVoltage)+"'"+",'"+str(measurementType)+"')")
            conn.commit()
    DeviceControl(source_device, "Finish")
    DeviceControl(switching_device, "Finish")
    if(userInteraction == "Terminal"):
        print("Done!")
try:
    ViaGUI(sys.argv)
except:
    print("Using Terminal \n")
    ViaTerminal()
