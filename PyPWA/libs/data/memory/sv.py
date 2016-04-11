import csv
import io

import numpy

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class SvParser(object):
    """
    Object for reading and writing delimiter separated data files.
    """

    def reader(self, file_location):
        """Reads a delimiter separated file containing data from disk.

        Args:
            file_location (str): The file that contain the data to be read.
        Returns:
            dict: Dictionary of arrays containing the data.
        """
        with io.open(file_location, "rt") as stream:
            for line_count, throw in enumerate(stream):
                pass

        with io.open(file_location, "rt") as stream:
            dialect = csv.Sniffer().sniff(stream.read(1024))
            stream.seek(0)

            sv = csv.reader(stream, dialect)

            elements = next(sv)
            parsed = {}
            for element in elements:
                parsed[element] = numpy.zeros(shape=line_count, dtype="float64")

            for index, row in enumerate(sv):
                for count in range(len(row)):
                    parsed[elements[count]][index] = row[count]

        return parsed

    def writer(self, file_location, data):
        """Writes the data from memory to file.

        Args:
            file_location  (str): Where to write the data to.
            data (dict): Dictionary of the arrays containing the data.
        """
        extension = file_location.split(".")[-1]

        if extension == ".tsv":
            dialect = csv.excel_tab
        else:
            dialect = csv.excel

        with io.open(file_location, "wt") as stream:
            field_names = list(data.keys())

            writer = csv.DictWriter(stream, fieldnames=field_names, dialect=dialect)
            writer.writeheader()

            for index in range(len(data[field_names[0]])):
                temp = {}
                for field in field_names:
                    temp[field] = data[field][index]
                writer.writerow(temp)
