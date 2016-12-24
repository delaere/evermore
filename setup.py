from setuptools import setup, find_packages


setup(
    name="evermore",
    version="1.0.0",
    description="A tool to export data from Evernote to a semantic filesystem",
    long_description="""
A tool to export data from Evernote (more precisely NixNote) 
to a directory structure indexed with TMSU.

Notes are converted to markdown and attachments are saved. 
Every file is indexed with the tags from the related note.

~~~~
Usage: evermore.py [options] source.nnex destdir

Options:
  -h, --help     show this help message and exit
  -d, --dry      dry run (do not create files nor touch the database)
  -v, --verbose  verbose mode
~~~~
    """,
    url="https://github.com/delaere/evermore",
    author="Christophe Delaere",
    author_email="christophe.delaere@gmail.com",
    license="GPLv3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities"
        ],
    keywords="Evernote Nixnote TMSU migration import export",
    packages=find_packages(),
    install_requires=[ 
        'lxml',
        'html2text',],
    entry_points={
        'console_scripts': [
                'evermore=evermore.evermore:main',
            ],
        }
)
