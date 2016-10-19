from PyPWA.libs.data.builtin import sv, kv, gamp


def DataPlugin_CheckPlugin(the_object):
    the_object.plugin_name()
    the_object.plugin_supported_extensions()
    the_object.plugin_memory_parser()
    the_object.plugin_reader()
    the_object.plugin_writer()


def test_EVILDataPlugin_AllPass():
    options = kv.EVILDataPlugin()
    DataPlugin_CheckPlugin(options)


def test_GampDataPlugin_AllPass():
    options = gamp.GampDataPlugin()
    DataPlugin_CheckPlugin(options)


def test_SvDataPlugin_AllPass():
    options = sv.SvDataPlugin()
    DataPlugin_CheckPlugin(options)
