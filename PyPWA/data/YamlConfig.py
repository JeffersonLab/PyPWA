import yaml, os

class YamlConfig(object):


    default1 = {
        "calc" : {
            "Generated Length" : 10000,
            "Function Location" : "Example.py",
            "Function Name" : "the_function"
            },

        "data" : {
            "Kinematic Variable File" : "kvVars.txt", #Will this make it?
            "Accepted Kinematic Variable File": "kvArgs.txt",
            "QFactor List Location" : "Qfactor.txt", 
            "Use Cache": True
            }
    }
    default2 = {
        "general": {
            "Initial Minuit Settings" : {'A1': 1,'A2':2,'A3':0.1,'A4':-10,'A5':-0.00001 },
            "Minuit Parameters" : ["A1","A2","A3","A4", "A5"],
            "Minuit Strategy" : 1,
            "Number of Threads" : 1,
            "Use QFactor" : True,
            "Minuit Set Up": 0.5,
            "Minuit ncall" : 1000
            }
        }

    python_example = "import numpy\n\ndef the_function(the_array, the_params):\n    final = value*(A1**A2)*(A3**A4)*A5\n    return numpy.cos(final)\n"

    parsed_config = {}

    the_config = {}

    def __init__(self):
        self.defaults = self.default1.copy()
        self.defaults.update(self.default2)

        self.the_config = self.defaults

    def parse_all(self, file_location):
        self.load(file_location)
        self.generate_config()

    def load(self, the_file):
        if not os.path.isfile(the_file):
            raise IOError("{0} does not exist!".format(file_location,))

        with open(the_file) as stream:
            self.parsed_config = yaml.load(stream)

    def generate_config(self):
        self.the_config = self.defaults.copy()
        self.the_config.update(self.parsed_config)

    def dump_default(self, cwd):
        with open (cwd + "/Example.yml", "w") as stream:
            stream.write( yaml.dump(self.default1, default_flow_style=False) )
            stream.write( yaml.dump(self.default2) )
        with open (cwd + "/Example.py", "w") as stream:
            stream.write( self.python_example)
