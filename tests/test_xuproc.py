"""
Modules for unittests
Temp files for test of save method
Os operations
XML module for parsing XML
StringIO for creating input
XUProc class for testing
Testing data from test.data
"""
import unittest
import tempfile
import os
import xml.etree.ElementTree as ET
from io import StringIO
from xuproc import XUProc
from tests.test_data import XML_VALID, XML_ERORS


class TestXUProc(unittest.TestCase):
    """Test class for XUProc class
    Test methods:
    test_xml_with_errors
    test_badly_formed_xml
    test_empty_file
    test_empty_well_formed_xml
    test_concat_attr
    test_print_test_statistics
    test_save
    """

    def setUp(self):
        """
        Set up the test environment
        Create an instance of XUProc class with a valid XML

        :return: None
        """
        self.xuproc = XUProc(StringIO(XML_VALID))

    def test_xml_with_errors(self):
        """
        Test the XML with errors
        Test the get_test_statistics method with XML with errors

        :return: None
        """
        self.xuproc = XUProc(StringIO(XML_ERORS))
        stats = self.xuproc.get_test_statistics()  # Get the statistics
        expected_stats = {  # Expected statistics
            'Total': 8,
            'skipped': 0,
            'failure': 0,
            'error': 0
        }
        for key, value in expected_stats.items():  # compare them
            self.assertEqual(stats[key], value)

    def test_badly_formed_xml(self):
        """
        Test for badly formed XML
        Input in the XUProc class a badly formed XML

        :return: None
        """
        with self.assertRaises(ET.ParseError):  # should raise an exception
            self.xuproc = XUProc(StringIO("<testsuite><testcase></testsuite>"))

    def test_empty_file(self):
        """
        Test for an empty file
        Input in the XUProc class an empty file

        :return: None
        """
        with self.assertRaises(ValueError):  # should raise an exception
            self.xuproc = XUProc(StringIO(""))

    def test_empty_well_formed_xml(self):
        """
        Test for an empty well formed XML
        Input in the XUProc class an empty well formed XML

        :return: None
        """
        self.xuproc = XUProc(StringIO("<testsuite></testsuite>"))
        result = self.xuproc.concat_attr()
        root = ET.fromstring(result)
        self.assertEqual(len(root.findall('.//testcase')), 0)  # should pass

    def test_concat_attr(self):
        """
        Test the concat_attr method
        Test if the method returns the correct XML

        :return: None
        """
        test_result = self.xuproc.concat_attr()
        test_root = ET.fromstring(test_result)
        for testcase in test_root.iter('testcase'):
            classname = testcase.get('classname')
            name = testcase.get('name')
            if classname and name:  # Check if the attributes are in the XML
                self.assertIn(classname, name)

    def test_print_test_statistics(self):
        """
        Test the print_test_statistics method
        Test if the method returns the correct statistics

        :return: None
        """
        stats = self.xuproc.get_test_statistics()
        expected_stats = {
            'Total': 8,
            'skipped': 1,
            'failure': 1,
            'error': 1
        }
        for key in expected_stats:  # Check if the keys are in the stats
            self.assertIn(key, stats)

        for key, value in expected_stats.items():  # Check values are correct
            self.assertEqual(stats[key], value)
            self.assertIsInstance(stats[key], int)

    def test_save(self):
        """
        Test the save method
        Test if the method saves the XML correctly

        :return: None
        """
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xml') as temp_file:
            temp_path = temp_file.name
        try:
            self.xuproc.file = temp_path
            self.xuproc.save(self.xuproc.concat_attr())
            root = ET.parse(temp_path).getroot()
            # Check that the saved file is correct
            self.assertEqual(len(root.findall('.//testcase')), 8)
        finally:
            # Remove the temporary file
            os.remove(temp_path)


if __name__ == '__main__':
    unittest.main()
