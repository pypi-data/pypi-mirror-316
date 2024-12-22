# base64token

Encode list of tuples into a string. Decode that string into a dictionary.

```py
encoded = encode([("key1", "value1"), ("key2", 2)]) # "W1sia2V5MSIsICJ2YWx1ZTEiXSwgWyJrZXkyIiwgMl1d"
decoded = decode(encoded)  # {"key1": "value1", "key2": 2}
```