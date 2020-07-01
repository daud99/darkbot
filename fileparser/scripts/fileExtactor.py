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
        self.__path = path
        self.__extensions = extensions


    def getFiles(self):
        '''
        getFiles method return the generator object for required files by the parser

        :returns: file object generator
        '''
        for each in sorted(os.scandir(self.__path), key=FileExtractor.sortingKey):
            if each.is_file():
                try:
                    if FileExtractor.pattren.match(each.name).group(1) in self.__extensions:
                        yield each
                except Exception as e:
                    continue

    @staticmethod
    def sortingKey(file):
        '''
        The method used for sorting the files in the directory

        :returns: parse the string and return the former part of the . in string
        '''
        if file.is_file() and '.' in file.name:
            try:
                return int(file.name.split('.')[0])
            except ValueError:
                return file.name.split('.')[0]
        else:
            return 0

