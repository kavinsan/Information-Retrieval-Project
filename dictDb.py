#Dictionary Database Class - Useful to store sets of records
#Storing and retrieving speed O(1)
import timeit
import sys
from copy import deepcopy

class database:
    
    myDict = dict()
    myDict2 = dict()
    
    #Add as many static dictionary objects needed here
    complete = dict() #.I
    title = dict() #.T
    abstract = dict() #.W
    author = dict() #.A
    compile = dict() # .T + .W
    
    dictFile = dict()
    postFile = dict() #Value will be a list containing the term frequency and doc id
    recompile = dict() #Recompiled clean .T + .W
    
    index = {'complete':complete, 'title':title,'abstract':abstract,'author':author,'compile':compile,'dictFile':dictFile,'postFile':postFile,'recompile':recompile}
    
    def getDb(self,name):
        if hasattr(database, name):
            print("Database exists")
            print(database.index.items())
        else:
            print("Database does not exist")
            
    #Store method stores records through a key value pairs, values will be stored in lists
    @staticmethod
    def store(db,key,value):
        if hasattr(database, db):
            db = database.index.get(db)
            
            if (db.get(key) is None):
                #print("Storing for the first time")
                db[key] = [value]
                     
            else: 
                db[key].append(value)        
                    
    #Retrieve value of of a key
    @staticmethod
    def getRecord(db,key):
        db = database.index.get(db)
        value = db.get(key)
        
        if (value is None):
            #print("There is no data for the key: ", key)
            return value
        else:
            #print("From: %s Key: %s Value: %s" % (db, key, eval("database." + db + ".get(key)")))
            return value
            
    #Print value of all keys and values 
    @staticmethod
    def printAll(db):
        #g = open("dictFile.txt","w+")
        
        print("PRINTING ALL RECORDS of %s" % db)
        db = database.index.get(db)
        for key,values in db.items():
            print("Key: [%s]    Value: %s" % (key,values))
            #g.write(str(key) + " " + str(values) + "\n")
        print("")
    
    @staticmethod
    def printDict(db):
        g = open("dictionary.txt","w+")
        
        #print("PRINTING ALL RECORDS of %s" % db)
        db = database.index.get(db)
        for key,values in db.items():
            #print("Key: [%s]    Value: %s" % (key,values))
            docFreq = values[0]
            data = "%-20s" % str(key) + str(docFreq) + "\n"
            g.write(data)
        #print("")
    
    @staticmethod
    def printPost(db):
        
        
        g = open("posting.txt","w+")
        if hasattr(database, db):
            db = database.index.get(db)
            #print("PRINTING ALL RECORDS of %s" % db)
            for key,values in db.items():
                #print("Key: [%s]    Value: %s" % (key,values))
                breakShell = values[0]
                
                for data in list(breakShell):
                    docID = data[0]
                    termFreq = data[1]
                    completeData = "%-20s" % str(key) + "%-4s" % str(termFreq) + str(docID) + "\n"
                    g.write(completeData)
            #print("")   
            
    @staticmethod
    def length(db):
        name = deepcopy(db)
        db = database.index.get(db)
        length = len(db)
        print("    -Length of the %s data structure is %s" % (name,length))
        return length
    
    #This function resorts a dictionary by storing its values into a list, clearing the dictionary and restoring into it
    '''
    @staticmethod
    def alphaSort(db):
        listSort = eval("sorted(database." + db + ".items())")
        exec("database." + db + ".clear()")
        
        for i in listSort:
            key, value = i;
            database.store(db,key,value)
    '''  
    @staticmethod     
    def alphaSort(db):
        data = database.index.get(db)
        listSort = sorted(data.items())
        data.clear()
        
        for i in listSort:
            key, value = i;
            database.store(db,key,value)
            
class extract:
    
    db = database()
    #g = open("extractedData.txt","w+")
    def __init__(self, file=""):
        self.file = file #The file to be extracted (Usually cacm.all
        #self.type = type #Type of extraction { T. & W. or A. }
   
    def getData(self):
        count = 0;
        sentence = "";
        
        with open(self.file, 'r') as f:
            for line in iter(f):
                try:
                    terms = line.split()
                    word = terms[0] 
                except IndexError:
                    continue;
                
                if(terms[0] == ".I"):
                    count = count + 1
                    extract.db.store("complete",count,line.replace("\n",""))
                    #print(line) #prints .I

                if(terms[0] == ".T"):
                    line = f.readline()
                    terms = line.split()
                    try:
                        word = terms[0]
                    except IndexError:
                        break;
                    
                    #print("[Title: %d] " % count, end='')
                    while((".W" != word) & (".B" != word) & (".A" != word) & (".N" != word) & (".X" != word) & (".I" != word) & (".K" != word) & (".C" != word)):
                        #print(line) prints title
                        sentence = sentence + line.rstrip() + " "
                        line = f.readline()
                        try:
                            terms = line.split()
                            word = terms[0]
                        except IndexError:
                            break;
                    
                    extract.db.store("title",count,sentence.replace("\n","").lstrip())
                    sentence = ""
                    #print("")
                
                if(terms[0] == ".A"):
                    
                    line = f.readline()
                    terms = line.split()
                    try:
                        word = terms[0]
                    except IndexError:
                        break;
                    
                    #print("[Author: %d] " % count, end='')
                    while((".W" != word) & (".B" != word) & (".A" != word) & (".N" != word) & (".X" != word) & (".I" != word) & (".K" != word) & (".C" != word)):
                        #print(line) prints author
                        sentence = sentence + line + " "
                        
                        line = f.readline()
                        
                        try:
                            terms = line.split()
                            word = terms[0]
                            
                        except IndexError:
                            break;
                        
                        
                    extract.db.store("author",count,sentence.replace("\n",""))
                    sentence = ""
                    #print("")
                                                          
                if(terms[0] == ".W"):
                    
                    line = f.readline()
                    terms = line.split()
                    try:
                        word = terms[0]
                    except IndexError:
                        break;
                    
                    #print("[Abstract: %d] " % count, end='')
                    while((".W" != word) & (".B" != word) & (".A" != word) & (".N" != word) & (".X" != word) & (".I" != word) & (".K" != word) & (".C" != word)):
                        #print(line) prints abstract
                        sentence = sentence + line.rstrip() + " "
                        line = f.readline()
                        
                        try:
                            terms = line.split()
                            word = terms[0]
                        except IndexError:
                            break;
                    
                    extract.db.store("abstract",count,sentence.replace("\n","").strip())
                    
                    #parse = str(count) + " "+ sentence + "\n"
                    #extract.g.write(parse)
                    sentence = ""
                    #print("")
                
                #Limit the number of documents
                '''if(count == 65):
                    break'''

def compileTerms():
    db = database()
    
    #If a value does not exist in the dictionary for a key, then the value will return as None, type NoneType
    
    #There are at most 3204 keys
    for key in range(1,3205):
        recordTitle = ''.join(db.getRecord("title", key)).strip().lower().split()
            
        for terms in list(recordTitle):
            db.store("compile", key, terms)
    
    for key in range(1,3205): 
        #Try catch is needed because documents without a .W will return 'None' which is stored as NoneType in the dictionary
        try:
            recordAbstract = ''.join(db.getRecord("abstract", key)).strip().lower().split()
        except:
            continue #Dont add nothing to the document id/key if there isnt a abstract
           
        for terms in list(recordAbstract):
            db.store("compile", key, terms)                      
        
def dictionaryFile():
    db = database()
    di = db.dictFile
    for key,value in iter(db.compile.items()):
        for terms in list(value):
            #clean terms here
            terms = cleanwords(terms)
            
            for subTerms in list(terms):
                
                if subTerms in di:
                    di[subTerms] = di[subTerms] + 1
                else:
                    di[subTerms] = 1
                    
                #Recompiling the stored data with clean words
                db.store("recompile", key, subTerms)
    db.alphaSort("dictFile")
    #db.printAll("recompile")
    db.printDict("dictFile")
    
    #if implementing porter algorithm you need to scan the dictionary file and recompress it and combine the words old values

def postingFile():
    #Run the keys of the dictFile dictionary and check if the terms in the compile terms contain it and assign it its term freq per doc
    #Search up a dictionary containing 3 arguments or store a dictionary where its value is a dictionary
    db = database()
    
    count = 0;
    keyList = db.dictFile.keys()
    data = []
    
    for docID in range(1,3205): #There are at most 3204 iterations needed because there are 3204 doc ID
        
        record = db.getRecord("recompile", docID) #recompiled is a dictionary of a the cleaned values extracted { .T + .W }
        
        for keys in keyList: #The keys are equivalent to the 'terms' from the dictionary file dict()
            
            if keys in record:
                for term in list(record):
                    if(keys == term):
                        count = count + 1
                        data = [docID,str(count)]
                        db.store("postFile",term,data)
            count = 0;       
            '''elif not term in keyList:
                count = 0;
                data = [docID,str(count)]
                db.store("postFile",term,data)'''
        
        
        
    db.alphaSort("postFile")
    #db.printAll("postFile")
    db.printPost("postFile")  
    
def cleanwords(word): #Returns a string of the word cleaned up
    compiled = []
    symbols ="!@#$%^&*()_-+=/*-[]{}\|;:',.<>?\"~`0123456789"
       
    for i in range(0, len(symbols)): 
        word = word.replace(symbols[i], " ")
        
    
    if(len(word) > 0):
        subWords = word.split()

        
        for terms in list(subWords):
            if(terms.isdigit()):
                continue
            if(len(terms) == 1):
                continue            
            compiled.append(terms)
        
    #print(compiled)                    
    return compiled   

def generateDict():
    
    f = open("dictionary.txt", "w+")
    db = database()
    
    for key,value in iter(db.dictFile):
        data = "%-20s" + key + value + "\n"
        f.write(data)
        
def printDatabase():
    user = input("Enter a database to print")
    db = database()
    while(user != "done"):
        try:
            db.printAll(user)
        except:
            print("That database doesn't exist try again")
            
        user = input("Enter a database to print: ")
        if(user == "done"):
            print("Terminate program")

def termSearch():
    db = database()
    user = input("Enter a term to search: ")
    while(user != "ZZEND"):

        
        if(user == "ZZEND"):
            print("Terminate program")    
        else: 
            try:
                docInfo = db.getRecord("dictFile", user)
                print("Document Freq for [%s] is %s" %(user, str(docInfo)))
                
                termFreqInfo = db.getRecord("postFile",user)
                print("Term Freq for [%s] is %s" %(user, str(termFreqInfo)))
            except:
                print("That term doesn't exist try again")
        user = input("Enter a term to search: ")                                      
def main():
    #test()
   
    db = database()
    ex = extract("cacm.all")
    
    #Extract data
    start = timeit.default_timer()
    ex.getData()
    stop = timeit.default_timer()
    time = (stop - start)
    print("cacm.all took %.4f seconds to extract" % time)
    db.length("title") #3204
    db.length("author") #3120
    db.length("abstract") #1587
        
    #Compile the data
    start = timeit.default_timer()
    compileTerms()
    stop = timeit.default_timer()
    time = (stop - start) 
    print("compiling took %.4f seconds to extract" % time)
    
    #db.printAll("compile")
    start = timeit.default_timer()
    dictionaryFile()
    stop = timeit.default_timer()
    time = (stop - start) 
    print("Generating dictionary file took %.4f seconds" % time)
    db.length("dictFile") #8774
    
    #generateDict()
    
    start = timeit.default_timer()
    postingFile()
    stop = timeit.default_timer()
    time = (stop - start) 
    print("Generating posting list file took %.4f seconds" % time)
    db.length("postFile")
    
    #printDatabase()
    termSearch()
def test():
    myDict = "myDict"
    myDict2 = "myDict2"
    
    
    db = database()
    db.store(myDict,"hey","2")
    db.store(myDict,"jo","12")
    db.store(myDict,"asia","12")
    db.store(myDict,"kelvin","22")
    db.store(myDict2,"kelvin","22")
    db.store(myDict2,"hey","1")
    db.store(myDict,"kelvin","22")
    db.alphaSort(myDict)
    db.alphaSort(myDict2)
    db.printAll(myDict)
    db.printAll(myDict2)
    
    db.getRecord(myDict,"kelvin")
    db.getRecord(myDict2,"kelvin")
    db.length(myDict)
    db.length(myDict2)
    db.getDb("myDict")
def cacmTest():
    print("The cacmTest will extract data from cacm.all")
    db = database()
    ex = extract("cacm.all")
    #ex = extract("query.text") #Note: when extracting on this file, only abstracts can be extracted unless altering the extract method
    start = timeit.default_timer()
    ex.getData()
    stop = timeit.default_timer()
    time = (stop - start)    
    #db.printAll("complete") #This dictionary test runs the .I values
    #db.printAll("title") #This dictionary stores the titles
    #db.printAll("author") #This dictionary stores the author
    #db.printAll("abstract") #This dictionary stores the abstract
    #print(db.getRecord("abstract",3061))
    print("cacm.all took %.4f seconds to extract" % time)
    db.length("title") #3204
    db.length("author") #3120
    db.length("abstract") #1587
    
def queryTest():
    print("The cacmTest will extract data from cacm.all")
    db = database()
    ex = extract("query.text")
    db.complete.clear()
    db.title.clear()
    db.author.clear()
    db.abstract.clear()
    
    #ex = extract("query.text") #Note: when extracting on this file, only abstracts can be extracted unless altering the extract method
    start = timeit.default_timer()
    ex.getData()
    stop = timeit.default_timer()
    time = (stop - start)    
    #db.printAll("complete") #This dictionary test runs the .I values
    #db.printAll("title") #This dictionary stores the titles
    #db.printAll("author") #This dictionary stores the author
    #db.printAll("abstract") #This dictionary stores the abstract
    #print(db.getRecord("abstract",3061))
    print("query.text took %.4f seconds to extract" % time)
    db.length("title") #3204
    db.length("author") #3120
    db.length("abstract") #1587    
    
main()


#Note to self, eval is good for evaluating funtions, exec is good for assigning values
#eval and exec is very slow