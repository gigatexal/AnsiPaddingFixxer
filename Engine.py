import hashlib
import concurrent.futures
import pathlib
import re
import os
from iterablequeue import IterableQueue


class Engine(IterableQueue):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.unprocessed = IterableQueue()
        self.processed   = IterableQueue()
        self.num_cores   = os.cpu_count()
        #fix this, make it more dynamic
        self.regex = re.compile(r"(set\s*ansi_padding\s*off)", flags=re.IGNORECASE)

    def __getBytesFromFile__(self, filename=None):
        if filename is not None:
            with open(filename, mode='rb') as file:
                return file.read()
        else:
            return None

    def __enumerateFiles__(self, dirs=[], extension='*.sch'):
        for dir in dirs:
            yield from (file for file in pathlib.Path(dir).rglob(extension))

    def __transfer__(self, source=None, destination=None):
        for item in source:
            destination.put(item)

    def __take__(self, source=None):
        if source is not None:
            yield from (item for item in source)

    def __hashContents__(self, bytesToHash=None):
        if bytesToHash is not None:
            return hashlib.sha512(bytesToHash).hexdigest()
        else:
            return None

    def __setup__(self, *args, **kwargs):
        files = self.__enumerateFiles__(dirs=kwargs['directories'])
        self.__transfer__(source=files, destination=self.unprocessed)
        
















