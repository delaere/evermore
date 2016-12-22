import subprocess
import re

class client:
    def __init__(self, path):
        self.path_ = path

    def init(self):
        try:
            result = subprocess.check_output(['tmsu', 'init'], cwd=self.path_, stderr=subprocess.STDOUT).strip()
            # result should be "tmsu: PATH: creating database"
            if not (result.find("tmsu:")==0 and result.find("creating database")==len(result)-17):
                raise RuntimeError("Unexpected result when initializing the tag database: \n%s"%result)
        except subprocess.CalledProcessError as e:
            print "Impossible to initialize TMSU in",self.path_
            raise

    def tag(self, filename, tag, value=None, taglist={}):
        taglist[tag]=value
        tags = [ key if value is None else "%s=%s"%(key,value) for key,value in taglist.iteritems() ]
        try:
            result = subprocess.check_output(['tmsu', 'tag', filename] + tags , cwd=self.path_, stderr=subprocess.STDOUT).strip()
        except subprocess.CalledProcessError as e:
            print "Error while tagging ", filename
            raise
        
    def files(self):
        result = subprocess.check_output(['tmsu', 'files'], cwd=self.path_, stderr=subprocess.STDOUT).strip().split("\n")
        return result

    def tags(self):
        result = subprocess.check_output(['tmsu', 'tags'], cwd=self.path_, stderr=subprocess.STDOUT).strip().split("\n")
        return result

    def values(self):
        result = subprocess.check_output(['tmsu', 'values'], cwd=self.path_, stderr=subprocess.STDOUT).strip().split("\n")
        return result

    def status(self):
        result = subprocess.check_output(['tmsu', 'status'], cwd=self.path_, stderr=subprocess.STDOUT).strip().split("\n")
        return result

    def info(self):
        result = subprocess.check_output(['tmsu', 'info'], cwd=self.path_, stderr=subprocess.STDOUT).strip()
        regex = "Database: (.*)\nRoot path: (.*)\nSize: (.*)"
        output = re.match(regex,result)
        return { "database":output.group(1), "path":output.group(2), "size":output.group(3) }

