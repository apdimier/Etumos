from __future__ import absolute_import
from __future__ import print_function
from six.moves import input
try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import zipfile
import xml.dom.minidom

from types import StringType,\
                  UnicodeType
"""
Module extracting text from MS XML Word document (.docx).
(Inspired by python-docx <https://github.com/mikemaccana/python-docx>)

        Dimier Alain version 5.0e-23 (alain.dimier at gmail dot com)
"""

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'


def get_doc_text(path):
    """
    Take the path of a docx or a dot file as argument, return the text in unicode.
    """
    if "docx" == path[-4:]:
        document = zipfile.ZipFile(path)
        xml_content = document.read('word/document.xml')
        document.close()
        tree = XML(xml_content)
    #print tree

        paragraphs = []
        for paragraph in tree.getiterator(PARA):
            texts = [node.text for node in paragraph.iter(TEXT) if node.text]
            if texts:
                paragraphs.append(''.join(texts))
                pass
            pass
    #print paragraphs
        return paragraphs
#        
    elif "odt" == path[-3:]:
        document = zipfile.ZipFile(path)
        xml_content = document.read('content.xml')
        document.close()
        doc = xml.dom.minidom.parseString(xml_content)
        print(" doc: ",doc)
        print("doc::end")
        #paras = doc.getElementsByTagName('text:span')
        #paras = doc.getElementsByTagName('text:p')
        #
        # we get here all elements Headers, text and table components: 
        #
        paras = doc.getElementsByTagName("*")
        print("I have ", len(paras), " paragraphs ")
        paragraphs = []
        for p in paras:
            for ch in p.childNodes:
                if ch.nodeType == ch.TEXT_NODE:
                    paragraphs.append(''.join(ch.wholeText))
                    pass
                pass
            pass
        print(paragraphs)
        return paragraphs
    else:
        print() 
        raise Warning("only docx and odt files are handled")    
    #return '\n\n'.join(paragraphs)
 
def get_doc_tables(path):
    """
    the get_doc_table has been written based on an odt file which had an "odt" bug.
    The first table is the meshlayer table
    """
    document = zipfile.ZipFile(path)
    xml_content = document.read('content.xml')
    document.close()
    doc = xml.dom.minidom.parseString(xml_content)
    print(" doc: ",doc)
    print("doc::end")
    #paras = doc.getElementsByTagName('text:span')
    paras = doc.getElementsByTagName('text:p')
    print("I have ", len(paras), " paragraphs ")
    paragraphs = []
    for p in paras:
        for ch in p.childNodes:
            if ch.nodeType == ch.TEXT_NODE:
                paragraphs.append(''.join(ch.wholeText))
                pass
            pass
        pass
    print(paragraphs)
    listOfTables = []

    print("listOfTables 1: ",listOfTables)
    ind = 0
    indt = 0
    tables = []
    #
    # we create a list of tables with, for each table, the dimensions as first argument.
    #
    for t in listOfTables:
        indf = ind+t[0]*t[1]
        print(ind,indf)
        tables.append(paragraphs[ind:indf])
        ind = indf
        tables[-1].insert(0,t)
#        indt+=1
        pass
    return tables

def get_tableDim(tlist):
    """
    A list extracted from a word document.
    The table should be made of a list of alphabetic references followed by digits
    """
    lineTableLength = 0
    for element in tlist:
        if element.isalnum() and not element.isdigit():
            lineTableLength+=1
            pass
        else:
            break
    print(tlist)
    print(lineTableLength,len(tlist))
    input("def get_tableDim")
    numberOfLines = len(tlist)/lineTableLength
    return (lineTableLength,numberOfLines)
    
def get_doc_table(path):
    """
    the get_doc_table has been written based on an odt file which had an "odt" bug.
    The first table is the meshlayer table
    """
    document = zipfile.ZipFile(path)
    xml_content = document.read('content.xml')
    document.close()
    doc = xml.dom.minidom.parseString(xml_content)
    print(" doc: ",doc)
    print("doc::end")
    #paras = doc.getElementsByTagName('text:span')
    paras = doc.getElementsByTagName('text:p')
    print("I have ", len(paras), " paragraphs ")
    paragraphs = []
    for p in paras:
        for ch in p.childNodes:
            if ch.nodeType == ch.TEXT_NODE:
                paragraphs.append(''.join(ch.wholeText))
                pass
            pass
        pass
    print(paragraphs)
    listOfTables = []
    lineTableLength = 0
    for p in paragraphs:
        if p.isalpha():
            lineTableLength+=1
            pass
        elif p.isalnum() and lineTableLength != 0:
            listOfTables.append([lineTableLength])
            lineTableLength = 0
            pass
        else:
            pass
    indList = 0
    ind = 0
    columnTableLength = 1
    print("listOfTables 0: ",listOfTables)
    for p in paragraphs:
        if p.isalpha() and columnTableLength == 1:
            ind+=1
            pass
        elif p.isalpha() and columnTableLength != 1:
            listOfTables[indList].append(ind/listOfTables[indList][0]+1)
            columnTableLength = 1
            indList+=1
            ind = 1
            pass
        elif p.isalnum():
            columnTableLength = 2
            ind+=1
            pass
        else:
            pass
    listOfTables[indList].append(ind/listOfTables[indList][0])
    print("listOfTables 1: ",listOfTables)
    ind = 0
    indt = 0
    tables = []
    #
    # we create a list of tables with, for each table, the dimensions as first argument.
    #
    
    for t in listOfTables:
        indf = ind+t[0]*t[1]
        print(ind,indf)
        tables.append(paragraphs[ind:indf])
        ind = indf
        tables[-1].insert(0,t)
        pass
#        indt+=1
    return tables

   
class DocxReader:
    def __init__(self,filename):
        """
        Open a docx file.
        """
        self.filename = filename
        self.my_docx = zipfile.ZipFile(filename)
        self.filelist = self.my_docx.infolist()
    

    def showContent(self):
        """
        Just tell me what files exist in the ODF file.
        """
        for s in self.filelist:
            #print s.orig_filename, s.date_time,
            s.filename, s.file_size, s.compress_size
            print(s.orig_filename)
            pass
        return None

    def getContents(self):
        """
        Just read the paragraphs from an XML file.
        """

        xml_content = self.my_docx.read('word/document.xml')
        self.my_docx.close()
        tree = XML(xml_content)

        self.text_in_paragraphs = []
        for paragraph in tree.getiterator(PARA):
            texts = [node.text for node in paragraph.iter(TEXT) if node.text]
            if texts:
                self.text_in_paragraphs.append(''.join(texts))
                pass
            pass
    #print paragraphs
        return self.text_in_paragraphs

            
            
class OdfReader:
    def __init__(self,filename):
        """
        Open an ODF file.
        """
        self.filename = filename
        self.m_odf = zipfile.ZipFile(filename)
        self.filelist = self.m_odf.infolist()

    def showContent(self):
        """
        Just tell me what files exist in the ODF file.
        """
        for s in self.filelist:
            #print s.orig_filename, s.date_time,
            s.filename, s.file_size, s.compress_size
            print(s.orig_filename)
            pass

    def getSpec(self):
        """
        Just reads the paragraphs from an XML file.
        """
        ostr = self.m_odf.read('content.xml')
        doc = xml.dom.minidom.parseString(ostr)
        paras = doc.getElementsByTagName('text:span')
        print("I have ", len(paras), " paragraphs ")
        self.specs = []
        for p in paras:
            for ch in p.childNodes:
                if ch.nodeType == ch.TEXT_NODE:
                    self.specs.append(''.join(ch.wholeText.encode('UTF-8')))
                    pass
                pass
            pass

    def getContents(self):
        """
        Just read the paragraphs from an XML file.
        """
        ostr = self.m_odf.read('content.xml')
        doc = xml.dom.minidom.parseString(ostr)
        paras = doc.getElementsByTagName('text:p')
        print("I have ", len(paras), " paragraphs ")
        self.text_in_paras = []
        for p in paras:
            for ch in p.childNodes:
                if ch.nodeType == ch.TEXT_NODE:
                    self.text_in_paras.append(ch.data)
                    pass
                pass
            pass
        return None

    def findIt(self,name):
        for s in self.text_in_paras:
            if name in s:
                print(s.encode('utf-8'))
                pass
            pass
        return None

#                   logK25 = "[(" Tr",1)]",\
               

def formationReactionIdentification(a):
    print(" 0 ",a)
    string = a[a.index("=")+1:]
    print(" 1 ",string)
    try:
        lString = string.split(" + ")
        print(" 1 2",lString)
    except:
        lString = [string]
    print(" 2 ",lString)
    listOfTuples = "["
    for string in lString:
        print("2 3 ",string)
        listOfTuples+="(\""+string+"\",1)"
        print("3 2 ",listOfTuples)
        return None
    print(" 3 ",listOfTuples)
    listOfTuples+= "]"
    return listOfTuples

