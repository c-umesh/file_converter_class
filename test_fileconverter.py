from fileconverter import FileConverter
from fileconverter import FileConvertToJson
from fileconverter import FileConverterToXML
import pytest


@pytest.mark.parametrize("test_input,expected", [(1, "label"), (2, "Id"), (0, "link")])
def test_element_name(test_input, expected):
    core_attribute_val = FileConverter.element_name(test_input)
    assert core_attribute_val == expected


@pytest.fixture
def init_FileConverter():
    return FileConverter("sample_recs2.csv", ",", 1, 0)


def test_FileConverter(init_FileConverter):
    init_FileConverter.convert()
    expected_val = [{'label': 'Meat & Fish', 'Id': '179549', 'link': 'browse/179549',
                     'children': [{'label': 'Fish', 'Id': '176741', 'link': 'browse/179549/176741', 'children': []}]}]
    if expected_val == init_FileConverter.main_data_list:
        assert_val = True
    else:
        assert_val = False
    assert assert_val


@pytest.fixture
def init_FileConverterToXML():
    return FileConverterToXML("sample_recs2.csv", ",", 1, 0)


def test_FileConverterToXML(init_FileConverterToXML):
    init_FileConverterToXML.convert()
    with open("test_output_xml.xml", "r") as fp:
        expected_val = fp.read()
    # print(expected_val)
    # print(init_FileConverterToXML.xml_data)
    if expected_val == str(init_FileConverterToXML.xml_data):
        assert_val = True
    else:
        assert_val = False
    assert assert_val


@pytest.fixture
def init_FileConvertToJson():
    return FileConvertToJson("sample_recs2.csv", ",", 1, 0)


def test_FileConvertToJson(init_FileConvertToJson):
    init_FileConvertToJson.convert()
    with open("test_output_json.json", "r") as fp:
        expected_val = fp.read()
    if expected_val == init_FileConvertToJson.json_data:
        assert_val = True
    else:
        assert_val = False
    assert assert_val
