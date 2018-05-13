'''
CPS842 Project - Topic 1

Group Members:
    Kavinsan Thavanesan - 500642698
    Tommy Tran - 500495058
     
'''
import sys
import timeit
import re

#This class organizes the document's with its document type corresponding document block data
class document_section:
    def __init__(self, first):
        self.lines = []
        self.type_data = first.split(' ')
        self.type = self.type_data[0]


    def append(self, line):
        self.lines.append(line)


#This class is used to manage the data of the document
class document:
    abstract_cleaner = "!@#$%^&*()_-+=/*-[]{}\|;:',.<>?\"~`0123456789"
    author_cleaner = "!@#$%^&*()_-+=/*-[]{}\|;:',.<>?\"~`0123456789"

    def __init__(self, id_section):
        self.id = int(id_section.type_data[1])
        self.title = ''
        self.abstract = ''
        self.authors = []
        self.citation = []
        self.query = []

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

    def set_query(self, query_section):
        for query in query_section.lines:
            self.query.append(self._clean(query, document.abstract_cleaner))


class queryList:
    def __init__(self, file_name):
        self.documents = dict()
        self._make_context(file_name)
        self._process_context()
        self.query = dict()

        for doc_id, document in self.documents.items():
            self.query[doc_id] = document.query

    def save_queryList(self, file_name):
        with open(file_name, 'w') as fp:
            tempStr = ''
            for word, xSet in self.query.items():
                #fp.write("." + '%-7s' % str(word) + "\n")
                for item in xSet:
                    tempStr += (item + ' ')
                #re.sub('\s+', ' ', tempStr).strip()
                tempStr = re.sub('\s+', ' ', tempStr).strip().lower()
                #print(tempStr + "\n\n")
                fp.write(tempStr + "\n")
                tempStr = ''
            #fp.write(".")
        print("QueryList File created")

    def _process_context(self):
        doc = None

        #Using the context (section type) organize the data for the corresponding type
        for section in self.context:
            #print(section.type)
            #print(section.lines)
            sectType = section.type
            if (sectType == '.I'):
                # we hit a new document, so add the current one to the database
                if (doc is not None):
                    self.documents[doc.id] = doc
                doc = document(section)
            elif (sectType == '.W'):
                doc.set_query(section)
            elif (sectType == '.A'):
                doc.set_query(section)
            elif (sectType == '.N'):
                #doc.set_query(section)
                pass
            else:
                raise ValueError('Unexpected section type: ' + sectType)

        # this was the last document, no more to process
        if (doc is not None):
            self.documents[doc.id] = doc

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

class cacm:
    def __init__(self, file_name):
        self.documents = dict() # [doc_id, document]
        self.posting = dict() # [doc_id, [word, freq]]
        self.words = dict() # [doc_id, freq]
        self.citation = dict()
        self._make_context(file_name)
        self._process_context()

        for doc_id, document in self.documents.items():
            data = ' '.join(document.authors) + ' ' + document.title + ' ' + document.abstract
            data = data.lower()

            # local count (how many times it occurs in this document)
            ignore = ['','i', 'a', 'about', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'how', 'in', 'is', 'it', 'of', 'on', 'or', 'that', 'the', 'this', 'to', 'was', 'what', 'when', 'where', 'who', 'will', 'with', 'the']

            local_words = dict()
            for word in data.split(' '):
                if (word in ignore): # kinda hacky...
                    continue
                count = local_words.get(word)
                local_words[word] = (count if (count is not None) else 0) + 1
            self.posting[doc_id] = local_words

            # global count (how many documents contain a word)
            for word, freq in local_words.items():
                count = self.words.get(word)
                self.words[word] = (count if (count is not None) else 0) + 1

            self.citation[doc_id] = document.citation
        print("Total words: %d" % len(self.words))

    def save_citation(self, file_name):
        with open(file_name, 'w') as fp:
            for word, xSet in self.citation.items():
                fp.write("." + '%-7s' % str(word) + "\n")
                for item in xSet:
                    item = item.split()
                    middle = int(item[1])
                    if(middle != 5):
                        continue
                    fp.write('%-5s' % str(item[0]) + '%-2s' % str(middle) + '%-4s' % str(item[2]) + '\n')

            fp.write(".")


        print("Citation File created")
    def save_dictionary(self, file_name):
        with open(file_name, 'w') as fp:
            for word, freq in sorted(self.words.items(), key=lambda x: x[0]):
                fp.write('%-21s' % str(word) + str(freq) + '\n')
        print("Dictionary File created")
    def save_posting(self, file_name):
        data = list()
        for doc_id, local_words in self.posting.items():
            for word, freq in local_words.items():
                data.append((word, freq, doc_id))

        with open(file_name, 'w') as fp:
            for word, freq, doc_id in sorted(data, key=lambda x: x[0]):
                fp.write('%-21s' % str(word) + '%-4s' % str(freq) + str(doc_id) + '\n')

        print("Posting File created")

    def _process_context(self):
        doc = None

        #Using the context (section type) organize the data for the corresponding type
        for section in self.context:
            #print(section.type)
            #print(section.lines)
            sectType = section.type
            if (sectType == '.I'):
                # we hit a new document, so add the current one to the database
                if (doc is not None):
                    self.documents[doc.id] = doc
                doc = document(section)
            elif (sectType == '.T'):
                doc.set_title(section)
            elif (sectType == '.A'):
                doc.set_authors(section)
            elif (sectType == '.W'):
                doc.set_abstract(section)
            elif (sectType == '.X'):
                doc.set_citation(section)
            elif (sectType == '.B'):
                pass
            elif (sectType == '.N'):
                pass
            elif (sectType == '.K'):
                pass
            elif (sectType == '.C'):
                pass
            else:
                raise ValueError('Unexpected section type: ' + sectType)

        # this was the last document, no more to process
        if (doc is not None):
            self.documents[doc.id] = doc

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


def main():
    start = timeit.default_timer()
    cacm_all = cacm('cacm.all')
    cacm_all.save_dictionary('dictionary.txt')
    cacm_all.save_posting('posting.txt')
    cacm_all.save_citation('citation.txt')
    query_list = queryList('query.text')
    query_list.save_queryList('queryList.txt')
    stop = timeit.default_timer()
    time = (stop - start)
    print("%.4f seconds" % time)

main()
