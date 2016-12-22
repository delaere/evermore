import TmsuClient
import pprint
import os
from html2text import HTML2Text

def html2md(title,text):
    html2plain = HTML2Text(None, "")
    html2plain.feed("<h1>%s</h1>" % title)
    html2plain.feed(text)
    return html2plain.close()

def filename(name):
    if os.path.exists(name):
        fname, file_extension = os.path.splitext(name)
        # check if it ends already by .n, then increment. Otherwise add .1
        if os.path.basename(fname).split(".")[-1].isdigit():
            newname = '.'.join(os.path.basename(fname).split(".")[:-1]+[str(int(os.path.basename(fname).split(".")[-1])+1)])
            #iterate if needed
            return filename(os.path.join(os.path.dirname(fname),newname+file_extension))
        return filename(''.join([fname,'.1',file_extension]))
    else:
        # unique: do nothing and exit
        return name

class Writer:
    def __init__(self,notebooks,output,verbose=True):
        self.notebooks_ = notebooks
        self.output_ = os.path.abspath(output)
        self.tmsu_ = TmsuClient.client(self.output_)
        self.countNotes_ = 0
        self.countFiles_ = 0
        self.verbose_ = verbose

    def createDirectories(self):
        # here we must check that it doesn't exist, create output and a dir for each workbook, and finally run tmsu init
        # create the destination directory
        if not os.path.exists(self.output_):
                os.makedirs(self.output_)
        else:
            raise RuntimeError("%s exists!"%self.output_)
        # loop over notebooks and create directories
        for guid,name in self.notebooks_.iteritems():
            os.makedirs(os.path.join(self.output_,''.join(e for e in name if e.isalnum() or e.isspace())))
        # init the db
        self.tmsu_.init()

    def write(self,note):
        # get the directory where to write the note.
        notebook = self.notebooks_[note.notebookGuid_]
        path = os.path.join(self.output_,''.join(e for e in notebook if e.isalnum() or e.isspace()))
        # filename for the note
        noteFilename = filename(os.path.join(path,''.join(e for e in note.title_ if e.isalnum() or e.isspace()))+".md")
        # convert note to markdown and write to noteFilename
        content = html2md(note.title_,note.content_)
        if self.verbose_: print "Writing",noteFilename
        with open(noteFilename, 'wb') as output_file:
            output_file.write(content.encode(encoding='utf-8'))
        self.countFiles_ += 1
        # set the access and modified times of the file specified by path.
        os.utime(noteFilename,(int(note.updated_)/1000,int(note.updated_)/1000))
        # tag the note
        for _,tag in note.tags_.iteritems():
            self.tmsu_.tag(noteFilename,tag)
        # now tackle ressources
        for ressource in note.ressources_:
            ressourceFilename = filename(os.path.join(path,ressource.filename_))
            if self.verbose_: print "Writing",ressourceFilename
            with open(ressourceFilename,"wb") as fout: fout.write(ressource.data_)
            # set the access and modified times of the file specified by path.
            os.utime(ressourceFilename,(int(note.updated_)/1000,int(note.updated_)/1000))
            # tag ressourceFilename
            for _,tag in note.tags_.iteritems():
                self.tmsu_.tag(ressourceFilename,tag)
            self.countFiles_ += 1
        # count 
        self.countNotes_ += 1

    def printReport(self):
        pprint.pprint(self.tmsu_.info())
        print "Number of Notes processed:", self.countNotes_
        print "Number of Files created:", self.countFiles_
        print "Number of Files tagged:", len(self.tmsu_.files())
        print "Number of Tags:",len(self.tmsu_.tags())
        print "Number of Notebooks:",len(self.notebooks_)
