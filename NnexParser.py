import os
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
        self.updated_ = None
        self.notebookGuid_ = None
        self.ressources_ = []
        self.tags_ = {}
        self.valid_ = False
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
        self.valid_ = (None not in [self.guid_,self.title_,self.content_,self.created_,self.updated_,self.notebookGuid_])

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
        self.valid_ = False
        # read the ressource
        for subel in element:
            if subel.tag=="Guid": self.guid_ = subel.text
            if subel.tag=="NoteGuid": self.noteGuid_ = subel.text
            if subel.tag=="Data": 
                for c in subel.getchildren():
                    if c.tag=="Body":
                        self.data_ = binascii.unhexlify(c.text) if c.text is not None else None
            if subel.tag=="Mime": self.mime_ = subel.text
            if subel.tag=="ResourceAttributes":
                for c in subel.getchildren():
                    if c.tag=="FileName" : self.filename_ = c.text
        # add missing filename if needed
        if self.filename_ is None:
            extension = mimetypes.guess_extension(self.mime_, False) if self.mime_ is not None else None
            if extension is None: extension = ".bin"
            self.filename_ = self.guid_ + extension if self.guid_ is not None else None
        # sanity checks
        self.valid_ = (None not in [self.guid_,self.noteGuid_,self.data_,self.filename_])

class Parser:
    def __init__(self, inputfile, verbose=True):
        self.inputfile_ = inputfile
        self.verbose_ = verbose
        self.fileSize_ = os.path.getsize(self.inputfile_)
        self.position_ = 0
        
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
        with open(self.inputfile_, 'r') as f:
            context = etree.iterparse(f,events=('end',), tag='Note',huge_tree=True)
            for event, element in context:
                self.position_ = float(f.tell())
                yield Note(element)
                element.clear()

    def progress(self):
        return self.position_/self.fileSize_

