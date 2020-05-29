# from fileExtactor import FileExtractor # for running as script
from abc import abstractmethod, ABC
from gatherdumps.models import Email_passwords
from search.api import misc

class FileParser(ABC):
    '''
    Abstract class for different file type parsers
    '''
    def __init__(self, file, length, field_order, delimeter = [":"], start_line = 0):
        self._file = file
        self._length = length
        self._field_order = field_order
        self._delimeter = delimeter
        self._start_line = start_line

    @abstractmethod
    def readFile(self):
        '''
        Abstract method that's need to be override by all the derived class
        '''
        pass

    @staticmethod
    def lineStriping(line):
        '''
        Static method parses the given input
        :param line: The text you want to remove spaces and next line \n from the end
        :type line: str

        :returns: line string after removing the special character from the right side and spaces from the both sides of the given file
        '''
        return ((line.encode('ascii', 'ignore')).decode('utf-8').strip()).rstrip(r"\n")

    @staticmethod
    @misc.checkRecordUniqueness
    def storeInDb(each):
        '''
        Static method use to store given object in table Email_passwords
        :param each: The object you want to save in DB
        :type each: dict
        '''
        # misc.validateSavageInEmailPassword(each)
        try:
            if "email" in each:
                each["before_at"], each["domain"] = misc.returnTwo(each["email"])
                each["email"] = each["email"].lower()
            if not (each == {}):
                e = Email_passwords(**each)
                e.save()
        except Exception as e:
            # pass
            print(e)
            print('exception while storing in email_passwords table')

        # print('stored successfully check your DB')



class TextFileParser(FileParser):
    '''
    TextFileParser object used to parse the text files
    :param file: The file object
    :type file: file object
    :param length: The number of values contain by the file in each row
    :type length: int
    :param field_order: The name for the values in each row
    :type field_order: list
    :param delimeter: The value in which you want to seperate the values from each other in a row
    :type delimeter: list
    '''


    def __init__(self, file, length, field_order, delimeter = [":"], start_line = 0, additional_values = None, additional_fields = None):
        super().__init__(file, length, field_order, delimeter, start_line)
        self.__additional_values = additional_values
        self.__additional_fields = additional_fields


    def readFile(self):
        '''
        Instance Method readFile and process it
        '''
        if len(self._delimeter) == 1:
            self._delimeter = [ self._delimeter[0] for x in range(self._length-1) ]
        with open(self._file) as lines:
            lines.seek(0)
            for _ in range(self._start_line):
                lines.readline()
            while(True):
                try:
                    line = lines.readline()
                    if line == "" or line == None:
                        break
                    line = super().lineStriping(line)
                    leak = TextFileParser.processLine(line, self._delimeter.copy(), self._field_order.copy(), {})
                    if self.__additional_fields != None and self.__additional_values != None:
                        for index in range(len(self.__additional_values)):
                            leak[self.__additional_fields[index]] = self.__additional_values[index]
                    super().storeInDb(leak)
                except Exception as e:
                    print(e)
                    continue

    @staticmethod
    def processLine(line, sep, order_fields, d):
        '''
        Static method that takes in the line and return the respective object
        :param line: The line you want to process
        :type line: str
        :param sep: The seperator for given fields
        :type sep: list
        :param order_fields: The name for fields with sequence to specify the order
        :type order_fields: list
        :param d: For the sake of recurrsion empty object
        :type d: dict


        :returns: a dict containing email password complete row
        '''

        if len(sep) == 0:
            d[order_fields[0]] = TextFileParser.lowerCaseValue(order_fields[0], line)
            return d

        line = list(line.partition(sep[0]))
        d[order_fields[0]] = TextFileParser.lowerCaseValue(order_fields[0], line[0])
        sep.pop(0)
        order_fields.pop(0)
        return TextFileParser.processLine(line[-1], sep, order_fields, d)

    @staticmethod
    def lowerCaseValue(key, value):
        '''
        Static Method to return the value as lower for specific key values
        :param key: The key based on which value will be converted to lower or not
        :type value: str
        :param value: The value which will be converted to lower case
        :type value: str

        :returns: lower case string value
        '''

        if key == "email":
            value = value.lower()
        return value

