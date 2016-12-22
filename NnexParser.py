import binascii
import mimetypes
from lxml import etree

class Note:
    def __init__(self, element):
        """ This constructor looks for the following tags in childs:
        Guid
        Title
        Content
        ContentHash               IGNORE
        ContentLength             IGNORE
        Created
        Updated
        Active                    IGNORE
        UpdateSequenceNumber      IGNORE
        NotebookGuid
        Attributes                IGNORE
            SubjectDate
            Latitude
            Longitude
            Altitude
        Dirty                     IGNORE
        NoteResource
        """
        # defaults
        self.guid_ = None
        self.title_ = None
        self.content_ = None
        self.created_ = None
        self.Updated_ = None
        self.notebookGuid_ = None
        self.ressources_ = []
        self.tags_ = {}
        # read the note
        for subel in element:
            if subel.tag=="Guid": self.guid_ = subel.text
            if subel.tag=="Title": self.title_ = subel.text
            if subel.tag=="Content": self.content_ = subel.text
            if subel.tag=="Created": self.created_ = subel.text
            if subel.tag=="Updated": self.updated_ = subel.text
            if subel.tag=="NotebookGuid": self.notebookGuid_ = subel.text
            if subel.tag=="Tag":
                for c in subel.getchildren():
                    if c.tag=="Guid" : guid = c.text
                    if c.tag=="Name" : name = c.text
                self.tags_[guid] = name
            if subel.tag=="NoteResource" :
                self.ressources_.append(Ressource(subel))
        # sanity checks
        assert(self.guid_ is not None)
        assert(self.title_ is not None)
        assert(self.content_ is not None)
        assert(self.created_ is not None)
        assert(self.updated_ is not None)
        assert(self.notebookGuid_ is not None)

class Ressource:
    def __init__(self,element):
        """ This constructor looks for the following tags in childs:
        Guid
        NoteGuid
        Data
        Mime
        Width                     IGNORE
        Height                    IGNORE
        Duration                  IGNORE
        Active                    IGNORE
        Recognition               IGNORE
            Body
            BodyHash
            Size
        ResourceAttributes
            FileName
            Attachment            IGNORE
        """
        # defaults
        self.guid_ = None
        self.noteGuid_ = None
        self.data_ = None
        self.mime_ = None
        self.filename_ = None
        # read the ressource
        for subel in element:
            if subel.tag=="Guid": self.guid_ = subel.text
            if subel.tag=="NoteGuid": self.noteGuid_ = subel.text
            if subel.tag=="Data": 
                for c in subel.getchildren():
                    if c.tag=="Body":
                        self.data_ = c.text
            if subel.tag=="Mime": self.mime_ = subel.text
            if subel.tag=="ResourceAttributes":
                for c in subel.getchildren():
                    if c.tag=="FileName" : self.filename_ = c.text
        # sanity checks
        assert(self.guid_ is not None)
        assert(self.noteGuid_ is not None)
        assert(self.data_ is not None)
        assert(self.mime_ is not None or self.filename_ is not None)
        # add missing filename if needed
        if self.filename_ is None:
            extension = mimetypes.guess_extension(self.mime_, False)
            if extension is None: extension = ".bin"
            self.filename_ = self.guid_ + extension
        # work on the data part
        self.data_ = binascii.unhexlify(self.data_)

class Parser:
    def __init__(self, inputfile):
        self.inputfile_ = inputfile
        
    def getNotebooks(self):
        output = {}
        context = etree.iterparse(self.inputfile_,events=('end',), tag='Notebook',huge_tree=True)
        for event, element in context:
            name = None
            guid = None
            for c in element.getchildren():
                if c.tag=="Guid" : guid = c.text
                if c.tag=="Name" : name = c.text
            if name is None or guid is None:
                raise RuntimeError("Incomplete Notebook description: (name,guid)=(%s,%s)"%(name,guid))
            output[guid] = name
            element.clear()
        return output

    def getTags(self):
        output = {}
        context = etree.iterparse(self.inputfile_,events=('end',), tag='Tag',huge_tree=True)
        for event, element in context:
            name = None
            guid = None
            for c in element.getchildren():
                if c.tag=="Guid" : guid = c.text
                if c.tag=="Name" : name = c.text
            if name is None or guid is None:
                raise RuntimeError("Incomplete Tag description: (name,guid)=(%s,%s)"%(name,guid))
            output[guid] = name
            element.clear()
        return output

    def getNotes(self):
        context = etree.iterparse(self.inputfile_,events=('end',), tag='Note',huge_tree=True)
        for event, element in context:
            yield Note(element)
            element.clear()

