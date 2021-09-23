configuration = '''
---
version: 1
formatters:
    default:
        # colorlog is really useful
        (): colorlog.ColoredFormatter
        format: "%(asctime)s [%(bold)s%(log_color)s%(levelname)s%(reset)s]: (%(bold)s%(name)s:%(lineno)d%(reset)s) %(message)s"
        style: "%"
        datefmt: "%X"
        log_colors:
            DEBUG:    cyan
            INFO:     green
            WARNING:  yellow
            ERROR:    red
            CRITICAL: red,bg_white
handlers:
    stderr:
        class: colorlog.StreamHandler
        formatter: default
loggers:
    tavern:
        handlers:
            - stderr
        level: INFO
'''

from logging import config
import pytest
import yaml

config.dictConfig(yaml.load(configuration, Loader=yaml.FullLoader))
import os

@pytest.fixture
def supported_profiles_from_env():
    PREFIX = {
      'alt':  'http://www.w3.org/ns/dx/conneg/altr',
      'sdo':  'https://schema.org',
      'dcat': 'https://www.w3.org/TR/vocab-dcat/',
    }

    supported_profiles = os.environ['SUPPORTED_PROFILES'].split(',')
    structured_profiles = []

    for profile, mime_type in map(lambda x: x.split(':', 1), supported_profiles):
      structured_profiles.append(
        {
          'profile': PREFIX.get(profile, profile),
          'mime'   : mime_type
        }
      )

    return structured_profiles
