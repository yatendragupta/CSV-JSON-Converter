import unittest
import json
import Converter
import Logger

def read_file_data(filename):
    with open(filename, encoding="utf8") as data_file:
        json_data = json.load(data_file)
    return json_data

class TestStringMethods(unittest.TestCase):

    def test_NestedJson(self):
        sampleJson = {
                        "Base URL": [
                            {
                                "label": "THE BEST",
                                "id": "178974",
                                "link": "https://testabc.com/browse/178974",
                                "children": [
                                    {
                                        "label": "FRESH",
                                        "id": "178969",
                                        "link": "https://testabc.com/browse/178974/178969",
                                        "children": [
                                            {
                                                "label": "CHEESE",
                                                "id": "178975",
                                                "link": "https://testabc.com/browse/178974/178969/178975",
                                                "children": [
                                                    {
                                                        "label": "Dairy",
                                                        "id": "123456",
                                                        "link": "https://testabc.com/browse/178974/178969/178975/123456",
                                                        "children": []
                                                    }
                                                ]
                                            },
                                            {
                                                "label": "COOKED MEAT & ANTIPASTI",
                                                "id": "178976",
                                                "link": "https://testabc.com/browse/178974/178969/178976",
                                                "children": []
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
        # Converting test_NestedJson.csv to test_NestedJson.json
        Converter.convertToJson("test_NestedJson.csv", "test_NestedJson.json")
        # Comparing the result output of json with expected json
        self.assertEqual(read_file_data("test_NestedJson.json"), sampleJson)

    def test_InvalidCSV(self):
        str = Converter.convertToJson("test_InvalidCSV.csv", "test_InvalidCSV.json")
        self.assertEqual(str, "Required Data not found OR Invalid CSV File")


if __name__ == '__main__':
    Logger.init("UnitTest.log", "Debug")
    unittest.main()