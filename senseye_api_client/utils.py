import os
from pathlib import Path
import uuid

import yaml

from senseye_api_protos.common_pb2 import VideoConfig, Feature

# Default Config Path ~/.config/senseye.yaml
DEFAULT_CONFIG_PATH = (Path.home() / '.config' / 'senseye.yaml').absolute()


def video_config(shape, features=(Feature.UNET_METRICS,), store=False):
    return VideoConfig(
        features=features,
        width=shape[1],
        height=shape[0],
        channels=1 if len(shape) == 2 else shape[2],
        video_id=str(uuid.uuid4()),

        # this will save video to senseye's s3 bucket at eucalyptus-dev
        store=store,
    )


def load_config(config_file=None):
    '''
    Load Config from a file, and incorporate environment variables
    '''
    if not config_file:
        config_file = DEFAULT_CONFIG_PATH

    # Get the path for the config file
    config_file = Path(config_file)

    # Start with default config dict
    config_dict = {
        'api_url': None,
        'api_auth_token': None,
    }

    # If config file exists, merge that in
    if config_file.exists():
        with open(config_file, 'r') as f:
            deep_merge(yaml.load(f), config_dict)

    # Load Config from env variables and merge that in too
    env_config = get_config_from_env_vars(prefix='SENSEYE_')
    deep_merge(env_config, config_dict)

    # Return merged Config
    return config_dict


# TODO this is from common
def get_config_from_env_vars(env=os.environ, prefix='EUC_'):
    '''
    Inject environment variables into a destination dictionary
    '''
    ret = {}
    for key, value in env.items():
        if not key.startswith(prefix):
            continue

        # break path down i.e.
        # EUC_MY_KEY1__MY_KEY2' => ['my_key1', 'my_key2']
        path = key\
            .replace(prefix, '')\
            .lower()\
            .split('__')

        # Set the nested key
        set_nested(ret, path, value)

    return ret


# TODO this is from common
def deep_merge(source, destination):
    """
    run me with nosetests --with-doctest file.py

    >>> a = { 'first' : { 'all_rows' : { 'pass' : 'dog', 'number' : '1' } } }
    >>> b = { 'first' : { 'all_rows' : { 'fail' : 'cat', 'number' : '5' } } }
    >>> merge(b, a) == { 'first' : { 'all_rows' : { 'pass' : 'dog', 'fail' : 'cat', 'number' : '5' } } }
    True
    """
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            deep_merge(value, node)
        else:
            destination[key] = value

    return destination


# TODO this is from common
def set_nested(input_dict, nested_key, value):
    '''
    Set a nested key, i.e.
    nested_get({'a': {'b': 1}}, ['a', 'b'], 2) => {'a': {'b': 2}}
    '''
    current_dict = input_dict
    for k in nested_key[:-1]:
        if k not in current_dict or current_dict[k] is None:
            current_dict[k] = {}
        elif type(current_dict[k]) is not dict:
            raise Exception(f'{k} is not a dict')

        current_dict = current_dict[k]

    current_dict[nested_key[-1]] = value
