The next step is the trickiest part of DNS: Label Length Encoding.
In the raw data, google.com looks like:
06 67 6f 6f 67 6c 65 03 63 6f 6d 00
(6 characters "google", 3 characters "com", ending in a null byte).