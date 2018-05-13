'''
CPS842 Project - Topic 1

Group Members:
    Kavinsan Thavanesan - 500642698
    Tommy Tran - 500495058
     
'''
import timeit
import math
from collections import Counter
import sys
from threading import Thread
from itertools import starmap
from operator import mul

class document_section:
    def __init__(self, first):
        self.lines = []
        self.type_data = first.split(' ')
        self.type = self.type_data[0]

    def append(self, line):
        self.lines.append(line)

class document:
    abstract_cleaner = "!@#$%^&*()_-+=/*-[]{}\|;:',.<>?\"~`0123456789"
    author_cleaner = "!@#$%^&*()_-+=/*-[]{}\|;:',.<>?\"~`0123456789"
    
    def __init__(self, id_section):
        self.id = int(id_section.type_data[0].replace(".",""))#Modified for search
        self.title = ''
        self.abstract = ''
        self.authors = []
        self.citation = []
    
    def set_title(self, title_section):
        self.title = self._clean(' '.join(title_section.lines), document.abstract_cleaner)
    
    def set_abstract(self, abstract_section):
        self.abstract = self._clean(' '.join(abstract_section.lines), document.abstract_cleaner)

    def set_authors(self, authors_section):
        for author in authors_section.lines:
            self.authors.append(self._clean(author, document.author_cleaner))

    def _clean(self, words, cleaner):
        for sym in cleaner:
            words = words.replace(sym, ' ')
        return words
    
    def set_citation(self, citation_section):
        for citation in citation_section.lines:
            self.citation.append(citation)
    
class search():
    
    def __init__(self, file_name):
        self._userWeight()
        self._qrels()
        self.citation = dict() #dictionary to hold citations
        self.tfValues = dict() #Key = doct id, values = list of tf values for all terms
                                # tfValues[1] = [0,0,0,0,0,1,0,0,0,2,0,0,0,1..]
                                #tf value is calculated by 1 + log(term freq)
        self.idfValues = dict() #Key = doc id, values = idf values
        self.workValues = dict()
        self.magValues = dict()
        self.cosValues = dict()
        self.pageRankValues = dict()

        self._vocabulary()
        self._make_context(file_name)
        self._proccess_context() 
        self._page_rank() 

        start = timeit.default_timer() 
        self._idfValue()
        stop = timeit.default_timer()
        time = (stop - start)       
        print("Generate idfValues %.4f seconds" % time)   
        
        start = timeit.default_timer()
        self._tfValue()
        stop = timeit.default_timer()
        time = (stop - start)        
        print("Generate tfValues/workValues/magnitude/ %.4f seconds" % time)
        
        queryCount = 1
        self.queryDict = dict()
        self.rankDict = dict()
        with open("queryList.txt","r") as fp: 
            for query in iter(fp):
                self.queryDict[queryCount] = query
                self._userQuery(query,queryCount)
                self._cos(queryCount)
                queryCount = queryCount + 1
                #if(queryCount == 4):
                #    break
        self._r_precision()
                
    def _qrels(self):
        self.qrels = dict()
        
        with open("qrels.text","r") as fp:
            for lines in iter(fp):
                lines = lines.split()
                key = int(lines[0])
                value = int(lines[1]) 
                                
                if key in self.qrels:
                    self.qrels[key].append(value)
                    
                elif not key in self.qrels:
                    self.qrels.setdefault(key, [value])
        
        self.qrelsUpdate = dict()           
        for key in range(1,65):
            if key not in self.qrels.keys():
                self.qrelsUpdate[key] = [0]
            else:
                self.qrelsUpdate[key] = self.qrels[key]
                
        #print(self.qrelsUpdate.items())
        
    def _r_precision(self):
        
        self.rPerc = dict()
        self.AP = dict()
        map = 0
        
        countRel = 0
        count = 0
        rPercision = 0
        AP = 0
        
        f = open("Eval.txt","a+")
        for i in range(1,65):
            list = self.rankDict[i]
            for items in list:
                docID = items[0]
                for docID2 in self.qrelsUpdate[i]:
                    count = count + 1
                    if(docID == docID2):
                        countRel = countRel + 1
                        AP = AP + (countRel/count)
                        
            rPercision = countRel/len(list)
            self.rPerc[i] = rPercision
            if countRel != 0:
                AP = AP/countRel
                self.AP[i] = AP
            elif countRel == 0:
                self.AP[i] = AP
            
            map = map + AP
            #print("Relevant: %d" % countRel)
            print("Query [%d] R Precision: %.2f" % (i,rPercision))
            data = "Query [%d] R Precision: %.2f\n" % (i,rPercision)
            f.write(data)
            #print("AP: %.2f" % AP)
            AP = 0
            count = 0
            countRel = 0
            rPercision = 0
        map = map/64
        
        data = "Map Value:" + str(map) + "\n"
        f.write(data)
        print("MAP: %.4f" % map)      
        f.close()
    def _page_rank(self):
        start = timeit.default_timer() 
        
        self.matrix = [0] * 3204
        a = 0.85
        prob = float("{0:.2f}".format(1 - a))
        N = 3204
        default = float("{0:.6f}".format(a/N))
        for i in range(3204):
            self.matrix[i] = [default*10] * 3204
       
        rand = dict()
        #Retrieve all the citations containing the value 5 in as the second citation value
        for i in range(1,3205):
            citationValues = self.citation[i].citation
    
            #print("Document: %d" % self.citation[i].id)
            for values in citationValues:
                values = values.split()
                left = int(values[0])
                right = int(values[2])     
                if(int(values[1]) == 5):

                    #collection = [values[0],values[1],values[2]]
                    
                    if(rand.get(right) == None):
                        rand[right] = [left]
                    elif(rand[right] != None):
                        rand[right].append(left)
                        
                    #print(str(left) + " " + str(right))
                    
                    #self.matrix[right][left] = 1
                    #print(values[0] + " " + values[1] + " " + values[2])
            #print("")   
        

        
        for i in range(1,3204): #Page i
            doclist = rand[i] 
            doclist = list(set(doclist))
             
            for j in range(0, len(doclist)):
                
                self.matrix[i][doclist[j]-1] = float("{0:.6f}".format((((1/len(doclist))*(prob)) + (a/N))))
        
        stop = timeit.default_timer()
        time = (stop - start)        
        print("Matrix P Generated %.4f seconds" % time)        
        
        self._power_method(2)
    
            
    def _power_method(self,limit):
        start = timeit.default_timer() 
        #f = open("matrix.txt","w+")
        '''
        data = ""
        for i in range(1,5): #Page i #Range should not be lower than 1,2
            for j in range(1,3204): #Page j
                data = data + str((float("{0:.3f}".format(self.matrix[i][j])))) + " "
                print(" %.3f " % self.matrix[i][j-1],end='')
          
            #f.write(data + "\n")
            print("")'''
        
        y = [[0] * 3204]
        y[0][1] = 1
        for i in range(0,limit):
            #print("t = %d" % (i))
            temp = self._matrix_mult(y, self.matrix)
            y = temp
        
        self.matrix = y[0]
        #f.write(str(self.matrix))    
   
        #f.close()
        #print(len(self.matrix[1][3203]))
        
        stop = timeit.default_timer()
        time = (stop - start)        
        print("Power Method for %d iterations Applied %.4f seconds" % (limit,time)) 
        
    def _matrix_mult(self,a,b):
        zip_b = zip(*b)
        # uncomment next line if python 3 : 
        zip_b = list(zip_b)
        return [[float("{0:.3f}".format(sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b)))) 
                 for col_b in zip_b] for row_a in a]
           
    def _proccess_context(self):
        doc = None
        
        for section in self.context:
            doc = document(section)
            doc.set_citation(section)
            #print(doc.citation)
            self.citation[doc.id] = doc #Store each document id with its document into the citation dict() 
      
    def _make_context(self, file_name):
        self.context = list()
        section = None #Section is the data for the context
        
        with open(file_name, 'r') as fp:
            for line in iter(fp):
                line = line.rstrip()
                if (line.startswith('.')):
                    if (section is not None):  
                        self.context.append(section) 
                        section = None #Once one type is found, toggle section off

                    section = document_section(line)#Store each document section object containing a doc type

                else:
                    section.append(line)#Store the corresponding data for the data type
    
    def _userWeight(self):
        print("Search.py will be done when 'OK' message appears. Type ZZEND to terminate\n")
        sum = 0
        while(sum != 1):
            user = input(("Enter the weights for cosine similarity and PageRank respectively: ")).split()   
            self.w1 = float(user[0])
            self.w2 = float(user[1])
            sum = self.w1 + self.w2
            if(sum > 1):
                print("Please enter values that sum to 1")
            
    def _userQuery(self,query,queryCount): 
        ignore = ['','i', 'a', 'about', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'how', 'in', 'is', 'it', 'of', 'on', 'or', 'that', 'the', 'this', 'to', 'was', 'what', 'when', 'where', 'who', 'will', 'with', 'the']
        print("Rank for query: [%d]" % (queryCount))
        '''
        print("Search.py will be done when 'OK' message appears. Type ZZEND to terminate\n")
        user = input(("Enter a query: "))

        if(user == "ZZEND"):
            sys.exit()
        user = user.split()
        '''
        user = query.split()
        local_words = dict()
        for term in user:
            if (term in ignore): # kinda hacky...
                continue
            count = local_words.get(term)
            local_words[term] = (count if (count is not None) else 0) + 1
            
        self.queryMag = 0
        for tfValue in local_words:
            value = local_words[tfValue]
            self.queryMag = self.queryMag + (value*value)
        self.queryMag = math.sqrt(self.queryMag)
        
        '''
        # global count (how many documents contain a word)
        for word, freq in local_words.items():
            count = words.get(word)
            words[word] = (count if (count is not None) else 0) + 1'''
        
        self.queryVector = [0] * (len(self.vocab))
        
        for term in user:
            if term in self.vocab:
                vecIndex = int(self.vocab.index(term))
                self.queryVector[vecIndex] = round(1 + math.log10(int(local_words[term])),3)
        
    def _vocabulary(self): 
        self.vocab = [] 
        with open("dictionary.txt",'r') as fp:
            for line in iter(fp):
                lines = line.split()
                term = lines[0]
                self.vocab.append(term)
    
    def _tfValue(self):
        vector = [0] * (len(self.vocab))
        
        self.db = dict()
        with open("posting.txt","r") as f:
            for line in iter(f):
                line = line.split()
                key = int(line[2]) #doc ID
                term = line[0] #term
                freq = line[1] #term freq
                bucket = self.db.get(key)
                if (bucket is None):
              
                    bucket = dict()
                    self.db[key] = bucket
        
                bucket[term] = freq

        magnitude = 0#Temporary variable for document magnitude
        num = 0 #Temporary variable for document numerator
        self.numerator = dict() #Dictionary holds numerator values for every document
        
        
        for docs in self.db.items():
            record = docs 
            key = int(record[0]) #The document ID
            dictionary = record[1] #Each term and term freq is stored in a dictionary
            
            for term in dictionary:
                freq = dictionary[term]
                vecIndex = int(self.vocab.index(term))
                element = round((1 + math.log10(int(freq))) * self.idfValues[vecIndex],3)
                vector[vecIndex] = element
                magnitude = magnitude + (element * element)
                #num = num + element* self.queryVector[vecIndex]
                
            #self.numerator[key] = num #Assign numerator value to each document
            #num = 0 #reset individual numerator
            self.workValues[key] = vector #Assign work vector values to each document
            self.magValues[key] = math.sqrt(round(magnitude,3)) #Assign magnitude values to each document
            magnitude = 0 #reset individual magnitude
            vector = [0] * (len(self.vocab)) #reset vector for individual document vocabulary vector

    def _idfValue(self): #Does not include query words
        count = 0
        with open("dictionary.txt", 'r') as fp:
            for line in iter(fp):
                line = line.split()
                freq = int(line[1])
                
                self.idfValues[count] = round(math.log10((3204/freq)),3)
                count = count + 1
        #print("There are %d idfN values" % len(self.idfValues))
        
    def _cos(self,queryCount):
        #start = timeit.default_timer()
        #f = open("score.txt",'w')
        for i in range(1,3205):
        
            numerator = sum(starmap(mul,zip(self.queryVector,self.workValues[i])))
            #numerator = sum([round(a * b,3) for a, b in zip(self.queryVector, self.workValues[i])])
            denominator = self.magValues[i] * self.queryMag
            self.cosValues[i] = round((((numerator/denominator))*self.w1) + (self.matrix[i-1]*self.w2),3)
            self.pageRankValues[i] = self.matrix[i-1]*self.w2
            
            
            
            #self.cosValues[i] = round((((self.numerator[i]/denominator))),3)
            #data = str(i) + "    " + str(round(numerator/denominator,3)) + "\n"
            #f.write(data)
        #stop = timeit.default_timer()
        #time = (stop - start)
        #print("Generate Cosine similarity scores: %.4f seconds\n" % time)
                
        relvant = Counter(self.cosValues).most_common(5)
        self.rankDict[queryCount] = relvant
        
        f = open("PageRank.txt","a+")
        data = "Rank for query: " + str(queryCount) + "\n"
        f.write(data)
        #Used for printing ranking
        count = 1
        for docs in relvant:
            docID = docs[0]
            score = docs[1]
            if(score == 0):
                break
            print("Rank [%d] Doc: [%d] Score: [%.3f]" % (count,docID,self.pageRankValues[docID]*100))
            data = "    Rank " + str(count) + " Doc: " + str(docID) + " PageRank Score: " + str(self.pageRankValues[docID]*10) + "\n"
            f.write(data)
            count = count + 1
        f.close()
def main():
    search("citation.txt")
    print("OK")
main()