import json


breakRoom = {
    "emergencyDone": False,
    "type": "Break",
    "class": "Utility",
    "mergeLevel": 1,
    "row": 0,
    "col": 0,
    "power": True,
    "roomHealth": {
      "damageValue": 0,
      "initialValue": 0
    },
    "mrHandyList": [],
    "rushTask": -1,
    "level": 1,
    "dwellers": [],
    "deadDwellers": [],
    "currentStateName": "Idle",
    "currentState": {},
    "deserializeID": 97,
    "assignedDecoration": "",
    "roomVisibility": False,
    "roomOutline": False,
    "withHole": False
     }
def FindDwellerRoom(DwellerID):
    for i in range(len(roomlist)):
        R = roomlist[i]
        if "dwellers" in R:
            for d in range(len(R["dwellers"])):
                if R["dwellers"][d] == DwellerID:
                    return R
    return breakRoom
            

class Field(object):
    label = ""
    helptext = ""
    path = []
    DataColumnWidth = 5 #When outputting data, column wil be this wide
    forceDataColumnWidth = False #manually set the data column width to a specific number 
    def __init__(self, label, path, helptext=""):
        self.label = label
        if type(path) == str:
            path = [path]
        self.path = path
        self.CollectedData = {}
        self.helptext = helptext
        DataColumnWidth = max(len(label), 5) #Width of co
        

    def IDValidation(self, ID):
        if ID == None:
            ID = len(self.CollectedData)
            if ID in self.CollectedData:
                print("------------------ID CONFLICT-------------------")
                print("NO ID WAS PROVIDED, GENERATED ID IS INVALID")
                raise ValueError('No id provided for field, generated id was already in use')
        if ID in self.CollectedData:
            print("------------------ID CONFLICT-------------------")
            print("ID provided already in use")
            raise ValueError("ID provided already in use")
        return ID
    def GetData(self, JSONdict, ID=None):
        ID = self.IDValidation(ID)
        Data = JSONdict
        for pathsegment in self.path:
            Data = Data[pathsegment]
        self.CollectedData[ID] = Data

    def UpdateDataColumnWidth(self):
        minWidth = max(len(self.label), 5)
        for entry in self.CollectedData.values():
            WidthOfEntry = 1
            if type(entry) == float or type(entry) == int:
                WidthOfEntry = len(str(int(entry))) + 5
            elif type(entry) == str:
                WidthOfEntry = len(entry) + 2
            else:
                WidthOfEntry = len(str(entry)) + 2
            minWidth = max(minWidth, WidthOfEntry)
        self.DataColumnWidth = minWidth

    def OutputHeader(self):
        if not  self.forceDataColumnWidth:
            self.UpdateDataColumnWidth()
        formatString = ('{:%s.%s}' % (str(self.DataColumnWidth),str(self.DataColumnWidth)))
        return formatString.format(self.label)

    def Output(self, ID):
        entry = self.CollectedData[ID]
        if not  self.forceDataColumnWidth:
            self.UpdateDataColumnWidth()
        if type(entry) == float:
            formatString = ('{:%s.%s}  ' % (str(self.DataColumnWidth - 2),str(self.DataColumnWidth-4)))
        else:
            formatString = ('{:%s}  ' % (str(self.DataColumnWidth - 2))) 
        #print(formatString.format(entry))
        return formatString.format(entry)
#        
#            return ('{:%}' % (str(DataColumnWidth))).format(entry)
#        elif type(entry) == str:
#            
#        else:
#            WidthOfEntry = len(str(entry))
    def GetIDsSorted(self, ascending = True):
        sortedIDs = []
        for key, value in sorted(self.CollectedData.items(), key=lambda kv : kv[1]):
            sortedIDs.append(key)
        if not ascending:
            sortedIDs.reverse()
        return sortedIDs
class NameField(Field):
    def GetData(self, JSONdict, ID=None):
        self.IDValidation(ID)
        Data = JSONdict
        for pathsegment in self.path:
            if pathsegment == "name":
                lastName = Data["lastName"]
            Data = Data[pathsegment]
        self.CollectedData[ID] = Data + " " + lastName

class RoomField(Field):
    def GetData(self, JSONdict, ID=None):
        ID=self.IDValidation(ID)
        
        Room = FindDwellerRoom(ID)
        self.CollectedData[ID] = Room["type"]

class RoomCoordsField(Field):
    def GetData(self, JSONdict, ID=None):
        ID=self.IDValidation(ID)
        
        Room = FindDwellerRoom(ID)
        self.CollectedData[ID] = str(Room["row"]) + " ," + str(Room["col"])

class HealthPerLevelField(Field):
    def GetData(self, JSONdict, ID=None):
        ID=self.IDValidation(ID)
        Level = None
        Maxhealth = None
        Data=JSONdict
        for pathsegment in self.path:
            if pathsegment == "health":
                Level  = Data["experience"]["currentLevel"]
            if pathsegment == "experience":
                Maxhealth = Data["health"]["maxHealth"]
            Data = Data[pathsegment]
        if Level == None:
            Level = Data
        elif MaxHealth == None:
            Maxhealth = Data
        self.CollectedData[ID] = Maxhealth/Level

class AvgEndurance(Field):
    def GetData(self, JSONdict, ID=None):
        ID=self.IDValidation(ID)
        Level = None
        Maxhealth = None
        Data=JSONdict
        for pathsegment in self.path:
            if pathsegment == "health":
                Level  = Data["experience"]["currentLevel"]
            if pathsegment == "experience":
                Maxhealth = Data["health"]["maxHealth"]
            Data = Data[pathsegment]
        if Level == None:
            Level = Data
        elif MaxHealth == None:
            Maxhealth = Data
        self.CollectedData[ID] = (Maxhealth-105 - 2.5 * (Level-1))*2/Level
DwellerFields = [
    NameField("Name",               ["name"], helptext="Dweller Name"),
    Field("Health",             ["health", "maxHealth"], helptext="Max Health"),
    Field("Level",              ["experience","currentLevel"], helptext="Level"),
    AvgEndurance("Avg. E",                ["experience","currentLevel"], helptext="HAverage Endurace"),
    HealthPerLevelField("H/L",                ["experience","currentLevel"], helptext="Health per Level"),
    RoomField("Room",               [], helptext="Dweller Name"),
    RoomCoordsField("Coords",             [], helptext="Dweller Name"),
    Field("?",                  ["stats","stats",0,"value"], helptext="strength"),
    Field("S",                  ["stats","stats",1,"value"], helptext="strength"),
    Field("P",                  ["stats","stats",2,"value"], helptext="strength"),
    Field("E",                  ["stats","stats",3,"value"], helptext="strength"),
    Field("C",                  ["stats","stats",4,"value"], helptext="strength"),
    Field("I",                  ["stats","stats",5,"value"], helptext="strength"),
    Field("A",                  ["stats","stats",6,"value"], helptext="strength"),
    Field("L",                  ["stats","stats",7,"value"], helptext="strength")
]

def GetDwellerInfo(FieldList):
    for D in dwellerslist:
        ID = D["serializeId"]
        for field in FieldList:
            field.GetData(D, ID)

def ListDwellerInfo(FieldList, sortBy=None, ascending=True):
    HeaderString = ""
    for F in FieldList:
        HeaderString += F.OutputHeader()

    if sortBy == None:
        sortBy = FieldList[0]

    IDList = sortBy.GetIDsSorted(ascending)
    print(HeaderString)
    for ID in IDList:
        dataString = ""
        for F in FieldList:
            dataString += F.Output(ID)
        print(dataString)

print("opening file")
file =  open("decodedsave.json", "r")
fileobj = json.loads(file.read())
print("Getting dweller info")
dwellerslist = fileobj["dwellers"]["dwellers"]
roomlist = fileobj["vault"]["rooms"]
print(str(len(dwellerslist)) + " dwellers")
GetDwellerInfo(DwellerFields)
print("done")
print(" ")
print("Type help for a list of commands")
SortIndex = 3
SortReversed = False

while True:
    
    command = input(">>").strip()
    commandList = command.split(" ")
    if len(commandList) > 0:
        if commandList[0].strip().lower() == "help":
            print(
                """
                FOS Stat Viewer:

                    Allows you to see stats regarding your vault that would otherwise be hidden

                SYNOPSIS

                    list
                        List's all the stats

                    sort [column number] [-R]
                        Sorts stats by column number specified.


                DESCRIPTION

                    Use the List command to print a list of all dwellers and their stats in either
                    an arbitrary order, or the order previously specified by Sort.

                    Use the sort command to specify a column you want to sort by. if -R is set to 1,
                    the order will be Reversed. If it is set to anything else or not included, the order will be normal.


                    Stats:
                        Most of the stats are self explanatory, but some are not.

                        Avg. E refers to average Endurance over the course of the dweler leveling up. For
                        A dweller that leveled to 25 with an endurance of 1 and then leveled the rest of the
                        way to 50 with an endurance of 10 would have an Avg. E around 5. If the dweller's END
                        remained static as it leveled up, it's Avg. E would be the same as it's E now.
                        I computed this value to determine what dwellers have lost the most potential health points
                        so that I could remove them.

                        H/L refers to health per level. This isn't a particularly useful stat, I think Avg. E does
                        essentially the same thing better, but I had already built this and included it anyway.

                        Room refers to the room the dweller is currently in. If it says break, it could also mean exploring
                        or returning from an adventure.

                        Coords refer to the coordinates of the room that they are in if you are looking for them. The first
                        number represents the vertical coordinate, the second the horizontal.

                        The SPECIAL stats are normal, expect for the first one. The column heading is ? because I have no idea
                        what it is. For my dwellers, it was 1. Let me know if you discover it's meaning.

                        

                    
                Andy Tewfik
                Andy.Tewfik@gmail.com
                """)
        if commandList[0].strip().lower() == "list":
                ListDwellerInfo(DwellerFields, DwellerFields[SortIndex - 1], SortReversed)

        if commandList[0].strip().lower() == "sort":
                tempSortIndex = SortIndex
                try:
                    tempSortIndex = int(commandList[1])
                except:
                    print("Not a valid column number. Try again.")
                if tempSortIndex < 1 or tempSortIndex > len(DwellerFields):
                    print("Column number out of range. Try Again.")
                else:
                    SortIndex = tempSortIndex
                    if len(commandList) > 2:
                        SortReversed = (commandList[2].strip() == "1")

            
                    
            

        
        
        
        
        
