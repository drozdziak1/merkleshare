#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The MerkleShare entrypoint.
"""
import argparse
import ipfsapi
import sys

IPFS_LOCAL_GATEWAY_HOST = '127.0.0.1'
IPFS_PORT = 5001
IPFS_LOCAL_GATEWAY_PORT = 8080


def get_args(args=sys.argv):
    """
    Extract command-line arguments.

    :param args: A list of command-line arguments
    :type args: list
    :returns: A command-line argument namespace
    :rtype: Namespace
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

    return p.parse_args(args[1:])


def connect(host=IPFS_LOCAL_GATEWAY_HOST, port=IPFS_PORT, verbose=False):
    """
    Connect to an IPFS instance

    :param host: The host of the gateway you want to reach
    :type host: str
    :param port: The port of the gateway you want
    :type port: int

    :returns: An ipfsapi client instance
    :rtype: ipfsapi.Client
    """
    try:
        if verbose:
            sys.stderr.write('Connecting... \n')
            sys.stderr.flush()

        api = ipfsapi.connect(host, port)

    except Exception as e:
        sys.stderr.write('Could not connect! Are you sure that the ' +
                         'ipfs daemon is running?\n')
        sys.exit(1)

    if verbose:
        sys.stderr.write('connected to the API.\n')

    return api


def main():
    args = get_args()
    api = connect(verbose=args.verbose)

    # Read stdin...
    if args.input_file is None:
        if args.verbose:
            sys.stderr.write(
                'Waiting for standard input... ' +
                '(type your doc and press Ctrl+D)\n'
            )
            sys.stderr.flush()
        addr = api.add_str(sys.stdin.read())
    # ...or the specified file
    else:
        addr = api.add(args.input_file)['Hash']

    if args.verbose:
        sys.stderr.write('\nDone handling input.')

    print()

    if args.all:
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
    if args.link_type == 'hash':
        print(addr)
    elif args.link_type == 'regular':
        print('/ipfs/%s' % addr)
    elif args.link_type == 'gateway':
        print('https://ipfs.io/ipfs/%s' % addr)
    else:
        print('http://%s:%d/ipfs/%s' %
              (IPFS_LOCAL_GATEWAY_HOST, IPFS_LOCAL_GATEWAY_PORT, addr))


if __name__ == "__main__":
    main()
