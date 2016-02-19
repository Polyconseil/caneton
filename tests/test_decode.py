# -*- coding: utf-8 -*-
# Copyright © 2015 Polyconseil SAS
# SPDX-License-Identifier: BSD-3-Clause
#

from unittest import TestCase
import binascii
import json

import caneton


class TestDecode(TestCase):

    def test_signal_with_empty_value(self):
        signal_info = {
            'bit_start': 32,
            'length': 16,
            'little_endian': 1,
        }
        message_binary_lsb = '0000000010101111000000001010001100000000'
        # message_binary_msb is not required (LSB)
        with self.assertRaises(caneton.DecodingError) as cm:
            caneton.signal_decode(
                "Foo", signal_info, None, message_binary_lsb, len(message_binary_lsb))
        exception = cm.exception
        self.assertEqual(
            str(exception),
            "The string value extracted for signal 'Foo' is empty [-8:8].")

    def test_message(self):
        message_id = 0x701
        message_data = binascii.unhexlify('01780178010000')
        message_length = len(message_data)

        with open('./tests/dbc.json', 'r') as f:
            dbc_json = json.loads(f.read())

        message = caneton.message_decode(
            message_id=message_id, message_length=message_length,
            message_data=message_data, dbc_json=dbc_json)
        signal = caneton.message_get_signal(message, 'Bar2')
        self.assertEqual(signal['name'], 'Bar2')
        self.assertEqual(signal['value'], 188.0)
        self.assertEqual(signal['unit'], 'V')

    def test_message_wo_signals(self):
        message_id = 542
        message_length = 8
        message_data = b' ' * message_length

        with open('./tests/dbc.json', 'r') as f:
            dbc_json = json.loads(f.read())

        message = caneton.message_decode(
            message_id=message_id, message_length=message_length,
            message_data=message_data, dbc_json=dbc_json)
        self.assertEqual(message['signals'], [])
        self.assertEqual(
            caneton.message_get_signal(message, 'Doesntexist'), None)
