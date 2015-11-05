Caneton
=======

Python 3 project under BSD license to decode CAN messages (also called frames).

To decode a CAN message, you must provide the message ID, the message data
(payload) and the DBC file which describes the format of the data on the CAN
bus.

Caneton can be used as Python module:

```python
import json
import caneton

with open('dbc.json') as dbc_file:
    dbc_json = json.loads(dbc_file.read())
    message_length, message_data = caneton.hex_ascii_to_bytes('01780178010000')
    message = caneton.message_decode(message_id=0x701,
        message_length=message_length, message_data=message_data,
        dbc_json=dbc_json)
    print(message)
```

The project [libcanardbc](https://github.com/Polyconseil/libcanardbc) can
convert a CAN DBC file to JSON.

Caneton provides a CLI tool to decode CAN message:

```caneton-decode dbc.json 0x701 0x01780178010000```
