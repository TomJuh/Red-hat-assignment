"""
Modules used for XML processing
Argument parsing
Os operations
And file handling
"""
import xml.etree.ElementTree as ET
import argparse
import os
from io import StringIO


class XUProc:
    """
    Main class for JUnit XML processing

    Attributes:
    file: str - xml file path
    tree: ElementTree - xml tree object
    root: Element - root of the xml tree

    Methods:
    file_checks(file)   - checks if file is valid
    try_load_file(file) - loads the xml file with error handling
    concat_attr() - concatenates classname to name attr
    get_test_statistics() - returns test statistics (counts)
    print_status_counts(status_counts) - prints the test statistics
    save(output) - saves changes to the file
    """

    def __init__(self, file):
        """
        Constructor of XUProc class
        Parameters:
        file: str - xml file path

        Returns:
        None
        """
        self.file = file
        self.tree = None
        self.root = None
        self.try_load_file(file)

    def file_checks(self, file):
        """
        Checks if file is valid, mainly user input validation
        Parameters:
        file: str - xml file path

        Raises:
        ValueError: if file is empty, doesn't exist or is of wrong type

        Returns:
        None
        """
        if isinstance(file, StringIO):
            file.seek(0)
            content = file.read()
            if len(content) == 0:
                raise ValueError("File cannot be empty")
            if not content.strip().startswith("<"):
                raise ValueError("Wrong File type - only xml is supported")
            file.seek(0)
        else:
            if not os.path.exists(file):
                raise ValueError("File Path doesn't exist")
            if os.path.getsize(self.file) == 0:
                raise ValueError("File cannot be empty")
            if not str(file).endswith("xml"):
                raise ValueError("Wrong File type - only xml is supported")

    def try_load_file(self, file):
        """
        Loads the xml file with error handling
        Parameters:
        file: str - xml file path

        Raises:
        ET.ParseError: if xml file is invalid
        PermissionError: if script lacks permission for xml file
        RuntimeError: if any other error

        Returns:
        None
        """
        try:
            self.file_checks(file)
            self.tree = ET.parse(self.file)
            self.root = self.tree.getroot()
        except ET.ParseError as exml:
            raise ET.ParseError("Invalid XML File") from exml
        except PermissionError as pe:
            raise PermissionError("Lacks permission for XML file") from pe
        except ValueError as vale:
            raise ValueError from vale
        except Exception as e:
            raise RuntimeError(f"Error encountered {e}") from e

    def concat_attr(self):
        """
        Concatenates classname to name attr
        Returns:
        str - xml content
        """
        for testcase in self.root.iter('testcase'):  # iter through testtcases
            classname = testcase.get('classname')
            name = testcase.get('name')
            if classname and name:  # if both classname and name exist
                testcase.set('name', f"{name}.{classname}")  # concat them
        return ET.tostring(self.root, encoding='unicode')

    def get_test_statistics(self):
        """
        Gets test statistics (counts)
        Returns:
        dict - status_counts
        """
        status_counts = {'Total': 0, 'skipped': 0, 'error': 0, 'failure': 0}
        for testcase in self.root.iter('testcase'):  # iter through testtcases
            status_counts['Total'] += 1  # count total
            for elem in testcase:
                if elem.tag in status_counts:
                    status_counts[elem.tag] += 1  # count individual statuses
        return status_counts

    def print_status_counts(self, status_counts):
        """
        Prints the test statistics
        Parameters:
        status_counts: dict - status_counts
        Returns:
        None
        """
        for status, count in status_counts.items():  # print each category
            print(f"{status.capitalize()}: {count}")

    def save(self, output):
        """
        Saves changes to the file
        Parameters:
        output: str - xml content
        Returns:
        None
        """
        try:  # file handling safety
            if isinstance(self.file, StringIO):  # StringIO is used for testing
                self.file.write(output)
            else:
                with open(self.file, 'w', encoding='utf-8') as self.file:
                    self.file.write(output)
        except IOError as ioe:
            raise IOError("I/O operation failed") from ioe
        except Exception as e:
            raise RuntimeError(f"Error encountered {e}") from e


def get_parser():
    """
    Argument parser for the script
    Returns:
    parser - ArgumentParser object
    """
    parser = argparse.ArgumentParser(  # Set up arguments
        description="Script for statistic and test attribute manipulation")
    parser.add_argument('-j', action='store_true',
                        help="Concat classname of a testcase to the name attr")
    parser.add_argument('file', type=str, nargs='?',
                        help="The XML file to process")
    return parser


def main():
    """
    Main function for the script, argument checks and execution
    Returns:
    None
    """
    parser = get_parser()
    args = parser.parse_args()
    if args.file:  # run only if file is provided
        xuproc = XUProc(args.file)
        if args.j:  # concat with -j flag
            xuproc.save(xuproc.concat_attr())
        else:  # print statistics
            xuproc.print_status_counts(xuproc.get_test_statistics())
    else:  # else print help
        parser.print_help()


if __name__ == "__main__":
    main()
