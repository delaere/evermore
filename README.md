# evermore
A tool to export data from Evernote (more precisely NixNote) to a directory structure indexed with TMSU.

Evermore creates one directory per notebook in the destination location. Notes are converted to markdown and attachments are saved in the same directory as the note. Every file is indexed with the tags from the related note. Among other things, evermore preserves the modification time of notes.

~~~~
Usage: evermore.py [options] source.nnex destdir

Options:
  -h, --help     show this help message and exit
  -d, --dry      dry run (do not create files nor touch the database)
  -v, --verbose  verbose mode
~~~~

Requirements:
python 2.7, TMSU, python2-lxml, python-html2text
