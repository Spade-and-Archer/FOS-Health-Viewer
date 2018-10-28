import json
file =  open("decodedsave.json", "r")
fileobj = json.loads(file.read())
dwellerslist = fileobj["dwellers"]["dwellers"]
roomlist = fileobj["vault"]["rooms"]
print(len(dwellerslist))

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
        print (self.DataColumnWidth)
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


def ListDwellerInfo(FieldList, sortBy=None, ascending=True):
    for D in dwellerslist:
        ID = D["serializeId"]
        for field in FieldList:
            field.GetData(D, ID)
          

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

ListDwellerInfo(DwellerFields, DwellerFields[3])



        
        
        
        
        
