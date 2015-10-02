import  argparse, PyPWA.data.YamlConfig, os

def the_generalfitting_args():
    arguments = argparse.ArgumentParser(description="PyPWA Threaded GeneralFitting")

    arguments.add_argument("-c", "--Config", help="Use to point to the direction of the configuration")
    arguments.add_argument("-wc", "--writeConfig", action="store_true", help="Writes Example.yml and Example.py")

    try:
        args = arguments.parse_args()
    except:
        arguments.print_help()
        raise
        exit(1)

    configuration = PyPWA.data.YamlConfig.YamlConfig()

    if args.writeConfig:
        configuration.dump_default(os.getcwd())
        exit(0)

    if args.Config == None:
        arguments.print_help()
        exit(0)


    configuration.parse_all(os.getcwd() +"/"+args.Config)

    return configuration.the_config

def Lets_Get_Fit():
    import PyPWA.core.GeneralFitting
    values = the_generalfitting_args()
    values["calc"]["cwd"] = os.getcwd()
    PyPWA.core.GeneralFitting.GeneralFitting(values)

if __name__ == '__main__':
    Lets_Get_Fit()