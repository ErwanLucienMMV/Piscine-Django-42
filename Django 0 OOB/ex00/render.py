#!/usr/bin/env python3

import os
import sys


def render(filename):
    if os.path.splitext(filename)[1] != '.template':
        raise ValueError('The input file must have a .template extension.')
    import settings

    with open(filename, encoding='utf-8') as source:
        result = source.read().format(**vars(settings))
    output = os.path.splitext(filename)[0] + '.html'
    with open(output, 'w', encoding='utf-8') as destination:
        destination.write(result)


def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError('Usage: python3 render.py <file.template>')
        render(sys.argv[1])
    except Exception as error:
        print('Error: {}'.format(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
