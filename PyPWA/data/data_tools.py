import os, numpy

class DataTypeSearch(object):
    def search(self, file_location):
        
        result = self._extension_test(file_location)
        if result:
            return result

        result = self._character_test(file_location)
        if result:
            return result

        result = self._line_test(file_location)
        if result:
            return result

        raise TypeError("File Type not known!")


    def _extension_test(self,file_location):
        file_extenstion = os.path.splitext(file_location)[1].lower()

        if file_extenstion == ".txt":
            return 0
        elif file_extenstion == ".csv":
            return "KvCsv"
        elif file_extenstion == ".tsv":
            return "KvTsv"
        elif file_extenstion == ".yml":
            return "Yaml"
        else:
            return 0


    def _character_test(self, file_location):
        characters = []

        with open(file_location, "r") as stream:
            for x in range(25):
                characters.append(stream.read(1))

        try:
            for character in characters:
                if not int(character) < 2:
                    return 0
                else:
                    pass
            return "NewWeights"
        except:
            return 0

    def _line_test(self, file_location):
        with open(file_location, "r") as stream:
            first_line = stream.readline().strip("\n")

        if "=" in first_line:
            return "Kv"
        elif len(first_line) > 1:
            return "Qf"
        elif len(first_line) == 1:
            return "OldWeights"
        else:
            return 0

class DataTypeWrite(object):
    def search(data, new = False):
        if type(data) == dict:
            data_type = "Kv"
        elif type(data) == numpy.ndarray:
            if data.dtype == bool:
                data_type = "OldWeights"
            else:
                data_type = "Qfactor"

        if new:
            if data_type == "Kv":
                data_type == "KvTsv"
            elif data_type == "OldWeights":
                data_type == "NewWeights"
        return data_type


