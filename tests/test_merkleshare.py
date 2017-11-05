#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_merkleshare
----------------------------------

Tests for `merkleshare` module.
"""

from merkleshare import merkleshare


TEST_FILENAME = 'test.txt'


def test_get_args_with_file():
    args = merkleshare.get_args(args=['mersh', TEST_FILENAME])

    assert args.input_file == TEST_FILENAME
