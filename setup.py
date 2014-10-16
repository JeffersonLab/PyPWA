from distutils.core import setup

setup(
    name='pythonPWA',
    version='0.5.0',
    author='Brandon DeMello',
    author_email='bdemello@jlab.org',
    packages=['pythonPWA','pythonPWA.dataTypes','pythonPWA.fileHandlers','pythonPWA.model','pythonPWA.utilities','pythonPWA.test'],
    #scripts=['bin/pythonPWATest.py'],
    url='https://clas12svn.jlab.org/repos/users/bdemello/pythonPWA',
    #license='',
    description='Python Tools For Partial-Wave Analysis',
    #long_description=open('README.txt').read(),
    install_requires=[
        "numpy >= 1.8.0",
        "matplot >= 1.3.1"],
)