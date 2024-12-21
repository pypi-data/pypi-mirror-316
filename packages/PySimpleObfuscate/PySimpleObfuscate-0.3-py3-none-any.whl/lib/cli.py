#!/bin/env python3

import argparse
import pathlib
import os

from framework import encrypt_file, cyphers

parser = argparse.ArgumentParser(
    prog = 'PyObfuscate',
    description = 'A simple python obfuscator',
)


parser.add_argument("src", metavar="SRC", help="Filepath to the file(s) to obfuscate")
parser.add_argument("--lock", action='store_true', default=False, help="Lock the files with md5 hash (this wont work with elf or exe...)", required=False)
parser.add_argument("--dest", metavar="DEST", default="./dist", help="Destination Folder", required=False)
parser.add_argument("--msg", metavar="MSG", default="please dont touch the files things might stop working correctly", help="Encoding Warning", required=False)
def cli():

    args = vars(parser.parse_args())
    
    filepath = os.path.abspath(args['src'])
    if not os.path.exists(filepath):
        raise Exception("invalid source path: %s" % filepath)

    sources = []
    ftype = None

    if os.path.isdir(filepath):
        ftype = "dir"
        for root, subdirs, files in os.walk(filepath):
            for file in files:
                fpath = os.path.join(root, file)
                fPath = pathlib.Path(fpath)
                if fPath.suffix == ".py":
                   sources.append(fpath)

    elif os.path.isfile(filepath):
        ftype = "file"
        fPath = pathlib.Path(filepath)
        if fPath.suffix == ".py":
            sources.append(filepath)
    
    
    if not len(sources):
        raise Exception("could not any .py files...")

    for fp in sources:
        
        args['src'] = os.path.abspath(args['src'])
        args['dest'] = os.path.abspath(args['dest'])

        if args['src'] == args['dest']:
            raise Exception("The Source Folder must different from the destination folder or the files will be encrypted!")

        fd = fp.replace(args['src'], args['dest'])
        #fd = fd.rstrip('.py') + '.encoded.py'

        message=args['msg'].split(" ")

        if len(message) < 3:
            raise Exception("The message must contain at least 3 words")

        encrypt_file(fp, fd, varnames=message, cyphers=cyphers, iterations=6, lock=args['lock'])

if __name__ == '__main__':
    cli()