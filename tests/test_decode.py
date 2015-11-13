# Copyright © 2015 Polyconseil SAS
# SPDX-License-Identifier: BSD-3-Clause
#

from unittest import TestCase

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
        self.assertEqual(str(exception),
            "The string value extracted for signal 'Foo' is empty [-8:8].")
