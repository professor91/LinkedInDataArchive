import csv
import json

class jsdb:
    #0. constructor
    def __init__(self, filename):
        self._cacheddata= {}
        self.filename= filename

        self.reload()

    #1. dump data in json file
    def dumpdata(self):
        with open(self.filename, "w") as wf:
            json.dump(self._cacheddata, wf, indent=4)
            print("log: Wrote data in json file")
        self.reload()

    #2. reload data from json file
    def reload(self):
        with open(self.filename, "r") as rf:
            self._cacheddata= json.load(rf)
            print("log: Reloaded the database into dictionary")

    def addItem(self, key, item):
        if key not in self._cacheddata.keys():
            self._cacheddata[key] = [item]
            print("log: Appended a value to a key in dictionary")
        else:
            self._cacheddata[key].append(item)
            print("log: Added a new key in the dictionary")

class Connections:
    def __init__(self, filename):
        self.csvfile= filename
        self._jsdb_class= jsdb("connections.json")

        # self.loadData()

    def loadData(self):
        with open(self.csvfile, "r") as rf:
            reader= csv.reader(rf)
            for row in reader:
                connection=     {
                                    "FirstName" : row[0],
                                    "LastName" : row[1],
                                    "Email" : row[2],
                                    "Company": row[3],
                                    "Position": row[4],
                                }
                self._jsdb_class.addItem(row[5], connection)
        self._jsdb_class.dumpdata()
        print("log: Loaded data from csv to json")

    def getKeys(self):
        return list(self._jsdb_class._cacheddata.keys())
    
    def maxconnectionsDay(self):
        maxConnection= len(self._jsdb_class._cacheddata[self.getKeys()[0]])
        maxConnectionKey= self.getKeys()[0]


        for key in self.getKeys():
            if(len(self._jsdb_class._cacheddata[key]) > maxConnection):
                maxConnection = len(self._jsdb_class._cacheddata[key])
                maxConnectionKey= key

        print("Max connection in 1 day:  ", maxConnection, " on: ", maxConnectionKey)

    def typesofProfessionals(self):
        profession= {}

        for key in self.getKeys():
            for connection in self._jsdb_class._cacheddata[key]:
                if connection["Position"] not in profession.keys():
                    profession[connection["Position"]]= 1
                else:
                    profession[connection["Position"]] += 1
        
        pretty= json.dumps(profession, indent= 3)
        print(pretty)

    def howmanyFounders(self):
        count= 0
        for key in self.getKeys():
            for connection in self._jsdb_class._cacheddata[key]:
                if connection["Position"] == "Founder":
                    count += 1
        
        print(count)

    def howmanySaini(self):
        count= 0
        for key in self.getKeys():
            for connection in self._jsdb_class._cacheddata[key]:
                if connection["LastName"] == "Saini":
                    count += 1
        print(count)
                    

class Invitations:
    def __init__(self, filename):
        self.csvfile= filename
        self._jsdb_class= jsdb("intivations.json")
        
        # self.loadData()

    def loadData(self):
        with open(self.csvfile, "r") as rf:
            reader= csv.reader(rf)
            for row in reader:
                if row[0] == "Keshav Saini":
                    self._jsdb_class.addItem("sent", [row[1], row[2]])
                else:
                    self._jsdb_class.addItem("receive", [row[0], row[2]])
        
        self._jsdb_class.dumpdata()
        print("log: Loaded data from csv to json")

    def connectionsSent(self):
        return len(self._jsdb_class._cacheddata["sent"])

    def connectionsReceived(self):
        return len(self._jsdb_class._cacheddata["receive"])

# delete first 5 rows from csv first time
cc = Connections("Connections.csv")

cc.maxconnectionsDay()
# cc.typesofProfessionals()
# cc.howmanyFounders()
# cc.howmanySaini()

iv = Invitations("Invitations.csv")

print(iv.connectionsSent())
print(iv.connectionsReceived())
