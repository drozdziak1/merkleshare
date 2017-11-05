#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The MerkleShare entrypoint.
"""
import argparse
import errno
import ipfsapi
import re
import sys

from base58 import b58encode, b58decode
from cryptography.fernet import Fernet

IPFS_LOCAL_GATEWAY_HOST = '127.0.0.1'
IPFS_PORT = 5001
IPFS_LOCAL_GATEWAY_PORT = 8080


def get_args(args=sys.argv):
    """
    Extract command-line arguments.

    :param list args: A list of command-line arguments
    :returns: A command-line argument namespace
    :rtype: Namespace
    """
    p = argparse.ArgumentParser()
    p.add_argument('-a', default=False, dest='all', action='store_true',
                   help='print all link types to stderr')
    p.add_argument('-d', default=None, dest='download_link',
                   metavar='LINK/#KEY',
                   help='download content under LINK (optionally encrypted ' +
                   'using KEY); Note: links of format \'LINK/#webui:KEY\' ' +
                   'are meant to be visited from a browser.',
                   nargs=1)
    p.add_argument('-e', default=False, dest='encrypt', action='store_true',
                   help='encrypt ')
    p.add_argument('-v', default=False, dest='verbose', action='store_true',
                   help='be verbose')
    p.add_argument(
        '-t', default='regular', dest='link_type',
        help='link type to print to stdout',
        choices=['hash', 'regular', 'gateway', 'local']
    )

    # Positional arguments
    p.add_argument('input_file', nargs='?', default=sys.stdin,
                   type=str, help='input file')

    return p.parse_args(args[1:])


def connect(host=IPFS_LOCAL_GATEWAY_HOST, port=IPFS_PORT, verbose=False):
    """
    Connect to an IPFS instance

    :param str host: The host of the gateway you want to reach
    :param int port: The port of the gateway you want

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
        sys.stderr.write('Connected to the API.\n')

    return api


def upload(api, input_file=sys.stdin, verbose=False,
           encrypt=False):
    """
    Upload and (optionally) encrypt a specified file.

    :param ipfsapi.Client api: The IPFS API client instance to use
    :param input_file: The file to upload
    :param bool verbose: Verbosity on/off
    :param bool encrypt: Encryption on/off

    :returns: A hash of the uploaded file
    :rtype: str
    """
    # Read stdin...
    if input_file is sys.stdin:
        if verbose:
            sys.stderr.write(
                'Waiting for standard input... ' +
                '(type your doc and press Ctrl+D)\n'
            )
            sys.stderr.flush()

        file_contents = sys.stdin.buffer.read()
        sys.stderr.write('\n')
    # ...or the specified file
    else:
        with open(input_file, 'rb') as f:
            file_contents = f.read()

    if encrypt:
        secret = Fernet.generate_key()
        cipher = Fernet(secret)
        addr = api.add_bytes(cipher.encrypt(file_contents)) + \
            '/#' + b58encode(secret)

    else:
        addr = api.add_bytes(file_contents)

    return addr


def download(api, link, verbose=False):
    """
    Download (and decrypt if necessary) a specified IPFS link.

    :param ipfsapi.Client api: The IPFS API instance to use
    :param str link: The link
    :param verbose: Verbosity on/off

    :returns: The decrypted file
    :rtype: bytes
    """
    regex = re.compile(r'/ipfs/(\w+)(/#(webui:)?(\w*))?')

    matches = regex.findall(link)[0]  # unwrap the match

    if verbose:
        sys.stderr.write('Got link %s\n' % link +
                         'Encrypted: %s\n' % (matches[3] != '') +
                         'WebUI: %s\n' % (matches[2] != ''))

    if matches[2] != '':
        sys.stderr.write('WebUI download from command line is not supported' +
                         'yet. Sorry!')
        sys.exit(errno.EINVAL)

    addr = matches[0]

    if matches[3] != '':
        secret = b58decode(matches[3])
        cipher = Fernet(secret)
        ciphertext = api.cat(addr)
        file_contents = cipher.decrypt(ciphertext)

    else:
        file_contents = api.cat(addr)

    return file_contents


def main():
    args = get_args()
    api = connect(verbose=args.verbose)

    if args.download_link is None:
        addr = upload(api, args.input_file, verbose=args.verbose,
                      encrypt=args.encrypt)

        if args.verbose:
            sys.stderr.write('\nDone handling input.\n')

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

    else:
        file_contents = download(api, args.download_link[0],
                                 verbose=args.verbose)
        if args.verbose:
            sys.stderr.write('Contents of your file:\n')
            sys.stderr.flush()

        sys.stdout.buffer.write(file_contents)


if __name__ == "__main__":
    main()
