import hashlib
import concurrent.futures
import pathlib
import re
import os
import chardet
from iterablequeue import IterableQueue


class Engine(IterableQueue):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.unprocessed = IterableQueue()
        self.processed   = IterableQueue()
        self.num_cores   = os.cpu_count()
        #fix this, make it more dynamic
        self.regex = re.compile(b"(set\s*ansi_padding\s*off)", flags=re.IGNORECASE)
        self.replacement = b'SET ANSI_PADDING ON'


    def __getBytesFromFile__(self, filename=None):
        if filename is not None:
            with open(filename, mode='rb') as file:
                return file.read()
        else:
            return None

    def __hashContents__(self, bytesToHash=None):
        if bytesToHash is not None:
            return hashlib.sha512(bytesToHash).hexdigest()
        else:
            return None

    def __enumerateFiles__(self, dirs=[], extension='*.sch'):
        files = set()
        for dir in dirs:
            #TODO: multi-thread this?
            #TODO: deal with how to have distinct files, a topleveldir method to 
            # only iterate through unique top level directories?
            filesInCurDir = (file for file in pathlib.Path(dir).rglob(extension) if file.is_file())
            for file in filesInCurDir:
                files.add(file)

    def __transfer__(self, source=None, destination=None):
        for item in source:
            destination.put(item)

    def __take__(self, source=None):
        if source is not None:
            yield from (item for item in source)
        else:
            return None
    
    def __getEncoding__(self, filename=None):
        if file is not None:
            fileContents = self.__getBytesFromFile__(filename=filename)
            return chardet.detect(fileContents)['encoding']
        else:
            return None
    
    def __findAndReplace__(self, contents=None, search=self.regex, replacement=self.replacement):
        if all(contents,search,replacement):
            return re.sub(search, contents, replacement) 
        else:
            return None 

    def __setup__(self, *args, **kwargs):
        files = self.__enumerateFiles__(dirs=kwargs['directories'])
        self.__transfer__(source=files, destination=self.unprocessed)
        
















