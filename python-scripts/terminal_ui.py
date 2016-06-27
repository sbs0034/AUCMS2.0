def CreateScriptTitle(MeasurementType):
    welcome_message = "Script for measuring "+str(MeasurementType)
    # 5 spaces on each side
    # 1 * on top and bottom
    top_border = "*"
    top_border = top_border*(len(welcome_message)+8)
    bottom_border = top_border
    side_border = "*"+" "*(len(welcome_message)+6)+"*"
    spacing = "   "
    print("\n \n")
    print(top_border)
    print(side_border)
    print("*"+spacing+welcome_message+spacing+"*")
    print(side_border)
    print(bottom_border)
    print("\n \n")
def SwitchInputChooser(Options):
    walkthrough = True
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
        if "VoltageLimit" in Options:
            wantedVoltage_ = input("Input voltage limit: ")
        if "SweepCurrent" in Options:
            currentSteps_ = input("Input current steps(ma): ")
            wantedCurrent_ = input("Current limit: ")
        else:
            currentToPush_ = input("Enter current to force(ma): ")

        deviceIdentifier_ = input("Input device id: ")
        deviceIdentifier.append(deviceIdentifier_)
        if "VoltageLimit" in Options:
            wantedVoltageArray.append(wantedVoltage_)
        if "SweepCurrent" in Options:
            currentStepsArray.appen(currentSteps_)
        wantedCurrentArray.append(wantedCurrent_)
        currentStepsArray.append(currentSteps_)
    # try:
    #     return({})
