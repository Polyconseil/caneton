Caneton
=======

Python 2/3 project under BSD license to decode messages (or frames) from a CAN bus.

DBC in JSON
-----------

Before decoding a message, you need to convert the DBC file which describes the format of the data on the bus in JSON. The project [libcanardbc](https://github.com/Polyconseil/libcanardbc) can
convert a CAN DBC file to JSON suitable for caneton project.

Use
---

To decode a CAN message, you must provide the message ID, the message data
(payload) and the DBC file (in JSON).

Caneton can be used as Python module:

```python
import binascii
import json

import caneton

with open('dbc.json') as dbc_file:
    dbc_json = json.loads(dbc_file.read())
    message_data = binascii.unhexlify('01780178010000')
    message = caneton.message_decode(message_id=0x701,
        message_length=len(message_data), message_data=message_data,
        dbc_json=dbc_json)
    print(message)
```

or as CLI tool to decode CAN message:

`$ caneton-decode dbc.json 0x701 0x01780178010000`


Tests
-----

To run the unit tests:

`$ nosetests`
