import os, sys
# import sqlite3
def ConnectToDatabase():
    global conn
    os_ = sys.platform
    scriptPath_ = os.path.dirname(os.path.realpath(sys.argv[0]))
    scriptPath_ = str(scriptPath_)
    if os_ == 'win32':
        scriptPath_ = scriptPath_.split("\\")
    else:
        scriptPath_ = scriptPath_.split("/")
    del scriptPath_[0]
    scriptPath__ = scriptPath_
    scriptPath = ""
    for i in (scriptPath_[:-2]):
        scriptPath = scriptPath+"/"+i
    UniversalDatabase = os.path.isfile(scriptPath+"/database.db")
    if UniversalDatabase == False:
        sc = ""
        for i in (scriptPath__[:]):
            sc = sc+"/"+i
        conn = sqlite3.connect(sc+"/database.db")
    else:
        conn = sqlite3.connect(scriptPath+"/database.db")

def CreateTableContent(TablesColums):
    columns = TablesColums.split(",")
    i = 0
    TableContent = "("
    while i < len(columns):
        columns[i] = columns[i]+" TEXT,"
        TableContent = TableContent+columns[i]
        i+=1
    TableContent = TableContent[:-1]
    TableContent = TableContent+")"
    return(TableContent)
def CreateTable(TableName, TablesColums):
    global conn
    global TablesColums_
    TablesColums_ = TablesColums
    ConnectToDatabase()
    columns = CreateTableContent(TablesColums)
    try:
        conn.execute("CREATE TABLE "+"'"+str(TableName)+"'"+columns)
        conn.commit()
    except:
        print("CREATE TABLE "+"'"+str(TableName)+"'"+columns)
def WriteToDatabase(TableName, Data):
    global conn
    global TablesColums_
    values = "VALUES("
    i=0
    while i < len(Data):
        values=values+"'"+str(Data[i])+"',"
        i+=1
    values = values[:-1]
    values=values+")"
    conn.execute("INSERT INTO "+"'"+TableName+"' "+"("+TablesColums_+")"+" "+values)
    conn.commit()
