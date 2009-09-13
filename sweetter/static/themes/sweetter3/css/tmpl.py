#!/usr/bin/python

import sys
import re

tagname = re.compile(r"\* (?P<tagname>.*) ?= ?(?P<value>.*)")

def get_tags(input_string):
    return dict(tagname.findall(input_string))

def parse_tmpl(filename):
    iin = open(filename+'.tmpl')
    oout = open(filename, 'w')

    all_file = iin.read()
    tags = get_tags(all_file)

    oout.write(all_file % tags)

    iin.close()
    oout.close()

if __name__ == '__main__':
    parse_tmpl(sys.argv[1])
