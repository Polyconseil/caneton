# -*- coding: utf-8 -*-
# Copyright © 2015 Polyconseil SAS
# SPDX-License-Identifier: BSD-3-Clause
#

from unittest import TestCase

import caneton
from caneton import cli


class TestCLI(TestCase):

    def setUp(self):
        self.parser = cli.create_parser()  # flake8: noqa

    def test_message_701(self):
        args = self.parser.parse_args(['./tests/dbc.json', '0x701', '0x01780178010000'])
        cleaned_args = cli.args_cleanup(args)
        args.dbcfile.close()
        message = caneton.message_decode(**cleaned_args)
        self.assertEqual(message['name'], 'CU_MULTI_FOO_BAR')
        signals = message['signals']
        # The multiplexor is excluded from the list of signals
        expected_signals = [
            {'name': 'Bar1', 'value': 376},
            {'name': 'Bar2', 'value': 188.0},
        ]
        self.assertEqual(len(signals), len(expected_signals))
        for (signal, expected_signal) in zip(signals, expected_signals):
            self.assertEqual(signal['name'], expected_signal['name'])
            self.assertEqual(signal['value'], expected_signal['value'], signal['name'])
            self.assertIsInstance(signal['value'], type(expected_signal['value']), signal['name'])
