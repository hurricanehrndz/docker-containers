import yaml
import os
import subprocess

class ConfigReader(object):
    def __init__(self, config_file_path):
        self._config = self._read(config_file_path)

    def _read(self, config_file_path):
        if os.path.lexists(config_file_path) and os.access(config_file_path, os.X_OK):
            try:
                sub = subprocess.Popen([config_file_path], stdout=subprocess.PIPE)
                fin = sub.communicate()[0] #sub.stdout
                data = yaml.safe_load(fin)
                return data
            except Exception as e:
                msg = str(e)
                raise ReadingError('Could not read config file:\n%s' % msg)
        elif os.path.lexists(config_file_path):
            try:
                with open(config_file_path) as fin:
                    data = yaml.safe_load(fin)
                return data
            except Exception as e:
                msg = str(e)
                raise ReadingError('Could not read config file:\n%s' % msg)
        return None

    def get_config(self):
        return self._config

class ReadingError(Exception):
    pass
