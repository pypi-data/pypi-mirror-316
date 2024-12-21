import random
import codecs
import base64
import os
import inspect
import hashlib

cyphers = {
    "codecs": ["rot_13"],
    "base64": ["b85", "b64", "b16", "a85", "b32hex"]
}

def random_cypher(cyphers, enctype=None):

    if not enctype:
        enctype = list(filter(lambda cypher: cypher != "sep", list(cyphers))) \
            [random.randint(0, len(list(cyphers))-2)]
    
    index = random.randint(0, len(cyphers[enctype])-1)
    cypher = cyphers[enctype][index]
    
    if enctype  == "codecs":

        def _encode(val):
            return codecs.getencoder(cypher)(val)[0]
        def _decode(val):
            #if cypher == "hex": 
            #    val = bytes(val, "utf-8")
            return codecs.getencoder(cypher)(val)[0]

        encoder = lambda val: _encode(val)
        decoder = lambda val: _decode(val)
    
    elif enctype == "encoding":
        encoder = lambda val: ascii(val)
        decoder = lambda val: deascii(val)
    
    elif enctype == "base64":
    
        def _encode(val):
            if(isinstance(val, str)):
                val = bytes(val, "utf-8")
            return eval("base64.%sencode" % (cypher))(val).decode("utf-8")
        
        encoder = lambda v: _encode(v)
        
        def _decode(val):
            if(isinstance(val, str)):
                val = bytes(val, "utf-8")
            return eval("base64.%sdecode" % (cypher))(val).decode("utf-8")
            
        decoder = lambda v: _decode(v)
    
    else:
        encoder = None
        decoder = None

    return enctype, cypher, encoder, decoder

def ascii(msg):
    if msg is None: 
        return ""
    if not isinstance(msg, str): msg = str(msg)
    #print(len(msg), isinstance(msg, list))
    encoded = ""
    for code in msg.encode('ascii'):
        encoded += '\\x%s' % code
    return encoded

def deascii(msg):

    if msg is None: 
        return ""
    if not isinstance(msg, str): msg = str(msg)

    decoded = ""
    parts = msg.split("\\x")

    parts.pop(0)
    decoded = "".join([chr(int(c)) for c in parts])
    
    return decoded

def random_encryption(cyphers, iterations=8):
    encryption = []
    enctypes = list(filter(lambda cypher: cypher != "sep", list(cyphers)))
    #print(enctypes)
    for i in range(0, iterations):
        encryption.append(random_cypher(cyphers, enctype=enctypes[random.randint(0, len(enctypes)-1)]))
    encryption.append(random_cypher(cyphers={ "base64": ["b64"] }, enctype="base64"))
    decryption = [] + encryption
    decryption.reverse()

    return (encryption, decryption, cyphers)   

def get_random_cypher(cyphers={ "base64": ["b64"], "codecs": ["rot13"] }, enctype="base64"):
    return cyphers[enctype][random.randint(0, len(cyphers[enctype])-1)]

def encrypt_string(string, cyphers):
    #print(string, cyphers)
    for cypher in cyphers:
        (enctype, cypher, encode, decode) = cypher
        string = encode(string)
    return string

def decrypt_string(string, keys):

    if string is None:
        return ' '
    

    for cypher in keys:
        (enctype, cypher) = cypher
        if enctype == "codecs":
            string = eval("codecs.decode(str(%s), cypher))")
        elif enctype == "base64":
            string = eval("base64.%sdecode" % (cypher))(bytes(string, "utf-8")).decode("utf-8") # codecs.getdecoder(cypher)(string)[0]
        elif enctype == "encoding":
            def __skip_none(c):
                try:
                    chr(int(("%s"%c)))
                except:
                    return ""
            decoded = ""
            parts = string.split("\\x")
            parts.pop(0)
            decoded = "".join(filter(__skip_none, [c for c in parts]))
            string = decoded
        else:
            string = map(lambda x: x, [string.split(cypher)])
    
            return string

def encrypt_source(seed, varnames, cyphers, iterations = 3):

    sysvars = varnames[0:int((len(varnames))-1):]
    bootvar = varnames[-1]
    
    obf = {}
    strslice = None
    remainder = len(seed) % len(varnames)
    slicelength = len(seed) // len(varnames)
    i = 0

    (encryption, decryption, _) = random_encryption(cyphers=cyphers, iterations=iterations)

    for varname in sysvars:
        if strslice:
            strslice = seed[(i*slicelength):(i*slicelength)+slicelength:]
            if i == len(sysvars)-1:
                strslice = seed[(i*slicelength)::]
        else:
            strslice = seed[0:slicelength:]
        i += 1

        obf[varname] = encrypt_string(strslice, encryption)

    keys = [(enctype, cypher) for enctype, cypher, _, _ in decryption]

    interpreter = []

    def decrypt(varname):

        for t in keys:
            if t[0] == "base64":
                interpreter.append("%s = base64.%sdecode(bytes(%s, 'utf-8')).decode('utf-8')" % (varname, t[1], varname))
            elif t[0] == "codecs":
                interpreter.append("%s = codecs.decode(str(%s), '%s')" % (varname, varname, t[1]))
            else:
                raise Exception("Unsoportted key type %s" % (str(t[0])))

    #interpreter.append("%s = list(map(lambda t: (deascii(t[0]), deascii(t[1])), [(e[0], e[1]) for e in [d.split(\"\\%s\") for d in [c for c in %s.split(\"\\%s\")]]]))" % (keyvar, ascii(";"), keyvar, ascii("$")))
    #interpreter.append("%s.reverse()" % keyvar)

    bootloader = []
    for var in sysvars:
        decrypt(var)
        bootloader.append("eval(\"%s\")" % ("".join(['\\'+hex(ord(c))[1:] for c in var])))
    
    interpreter = ";".join(interpreter) + ";"

    bootloader = " + ".join(bootloader)
    bootloader = "eval(compile(%s, '<string', 'exec'))" % (bootloader)     
    
    bootloader = "%s%s" % (interpreter, bootloader)
    
    #print(bootloader)

    obf[bootvar] = base64.b64encode(bytes(bootloader, "utf-8")).decode("utf-8")
    #obf[bootvars[1]] = "eval(base64.b64decode(%s))" % (bootvars[0]) 

    out = ""
    for var in obf:
        out += "%s%s\"%s\"%s" % (var, "=", obf[var], "\r\n")
    
    out += "eval(compile(base64.b64decode(%s).decode(\"utf-8\"), '<string>', 'exec'))" % (bootvar)
    return out

def encrypt_keys(keys, encryption):
    keys = ascii("$").join(map(lambda kt: "%s%s%s" % (ascii(kt[0]), ascii(";"), ascii(kt[1])), keys))
    keys = encrypt_string(keys, encryption)
    return keys 

def encrypt_file(filepath, dest, varnames, cyphers, iterations=3):
    if not os.path.isfile(filepath):
        raise Exception("could not find file %s" % (str(filepath)))
    
    src = None
    with open(filepath) as f:
        src = f.read()
        f.close()

    if not isinstance(src, str):
        raise Exception("could not read file %s" % (str(filepath)))

    program = encrypt_source(seed=src, varnames=varnames, cyphers=cyphers, iterations=iterations)

    header = """
import base64
import codecs
"""
    template = """%s
%s
""" % (header, program,)

    
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(bytes(template, "utf-8"))
        f.close()

    return template