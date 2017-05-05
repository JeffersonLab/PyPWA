from PyPWA.core.configurator import options


class SimpleOptions(options.Plugin):
    plugin_name = "SimpleOptions"
    default_options = {
        "Option1": "item 1",
        "Option2": 3,
        "Option3": "A string value"
    }

    option_difficulties = {
        "Option1": options.Levels.REQUIRED,
        "Option2": options.Levels.OPTIONAL,
        "Option3": options.Levels.ADVANCED
    }

    option_types = {
        "Option1": ["item1", "item2", "item3"],
        "Option2": int,
        "Option3": str
    }

    module_comment = "A Simple test plugin"
    option_comments = {
        "Option1": "A specific item, predefined",
        "Option2": "Any integer",
        "Option3": "Anything as a string"
    }

    defined_function = None

    setup = options.Setup
    provides = options.Types.SKIP

