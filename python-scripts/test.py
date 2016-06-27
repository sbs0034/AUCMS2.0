import terminal_ui, database, datetime, sys
from measurement_script import*
def ViaTerminal():
    terminal_ui.CreateScriptTitle("JJs")
    database.ConnectToDatabase()
    chipID = input("Input chip ID: ")
    database.CreateTable(chipID,"UserName,Current,FourWireVoltage,Resistance,NormalResistance,Time,Date,Notes,Device,CriticalCurrent,TwoWireVoltage")
    dataFile = open("DataDump.csv", "w")
    delay = input("Input delay between each current step: ")
    numOfLoops = int(input("Input number of times to measure: "))
    measurementDelay = float(input(("Input the delay between each measurement cylcle: ")))
    userName = input("Input user name: ")
    voltageLimitTW = input("Input 2 Wire Compliance Voltage: ")
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
    # wantedVoltageArray = []
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
        # wantedVoltage_ = input("Input 4 Wire voltage limit for critical current: ")
        currentSteps_ = input("Input current steps(ma): ")
        deviceIdentifier_ = input("Input device id: ")
        deviceIdentifier.append(deviceIdentifier_)
        # wantedVoltageArray.append(wantedVoltage_)
        currentStepsArray.append(currentSteps_)
    print("\n \n")
    print(deviceIdentifier)
    DeviceControl(switching_device, "Setup")
    DeviceControl(source_device, "Setup")
    DeviceControl(measurement_device, "Setup")
    i = 0
    i_ = 0
    dataFile.write("Voltage,Current,Resistance \n")
    measureVoltageFW = 0
    measureVoltageTW = 0
    while i_ < numOfLoops:


        DeviceControl(switching_device, "Finish")
        DeviceControl(source_device, "Finish")


        t= 0
        i_ +=1
        startTime = str(time())
        while(t < len(switch_inputs_high)):
            id = deviceIdentifier[t]
            # voltageLimitFW = wantedVoltageArray[t]
            currentSteps = currentStepsArray[t]
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
            database2WireVoltage = ""
            databaseCurrent = ""
            databaseResistance = ""
            CURSOR_UP_ONE = '\x1b[1A'
            ERASE_LINE = '\x1b[2K'
            #-1.39E-01
            oldMV = 0
            newMV = 0
            key_words["nin_var"] = "2"
            key_words["s_var"] = "3"
            DeviceControl(switching_device, "Main")
            key_words["nin_var"] = "11"
            key_words["s_var"] = "3"
            DeviceControl(switching_device, "Main")
            while abs(float(oldMV) - float(newMV)) < ((1.39)/10) and float(measureVoltageTW) <= float(voltageLimitTW):
                oldMV = newMV
                measuredTemp = DeviceControl(temp_device, "Main")[1]
                currentToPush = currentToPush+(float(currentSteps)/1000)
                databaseCurrent = databaseCurrent+str(currentToPush)+"\n"
                key_words["i_var"] = currentToPush
                DeviceControl(source_device, "Main")
                measureVoltageFW = DeviceControl(measurement_device, "Main")[1]
                newMV = measureVoltageFW
                measureVoltageTW = DeviceControl(source_device, "Main")[1]
                databaseVoltage = databaseVoltage+str(measureVoltageFW)+"\n"
                database2WireVoltage = database2WireVoltage+str(measureVoltageTW)+"\n"
                databaseResistance = databaseResistance+str(float(measureVoltageFW)/float(currentToPush))+"\n"
                dataFile.write(str(measureVoltageFW)+","+str(currentToPush)+","+str(float(measureVoltageFW)/float(currentToPush))+"\n")
                print(CURSOR_UP_ONE + ERASE_LINE+CURSOR_UP_ONE)
                print(str(id)+" --->   Current Pushed: "+str("%.8f" % currentToPush)+"   4 Wire Voltage Measureed: "+str(float("%.8f" % measureVoltageFW))+ "   2 Wire Voltage Measureed: "+str(measureVoltageTW)+"   Resistance: "+str("%.8f" % ((float(measureVoltageFW)/(float(currentToPush))))) +"   Tempurature: "+str(measuredTemp))
                sleep(float(delay))
            criticalCurrent = float(currentToPush)-(float(currentSteps)/1000)
            NewR = 100000000
            PrevR = 0
            currentToGo = 0
            while abs(NewR - PrevR) >= 15 and float(measureVoltageTW) < float(voltageLimitTW):
                PrevR = NewR
                measuredTemp = DeviceControl(temp_device, "Main")[1]
                currentToPush = currentToPush+(float(currentSteps)/1000)
                databaseCurrent = databaseCurrent+str(currentToPush)+"\n"
                key_words["i_var"] = currentToPush
                DeviceControl(source_device, "Main")
                measureVoltageFW = DeviceControl(measurement_device, "Main")[1]
                measureVoltageTW = DeviceControl(source_device, "Main")[1]
                databaseVoltage = databaseVoltage+str(measureVoltageFW)+"\n"
                database2WireVoltage = database2WireVoltage+str(measureVoltageTW)+"\n"
                databaseResistance = databaseResistance+str(float(measureVoltageFW)/float(currentToPush))+"\n"
                dataFile.write(str(measureVoltageFW)+","+str(currentToPush)+","+str(float(measureVoltageFW)/float(currentToPush))+"\n")
                NewR = (float(measureVoltageFW)/(float(currentToPush)))
                print(CURSOR_UP_ONE + ERASE_LINE+CURSOR_UP_ONE)
                print(str(id)+" --->   Current Pushed: "+str("%.8f" % currentToPush)+"   4 Wire Voltage Measureed: "+str(float("%.8f" % measureVoltageFW))+ "   2 Wire Voltage Measureed: "+str(measureVoltageTW)+"   Resistance: "+str("%.8f" % ((float(measureVoltageFW)/(float(currentToPush))))) +"   Tempurature: "+str(measuredTemp) + "    Critical Current: "+str(criticalCurrent))
                sleep(float(delay))
                i+=1
            counter = 0
            normalResistance = 0
            while counter < 10 and float(measureVoltageTW) < float(voltageLimitTW):
                measuredTemp = DeviceControl(temp_device, "Main")[1]
                currentToPush = currentToPush+(float(currentSteps)/1000)
                databaseCurrent = databaseCurrent+str(currentToPush)+"\n"
                key_words["i_var"] = currentToPush
                DeviceControl(source_device, "Main")
                measureVoltageFW = DeviceControl(measurement_device, "Main")[1]
                measureVoltageTW = DeviceControl(source_device, "Main")[1]
                databaseVoltage = databaseVoltage+str(measureVoltageFW)+"\n"
                database2WireVoltage = database2WireVoltage+str(measureVoltageTW)+"\n"
                databaseResistance = databaseResistance+str(float(measureVoltageFW)/float(currentToPush))+"\n"
                dataFile.write(str(measureVoltageFW)+","+str(currentToPush)+","+str(float(measureVoltageFW)/float(currentToPush))+"\n")
                normalResistance = normalResistance + (float(measureVoltageFW)/(float(currentToPush)))
                print(CURSOR_UP_ONE + ERASE_LINE+CURSOR_UP_ONE)
                print(str(id)+" --->   Current Pushed: "+str("%.8f" % currentToPush)+"   4 Wire Voltage Measureed: "+str(float("%.8f" % measureVoltageFW))+ "   2 Wire Voltage Measureed: "+str(measureVoltageTW)+"   Resistance: "+str("%.8f" % ((float(measureVoltageFW)/(float(currentToPush))))) +"   Normal Resistance: "+str(normalResistance) + "    Critical Current: "+str(criticalCurrent))
                sleep(float(delay))
                i+=1
                counter +=1
            normalResistance = normalResistance/(counter-1)
            currentToGo = -1*currentToPush
            while(float(currentToPush) > float(currentToGo) and abs(float(measureVoltageTW)) < float(voltageLimitTW)):
                measuredTemp = DeviceControl(temp_device, "Main")[1]
                currentToPush = currentToPush-(float(currentSteps)/1000)
                databaseCurrent = databaseCurrent+str(currentToPush)+"\n"
                key_words["i_var"] = currentToPush
                DeviceControl(source_device, "Main")
                measureVoltageFW = DeviceControl(measurement_device, "Main")[1]
                measureVoltageTW = DeviceControl(source_device, "Main")[1]
                databaseVoltage = databaseVoltage+str(measureVoltageFW)+"\n"
                database2WireVoltage = database2WireVoltage+str(measureVoltageTW)+"\n"
                databaseResistance = databaseResistance+str(float(abs(measureVoltageFW))/float(abs(currentToPush)))+"\n"
                dataFile.write(str(measureVoltageFW)+","+str(currentToPush)+","+str(float(abs(measureVoltageFW))/float(abs(currentToPush)))+"\n")
                print(CURSOR_UP_ONE + ERASE_LINE+CURSOR_UP_ONE)
                print(str(id)+" --->   Current Pushed: "+str("%.8f" % currentToPush)+"   4 Wire Voltage Measureed: "+str(float("%.8f" % measureVoltageFW))+ "   2 Wire Voltage Measureed: "+str(measureVoltageTW)+"   Resistance: "+str("%.8f" % ((float(abs(measureVoltageFW))/(float(abs(currentToPush)))))) +"   Nomal Resistance: "+str(normalResistance) + "    Critical Current: "+str(criticalCurrent))
                sleep(float(delay))
            while float((currentToPush) < 0):
                measuredTemp = DeviceControl(temp_device, "Main")[1]
                currentToPush = currentToPush+(float(currentSteps)/1000)
                databaseCurrent = databaseCurrent+str(currentToPush)+"\n"
                key_words["i_var"] = currentToPush
                DeviceControl(source_device, "Main")
                measureVoltageFW = DeviceControl(measurement_device, "Main")[1]
                measureVoltageTW = DeviceControl(source_device, "Main")[1]
                databaseVoltage = databaseVoltage+str(measureVoltageFW)+"\n"
                database2WireVoltage = database2WireVoltage+str(measureVoltageTW)+"\n"
                databaseResistance = databaseResistance+str(float(measureVoltageFW)/float(currentToPush))+"\n"
                dataFile.write(str(measureVoltageFW)+","+str(currentToPush)+","+str(float(measureVoltageFW)/float(currentToPush))+"\n")
                print(CURSOR_UP_ONE + ERASE_LINE+CURSOR_UP_ONE)
                print(str(id)+" --->   Current Pushed: "+str("%.8f" % currentToPush)+"   4 Wire Voltage Measureed: "+str(float("%.8f" % measureVoltageFW))+ "   2 Wire Voltage Measureed: "+str(measureVoltageTW)+"   Resistance: "+str("%.8f" % ((float(measureVoltageFW)/(float(currentToPush))))) +"   Normal Resistance: "+str(normalResistance) + "    Critical Current: "+str(criticalCurrent))
                sleep(float(delay))
            print("\n")
            #  UserName,Current,Voltage,Resistance,Time,Date,Notes
            time_ = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)
            date_ = str(datetime.datetime.now().year)+'-'+str(datetime.datetime.now().month)+'-'+str(datetime.datetime.now().day)
            database.WriteToDatabase(chipID,[userName,databaseCurrent,databaseVoltage,databaseResistance,normalResistance,time_,date_,notes,id,criticalCurrent,database2WireVoltage])

            # Switch to forcing Current
            DeviceControl(switching_device, "Finish")
            DeviceControl(source_device, "Finish")
            key_words["nin_var"] = "1"
            key_words["s_var"] = "3"
            DeviceControl(switching_device, "Main")
            key_words["nin_var"] = "12"
            key_words["s_var"] = "3"
            DeviceControl(switching_device, "Main")
            key_words["i_var"] = 45/1000000
            DeviceControl(source_device, "Main")
            sleep(float(measurementDelay))


            if(float(voltageLimitTW) >= float(abs(measureVoltageTW))):
                DeviceControl(source_device,"Finish")
                DeviceControl(switching_device, "Finish")
    DeviceControl(source_device, "Finish")
    DeviceControl(switching_device, "Finish")
    print("Done!")
def ViaGUI(arguments):
    print(arguments)
ViaTerminal()
try:
    ViaGUI(sys.argv[1])
except:
    ViaTerminal()
