from optparse import OptionParser
import os
import NnexParser 
import NoteWriter

def importdata(inputfile, output, options):
    verbose = options["verbose"]
    print "Importing data from", inputfile, "to",output,"..."
    parser = NnexParser.Parser(inputfile,verbose)
    # read notebooks and create corresponding directories
    notebooks = parser.getNotebooks()
    if verbose: print "Found",len(notebooks),"notebooks."
    writer = NoteWriter.Writer(notebooks,output,verbose)
    if not options["dryrun"]: writer.createDirectories()
    # read tags
    tags = parser.getTags()
    if verbose: print "Found",len(tags),"tags."
    # read notes
    if options["dryrun"]:
        count = 0
        for note in parser.getNotes():
            if verbose: print note.title_
            count += 1
        if verbose: print "Found %d notes"%count
    else:
        for note in parser.getNotes():
            writer.write(note)
    # final printout; should be controled by an option flag (verbosity)
    print "Import completed."
    if not options["dryrun"]: writer.printReport()


class MyOptionParser: 
    def __init__(self):
        usage  = "Usage: %prog [options] source.nnex destdir"
        self.parser = OptionParser(usage=usage)
        self.parser.add_option("-d","--dry", action="store_true",
                               dest="dryrun", default=False,
             help="dry run (do not create files nor touch the database)")
        self.parser.add_option("-v","--verbose", action="store_true",
                               dest="verbose", default=False,
             help="verbose mode")

    def get_opt(self):
        """
        Returns parse list of options
        """
        opts, args = self.parser.parse_args()
        # add source and destination to the options
        if len(args) != 2:
            self.parser.error("source and destination are mandatory")
        opts.sourcefile  = os.path.abspath(os.path.expandvars(os.path.expanduser(args[0])))
        opts.destination = os.path.abspath(os.path.expandvars(os.path.expanduser(args[1])))
        # check that inputfile exists
        if not os.path.isfile(opts.sourcefile):
            self.parser.error("%s: no such file."%opts.sourcefile)
        if os.path.exists(opts.destination):
            self.parser.error("%s: destination already exists."%opts.destination)
        # check that output directory does not exist (except if an option allows it)
        return opts

if __name__ == "__main__":
    # get the options
    opts = MyOptionParser().get_opt()
    importdata(opts.sourcefile, opts.destination, opts.__dict__)

