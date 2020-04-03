import logging
import os
from pathlib import Path

import jwt
import yaml


log = logging.getLogger(__name__)

# Default Config Path ~/.config/senseye.yaml
DEFAULT_CONFIG_PATH = (Path.home() / '.config' / 'senseye.yml').absolute()


def load_config(config_file=None):
    '''
    Load Config from a file, and incorporate environment variables
    '''
    # Load config from specified filepath
    if config_file:
        with open(config_file, 'r') as f:
            config_file = yaml.safe_load(f)
    # If unsuccessful, load from default filepath
    if not config_file:
        try:
            with open(DEFAULT_CONFIG_PATH, 'r') as f:
                config_file = yaml.safe_load(f)
        except:
            log.error(f'''
                Defaulting to config path {DEFAULT_CONFIG_PATH} failed!
                Cannot import configuration settings''')

    config_dict = config_file or {}

    # Load config from env variables and merge that in with file configs
    env_config = get_config_from_env_vars()
    deep_merge(env_config, config_dict)

    # Generate JWT token and add to request metadata
    try:
        token = jwt.encode(
            {'iss': config_dict['jwt']['key']},
            config_dict['jwt']['secret'],
            algorithm='HS256').decode("utf-8")
        config_dict['request_metadata'] = [('authorization', f'Bearer {token}')]
    except:
        log.warning('''
            JWT token could not be generated.
            Ensure configuration fields `jwt.key` and `jwt.secret` are set.
            You can obtain a key + secret pair from http://dev.senseye.co.''')

    # Return merged config
    return config_dict


def get_config_from_env_vars(env=os.environ, prefix='SENSEYE_'):
    '''
    Parse environment variables into a nested dictionary.
    '''
    ret = {}

    for key, value in env.items():
        if not key.startswith(prefix):
            continue

        # break path down
        # e.g. SENSEYE_MY_KEY1__MY_KEY2' => ['my_key1', 'my_key2']
        path = key\
            .replace(prefix, '')\
            .lower()\
            .split('__')

        set_nested(ret, path, value)

    return ret


def deep_merge(source, destination):
    '''
    Recursively merges two dictionaries together. Values in `source` will
    overwrite those in `destination`.
    '''
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            deep_merge(value, node)
        else:
            destination[key] = value

    return destination


def set_nested(input_dict, nested_key, value):
    '''
    Set a nested key
    e.g. nested_get({'a': {'b': 1}}, ['a', 'b'], 2) => {'a': {'b': 2}}
    '''
    current_dict = input_dict
    for k in nested_key[:-1]:
        if k not in current_dict or current_dict[k] is None:
            current_dict[k] = {}
        elif type(current_dict[k]) is not dict:
            raise Exception(f'{k} is not a dict')

        current_dict = current_dict[k]

    current_dict[nested_key[-1]] = value
