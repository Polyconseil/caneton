# -*- coding: utf-8 -*-
# Copyright © 2015 Polyconseil SAS
# SPDX-License-Identifier: BSD-3-Clause
#

from . import compat
from . import exceptions


MESSAGE_MAX_LENGTH = 8

def signal_decode(signal_name, signal_info,
        message_binary_msb, message_binary_lsb, message_binary_length):
    """
    Decode a signal of a CAN message

    Arguments:
        signal_name: str, human name of the signal
        signal_info: dict, information about the signal (length, endianness)
        message_binary_msb: str, data of CAN message in MSB binary format
        message_binary_lsb: str, data of CAN message in LSB binary format
        message_binary_length: int, length of CAN message in binary format

    Returns:
        signal: dict, a decoded signal from the CAN data message

    Raises:
        exceptions.InvalidBitStart: when signal's bit start is too high
    """
    signal = {
        'name': signal_name,
        'length': signal_info['length']
    }
    bit_start = signal_info['bit_start']
    is_little_endian = bool(signal_info['little_endian'])
    signal['is_little_endian'] = is_little_endian

    if is_little_endian:
        message_binary = message_binary_lsb
    else:
        message_binary = message_binary_msb

    if bit_start >= message_binary_length:
        raise exceptions.InvalidBitStart(
            "Bit start %d of signal %s is too high" % (bit_start, signal_name))

    if is_little_endian:
        # In Intel format (little-endian), bit_start is the position of the
        # Least Significant Bit so it needs to be byte swapped
        signal['bit_end'] = message_binary_length - bit_start
        signal['bit_start'] = signal['bit_end'] - signal['length']
    else:
        # Motorola. Weird thing of the DBC format
        signal['bit_start'] = (bit_start // 8) * 8 + (7 - (bit_start % 8))
        signal['bit_end'] = signal['bit_start'] + signal['length']

    s_value = message_binary[signal['bit_start']:signal['bit_end']]
    if not s_value:
        raise exceptions.DecodingError(
            "The string value extracted for signal '%s' is empty [%d:%d]." %
            (signal_name, signal['bit_start'], signal['bit_end']))

    signal['factor'] = signal_info.get('factor', 1)
    signal['offset'] = signal_info.get('offset', 0)
    signal['value'] = int(s_value, 2) * signal['factor'] + signal['offset']
    signal['unit'] = signal_info.get('unit', '')

    return signal


def message_get_current_multiplexing_mode(message_info, message_binary_msb, message_binary_lsb,
        message_binary_length):
    """Extract the current multiplexing mode of the message if any.

    Arguments:
        message_info: dict, information about the message (name, signals)
        message_binary_msb: str, data of CAN message in MSB binary format
        message_binary_lsb: str, data of CAN message in LSB binary format
        message_binary_length: int, length of CAN message in binary format

    Returns:
        multiplexing_mode: int, the current multiplexing mode or None
    """
    multiplexing_mode = None
    signals = message_info['signals']
    for signal_name, signal_info in signals.items():
        if signal_info.get('multiplexor', False):
            signal = signal_decode(signal_name, signal_info, message_binary_msb, message_binary_lsb,
                message_binary_length)
            multiplexing_mode = signal['value']
            break

    return multiplexing_mode

def message_get_signal(message, signal_name):
    """Loop over signals to find the requested signal.

    Arguments:
        message: dict, the message provided by message_decode()
        signal_name: str, name of the signal (from DBC)

    Return:
        signal: dict, information about the decoded signal
    """
    for signal in message.get('signals', []):
        if signal.get('name') == signal_name:
            return signal

def message_decode(message_id, message_length, message_data, dbc_json):
    """Decode a CAN message (also called a frame).

    Args:
        message_id: int, message identifier.
        message_length: int, length of the useful data in message data received (the length
            can be different of the CAN data length).
        message_data: bytes, binary data of the message.
        dbc_json: dict, deserialized version of a DBC file converted to JSON with libcanardbc.

    Returns:
        message: decoded message with list of signals.

    Raises:
        exceptions.InvalidDBC: when used DBC has not messages entry
        exceptions.MessageNotFound: when message's ID is not found in the DBC
    """
    if 'messages' not in dbc_json:
        raise exceptions.InvalidDBC("Invalid DBC file (no messages entry)")

    # Initialize the returns
    message = {'signals': []}

    try:
        message_info = dbc_json['messages'][str(message_id)]
        message['name'] = message_info['name']
        message['id'] = message_id
    except KeyError:
        raise exceptions.MessageNotFound(
            "Message ID {id:d} (0x{id:x}) not found in DBC".format(id=message_id))

    # The CAN message data is always 8 bytes so it's required to truncate it to keep only
    # the useful bytes (nop when already truncated)
    message_data = message_data[:message_length]

    # Convert length from bytes to bits
    message_binary_length = message_length * 8

    # Motorola
    # 0n to fit in n characters width with 0 padding (can't use bin())
    # [2:] to remove '0b' prefix and zfill constant length with 0 padding
    message_binary_msb = bin(compat.int_from_bytes(message_data, 'big'))[2:].zfill(
        message_binary_length)

    # For Intel, identical but swapped
    message_binary_lsb = bin(compat.int_from_bytes(message_data, 'little'))[2:].zfill(
        message_binary_length)

    if message_info.get('has_multiplexor', False):
        multiplexing_mode = message_get_current_multiplexing_mode(
            message_info, message_binary_msb, message_binary_lsb,
            message_binary_length)
    else:
        multiplexing_mode = None
    message['multiplexing_mode'] = multiplexing_mode

    message['raw_data'] = message_data

    if 'signals' not in message_info:
        return message

    signals = sorted(message_info['signals'].items(), key=lambda t: int(t[1]['bit_start']))
    for signal_name, signal_info in signals:
        # If the signal contains the multiplexor, we don't want to add it to the list of signals.
        if signal_info.get('multiplexor', False):
            continue

        # Decode signal only when no multiplexor or the signal is associated to the
        # current mode or the signal is not multiplexed.
        if (multiplexing_mode is None or
                multiplexing_mode == signal_info.get('multiplexing', multiplexing_mode)):
            if signal_info['bit_start'] >= message_binary_length:
                # The signal is invalid as the CAN frame is too small to contain it.
                # However, new signals may be added to an already existing CAN frame,
                # meaning the same DBC must support old versions with small frames
                # and newer versions with extended data. To keep retro-compatibility
                # we don't throw an error.
                continue
            signal = signal_decode(
                signal_name, signal_info, message_binary_msb, message_binary_lsb,
                message_binary_length)
            message['signals'].append(signal)

    return message
