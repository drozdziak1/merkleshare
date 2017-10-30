#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import ipfsapi
import sys
import time

IPFS_LOCAL_GATEWAY_HOST = 'localhost'
IPFS_PORT = 5001
IPFS_LOCAL_GATEWAY_PORT = 8080


def get_args():
    """
    Extract command-line arguments.
    """
    p = argparse.ArgumentParser()
    p.add_argument('input_file', nargs='?', default=None,
                   type=str, help='input file')
    p.add_argument('-a', default=False, dest='all', action='store_true',
                   help='print all link types to stderr')
    p.add_argument('-v', default=False, dest='verbose', action='store_true',
                   help='be verbose')
    p.add_argument(
        '-t', default='regular', dest='link_type',
        help='link type to print to stdout',
        choices=['hash', 'regular', 'gateway', 'local']
    )

    return p.parse_args()


ARGS = get_args()


def connect(host=IPFS_LOCAL_GATEWAY_HOST, port=IPFS_PORT):
    """
    Keep trying to connect to an IPFS instance
    """
    retries = 1
    while True:
        try:
            if ARGS.verbose:
                sys.stderr.write('Connecting... \n')
                sys.stderr.flush()

            api = ipfsapi.connect(host, port)
            if retries > 1:
                sys.stderr.write('Connected after %d retries\n' % retries)
            break

        except Exception as e:
            sys.stderr.write('Could not connect! Are you sure that the ipfs\n')
            sys.stderr.write(
                'daemon is running?' +
                ' Retrying in %d seconds...\n' % 2 ** retries)

            time.sleep(2 ** retries)
            retries += 1

    if ARGS.verbose:
        sys.stderr.write('connected to the API.\n')

    return api


def main():
    api = connect()

    # Read stdin...
    if ARGS.input_file is None:
        if ARGS.verbose:
            sys.stderr.write(
                'Waiting for standard input... ' +
                '(type your doc and press Ctrl+D)\n'
            )
            sys.stderr.flush()
        addr = api.add_str(sys.stdin.read())
    # ...or the specified file
    else:
        addr = api.add(ARGS.input_file)['Hash']

    if ARGS.verbose:
        sys.stderr.write('\nDone handling input.')

    print()

    if ARGS.all:
        sys.stderr.write('Your document is available at:\n')
        sys.stderr.write('Hash: %s\n' % addr)
        sys.stderr.write('Regular: /ipfs/%s\n' % addr)
        sys.stderr.write('Gateway: https://ipfs.io/ipfs/%s\n' % addr)
        sys.stderr.write('Local (on your node): http://%s:%d/ipfs/%s\n' %
                         (
                             IPFS_LOCAL_GATEWAY_HOST,
                             IPFS_LOCAL_GATEWAY_PORT,
                             addr
                         ))
        sys.stderr.write('Your choice: ')

    sys.stderr.flush()

    # Decide which link to print to stdout
    if ARGS.link_type == 'hash':
        print(addr)
    elif ARGS.link_type == 'regular':
        print('/ipfs/%s' % addr)
    elif ARGS.link_type == 'gateway':
        print('https://ipfs.io/ipfs/%s' % addr)
    else:
        print('http://%s:%d/ipfs/%s' %
              (IPFS_LOCAL_GATEWAY_HOST, IPFS_LOCAL_GATEWAY_PORT, addr))


if __name__ == "__main__":
    main()
