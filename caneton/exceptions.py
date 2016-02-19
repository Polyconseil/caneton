# -*- coding: utf-8 -*-
# Copyright © 2015 Polyconseil SAS
# SPDX-License-Identifier: BSD-3-Clause
#


class CanetonError(Exception):
    """Caneton base exception."""


class DecodingError(CanetonError):
    """Raised when there is a CAN message decoding error."""


class InvalidBitStart(DecodingError):
    """Raised during decoding of a CAN signal, when the bit start value is invalid (e.g. too high)."""


class InvalidDBC(DecodingError):
    """Raised during decoding of a CAN message, when used DBC have missing sections."""


class MessageNotFound(DecodingError):
    """Raised during decoding of a CAN message, when identifier of this last is not found in the DBC."""
