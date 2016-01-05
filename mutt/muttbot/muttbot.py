#!/usr/bin/env python
import sys, os
from config import ConfigReader, ReadingError
from accounts import AccountsSetuper, SetupError
from messenger import Messenger
from argparse import ArgumentParser

def add_options(parser):
    parser.add_argument('-c', '--config-file', nargs=1, dest='config_file',
        help='run commands given in CONFIGFILE', metavar='CONFIGFILE',
        required=True)

def read_config(config_file):
    reader = ConfigReader(config_file)
    return reader.get_config()

def main():
    log = Messenger()
    try:
        parser = ArgumentParser()
        add_options(parser)
        options = parser.parse_args()
        email_accounts = read_config(options.config_file[0])
        if not isinstance(email_accounts, list):
            raise ReadingError('Configuration file must be a list of tasks')
        setuper = AccountsSetuper()
        success = setuper.setup(email_accounts)
        if success:
            log.info('\n==> All tasks executed successfully')
        else:
            raise SetupError('\n==> Some tasks were not executed successfully')
    except (ReadingError, SetupError) as e:
        log.error('%s' % e)
        exit(1)
    except KeyboardInterrupt:
        log.error('\n==> Operation aborted')
        exit(1)

if __name__ == '__main__':
    main()
