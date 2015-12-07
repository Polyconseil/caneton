# Copyright © 2015 Polyconseil SAS
# SPDX-License-Identifier: BSD-3-Clause
#


def hex_ascii_to_bytes(hex_ascii_str):
    hex_ascii_list = []
    # Length in bytes
    length = int(len(hex_ascii_str) / 2)
    for i in range(length):
        hex_ascii_list.append(int(hex_ascii_str[i * 2:i * 2 + 2], 16))

    return length, bytes(hex_ascii_list)
