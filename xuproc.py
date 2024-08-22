import xml.etree.ElementTree as ET
import argparse
import os
from io import StringIO

class XUProc:
    def __init__(self, file):
        self.file = file
        self.tree = None
        self.root = None
        self.try_load_file(file)


    def file_checks(self, file):
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
            elif os.path.getsize(self.file) == 0:
                raise ValueError("File cannot be empty")
            elif not str(file).endswith("xml"):
                raise ValueError("Wrong File type - only xml is supported")


    def try_load_file (self, file):
        try:
            self.file_checks(file)
            self.tree = ET.parse(self.file)
            self.root = self.tree.getroot()
        except ET.ParseError:
            raise ET.ParseError("Invalid XML File")
        except PermissionError:
            raise PermissionError("Script lacks permission for XML file")
        except ValueError as vale:
            raise vale
        except Exception as e:
            raise RuntimeError(f"Error encountered {e}")

    def concat_attr(self):
        for testcase in self.root.iter('testcase'):
            classname = testcase.get('classname')
            name = testcase.get('name')
            if classname and name:
                testcase.set('name', f"{name}.{classname}")
        return ET.tostring(self.root, encoding='unicode')

    def get_test_statistics(self):
        status_counts = {'Total' : 0, 'skipped': 0, 'error': 0, 'failure': 0}
        for testcase in self.root.iter('testcase'):
            status_counts['Total'] += 1
            for elem in testcase:
                if elem.tag in status_counts:
                    status_counts[elem.tag] += 1
        return status_counts


    def print_status_counts(self, status_counts):
        for status, count in status_counts.items():
            print(f"{status.capitalize()}: {count}")

    def save(self, output):
        try:
            if isinstance(self.file, StringIO):
                self.file.write(output)
            else:
                with open(self.file, 'w', encoding='utf-8') as self.file:
                    self.file.write(output)
        except IOError:
            raise IOError("I/O operation failed")
        except Exception as e:
            raise RuntimeError(f"Error encountered {e}")


def get_parser():
    parser = argparse.ArgumentParser(description="Simple script for test statistic and test name attribute manipulation")
    parser.add_argument('-j', action='store_true', help="Concat classname of a testcase to the name attribute")
    parser.add_argument('file', type=str, nargs='?', help="The XML file to process")
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.file:
        xuproc = XUProc(args.file)
        if args.j:
            xuproc.save(xuproc.concat_attr())
        else:
            xuproc.print_status_counts(xuproc.get_test_statistics())
    else:
        parser.print_help()
if __name__ == "__main__":
    main()