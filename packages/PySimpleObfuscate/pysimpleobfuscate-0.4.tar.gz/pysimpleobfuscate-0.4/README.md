# PySimpleObfuscate
**_The Easiest Way to Encrypt your .py files_**

## Installation to Local Folder using _PIP_

### Linux / MacOS

```console
user@machine:~$ pip install ./PySimpleObfuscate --upgrade -t ~/.local/lib/<PYTHON>/site-packages/PyObfuscate
user@machine:~$ export PATH="~/.local/lib/<PYTHON>/site-packages/PySimpleObfuscate/bin:$PATH"
```

### Windows
```console
user@machine:~$ pip install ./PySimpleObfuscate --upgrade -t ~/.local/lib/<PYTHON>/site-packages/PySimpleObfuscate
```

## CLI Usage
```console
user@machine:~$ pyobfuscate --help
usage: PySimpleObfuscate [-h] SRC DEST MSG

A simple python obfuscator

positional arguments:
  SRC         Filepath to the file(s) to obfuscate
  DEST        Destination Folder
  MSG         Encoding Message

options:
  -h, --help  show this help message and exit
```

## API Usage
```python
from PySimpleObfuscate.lib.framework import encrypt_file, encrypt_source, cyphers

src = "/path/to/file.py"
dest = "/path/to/dest.py"

encrypt_file(src, dest, varnames=["your", "message", "here"], cyphers=cyphers, iterations=6)

source = """#!/bin/env python3
print("hello world")
"""

program = encrypt_source(seed=src, varnames=varnames, cyphers=cyphers, iterations=iterations)

header = """#!/bin/env python
import base64
import codecs
"""

program = """%s

%s

""" % (header, program,)

with open("encoded.py", "wb") as f:
    f.write(program)
    f.close()

```

## EXAMPLE OUTPUT
```python

import base64
import codecs

obfuscated="RTVQNzY4M0xFOVNOSU9IODU0VDBLODEw"
file="NDBHNjZQQk1DNUpJRzhKTEU5U05JT0gwRDlINkFVQkg0OEtHS1RCSUY1U000QTE5"
contents="b2JmdXNjYXRlZCA9IGJhc2U2NC5iNjRkZWNvZGUoYnl0ZXMob2JmdXNjYXRlZCwgJ3V0Zi04JykpLmRlY29kZSgndXRmLTgnKTtvYmZ1c2NhdGVkID0gY29kZWNzLmRlY29kZShzdHIob2JmdXNjYXRlZCksICdyb3RfMTMnKTtvYmZ1c2NhdGVkID0gY29kZWNzLmRlY29kZShzdHIob2JmdXNjYXRlZCksICdyb3RfMTMnKTtvYmZ1c2NhdGVkID0gYmFzZTY0LmIzMmhleGRlY29kZShieXRlcyhvYmZ1c2NhdGVkLCAndXRmLTgnKSkuZGVjb2RlKCd1dGYtOCcpO29iZnVzY2F0ZWQgPSBjb2RlY3MuZGVjb2RlKHN0cihvYmZ1c2NhdGVkKSwgJ3JvdF8xMycpO29iZnVzY2F0ZWQgPSBjb2RlY3MuZGVjb2RlKHN0cihvYmZ1c2NhdGVkKSwgJ3JvdF8xMycpO29iZnVzY2F0ZWQgPSBjb2RlY3MuZGVjb2RlKHN0cihvYmZ1c2NhdGVkKSwgJ3JvdF8xMycpO2ZpbGUgPSBiYXNlNjQuYjY0ZGVjb2RlKGJ5dGVzKGZpbGUsICd1dGYtOCcpKS5kZWNvZGUoJ3V0Zi04Jyk7ZmlsZSA9IGNvZGVjcy5kZWNvZGUoc3RyKGZpbGUpLCAncm90XzEzJyk7ZmlsZSA9IGNvZGVjcy5kZWNvZGUoc3RyKGZpbGUpLCAncm90XzEzJyk7ZmlsZSA9IGJhc2U2NC5iMzJoZXhkZWNvZGUoYnl0ZXMoZmlsZSwgJ3V0Zi04JykpLmRlY29kZSgndXRmLTgnKTtmaWxlID0gY29kZWNzLmRlY29kZShzdHIoZmlsZSksICdyb3RfMTMnKTtmaWxlID0gY29kZWNzLmRlY29kZShzdHIoZmlsZSksICdyb3RfMTMnKTtmaWxlID0gY29kZWNzLmRlY29kZShzdHIoZmlsZSksICdyb3RfMTMnKTtldmFsKGNvbXBpbGUoZXZhbCgiXHg2Zlx4NjJceDY2XHg3NVx4NzNceDYzXHg2MVx4NzRceDY1XHg2NCIpICsgZXZhbCgiXHg2Nlx4NjlceDZjXHg2NSIpLCAnPHN0cmluZycsICdleGVjJykp"
eval(compile(base64.b64decode(contents).decode("utf-8"), '<string>', 'exec'))
```
