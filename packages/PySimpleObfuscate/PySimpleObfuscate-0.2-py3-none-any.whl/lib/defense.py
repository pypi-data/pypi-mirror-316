

class UnauthorizedExecutionException(Exception):
    pass

def defense_measures():
    
    from os import linesep
    from inspect import getsourcefile
    from os.path import abspath
    from hashlib import md5
    from re import sub, match

    f = open(abspath(__file__), "rb")
    content_bytes = f.read()
    f.close()
    
    content = content_bytes.decode("utf-8")
    content = content.split(linesep)
    md5_line = content[0]
    content = linesep.join(content[1::])

    regex = r'^#md5:'
    if match(regex, md5_line) == None:
        raise UnauthorizedExecutionException("invalid checksum") 
    md5_line = sub(regex, "", md5_line).strip()
    content_hash = md5(content.strip().encode("utf-8")).hexdigest()
    if md5_line != content_hash:
        raise UnauthorizedExecutionException("invalid checksum %s" % (md5_line))

def verify_checksum():
    try:
        defense_measures()
    except UnauthorizedExecutionException as e:
        print(str(e))
        exit(0)
