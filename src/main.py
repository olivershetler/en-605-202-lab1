import yaml
import os
from pathlib import Path

from converters import *

def get_config():
    with open(os.getcwd() + '/src/config.yaml') as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def get_data_paths():
    config = get_config()
    cwd = Path(os.getcwd())
    base_dir = cwd / Path(config['base_dir'])
    infix_path = base_dir / config['infix_file']
    prefix_path = base_dir / config['prefix_file']
    postfix_path = base_dir / config['postfix_file']
    return {
        'infix': infix_path,
        'prefix': prefix_path,
        'postfix': postfix_path
    }

def main():
    paths = get_data_paths()
    # read .txt files for each expression type
    # separate by line, removing empty lines
    with open(paths['infix'], 'r') as f:
        infix_expressions = f.read().split('\n')
        infix_expressions = list(filter(None, infix_expressions))
    with open(paths['prefix'], 'r') as f:
        prefix_expressions = f.read().split('\n')
        prefix_expressions = list(filter(None, prefix_expressions))
    with open(paths['postfix'], 'r') as f:
        postfix_expressions = f.read().split('\n')
        postfix_expressions = list(filter(None, postfix_expressions))


    convert = lambda f, l: dict(zip(l, list(map(f, l))))
    format = lambda d: '\n'.join([f'{k} -> {v}' for k, v in d.items()])

    # convert infix to prefix and postfix
    infix_from_prefix = format(convert(prefix_to_infix, prefix_expressions))
    infix_from_postfix = format(convert(postfix_to_infix, postfix_expressions))

    # convert postfix to infix and prefix
    postfix_from_infix = format(convert(infix_to_postfix, infix_expressions))
    postfix_from_prefix = format(convert(prefix_to_postfix, prefix_expressions))

    # convert prefix to infix and postfix
    prefix_from_infix = format(convert(infix_to_prefix, infix_expressions))
    prefix_from_postfix = format(convert(postfix_to_prefix, postfix_expressions))

    # Format a string to print the results
    result = f"""Infix from Prefix:
{infix_from_prefix}

Infix from Postfix:
{infix_from_postfix}

Postfix from Infix:
{postfix_from_infix}

Postfix from Prefix:
{postfix_from_prefix}

Prefix from Infix:
{prefix_from_infix}

Prefix from Postfix:
{prefix_from_postfix}
"""
    print(result)

if __name__ == '__main__':
    main()