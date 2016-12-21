from optparse import OptionParser

# call independently the class to interface with TMSU
# - need a method to tag a file, mostly, using subprocess.check_output as in https://github.com/talklittle/tmsu-nautilus-python/blob/master/tmsu_tags.py#L31
import TmsuClient # may not be needed here (all done in NoteWriter)
import NnexParser 
import NoteWriter

def importdata(inputfile, output, options):
    print "Importing data from", inputfile, "to",output,"..."
    parser = NnexParser.Parser(inputfile)
    # read notebooks and create corresponding directories
    notebooks = parser.getNotebooks()
    print "Found",len(notebooks),"notebooks."
    writer = NoteWriter.Writer(notebooks,output)
    writer.createDirectories() # should also do the tmsu init
    # read tags
    tags = parser.getTags()
    print "Found",len(tags),"tags."
    # read notes
    #TODO: NnexParser notes should yield a note (generator)
    while note in parser.getNotes():
#     the nnexParser should return a nnexNote that we then pass to the noteWriter. That class writes the file(s) to disk and tags them using TMSU
        writer.write(note) # since the writer knows about notebooks and output, it knows where to create the file
    # final printout; should be controled by an option flag (verbosity)
    writer.printReport()


class MyOptionParser: 
    def __init__(self):
        usage  = "Usage: %prog [options] source.nnex destdir"
        self.parser = OptionParser(usage=usage)
        self.parser.add_option("-r","--replace", action="store_true", 
                               dest="replace", default=False,
             help="replace existing values")
        self.parser.add_option("-d","--dry", action="store_true",
                               dest="dryrun", default=False,
             help="dry run (do not touch the database)")
        # TODO: verbosity

    def get_opt(self):
        """
        Returns parse list of options
        """
        opts, args = self.parser.parse_args()
        #TODO add source and destination to the options
        # check that inputfile exists
        # check that output directory does not exist (except if an option allows it)
        return opts

if __name__ == "__main__":
    # get the options
    optmgr = MyOptionParser()
    opts = optmgr.get_opt()
    importdata(opts["inputfile"], opts["output"], **opts.__dict__)

