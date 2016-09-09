from PyPWA import libs
from PyPWA.core_libs import templates, plugin_loader
from PyPWA.libs import data, process, multinest_minimization, minuit


def test_PluginLoading_ImportsPlugins_FindsAllLibs():
    """
    Ensures that the PluginLoader finds all the plugins when supplied
    with a module and nothing more.
    """
    loader = plugin_loader.PluginLoading(templates.OptionsTemplate)
    plugins = loader.fetch_plugin([libs])

    assert data.DataIterator in plugins
    assert data.DataParser in plugins
    assert process.Processing in plugins
    assert minuit.MinuitOptions in plugins
    assert multinest_minimization.MultiNestOptions in plugins

    assert len(plugins) == 5