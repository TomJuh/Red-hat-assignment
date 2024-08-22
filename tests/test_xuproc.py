import unittest
import tempfile
import os
import xml.etree.ElementTree as ET
from io import StringIO
from xuproc import XUProc
from tests.test_data import XML_VALID, XML_ERORS

class TestXUProc(unittest.TestCase):

    def setUp(self):
        self.xuproc = XUProc(StringIO(XML_VALID))

    def test_xml_with_errors(self):
        self.xuproc = XUProc(StringIO(XML_ERORS))
        stats = self.xuproc.get_test_statistics()
        expected_stats = {
            'Total': 8,
            'skipped': 0,
            'failure': 0,
            'error': 0
        }
        for key, value in expected_stats.items():
            self.assertEqual(stats[key], value)


    def test_badly_formed_xml(self):
            with self.assertRaises(ET.ParseError):
                self.xuproc = XUProc(StringIO("<testsuite><testcase></testsuite>"))

    def test_empty_file(self):
        with self.assertRaises(ValueError):
            self.xuproc = XUProc(StringIO(""))

    def test_empty_well_formed_xml(self):
        self.xuproc = XUProc(StringIO("<testsuite></testsuite>"))  # Use a well-formed empty XML
        result = self.xuproc.concat_attr()
        root = ET.fromstring(result)
        self.assertEqual(len(root.findall('.//testcase')), 0)

    def test_concat_attr(self):
        test_result = self.xuproc.concat_attr()
        test_root = ET.fromstring(test_result)
        for testcase in test_root.iter('testcase'):
            classname = testcase.get('classname')
            name = testcase.get('name')
            if classname and name:
                self.assertIn(classname, name)

    def test_print_test_statistics(self):
        stats = self.xuproc.get_test_statistics()
        expected_stats = {
            'Total': 8,
            'skipped': 1,
            'failure': 1,
            'error': 1
        }
        for key in expected_stats:
            self.assertIn(key, stats)

        for key, value in expected_stats.items():
            self.assertEqual(stats[key], value)
            self.assertIsInstance(stats[key], int)

    def test_save(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xml') as temp_file:
            temp_path= temp_file.name
        try:
            self.xuproc.file = temp_path
            self.xuproc.save(self.xuproc.concat_attr())
            root = ET.parse(temp_path).getroot()
            self.assertEqual(len(root.findall('.//testcase')), 8)  # Adjust the expected number of test cases
        finally:
            os.remove(temp_path)

if __name__ == '__main__':
    unittest.main()
