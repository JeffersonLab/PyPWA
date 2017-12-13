from PyPWA.initializers.configurator import options


class SimpleOptions(options.Component):

    name = "SimpleOptions"
    module_comment = "A Simple test plugin"

    def get_default_options(self):
        return {
            "Option1": "item 1",
            "Option2": 3,
            "Option3": "A string value"
        }

    def get_option_difficulties(self):
        return {
            "Option1": options.Levels.REQUIRED,
            "Option2": options.Levels.OPTIONAL,
            "Option3": options.Levels.ADVANCED
        }

    def get_option_types(self):
        return {
            "Option1": ["item1", "item2", "item3"],
            "Option2": int,
            "Option3": str
        }

    def get_option_comments(self):
        return {
            "Option1": "A specific item, predefined",
            "Option2": "Any integer",
            "Option3": "Anything as a string"
        }


