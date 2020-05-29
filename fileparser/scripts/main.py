import re
from fileparser.scripts.fileExtactor import FileExtractor
from fileparser.scripts.fileParser import TextFileParser
from fileparser.models import FolderSelectInfoModel, FileReadInfoModel

def main(folder_path=None):
    '''
    The main controller of whole the file reading process

    :param folder_path: The path of the folder you want to start parser for
    :type folder_path: str
    '''


    if folder_path == None:
        return
    updateFSRStatus(folder_path, True)
    fsi_object = FolderSelectInfoModel.objects.get(folder_path__exact=folder_path)
    if fsi_object == None:
        updateFSRStatus(folder_path, False)
        return
    fri_object = FileReadInfoModel.objects.get(folder=fsi_object)
    if fri_object == None:
        updateFSRStatus(folder_path, False)
        return
    f = FileExtractor(fsi_object.folder_path, fsi_object.extensions)
    additional_file = fsi_object.additional_file_path
    additional_field = fsi_object.additional_fields
    # additonal_regex = r"^.*  (.*)\..*$"
    additional_regex = fsi_object.regex_for_additional_file_path
    try:
        if additional_file != '':
            with open(additional_file) as lines:
                subMain(f, fri_object, lines, additional_regex, additional_field)
        else:
            subMain(f, fri_object)

    except Exception as e:
        updateFSRStatus(folder_path, False)
        print("No here exception")
        print(e)
    finally:
        updateFSRStatus(folder_path, False)


def subMain(f, fri, lines=None, additonal_regex=None, additional_field=None):
    '''
    The main method calls the subMain method accordingly

    :param f: The file object you want to read
    :type f: file Object
    :param fri: The File Read Info object got from the DB
    :type fri: QueryDict
    :param lines: The file object for additonal file
    :type lines: file Object
    :param additonal_regex: regex for extracting info from additional file
    :type: str
    :param additional_field: The array consists of the name for values extracted from the additonal file
    :type additional_field: list
    '''


    groups = None
    if additonal_regex != None and additonal_regex != '':
        pattren = re.compile(additonal_regex)
    for each in f.getFiles():
        print('started reading new file')
        print(each.name)
        try:
            if lines != None:
                line = lines.readline()
                if line not in ["\n", "", None]:
                    groups = pattren.match(line)
                else:
                    groups = None
            Parser = returnRightParser(fri.folder.parser)
            if Parser == None:
                print("The parser is not found")
                return
            if groups:
                groups = list(groups.groups())
                print("should be updated from the previous one below")
                print(groups)
                if len(groups) == len(additional_field):
                    p = Parser(each, fri.length, fri.order, fri.delimeter, fri.start_line, groups, additional_field)
                else:
                    p = Parser(each, fri.length, fri.order, fri.delimeter, fri.start_line)
                p.readFile()
            else:
                p = Parser(each, fri.length, fri.order, fri.delimeter, fri.start_line)
                p.readFile()

        except Exception as e:
            print("here exception")
            print(e)
            continue


def updateFSRStatus(folder_path, status):
    '''
    The method for updating the status property in the DB for given folder_path
    '''
    try:
        FolderSelectInfoModel.objects.filter(folder_path=folder_path).update(status=status)
    except Exception as e:
        print(e)
        print('exception in updating FSR instance')

def returnRightParser(parser):
    '''
    The method for returning the instance of right Parser given the parser name

    :param parser: The name of parser
    :type parser: str

    :returns: the appropriate parser given the parser string may return nothing given the string
    '''
    if parser == None or parser == "":
        return
    parserDict = {
        "TextFileParser": TextFileParser
    }
    if parser in parserDict:
        return parserDict[parser]
    else:
        return None