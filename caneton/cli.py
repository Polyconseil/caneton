# -*- coding: utf-8 -*-
# Copyright © 2015 Polyconseil SAS
# SPDX-License-Identifier: BSD-3-Clause
#
# Interpret CAN message DLC (payload) to extract the values of the signals.
# Requires a DBC file.
#

import binascii
import json
import argparse

import caneton


def create_parser():
    parser = argparse.ArgumentParser(description="Decode of CAN message with the help of DBC information.")
    parser.add_argument(
        'dbcfile', type=argparse.FileType('r'),
        help="DBC file converted in JSON format to use for decoding.")
    parser.add_argument('id', type=str, help="ID of the message on the CAN bus (eg. 0x5BB or 1467)")
    parser.add_argument('data', type=str, help="message data in hexadecimal (eg. 0x1112131415161718)")
    parser.add_argument('--output', type=str, choices=['json', 'text'], default='text',
        help="Format of the output (JSON or text)")
    return parser

def args_cleanup(args):
    # Check and cleanup message ID (minium 0x1)
    if len(args.id) > 2 and args.id[:2] == '0x':
        # It's an hexadecimal number
        message_id = int(args.id, 16)
    else:
        message_id = int(args.id)

    # Check the message data
    # Check the length of the data before removing the 0x prefix
    if len(args.data) < 4:
        raise ValueError("The CAN message data is too short '%s'." % args.data)

    # Test the first bytes are the 0x prefix
    if args.data[:2] != '0x':
        raise ValueError("The CAN message data '%s' is not prefixed by 0x." % args.data)

    # Remove the 0x prefix
    data = args.data[2:]
    data_length = len(data)

    is_multiple_of_two = (data_length % 2) == 0
    if not is_multiple_of_two:
        raise ValueError("The CAN data is not a multiple of two '%s'." % args.data)

    byte_length = data_length // 2
    if byte_length > caneton.MESSAGE_MAX_LENGTH:
        raise ValueError("The CAN message data length is too large (%d > %d)" % (
            byte_length, caneton.MESSAGE_MAX_LENGTH))

    try:
        # Convert hexadecimal string to bytes
        data = binascii.unhexlify(data)
        length = len(data)
    except ValueError:
        raise ValueError("Invalid data argument '%s'." % args.data)

    # Load file as JSON file
    try:
        dbc_json = json.loads(args.dbcfile.read())
    except ValueError:
        raise ValueError("Unable to load the DBC file '%s' as JSON." % args.dbcfile)

    return {
        'message_id': message_id, 'message_data': data, 'message_length': length,
        'dbc_json': dbc_json
    }


def message_output(message, is_json_output):
    if is_json_output:
        return message
    else:
        print("Message {name} {id:d} (0x{id:x})".format(**message))
        if message['multiplexing_mode']:
            print("Multiplexing mode: %s" % message['multiplexing_mode'])

        for signal in message['signals']:
            signal['endianness'] = 'LSB' if signal['is_little_endian'] else 'MSB'
            print("Signal {name} - ({length}@{bit_start} {endianness})x{factor}+{offset} = {value} {unit}".format(
                **signal))

def main():
    parser = create_parser()
    args = parser.parse_args()
    cleaned_args = args_cleanup(args)
    args.dbcfile.close()

    message = caneton.message_decode(**cleaned_args)
    message_output(message, args.output == 'json')



if __name__ == '__main__':
    main()
