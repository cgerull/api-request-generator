"""
Config module for api-request-generator.
Read initial configuration from file.
If defined overwrite settings from Environment variables.

Expect config.yml configuration file in app directory.
"""
import yaml
import os
import sys

_config_file = './config.yml'
config = {}

# Overwrite and append default from the configuration file
# in YAML format.
# Do nothing if config file does not exists or load operations fails.
def load_yaml(config, file):
    """
    Overwrite and append default from the configuration file
    in YAML format.
    Exit with error if config file does not exists or load operations fails.
    """
    try:
        config_stream = open(file, 'r')
        ext_config = yaml.safe_load(config_stream)
        # QQQ merge config
        for key in iter(ext_config.keys()):
            config[key] = ext_config[key]
    except:
        print("FATAL! Can't read configuration file {}.".format(_config_file), file=sys.stderr)
        exit(1)
    return config


def load_environment(config):
    """
    Finally overwrite configuration with environment
    If no ENV variable is set, the existing value is retained.
    """
    config["logger_name"] = os.getenv('LOGGER_NAME', config["logger_name"])
    config["log_format"] = os.getenv('LOG_FORMAT', config["log_format"])
    config["logfile"] = os.getenv('LOGFILE', config["logfile"])
    config["server"] = os.getenv('SERVER', config["server"])
    config["port"] = os.getenv('SERVER_PORT', config["port"])
    config["srv_path"] = os.getenv('SRV_PATH', config["srv_path"])
    return config


# Load confguration file if exists.
config = load_yaml(config, _config_file)
config = load_environment(config)


