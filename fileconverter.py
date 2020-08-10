"""
fileconverter module read csv file and can convert into nested Json or
XML format which forms a tree structure.

Classes:
    FileConverter: Base class which read csv file and it converts CSV into dict tree structure
    FileConvertToJson: extended class from FileConverter and it converts from dict to json tree structure
    FileConvertToXML: extended class from FileConverter and it converts from dict to XML tree structure
"""

import csv
import copy
import logging
import json
import dicttoxml
from xml.dom.minidom import parseString


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class FileConverter:
    """
    Base class which read csv file and it converts CSV into dict tree structure
    Class Attributes:
        core_attribute :  reprent core columns set and labels in the csv file
        length :  number of core attributes
    Instance Attributes:
        main_data : main dictonary object which contains nested dict tree strcuture
        level_dict : dictonary of list maintained at each level/heirarchy
        main_data_list : list of main_data
        input_filename : CSV filename
        delimiter : delimiter used in CSV filename
        skip_header : No. of rows to be skipped for which is not part of tree structure
        skip_columns: No. of columns to be skipped for which is not part of tree structure
    """
    core_attribute = {1: 'label', 2: 'Id', 0: 'link'}
    length = len(core_attribute)

    def __init__(self, input_filename: str, delimiter: str,
                 skip_header: int, skip_columns: int
                 ):
        """initilazation code to construct base object"""
        self.main_data = {}
        self.level_dict = {}
        self.main_data_list = []
        self.input_filename = input_filename
        self.delimiter = delimiter
        self.skip_header = skip_header
        self.skip_columns = skip_columns
        # self.json_data = ''

    def read_and_clean_file(self) -> list:
        """
        load file into list of list , excluding no. of rows and columns are
        passed as skip_header and skip_columns. It also exclude empty rows.
        """
        tab_row_cols = []
        with open(self.input_filename) as csv_fp:
            file_reader = csv.reader(csv_fp, delimiter=self.delimiter)
            cntr = 0
            for line in file_reader:
                if cntr < self.skip_header:
                    cntr = cntr + 1
                    continue
                if not ''.join(line):
                    continue
                tab_row_cols.append(line[self.skip_columns::])
            return tab_row_cols

    @staticmethod
    def element_name(column_no: int) -> str:
        """ lookup for core attributes"""
        key = column_no % FileConverter.length
        return FileConverter.core_attribute.get(key)

    def get_node_with_level(self, row: list) -> dict:
        """
        derives value label ,id and link for given row along with
        its level in the hierarchy
        """
        log.info('get_node_with_level')
        sub_data = {'label': '', 'Id': '', 'link': ''}
        col_no = 0
        for item in row:
            col_no = col_no + 1
            if bool(item):
                key = self.element_name(col_no)
                sub_data[key] = item
            else:
                break
        if col_no < FileConverter.length:
            col_no = col_no - 1
        level = col_no / FileConverter.length
        sub_data['level'] = int(level)
        return sub_data

    def add_node(self, row: list) -> None:
        """node is added as per the level in the dict tree hierarchy """
        log.info('add node')
        sub_data = self.get_node_with_level(row)
        level = sub_data['level']
        sub_data.popitem()
        sub_data['children'] = []
        log.debug('sub_data : %s', sub_data)
        if level == 1:
            # parent or root node
            self.level_dict[level] = sub_data['children']
            self.main_data_list.append(copy.copy(sub_data))
        else:
            # each dictionary maintain the reference of last children node added as per the level
            self.level_dict[level] = self.level_dict[level - 1]
            log.debug('level_dict[level] : %s', self.level_dict[level])
            log.debug('level_dict[level-1] : %s', self.level_dict[level - 1])
            self.level_dict[level].append(copy.copy(sub_data))
            self.level_dict[level] = sub_data['children']

    def build_tree(self, row_tables: list) -> None:
        """nodes are nested in dictornary object """
        log.info('build_tree')
        no_of_cols = len(row_tables[1])
        log.info('intializing dictionary for each level with list')
        for c in range(0, no_of_cols, FileConverter.length):
            level = int(c / FileConverter.length) + 1
            self.level_dict[level] = []
        log.info('adding node to dictonary tree based on its heirarchy')
        for row in row_tables:
            self.add_node(row)

    def convert(self):
        """read csv file and converts into dictonary which is nested tree structure """
        try:
            log.info('reading csv file')
            row_tables = self.read_and_clean_file()
            log.info('building dictonary with children')
            self.main_data_list = []
            self.build_tree(row_tables)
        except FileNotFoundError:
            log.error('csv file missing')


class FileConvertToJson(FileConverter):
    """extended class from FileConverter and it converts from dict to json tree structure"""

    def convert(self):
        """overrides base convert functions and converts dictonary tree to json tree"""
        self.json_data = ''
        super().convert()
        self.json_data = json.dumps(self.main_data_list, indent=4)

    def __enter__(self) -> 'self':
        """to implement context managament control"""
        log.info('inside enter dunder')
        self.convert()
        # print(self.json_data)
        return self

    def write(self, output_filename: str):
        """extend the base class and write json tree contents into file"""
        with open(output_filename, 'w') as json_fp:
            json_fp.write(self.json_data)

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        log.info('inside exit dunder')
        if exc_type is FileNotFoundError:
            pass
        elif exc_type:
            self.main_data_list = []
            log.error('some unexpected error occured')


class FileConverterToXML(FileConverter):
    """extended class from FileConverter and it converts from dict to XML tree structure"""

    def convert(self):
        """overrides base convert functions and converts dictonary tree to xml tree"""
        self.xml_data = ''
        super().convert()
        self.xml_data = dicttoxml.dicttoxml(self.main_data_list, attr_type=False)

    def __enter__(self) -> 'self':
        """to implement context managament control"""
        log.info('inside enter dunder')
        self.convert()
        return self

    def write(self, output_filename: str):
        """extend the base class and write xml tree contents into file"""
        dom = parseString(self.xml_data)
        with open(output_filename, 'w') as fp:
            fp.write(dom.toprettyxml())

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        log.info('inside exit dunder')
        if exc_type is FileNotFoundError:
            pass
        elif exc_type:
            self.main_data_list = []
            log.error('some unexpected error occured')
