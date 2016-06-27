import visa, sys, sqlite3, os, datetime
from time import time, sleep
scriptLog = open("scriptLog.txt", 'a')
key_words = {'i_var': 0, "v_var": 0, "nin_var": "", "s_var": "", "im_var =": "", "im_var=": "",
             "vm_var =": "", "vm_var=": "", "oin_var": 0, "tm_var =":""}
source_device = "DeviceFiles/source_device_script.txt"
measurement_device = "DeviceFiles/measurement_device_script.txt"
switching_device = "DeviceFiles/switching_device_script.txt"
temp_device = "DeviceFiles/temp_device_script.txt"
os_ = sys.platform
scriptPath_ = os.path.dirname(os.path.realpath(sys.argv[0]))
scriptPath_ = str(scriptPath_)
print(scriptPath_+" script path")
if os_ == 'win32':
    scriptPath_ = scriptPath_.split("\\")
else:
    scriptPath_ = scriptPath_.split("/")
del scriptPath_[0]
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
def CreateDatabaseTables(_name, databaseMainTableFields):
    conn.execute("CREATE TABLE "+"'"+str(_name)+"'"+databaseMainTableFields)
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
