import os
import re

class FileExtractor():
    '''
    FileExtractor object contains the method for extracting the required information
    :param path: The path of the folder
    :type path: str
    :param extensions: The allowed extension for files
    :type extensions: List
    '''


    pattren = re.compile(r"^.*(\.[a-zA-Z]{3,4}$)")


    def __init__(self, path, extensions=[".txt"]):
        self._path = path
        self._extensions = extensions


    def getFiles(self):
        '''
        getFiles method return the generator object for required files by the parser
        '''
        for each in os.scandir(self._path):
            if each.is_file():
                try:
                    if FileExtractor.pattren.match(each.name).group(1) in self._extensions:
                        yield each
                except Exception as e:
                    continue


